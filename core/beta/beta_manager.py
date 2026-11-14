"""
Controlled Beta Pilot Management Module for IELTS by GAMA.
Supports:
1. Multi-cohort management (Academic, General Training, Academy A1-B1, Academy B2-C2).
2. Controlled participant enrollment with mandatory consent tracking.
3. Multi-dimensional feedback collection across 11 usability and pedagogical categories.
4. Bug and issue reporting classified by severity (Critical, High, Medium, Low).
5. Beta analytics and learning outcome tracking.
"""

import json
import uuid
import datetime
from typing import Optional, Dict, Any, List
from core.database.db_manager import DatabaseManager


class BetaManager:
    """Manages beta cohorts, participant consent, feedback, bug tracking, and analytics."""

    FEEDBACK_CATEGORIES = [
        "onboarding", "navigation", "reading", "listening",
        "writing", "speaking", "ai_feedback", "exam_sim",
        "mobile", "offline", "reliability"
    ]

    VALID_SEVERITIES = {"critical", "high", "medium", "low"}

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()

    def list_cohorts(self) -> List[Dict[str, Any]]:
        """Lists all beta cohorts with participant counts."""
        rows = self.db.fetchall("SELECT * FROM beta_cohorts ORDER BY created_at DESC")
        cohorts = []
        for r in rows:
            c = dict(r)
            cnt = self.db.fetchone("SELECT COUNT(*) FROM beta_participants WHERE cohort_id = ?", (c["id"],))[0]
            c["current_participants"] = cnt
            cohorts.append(c)
        return cohorts

    def create_cohort(
        self,
        name: str,
        track_or_level: str,
        start_date: str,
        end_date: str,
        max_participants: int = 50
    ) -> Dict[str, Any]:
        """Creates a new controlled beta cohort."""
        cid = f"cohort_{uuid.uuid4().hex[:10]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.db.execute(
            """INSERT INTO beta_cohorts (id, name, track_or_level, start_date, end_date, max_participants, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, 'active', ?)""",
            (cid, name, track_or_level, start_date, end_date, max_participants, now)
        )
        return {"success": True, "cohort_id": cid, "name": name, "status": "active"}

    def enroll_participant(
        self,
        cohort_id: str,
        user_id: str,
        email: Optional[str] = None,
        has_consent: bool = True
    ) -> Dict[str, Any]:
        """Enrolls a participant into a cohort with mandatory consent."""
        cohort = self.db.fetchone("SELECT * FROM beta_cohorts WHERE id = ?", (cohort_id,))
        if not cohort:
            return {"success": False, "error": f"Beta cohort '{cohort_id}' not found."}

        existing = self.db.fetchone(
            "SELECT id FROM beta_participants WHERE cohort_id = ? AND user_id = ?",
            (cohort_id, user_id)
        )
        if existing:
            return {"success": False, "error": "Participant is already enrolled in this cohort."}

        part_id = f"bpart_{uuid.uuid4().hex[:10]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        consent_status = "consented" if has_consent else "pending"

        self.db.execute(
            """INSERT INTO beta_participants (id, cohort_id, user_id, email, consent_status, status, enrolled_at)
               VALUES (?, ?, ?, ?, ?, 'active', ?)""",
            (part_id, cohort_id, user_id, email, consent_status, now)
        )

        return {
            "success": True,
            "participant_id": part_id,
            "cohort_id": cohort_id,
            "user_id": user_id,
            "consent_status": consent_status
        }

    def list_participants(self, cohort_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists enrolled beta participants."""
        query = "SELECT * FROM beta_participants"
        params = []
        if cohort_id:
            query += " WHERE cohort_id = ?"
            params.append(cohort_id)
        rows = self.db.fetchall(query, tuple(params))
        return [dict(r) for r in rows]

    def submit_feedback(
        self,
        cohort_id: str,
        category: str,
        rating: int,
        comments: str,
        participant_id: Optional[str] = None,
        is_anonymous: bool = False
    ) -> Dict[str, Any]:
        """Submits candidate feedback across defined usability/pedagogy categories."""
        if category not in self.FEEDBACK_CATEGORIES:
            return {"success": False, "error": f"Invalid category. Allowed: {', '.join(self.FEEDBACK_CATEGORIES)}"}

        if not (1 <= rating <= 5):
            return {"success": False, "error": "Rating must be between 1 and 5."}

        fid = f"fb_{uuid.uuid4().hex[:10]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        self.db.execute(
            """INSERT INTO beta_feedback (id, cohort_id, participant_id, is_anonymous, category, rating, comments, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (fid, cohort_id, None if is_anonymous else participant_id, 1 if is_anonymous else 0, category, rating, comments, now)
        )
        return {"success": True, "feedback_id": fid, "category": category, "rating": rating}

    def report_bug(
        self,
        cohort_id: str,
        title: str,
        description: str,
        severity: str = "medium",
        steps_to_reproduce: Optional[str] = None,
        reporter_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Submits a bug report classified by severity."""
        clean_sev = severity.lower().strip()
        if clean_sev not in self.VALID_SEVERITIES:
            return {"success": False, "error": f"Invalid severity '{severity}'. Allowed: {', '.join(self.VALID_SEVERITIES)}"}

        bug_id = f"bug_{uuid.uuid4().hex[:10]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        self.db.execute(
            """INSERT INTO beta_bug_reports (id, cohort_id, reporter_id, severity, title, description, steps_to_reproduce, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'open', ?)""",
            (bug_id, cohort_id, reporter_id, clean_sev, title, description, steps_to_reproduce or "", now)
        )
        return {"success": True, "bug_id": bug_id, "severity": clean_sev, "status": "open"}

    def get_beta_analytics(self) -> Dict[str, Any]:
        """Compiles analytics across cohorts, participants, feedback ratings, and bug reports."""
        cohorts = self.list_cohorts()
        total_participants = self.db.fetchone("SELECT COUNT(*) FROM beta_participants")[0]
        total_consented = self.db.fetchone("SELECT COUNT(*) FROM beta_participants WHERE consent_status = 'consented'")[0]

        feedback_count = self.db.fetchone("SELECT COUNT(*) FROM beta_feedback")[0]
        avg_rating_row = self.db.fetchone("SELECT AVG(rating) FROM beta_feedback")
        avg_rating = round(avg_rating_row[0], 2) if avg_rating_row and avg_rating_row[0] else 0.0

        # Bugs by severity
        bug_rows = self.db.fetchall("SELECT severity, COUNT(*) FROM beta_bug_reports GROUP BY severity")
        bugs_by_sev = {r[0]: r[1] for r in bug_rows}
        for s in self.VALID_SEVERITIES:
            bugs_by_sev.setdefault(s, 0)

        # Category rating breakdown
        cat_rows = self.db.fetchall("SELECT category, AVG(rating), COUNT(*) FROM beta_feedback GROUP BY category")
        ratings_by_cat = {r[0]: {"avg_rating": round(r[1], 2), "count": r[2]} for r in cat_rows}

        # Mock exams completed by enrolled beta participants
        exam_rows = self.db.fetchall(
            """SELECT e.status, COUNT(*) 
               FROM exam_sessions e
               JOIN beta_participants p ON e.learner_id = p.user_id
               GROUP BY e.status"""
        )
        exam_stats = {r[0]: r[1] for r in exam_rows}
        submitted_exams = exam_stats.get("submitted", 0)
        in_prog_exams = exam_stats.get("in_progress", 0)
        abandoned_exams = exam_stats.get("abandoned", 0)
        total_exams = submitted_exams + in_prog_exams + abandoned_exams
        completion_rate = round((submitted_exams / max(1, total_exams)) * 100.0, 1) if total_exams > 0 else 0.0

        return {
            "total_cohorts": len(cohorts),
            "total_participants": total_participants,
            "consented_participants": total_consented,
            "exam_completion_rate_pct": completion_rate,
            "submitted_exams_count": submitted_exams,
            "abandoned_exams_count": abandoned_exams,
            "total_feedback_submissions": feedback_count,
            "overall_usability_rating": avg_rating,
            "ratings_by_category": ratings_by_cat,
            "bugs_by_severity": bugs_by_sev,
            "cohorts": cohorts
        }
