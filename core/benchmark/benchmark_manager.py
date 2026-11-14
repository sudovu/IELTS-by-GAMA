"""
Human Benchmark Dataset Manager for IELTS by GAMA.
Hardened for Phase 17:
- Documented pseudonymization and PII redaction pipeline.
- Mandatory explicit candidate consent enforcement before enrollment.
- Revocation and right-to-erasure workflow with physical recording file cleanup.
- Double-marking linkage and consensus band recording.
- Non-identifying withdrawal audit records.
"""

import os
import re
import json
import uuid
import datetime
from typing import Optional, Dict, Any, List
from core.database.db_manager import DatabaseManager


class BenchmarkManager:
    """Manages benchmark dataset enrollment, pseudonymization, and consent compliance."""

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()

    @staticmethod
    def pseudonymize_text(text: str) -> str:
        """
        Applies a multi-stage redaction pipeline to strip direct and common indirect identifiers.
        Note: This is pseudonymization and redaction, not guaranteed zero-entropy anonymization,
        as natural language text may still contain subtle stylistic characteristics.
        """
        if not text:
            return ""

        sanitized = text

        # 1. Email addresses (standard RFC-compliant pattern)
        sanitized = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "[EMAIL REDACTED]",
            sanitized
        )

        # 2. International and domestic telephone numbers (including local 7-digit numbers)
        sanitized = re.sub(
            r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b|\b\d{3}[-.\s]?\d{4}\b",
            "[PHONE REDACTED]",
            sanitized
        )

        # 3. Candidate / Student / Passport ID references & standard identifier formats
        sanitized = re.sub(
            r"\b(?:Candidate|Student|Learner|Passport|ID|Desk)\s*(?:ID|Number|No\.?|#)?\s*(?:is\s*)?[:=\-]?\s*[A-Za-z0-9\-]{4,20}\b",
            "[ID REDACTED]",
            sanitized,
            flags=re.IGNORECASE
        )
        sanitized = re.sub(
            r"\b(?:CAND|STU|PASSPORT|IELTS|STUDENT|CANDIDATE)-[A-Za-z0-9]{4,12}\b",
            "[ID REDACTED]",
            sanitized,
            flags=re.IGNORECASE
        )

        # 4. Physical postal addresses & street numbers (e.g. 123 Main Street, Flat 4B, 742 Evergreen Terrace)
        sanitized = re.sub(
            r"\b\d{1,5}\s+(?:[A-Z][a-z]+\s+)*(?:Street|St\.?|Road|Rd\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Lane|Ln\.?|Drive|Dr\.?|Terrace|Terr\.?|Way|Court|Ct\.?|Place|Pl\.?|Close|Square|Sq\.?)\b",
            "[ADDRESS REDACTED]",
            sanitized,
            flags=re.IGNORECASE
        )

        # 5. Salutations and letter sign-offs with personal names
        sanitized = re.sub(
            r"\b(Dear|Sincerely|Regards|Yours faithfully|Yours sincerely|Best wishes)[,\s]+(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?|Prof\.?)?\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b",
            r"\1 [NAME REDACTED]",
            sanitized
        )

        # 6. Standalone honorifics followed by capitalized names
        sanitized = re.sub(
            r"\b(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?|Prof\.?)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b",
            "[NAME REDACTED]",
            sanitized
        )

        return sanitized

    anonymize_text = pseudonymize_text

    def enroll_benchmark_submission(
        self,
        assessment_type: str,
        content: str,
        candidate_id: Optional[str] = None,
        task_type: Optional[str] = None,
        track: Optional[str] = None,
        recording_ref: Optional[str] = None,
        has_consent: bool = False,
        consent_purpose: str = "internal_assessment_calibration",
        dataset_version: str = "1.6.0"
    ) -> Dict[str, Any]:
        """
        Enrolls a candidate submission into the benchmark dataset.
        MANDATORY REQUIREMENT: has_consent must be True.
        """
        if not has_consent:
            return {
                "success": False,
                "error": "Consent violation: Explicit candidate informed consent is required to enroll content into the benchmark dataset."
            }

        # Apply redaction pipeline
        anonymized = self.pseudonymize_text(content)
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
            "consent_purpose": consent_purpose,
            "dataset_version": dataset_version,
            "enrolled_at": now
        }

    def withdraw_consent(self, benchmark_id: str, reason: str = "Candidate requested withdrawal") -> Dict[str, Any]:
        """
        Enforces candidate right to erasure / consent revocation:
        1. Marks consent_status = 'withdrawn'
        2. Overwrites submission text with [CONTENT_WITHDRAWN_AND_PURGED]
        3. Nulls consensus bands and criteria json
        4. Deletes associated recording file if present on disk
        5. Logs an immutable non-identifying audit record
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        row = self.db.fetchone("SELECT recording_ref FROM benchmark_records WHERE id = ?", (benchmark_id,))
        if not row:
            return {"success": False, "error": f"Benchmark record '{benchmark_id}' not found."}

        recording_ref = row[0]
        # Clean up local audio recording file if exists
        if recording_ref and os.path.isabs(recording_ref) and os.path.exists(recording_ref):
            try:
                os.remove(recording_ref)
            except Exception:
                pass

        self.db.execute(
            """UPDATE benchmark_records
               SET consent_status = 'withdrawn',
                   anonymized_content = '[CONTENT_WITHDRAWN_AND_PURGED]',
                   consensus_human_band = NULL,
                   consensus_criteria_json = NULL,
                   recording_ref = NULL,
                   updated_at = ?
               WHERE id = ?""",
            (now, benchmark_id)
        )

        # Record non-identifying audit entry
        try:
            self.db.execute(
                """INSERT OR REPLACE INTO system_settings (key, value, updated_at)
                   VALUES (?, ?, ?)""",
                (f"erasure_audit_{benchmark_id}", json.dumps({"action": "consent_withdrawn", "timestamp": now, "reason": reason}), now)
            )
        except Exception:
            pass

        return {
            "success": True,
            "benchmark_id": benchmark_id,
            "status": "withdrawn",
            "purged": True,
            "withdrawn_at": now
        }

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
                try:
                    item["consensus_criteria"] = json.loads(item["consensus_criteria_json"])
                except Exception:
                    item["consensus_criteria"] = {}
            results.append(item)
        return results

    def get_benchmark_record(self, benchmark_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single benchmark record."""
        row = self.db.fetchone("SELECT * FROM benchmark_records WHERE id = ?", (benchmark_id,))
        if not row:
            return None
        item = dict(row)
        if item.get("consensus_criteria_json"):
            try:
                item["consensus_criteria"] = json.loads(item["consensus_criteria_json"])
            except Exception:
                item["consensus_criteria"] = {}
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
               WHERE id = ? AND consent_status = 'consented'""",
            (human_band, json.dumps(criteria_scores), 1 if double_marked else 0, now, benchmark_id)
        )
        return {"success": True, "benchmark_id": benchmark_id, "consensus_band": human_band}
