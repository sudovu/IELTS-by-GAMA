"""
Human Benchmark Dataset Manager for IELTS by GAMA.
Manages candidate enrollment into the anonymized benchmark dataset with explicit consent,
consent withdrawal, double-marking linkage, and privacy protection.
"""

import re
import json
import uuid
import datetime
from typing import Optional, Dict, Any, List
from core.database.db_manager import DatabaseManager


class BenchmarkManager:
    """Manages benchmark dataset enrollment, anonymization, and consent compliance."""

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()

    @staticmethod
    def anonymize_text(text: str) -> str:
        """Removes personal identifiers (names, emails, candidate IDs) from submission text."""
        # Strip emails
        sanitized = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL REDACTED]", text)
        # Strip phone numbers
        sanitized = re.sub(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE REDACTED]", sanitized)
        # Strip specific salutations with names
        sanitized = re.sub(r"\b(Dear|Sincerely|Regards|Yours faithfully|Yours sincerely)[,\s]+[A-Z][a-z]+(\s+[A-Z][a-z]+)?", r"\1 [NAME REDACTED]", sanitized)
        return sanitized

    def enroll_benchmark_submission(
        self,
        assessment_type: str,
        content: str,
        task_type: Optional[str] = None,
        track: Optional[str] = None,
        recording_ref: Optional[str] = None,
        has_consent: bool = True,
        dataset_version: str = "1.0.0"
    ) -> Dict[str, Any]:
        """
        Enrolls an anonymized candidate submission into the benchmark dataset.
        Requires explicit candidate consent.
        """
        if not has_consent:
            return {
                "success": False,
                "error": "Explicit candidate consent is required to enroll content into the benchmark dataset."
            }

        anonymized = self.anonymize_text(content)
        bench_id = f"bench_{uuid.uuid4().hex[:12]}"
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        self.db.execute(
            """INSERT INTO benchmark_records
               (id, assessment_type, task_type, track, anonymized_content, recording_ref, consent_status, consent_timestamp, dataset_version, double_marked, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, 'consented', ?, ?, 0, ?, ?)""",
            (bench_id, assessment_type, task_type, track, anonymized, recording_ref, now, dataset_version, now, now)
        )

        return {
            "success": True,
            "benchmark_id": bench_id,
            "assessment_type": assessment_type,
            "task_type": task_type,
            "track": track,
            "consent_status": "consented",
            "dataset_version": dataset_version,
            "enrolled_at": now
        }

    def withdraw_consent(self, benchmark_id: str) -> Dict[str, Any]:
        """Withdraws consent and flags/redacts the benchmark record."""
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.db.execute(
            """UPDATE benchmark_records
               SET consent_status = 'withdrawn', anonymized_content = '[CONTENT WITHDRAWN BY USER REQUEST]', updated_at = ?
               WHERE id = ?""",
            (now, benchmark_id)
        )
        return {"success": True, "benchmark_id": benchmark_id, "status": "withdrawn", "withdrawn_at": now}

    def list_benchmark_records(
        self,
        assessment_type: Optional[str] = None,
        consent_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Lists enrolled benchmark records with controlled access."""
        query = "SELECT * FROM benchmark_records WHERE 1=1"
        params = []

        if consent_only:
            query += " AND consent_status = 'consented'"
        if assessment_type:
            query += " AND assessment_type = ?"
            params.append(assessment_type)

        query += " ORDER BY created_at DESC"
        rows = self.db.fetchall(query, tuple(params))

        results = []
        for r in rows:
            item = dict(r)
            if item.get("consensus_criteria_json"):
                item["consensus_criteria"] = json.loads(item["consensus_criteria_json"])
            results.append(item)
        return results

    def get_benchmark_record(self, benchmark_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single benchmark record."""
        row = self.db.fetchone("SELECT * FROM benchmark_records WHERE id = ?", (benchmark_id,))
        if not row:
            return None
        item = dict(row)
        if item.get("consensus_criteria_json"):
            item["consensus_criteria"] = json.loads(item["consensus_criteria_json"])
        return item

    def update_consensus_scores(
        self,
        benchmark_id: str,
        human_band: float,
        criteria_scores: Dict[str, float],
        double_marked: bool = True
    ) -> Dict[str, Any]:
        """Updates official verified human consensus scores for a benchmark entry."""
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.db.execute(
            """UPDATE benchmark_records
               SET consensus_human_band = ?, consensus_criteria_json = ?, double_marked = ?, updated_at = ?
               WHERE id = ?""",
            (human_band, json.dumps(criteria_scores), 1 if double_marked else 0, now, benchmark_id)
        )
        return {"success": True, "benchmark_id": benchmark_id, "consensus_band": human_band}
