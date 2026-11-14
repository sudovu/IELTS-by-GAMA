"""
Review Manager for IELTS by GAMA.
Orchestrates teacher and examiner workflows for Writing and Speaking submissions.
Enforces criteria grading (TR/TA, CC, LR, GRA for Writing; FC, LR, GRA, P for Speaking),
draft saving, revision history, and student-teacher data segregation.
"""

import json
import uuid
import datetime
from typing import Optional, Dict, Any, List, Tuple
from core.database.db_manager import DatabaseManager


class ReviewManager:
    """Manages teacher and examiner assignments and criteria-based human evaluations."""

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()

    def assign_teacher_to_learner(self, teacher_id: str, learner_id: str, assigned_by: str = "admin") -> Dict[str, Any]:
        """Assigns a teacher to mentor a specific learner."""
        assign_id = f"teach_assign_{uuid.uuid4().hex[:12]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.db.execute(
            """INSERT OR REPLACE INTO teacher_assignments (id, teacher_id, learner_id, assigned_by, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (assign_id, teacher_id, learner_id, assigned_by, now)
        )
        return {"success": True, "assignment_id": assign_id, "teacher_id": teacher_id, "learner_id": learner_id}

    def get_assigned_learners(self, teacher_id: str) -> List[Dict[str, Any]]:
        """Retrieves list of learners assigned to a specific teacher."""
        rows = self.db.fetchall(
            """SELECT l.id, l.name, l.target_band, l.current_band, l.cefr_level, l.track, ta.created_at as assigned_at
               FROM teacher_assignments ta
               JOIN learners l ON ta.learner_id = l.id
               WHERE ta.teacher_id = ?
               ORDER BY ta.created_at DESC""",
            (teacher_id,)
        )
        return [dict(r) for r in rows]

    def create_assignment(
        self,
        submission_id: str,
        submission_type: str,
        learner_id: str,
        content_json: Dict[str, Any],
        assigned_to: str,
        assigned_role: str = "teacher",
        task_type: Optional[str] = None,
        track: Optional[str] = None,
        is_benchmark: int = 0,
        benchmark_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Creates a review assignment for a teacher or examiner."""
        assign_id = f"assign_{uuid.uuid4().hex[:12]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        self.db.execute(
            """INSERT INTO review_assignments 
               (id, submission_id, submission_type, learner_id, task_type, track, content_json, assigned_to, assigned_role, status, is_benchmark, benchmark_id, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?, ?, ?)""",
            (assign_id, submission_id, submission_type, learner_id, task_type, track, json.dumps(content_json), assigned_to, assigned_role, is_benchmark, benchmark_id, now, now)
        )
        return {"success": True, "assignment_id": assign_id, "assigned_to": assigned_to, "status": "pending"}

    def get_assignment(self, assignment_id: str, reviewer_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Retrieves an assignment, checking authorization if reviewer_id is provided."""
        row = self.db.fetchone("SELECT * FROM review_assignments WHERE id = ?", (assignment_id,))
        if not row:
            return None
        assign = dict(row)
        if reviewer_id and assign["assigned_to"] != reviewer_id:
            # Check if reviewer is admin
            u = self.db.fetchone("SELECT role FROM users WHERE id = ?", (reviewer_id,))
            if not u or u[0] != "admin":
                return None

        assign["content"] = json.loads(assign.get("content_json") or "{}")
        return assign

    def get_teacher_dashboard(self, teacher_id: str) -> Dict[str, Any]:
        """Compiles workload, assigned learners, pending essays, and completed reviews."""
        learners = self.get_assigned_learners(teacher_id)
        learner_ids = [l["id"] for l in learners]

        # Assignments for this teacher
        rows = self.db.fetchall(
            """SELECT a.*, l.name as learner_name
               FROM review_assignments a
               LEFT JOIN learners l ON a.learner_id = l.id
               WHERE a.assigned_to = ?
               ORDER BY a.created_at DESC""",
            (teacher_id,)
        )

        pending = []
        in_progress = []
        completed = []

        for r in rows:
            item = dict(r)
            item["content"] = json.loads(item.get("content_json") or "{}")
            if item["status"] == "pending":
                pending.append(item)
            elif item["status"] == "in_progress":
                in_progress.append(item)
            else:
                completed.append(item)

        return {
            "teacher_id": teacher_id,
            "assigned_learners": learners,
            "total_assigned_learners": len(learners),
            "pending_count": len(pending),
            "in_progress_count": len(in_progress),
            "completed_count": len(completed),
            "pending_reviews": pending,
            "in_progress_reviews": in_progress,
            "completed_reviews": completed
        }

    def save_evaluation(
        self,
        assignment_id: str,
        reviewer_id: str,
        reviewer_role: str,
        overall_band: float,
        criteria_scores: Dict[str, float],
        criterion_feedback: Optional[Dict[str, str]] = None,
        general_comments: Optional[str] = None,
        assessment_mode: str = "transcript",
        status: str = "submitted"
    ) -> Dict[str, Any]:
        """
        Saves a draft or final human assessment.
        Preserves original submission and maintains revision history.
        """
        assign = self.get_assignment(assignment_id, reviewer_id=reviewer_id)
        if not assign:
            return {"success": False, "error": "Assignment not found or unauthorized reviewer."}

        submission_id = assign["submission_id"]
        sub_type = assign["submission_type"]

        # Validate criteria for writing vs speaking
        if sub_type == "writing":
            required_criteria = ["task_achievement", "coherence_cohesion", "lexical_resource", "grammatical_accuracy"]
        else:
            required_criteria = ["fluency_coherence", "lexical_resource", "grammatical_accuracy", "pronunciation"]

        for rc in required_criteria:
            if rc not in criteria_scores:
                return {"success": False, "error": f"Missing required criterion score: '{rc}'"}
            score = float(criteria_scores[rc])
            if not (0.0 <= score <= 9.0 and (score * 2).is_integer()):
                return {"success": False, "error": f"Invalid criterion score {score} for '{rc}'. Must be in 0.5 band increments (0.0 - 9.0)."}

        # Validate overall band
        if not (0.0 <= float(overall_band) <= 9.0 and (float(overall_band) * 2).is_integer()):
            return {"success": False, "error": "Overall band must be between 0.0 and 9.0 in half-band increments."}

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Check existing evaluation for revision tracking
        existing = self.db.fetchone(
            "SELECT id, revision, status FROM human_evaluations WHERE assignment_id = ? AND reviewer_id = ?",
            (assignment_id, reviewer_id)
        )

        if existing:
            eval_id, old_rev, old_status = existing[0], existing[1], existing[2]
            if old_status in ("submitted", "reconciled"):
                return {"success": False, "error": "Evaluation has already been officially submitted and is immutable."}
            new_rev = old_rev + 1
            self.db.execute(
                """UPDATE human_evaluations
                   SET overall_band = ?, criteria_scores_json = ?, assessment_mode = ?, criterion_feedback_json = ?, general_comments = ?, status = ?, revision = ?, submitted_at = ?
                   WHERE id = ?""",
                (overall_band, json.dumps(criteria_scores), assessment_mode, json.dumps(criterion_feedback or {}), general_comments or "", status, new_rev, now, eval_id)
            )
        else:
            eval_id = f"eval_{uuid.uuid4().hex[:12]}"
            new_rev = 1
            self.db.execute(
                """INSERT INTO human_evaluations
                   (id, assignment_id, submission_id, reviewer_id, reviewer_role, overall_band, criteria_scores_json, assessment_mode, criterion_feedback_json, general_comments, status, revision, created_at, submitted_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)""",
                (eval_id, assignment_id, submission_id, reviewer_id, reviewer_role, overall_band, json.dumps(criteria_scores), assessment_mode, json.dumps(criterion_feedback or {}), general_comments or "", status, now, now)
            )

        # Update assignment status
        assign_status = "completed" if status == "submitted" else "in_progress"
        self.db.execute(
            "UPDATE review_assignments SET status = ?, updated_at = ? WHERE id = ?",
            (assign_status, now, assignment_id)
        )

        return {
            "success": True,
            "evaluation_id": eval_id,
            "assignment_id": assignment_id,
            "submission_id": submission_id,
            "overall_band": overall_band,
            "criteria_scores": criteria_scores,
            "status": status,
            "revision": new_rev,
            "submitted_at": now
        }

    def get_evaluation(self, evaluation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a human evaluation record."""
        row = self.db.fetchone("SELECT * FROM human_evaluations WHERE id = ?", (evaluation_id,))
        if not row:
            return None
        ev = dict(row)
        ev["criteria_scores"] = json.loads(ev.get("criteria_scores_json") or "{}")
        ev["criterion_feedback"] = json.loads(ev.get("criterion_feedback_json") or "{}")
        return ev
