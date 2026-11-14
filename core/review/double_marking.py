"""
Double-Marking & Disagreement Reconciliation Engine for IELTS by GAMA.
Supports:
1. Blind independent double-marking assignment.
2. Blind review enforcement (Reviewer 2 cannot view Reviewer 1's score before submitting).
3. Criterion-level and overall disagreement calculation.
4. Threshold-triggered workflow alerts (> 0.5 band difference).
5. Senior Examiner reconciliation workflow preserving original reviewer marks.
"""

import json
import uuid
import datetime
from typing import Optional, Dict, Any, List, Tuple
from core.database.db_manager import DatabaseManager
from core.review.review_manager import ReviewManager


class DoubleMarkingManager:
    """Manages independent double-marking, disagreement detection, and reconciliation."""

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()
        self.review_mgr = ReviewManager(self.db)

    def create_double_marking_pair(
        self,
        submission_id: str,
        submission_type: str,
        learner_id: str,
        content_json: Dict[str, Any],
        reviewer_1_id: str,
        reviewer_2_id: str,
        task_type: Optional[str] = None,
        track: Optional[str] = None,
        benchmark_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Creates paired independent review assignments for blind marking."""
        if reviewer_1_id == reviewer_2_id:
            return {"success": False, "error": "Reviewer 1 and Reviewer 2 must be distinct individuals."}

        # Assignment 1
        a1 = self.review_mgr.create_assignment(
            submission_id=submission_id,
            submission_type=submission_type,
            learner_id=learner_id,
            content_json=content_json,
            assigned_to=reviewer_1_id,
            assigned_role="examiner",
            task_type=task_type,
            track=track,
            is_benchmark=1 if benchmark_id else 0,
            benchmark_id=benchmark_id
        )

        # Assignment 2
        a2 = self.review_mgr.create_assignment(
            submission_id=submission_id,
            submission_type=submission_type,
            learner_id=learner_id,
            content_json=content_json,
            assigned_to=reviewer_2_id,
            assigned_role="examiner",
            task_type=task_type,
            track=track,
            is_benchmark=1 if benchmark_id else 0,
            benchmark_id=benchmark_id
        )

        return {
            "success": True,
            "submission_id": submission_id,
            "assignment_1_id": a1["assignment_id"],
            "reviewer_1_id": reviewer_1_id,
            "assignment_2_id": a2["assignment_id"],
            "reviewer_2_id": reviewer_2_id
        }

    def get_double_marked_evaluations(
        self,
        submission_id: str,
        requesting_reviewer_id: Optional[str] = None,
        user_role: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves double-marking records.
        ENFORCES BLIND REVIEW: A reviewer cannot see the peer evaluation until their own review is submitted!
        Admin / Senior Examiner can view both once both or either are available.
        """
        rows = self.db.fetchall(
            """SELECT e.*, u.full_name as reviewer_name, a.assigned_role
               FROM human_evaluations e
               JOIN review_assignments a ON e.assignment_id = a.id
               JOIN users u ON e.reviewer_id = u.id
               WHERE e.submission_id = ? AND e.status IN ('submitted', 'reconciled')
               ORDER BY e.submitted_at ASC""",
            (submission_id,)
        )

        evaluations = []
        for r in rows:
            ev = dict(r)
            ev["criteria_scores"] = json.loads(ev.get("criteria_scores_json") or "{}")
            ev["criterion_feedback"] = json.loads(ev.get("criterion_feedback_json") or "{}")
            evaluations.append(ev)

        # Separate regular evaluations from reconciled evaluations
        regular_evals = [e for e in evaluations if e.get("reviewer_role") != "senior_examiner" and e.get("status") != "reconciled"]
        reconciled_evals = [e for e in evaluations if e.get("reviewer_role") == "senior_examiner" or e.get("status") == "reconciled"]

        # Check blind review condition
        if user_role not in ("admin", "senior_examiner") and requesting_reviewer_id:
            # Check if requesting reviewer has submitted
            has_submitted = any(e["reviewer_id"] == requesting_reviewer_id for e in regular_evals)
            if not has_submitted:
                # Filter out peer evaluation!
                regular_evals = [e for e in regular_evals if e["reviewer_id"] == requesting_reviewer_id]

        return {
            "submission_id": submission_id,
            "evaluation_count": len(regular_evals),
            "evaluations": regular_evals,
            "reconciled_evaluation": reconciled_evals[0] if reconciled_evals else None,
            "both_submitted": len(regular_evals) >= 2
        }

    def calculate_disagreement(
        self,
        eval_1: Dict[str, Any],
        eval_2: Dict[str, Any],
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Calculates score differences between Reviewer 1 and Reviewer 2.
        Identifies criterion-level disagreements (> threshold band gap).
        """
        band_1 = float(eval_1["overall_band"])
        band_2 = float(eval_2["overall_band"])
        overall_diff = round(abs(band_1 - band_2), 1)

        crit_1 = eval_1.get("criteria_scores", {})
        crit_2 = eval_2.get("criteria_scores", {})

        criteria_diffs = {}
        criterion_alerts = []

        all_criteria = set(list(crit_1.keys()) + list(crit_2.keys()))
        for c in sorted(all_criteria):
            s1 = float(crit_1.get(c, 0.0))
            s2 = float(crit_2.get(c, 0.0))
            diff = round(abs(s1 - s2), 1)
            criteria_diffs[c] = {
                "reviewer_1_score": s1,
                "reviewer_2_score": s2,
                "difference": diff,
                "exceeds_threshold": diff > threshold
            }
            if diff > threshold:
                criterion_alerts.append(f"{c.replace('_', ' ').title()}: difference of {diff} bands exceeds {threshold}")

        requires_reconciliation = (overall_diff > threshold) or (len(criterion_alerts) > 0)

        return {
            "reviewer_1_id": eval_1.get("reviewer_id"),
            "reviewer_1_name": eval_1.get("reviewer_name"),
            "reviewer_1_band": band_1,
            "reviewer_2_id": eval_2.get("reviewer_id"),
            "reviewer_2_name": eval_2.get("reviewer_name"),
            "reviewer_2_band": band_2,
            "overall_difference": overall_diff,
            "criteria_differences": criteria_diffs,
            "disagreement_threshold": threshold,
            "requires_reconciliation": requires_reconciliation,
            "alerts": criterion_alerts
        }

    def submit_reconciliation(
        self,
        submission_id: str,
        reconciler_id: str,
        reconciled_band: float,
        reconciled_criteria: Dict[str, float],
        comments: str
    ) -> Dict[str, Any]:
        """
        Records a reconciled final evaluation by a Senior Examiner.
        PRESERVES both Reviewer 1 and Reviewer 2 original evaluations intact.
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        reconcile_id = f"eval_recon_{uuid.uuid4().hex[:12]}"

        # Find any assignment for this submission to link to
        assign = self.db.fetchone("SELECT id FROM review_assignments WHERE submission_id = ? LIMIT 1", (submission_id,))
        assign_id = assign[0] if assign else f"assign_recon_{submission_id}"

        self.db.execute(
            """INSERT INTO human_evaluations
               (id, assignment_id, submission_id, reviewer_id, reviewer_role, overall_band, criteria_scores_json, assessment_mode, criterion_feedback_json, general_comments, status, revision, created_at, submitted_at)
               VALUES (?, ?, ?, ?, 'senior_examiner', ?, ?, 'consensus', '{}', ?, 'reconciled', 1, ?, ?)""",
            (reconcile_id, assign_id, submission_id, reconciler_id, reconciled_band, json.dumps(reconciled_criteria), comments, now, now)
        )

        # Mark assignments as reconciled
        self.db.execute(
            "UPDATE review_assignments SET status = 'reconciled', updated_at = ? WHERE submission_id = ?",
            (now, submission_id)
        )

        return {
            "success": True,
            "reconciliation_id": reconcile_id,
            "submission_id": submission_id,
            "reconciled_band": reconciled_band,
            "reconciled_criteria": reconciled_criteria,
            "status": "reconciled",
            "submitted_at": now
        }
