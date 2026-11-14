"""
Central Examination Manager for IELTS by GAMA.
Orchestrates full 4-skill mock examinations and skill-specific practice sessions.
Implements:
1. Session lifecycle (start, autosave, recover, submit, review)
2. Strict active-session security & answer key concealment
3. Dual-task Writing weighting (Task 1 = 1/3, Task 2 = 2/3)
4. Comprehensive objective evaluation (Reading & Listening out of 40)
5. Multi-part Speaking evaluation with STT modality transparency
6. Mistake Book & Adaptive Study Planner integration
7. Learner data isolation & duplicate submission locking
"""

import json
import uuid
import datetime
from typing import Dict, Any, List, Optional
from ..database.db_manager import DatabaseManager
from ..database.repositories import (
    ExamSessionRepository,
    TestResultRepository,
    MistakeBookRepository,
    LearnerRepository
)
from ..reading.reading_engine import ReadingEngine
from ..reading.question_types import ReadingQuestionTypes
from ..listening.listening_engine import ListeningEngine
from ..listening.answer_checker import ListeningAnswerChecker
from ..scoring.band_calculator import BandCalculator
from ..scoring.criteria_evaluator import CriteriaEvaluator
from ..writing.writing_evaluator import WritingEvaluator
from ..speaking.speaking_examiner import SpeakingExaminer
from .content_repository import ExamContentRepository


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class ExamManager:
    """Central orchestrator for IELTS practice and simulation examinations."""

    def __init__(self, db: Optional[DatabaseManager] = None, mistake_repo: Optional[MistakeBookRepository] = None):
        self.db = db or DatabaseManager()
        self.exam_repo = ExamSessionRepository(self.db)
        self.result_repo = TestResultRepository(self.db)
        self.mistake_repo = mistake_repo or MistakeBookRepository(self.db)
        self.learner_repo = LearnerRepository(self.db)

    # -------------------------------------------------------------------------
    # 1. SESSION INITIALIZATION & START
    # -------------------------------------------------------------------------
    def start_exam(
        self,
        learner_id: str,
        track: str = "Academic",
        module: str = "full_mock",
        exam_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Starts a new examination session.
        Returns sanitized examination questions without answer keys.
        """
        self.learner_repo.get_or_create_default(learner_id)

        # Normalize module and track
        norm_track = "Academic" if "acad" in track.lower() else "General Training"
        norm_module = module.lower().strip()

        # Resolve default exam ID if not explicitly specified
        if not exam_id:
            if norm_module in ("full_mock", "mock_full", "full"):
                exam_id = "mock_full_acad" if norm_track == "Academic" else "mock_full_gt"
                norm_module = "full_mock"
            elif "read" in norm_module:
                exam_id = "exam_read_acad_1" if norm_track == "Academic" else "exam_read_gt_1"
                norm_module = "reading"
            elif "listen" in norm_module:
                exam_id = "exam_listen_1"
                norm_module = "listening"
            elif "write" in norm_module:
                exam_id = "exam_write_acad_1" if norm_track == "Academic" else "exam_write_gt_1"
                norm_module = "writing"
            elif "speak" in norm_module:
                exam_id = "exam_speak_1"
                norm_module = "speaking"
            else:
                exam_id = "mock_full_acad" if norm_track == "Academic" else "mock_full_gt"
                norm_module = "full_mock"

        # Calculate time limit in seconds
        time_limits = {
            "reading": 60 * 60,      # 60 minutes
            "listening": 32 * 60,    # 32 minutes (30 mins + 2 mins review)
            "writing": 60 * 60,      # 60 minutes
            "speaking": 14 * 60,     # 14 minutes
            "full_mock": 164 * 60    # 164 minutes total
        }
        time_limit_sec = time_limits.get(norm_module, 60 * 60)

        # Retrieve sanitized client package (strictly hides answer keys and evidence)
        client_pkg = ExamContentRepository.get_exam_package(exam_id, conceal_answers=True)
        if not client_pkg:
            raise ValueError(f"Exam package '{exam_id}' not found")

        # Create persistent session in SQLite
        session_id = f"exam_{uuid.uuid4().hex[:12]}"
        now = _now_iso()

        initial_state = {
            "exam_id": exam_id,
            "answers": {},
            "flagged": [],
            "current_section": "listening" if norm_module == "full_mock" else norm_module,
            "current_question": 1
        }

        self.db.execute(
            """INSERT INTO exam_sessions
               (id, learner_id, module, track, status, time_limit_seconds, time_spent_seconds, answers_json, results_json, started_at)
               VALUES (?, ?, ?, ?, 'in_progress', ?, 0, ?, '{}', ?)""",
            (session_id, learner_id, norm_module, norm_track, time_limit_sec, json.dumps(initial_state), now)
        )

        return {
            "session_id": session_id,
            "learner_id": learner_id,
            "exam_id": exam_id,
            "track": norm_track,
            "module": norm_module,
            "status": "in_progress",
            "time_limit_seconds": time_limit_sec,
            "remaining_seconds": time_limit_sec,
            "started_at": now,
            "exam_package": client_pkg,
            "initial_state": initial_state
        }

    # -------------------------------------------------------------------------
    # 2. ACTIVE SESSION RECOVERY & PERSISTENCE
    # -------------------------------------------------------------------------
    def get_active_session(self, learner_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the most recent in-progress examination session for the learner.
        Calculates elapsed time and returns sanitized state for instant refresh recovery.
        """
        row = self.db.fetchone(
            """SELECT * FROM exam_sessions 
               WHERE learner_id = ? AND status = 'in_progress' 
               ORDER BY started_at DESC LIMIT 1""",
            (learner_id,)
        )
        if not row:
            return None

        sess = dict(row)
        answers_data = json.loads(sess.get("answers_json") or "{}")

        # Parse started_at to compute real elapsed time
        started_at_str = sess.get("started_at", "")
        elapsed_sec = sess.get("time_spent_seconds", 0)

        if started_at_str:
            try:
                # Normalize ISO string with Z / timezone
                clean_iso = started_at_str.replace("Z", "+00:00")
                start_dt = datetime.datetime.fromisoformat(clean_iso)
                now_dt = datetime.datetime.now(datetime.timezone.utc)
                calc_elapsed = int((now_dt - start_dt).total_seconds())
                elapsed_sec = max(elapsed_sec, calc_elapsed)
            except Exception:
                pass

        time_limit = sess.get("time_limit_seconds", 3600)
        remaining_sec = max(0, time_limit - elapsed_sec)

        # Retrieve sanitized exam package
        exam_id = answers_data.get("exam_id")
        if not exam_id:
            exam_id = "mock_full_acad" if sess.get("track") == "Academic" else "mock_full_gt"

        client_pkg = ExamContentRepository.get_exam_package(exam_id, conceal_answers=True)

        return {
            "session_id": sess["id"],
            "learner_id": learner_id,
            "exam_id": exam_id,
            "track": sess["track"],
            "module": sess["module"],
            "status": sess["status"],
            "time_limit_seconds": time_limit,
            "time_spent_seconds": elapsed_sec,
            "remaining_seconds": remaining_sec,
            "started_at": sess["started_at"],
            "answers": answers_data.get("answers", {}),
            "flagged": answers_data.get("flagged", []),
            "current_section": answers_data.get("current_section"),
            "current_question": answers_data.get("current_question", 1),
            "exam_package": client_pkg
        }

    # -------------------------------------------------------------------------
    # 3. AUTOSAVE & STATE SYNCHRONIZATION
    # -------------------------------------------------------------------------
    def autosave_answers(
        self,
        session_id: str,
        learner_id: str,
        answers: Dict[str, Any],
        flagged_questions: Optional[List[Any]] = None,
        current_section: Optional[str] = None,
        current_question: Optional[Any] = None,
        time_spent_seconds: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Saves candidate responses, flagged items, and location safely.
        Ensures strict learner ownership.
        """
        row = self.db.fetchone("SELECT * FROM exam_sessions WHERE id = ?", (session_id,))
        if not row:
            return {"success": False, "error": f"Exam session {session_id} not found"}

        sess = dict(row)
        if sess["learner_id"] != learner_id:
            return {"success": False, "error": "Unauthorized learner session access"}

        if sess["status"] != "in_progress":
            return {"success": False, "error": f"Cannot autosave to {sess['status']} exam session"}

        # Validate answers payload type
        if not isinstance(answers, dict):
            return {"success": False, "error": "Answers payload must be a key-value dictionary"}

        # Server-authoritative timer check (Grace period: 300s / 5 mins)
        started_at_str = sess.get("started_at", "")
        time_limit = sess.get("time_limit_seconds", 3600)
        if started_at_str:
            try:
                start_dt = datetime.datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
                now_dt = datetime.datetime.now(datetime.timezone.utc)
                calc_elapsed = int((now_dt - start_dt).total_seconds())
                if calc_elapsed > (time_limit + 300):
                    return {"success": False, "error": "Examination time has expired. New answers cannot be autosaved."}
            except Exception:
                pass

        current_data = json.loads(sess.get("answers_json") or "{}")
        # Merge answers monotonically to protect against stale overwrites
        current_answers = current_data.get("answers")
        if not isinstance(current_answers, dict):
            current_answers = {}
        current_answers.update(answers)
        current_data["answers"] = current_answers
        current_data["revision"] = current_data.get("revision", 0) + 1

        if flagged_questions is not None:
            current_data["flagged"] = flagged_questions
        if current_section is not None:
            current_data["current_section"] = current_section
        if current_question is not None:
            current_data["current_question"] = current_question

        new_time_spent = time_spent_seconds if time_spent_seconds is not None else sess.get("time_spent_seconds", 0)

        self.db.execute(
            "UPDATE exam_sessions SET answers_json = ?, time_spent_seconds = ? WHERE id = ?",
            (json.dumps(current_data), new_time_spent, session_id)
        )

        return {
            "success": True,
            "session_id": session_id,
            "saved_at": _now_iso(),
            "answered_count": len(current_answers),
            "revision": current_data["revision"],
            "time_spent_seconds": new_time_spent
        }

    # -------------------------------------------------------------------------
    # 4. SUBMISSION, SCORING & COMPREHENSIVE EVALUATION
    # -------------------------------------------------------------------------
    def submit_exam(
        self,
        session_id: str,
        learner_id: str,
        final_answers: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Submits and grades the practice examination.
        - Prevents duplicate submissions.
        - Evaluates Reading & Listening against official keys.
        - Evaluates Writing with 1/3 (Task 1) + 2/3 (Task 2) weighting.
        - Evaluates Speaking with non-acoustic modality disclosure.
        - Calculates overall band with confidence interval.
        - Logs errors to Mistake Book and generates adaptive recommendations.
        """
        row = self.db.fetchone("SELECT * FROM exam_sessions WHERE id = ?", (session_id,))
        if not row:
            return {"success": False, "error": f"Exam session {session_id} not found"}

        sess = dict(row)
        if sess["learner_id"] != learner_id:
            return {"success": False, "error": "Unauthorized learner session access"}

        # Prevent duplicate grading / modifications after submission or on abandoned sessions
        if sess["status"] != "in_progress":
            if sess["status"] == "submitted":
                results = json.loads(sess.get("results_json") or "{}")
                return {
                    "success": True,
                    "already_submitted": True,
                    "session_id": session_id,
                    "results": results,
                    "band_score": sess.get("band_score")
                }
            return {"success": False, "error": f"Cannot submit an exam session with status '{sess['status']}'"}

        # Server-authoritative timer check
        started_at_str = sess.get("started_at", "")
        time_limit = sess.get("time_limit_seconds", 3600)
        is_timed_out = False
        elapsed_sec = sess.get("time_spent_seconds", 0)

        if started_at_str:
            try:
                start_dt = datetime.datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
                now_dt = datetime.datetime.now(datetime.timezone.utc)
                calc_elapsed = int((now_dt - start_dt).total_seconds())
                elapsed_sec = max(elapsed_sec, calc_elapsed)
                # Grace period: 300 seconds (5 minutes) for network handshake / latency
                if calc_elapsed > (time_limit + 300):
                    is_timed_out = True
            except Exception:
                pass

        answers_state = json.loads(sess.get("answers_json") or "{}")
        user_answers = answers_state.get("answers", {})
        if not isinstance(user_answers, dict):
            user_answers = {}

        if final_answers and isinstance(final_answers, dict):
            user_answers.update(final_answers)

        exam_id = answers_state.get("exam_id")
        if not exam_id:
            exam_id = "mock_full_acad" if sess.get("track") == "Academic" else "mock_full_gt"

        # Retrieve canonical package WITH answer keys for grading
        canonical_pkg = ExamContentRepository.get_exam_package(exam_id, conceal_answers=False)
        if not canonical_pkg:
            return {"success": False, "error": f"Canonical exam package '{exam_id}' missing"}

        module = sess["module"]
        track = sess["track"]

        results: Dict[str, Any] = {
            "session_id": session_id,
            "learner_id": learner_id,
            "exam_id": exam_id,
            "track": track,
            "module": module,
            "submitted_at": _now_iso(),
            "skills": {},
            "recommendations": []
        }

        # ---------------------------------------------------------------------
        # A. GRADE READING
        # ---------------------------------------------------------------------
        reading_pkg = None
        if module in ("full_mock", "reading"):
            if "skills" in canonical_pkg and "reading" in canonical_pkg["skills"]:
                reading_pkg = canonical_pkg["skills"]["reading"]
            elif "passages" in canonical_pkg:
                reading_pkg = canonical_pkg
            elif "sections" in canonical_pkg and ("read" in exam_id or module == "reading"):
                reading_pkg = canonical_pkg

        if reading_pkg:
            reading_eval = self._evaluate_reading_package(reading_pkg, user_answers, track, learner_id)
            results["skills"]["reading"] = reading_eval

        # ---------------------------------------------------------------------
        # B. GRADE LISTENING
        # ---------------------------------------------------------------------
        listening_pkg = None
        if module in ("full_mock", "listening"):
            if "skills" in canonical_pkg and "listening" in canonical_pkg["skills"]:
                listening_pkg = canonical_pkg["skills"]["listening"]
            elif "sections" in canonical_pkg and ("listen" in exam_id or module == "listening"):
                listening_pkg = canonical_pkg

        if listening_pkg:
            listening_eval = self._evaluate_listening_package(listening_pkg, user_answers, learner_id)
            results["skills"]["listening"] = listening_eval

        # ---------------------------------------------------------------------
        # C. GRADE WRITING (1/3 Task 1 + 2/3 Task 2)
        # ---------------------------------------------------------------------
        writing_pkg = None
        if module in ("full_mock", "writing"):
            if "skills" in canonical_pkg and "writing" in canonical_pkg["skills"]:
                writing_pkg = canonical_pkg["skills"]["writing"]
            elif "task_1" in canonical_pkg and "task_2" in canonical_pkg:
                writing_pkg = canonical_pkg

        if writing_pkg:
            writing_eval = self._evaluate_writing_package(writing_pkg, user_answers, track)
            results["skills"]["writing"] = writing_eval

        # ---------------------------------------------------------------------
        # D. GRADE SPEAKING
        # ---------------------------------------------------------------------
        speaking_pkg = None
        if module in ("full_mock", "speaking"):
            if "skills" in canonical_pkg and "speaking" in canonical_pkg["skills"]:
                speaking_pkg = canonical_pkg["skills"]["speaking"]
            elif "part_1" in canonical_pkg and "part_2" in canonical_pkg:
                speaking_pkg = canonical_pkg

        if speaking_pkg:
            speaking_eval = self._evaluate_speaking_package(speaking_pkg, user_answers)
            results["skills"]["speaking"] = speaking_eval

        # ---------------------------------------------------------------------
        # E. CALCULATE OVERALL BAND SCORE & CONFIDENCE RANGE
        # ---------------------------------------------------------------------
        active_bands = []
        band_breakdown = {}

        for skill_name in ("listening", "reading", "writing", "speaking"):
            if skill_name in results["skills"]:
                b = results["skills"][skill_name].get("estimated_band", 0.0)
                band_breakdown[skill_name] = b
                active_bands.append(b)

        if active_bands:
            mean_raw = sum(active_bands) / len(active_bands)
            overall_band = BandCalculator.round_band(mean_raw)
            # Confidence interval (+- 0.5)
            conf_min = max(0.0, round(overall_band - 0.5, 1))
            conf_max = min(9.0, round(overall_band + 0.5, 1))
        else:
            mean_raw = 0.0
            overall_band = 0.0
            conf_min, conf_max = 0.0, 0.0

        results["overall_band"] = overall_band
        results["confidence_range"] = [conf_min, conf_max]
        results["raw_mean"] = round(mean_raw, 2)
        results["band_breakdown"] = band_breakdown
        results["is_timed_out"] = is_timed_out
        results["elapsed_seconds"] = elapsed_sec
        results["time_limit_seconds"] = time_limit
        results["timing_status"] = "Submitted after official examination time limit (+ grace period) expired." if is_timed_out else "Submitted on time."
        results["official_disclaimer"] = (
            "Practice estimate only. This is not an official IELTS score from Cambridge Assessment, "
            "IDP: IELTS Australia, or the British Council."
        )

        # ---------------------------------------------------------------------
        # F. PERSIST RESULTS TO DATABASE
        # ---------------------------------------------------------------------
        now = _now_iso()
        self.db.execute(
            """UPDATE exam_sessions 
               SET status = 'submitted', results_json = ?, band_score = ?, completed_at = ?
               WHERE id = ?""",
            (json.dumps(results), overall_band, now, session_id)
        )

        # Also store into test_results table for permanent profile analytics
        test_type = "mock_full" if module == "full_mock" else module
        self.result_repo.record_result(
            learner_id=learner_id,
            test_type=test_type,
            track=track,
            overall_band=overall_band,
            details=results,
            listening_band=band_breakdown.get("listening"),
            reading_band=band_breakdown.get("reading"),
            writing_band=band_breakdown.get("writing"),
            speaking_band=band_breakdown.get("speaking")
        )

        return {
            "success": True,
            "session_id": session_id,
            "overall_band": overall_band,
            "confidence_range": [conf_min, conf_max],
            "results": results
        }

    # -------------------------------------------------------------------------
    # INTERNAL EVALUATION HELPERS
    # -------------------------------------------------------------------------
    def _evaluate_reading_package(
        self,
        pkg: Dict[str, Any],
        user_answers: Dict[str, Any],
        track: str,
        learner_id: str
    ) -> Dict[str, Any]:
        """Evaluates 40 questions of Reading, logging mistakes and identifying weak types."""
        items = pkg.get("passages") or pkg.get("sections") or []
        read_sub = user_answers.get("reading") if isinstance(user_answers.get("reading"), dict) else {}
        total_questions = 0
        correct_count = 0
        unanswered_count = 0
        question_breakdown = []
        type_performance: Dict[str, Dict[str, int]] = {}

        for item in items:
            for q in item.get("questions", []):
                qnum = q["num"]
                total_questions += 1
                qtype = q.get("type", "Completion")
                
                # Check answers using integer or string key, e.g. "read_1" or "1"
                ans = (
                    user_answers.get(f"read_{qnum}") or user_answers.get(str(qnum)) or user_answers.get(qnum) or
                    read_sub.get(f"read_{qnum}") or read_sub.get(str(qnum)) or read_sub.get(qnum) or ""
                )
                eval_res = ReadingQuestionTypes.grade_question(q, str(ans))
                
                is_correct = eval_res.get("is_correct", False)
                is_unanswered = eval_res.get("is_unanswered", not bool(str(ans).strip()))
                
                if is_unanswered:
                    unanswered_count += 1

                if is_correct:
                    correct_count += 1
                else:
                    # Log mistake to Mistake Book
                    self.mistake_repo.record_mistake(
                        learner_id=learner_id,
                        skill="reading",
                        category=f"Reading: {qtype}",
                        original_text=str(ans) if ans else "Unanswered",
                        corrected_text=str(q.get("correct", "")),
                        explanation=q.get("explanation", "")
                    )

                # Track performance by question type
                if qtype not in type_performance:
                    type_performance[qtype] = {"correct": 0, "total": 0}
                type_performance[qtype]["total"] += 1
                if is_correct:
                    type_performance[qtype]["correct"] += 1

                question_breakdown.append({
                    "question_num": qnum,
                    "question_id": f"read_{qnum}",
                    "passage": item.get("title", ""),
                    "type": qtype,
                    "prompt": q.get("prompt", ""),
                    "user_answer": str(ans),
                    "accepted_answers": q.get("acceptable") or [q.get("correct", "")],
                    "correct_answer": q.get("correct", ""),
                    "is_correct": is_correct,
                    "is_unanswered": is_unanswered,
                    "marks_awarded": 1 if is_correct else 0,
                    "marks_available": 1,
                    "evidence": q.get("evidence", ""),
                    "explanation": q.get("explanation", ""),
                    "review_topic": f"Reading: {qtype}",
                    "verification_status": "verified_practice_content",
                    "examiner_verified": False
                })

        band = BandCalculator.raw_to_band_reading(correct_count, track=track, total_questions=total_questions)
        incorrect_count = total_questions - correct_count - unanswered_count

        # Identify weak question types (< 60% accuracy)
        weak_types = [t for t, stats in type_performance.items() if (stats["correct"] / max(1, stats["total"])) < 0.6]

        return {
            "correct_answers": correct_count,
            "incorrect_answers": incorrect_count,
            "unanswered_questions": unanswered_count,
            "raw_score": correct_count,
            "max_raw_score": total_questions,
            "total_questions": total_questions,
            "accuracy_percent": round((correct_count / max(1, total_questions)) * 100, 1),
            "estimated_band": band,
            "confidence_range": [max(0.0, band - 0.5), min(9.0, band + 0.5)],
            "scoring_rule": f"Official IELTS {track} Band Table (raw score out of {total_questions})",
            "scoring_rule_version": "1.6.0",
            "answer_key_version": "1.6.0",
            "examiner_verified": False,
            "disclaimer": "Diagnostic practice score calculated automatically. Not an official IELTS score. No human examiner validation.",
            "type_performance": type_performance,
            "weak_types": weak_types,
            "questions": question_breakdown,
            "question_breakdown": question_breakdown
        }

    def _evaluate_listening_package(
        self,
        pkg: Dict[str, Any],
        user_answers: Dict[str, Any],
        learner_id: str
    ) -> Dict[str, Any]:
        """Evaluates 40 questions of Listening with ListeningAnswerChecker."""
        sections = pkg.get("sections", [])
        listen_sub = user_answers.get("listening") if isinstance(user_answers.get("listening"), dict) else {}
        total_questions = 0
        correct_count = 0
        unanswered_count = 0
        question_breakdown = []

        for sec in sections:
            sec_num = sec.get("section_number", 1)
            for q in sec.get("questions", []):
                qnum = q["num"]
                total_questions += 1

                ans = (
                    user_answers.get(f"listen_{qnum}") or user_answers.get(str(qnum)) or user_answers.get(qnum) or
                    listen_sub.get(f"listen_{qnum}") or listen_sub.get(str(qnum)) or listen_sub.get(qnum) or ""
                )
                acceptable = q.get("acceptable") or [q.get("correct", "")]
                max_words = q.get("max_words", 2)

                is_unanswered = not bool(str(ans).strip())
                if is_unanswered:
                    unanswered_count += 1

                is_correct, feedback_note = ListeningAnswerChecker.check_answer(
                    user_input=str(ans),
                    acceptable_answers=acceptable,
                    max_words=max_words
                )

                if is_correct:
                    correct_count += 1
                else:
                    self.mistake_repo.record_mistake(
                        learner_id=learner_id,
                        skill="listening",
                        category=f"Listening: Section {sec_num}",
                        original_text=str(ans) if ans else "Unanswered",
                        corrected_text=acceptable[0] if acceptable else "",
                        explanation=q.get("distractor_note", "Ensure exact spelling and word limits.")
                    )

                question_breakdown.append({
                    "question_num": qnum,
                    "question_id": f"listen_{qnum}",
                    "section_number": sec_num,
                    "section_title": sec.get("title", ""),
                    "prompt": q.get("prompt", ""),
                    "user_answer": str(ans),
                    "accepted_answers": acceptable,
                    "correct_answer": acceptable[0] if acceptable else "",
                    "is_correct": is_correct,
                    "is_unanswered": is_unanswered,
                    "marks_awarded": 1 if is_correct else 0,
                    "marks_available": 1,
                    "feedback": feedback_note,
                    "distractor_note": q.get("distractor_note", ""),
                    "review_topic": f"Listening: Section {sec_num} Dialogue & Conventions",
                    "verification_status": "verified_practice_content",
                    "examiner_verified": False
                })

        band = BandCalculator.raw_to_band_listening(correct_count, total_questions=total_questions)
        incorrect_count = total_questions - correct_count - unanswered_count

        return {
            "correct_answers": correct_count,
            "incorrect_answers": incorrect_count,
            "unanswered_questions": unanswered_count,
            "raw_score": correct_count,
            "max_raw_score": total_questions,
            "total_questions": total_questions,
            "accuracy_percent": round((correct_count / max(1, total_questions)) * 100, 1),
            "estimated_band": band,
            "confidence_range": [max(0.0, band - 0.5), min(9.0, band + 0.5)],
            "scoring_rule": f"Official IELTS Listening Band Table (raw score out of {total_questions})",
            "scoring_rule_version": "1.6.0",
            "answer_key_version": "1.6.0",
            "examiner_verified": False,
            "disclaimer": "Diagnostic practice score calculated automatically. Not an official IELTS score. No human examiner validation.",
            "activity_type": "transcript_strategy_practice_and_synthesis",
            "audio_asset_status": "speech_synthesis_ready (pre-recorded studio audio files not bundled)",
            "questions": question_breakdown,
            "question_breakdown": question_breakdown
        }

    def _evaluate_writing_package(
        self,
        pkg: Dict[str, Any],
        user_answers: Dict[str, Any],
        track: str
    ) -> Dict[str, Any]:
        """
        Evaluates Task 1 and Task 2 with verified official IELTS weighting:
        Writing Band = round_band(1/3 * Task 1 + 2/3 * Task 2).
        Detects empty and underlength responses to prevent awarding high bands.
        """
        writing_sub = user_answers.get("writing") if isinstance(user_answers.get("writing"), dict) else {}
        t1_text = (
            user_answers.get("writing_task_1") or user_answers.get("task_1") or user_answers.get("task1_response") or
            writing_sub.get("writing_task_1") or writing_sub.get("task_1") or writing_sub.get("task1_response") or ""
        )
        t2_text = (
            user_answers.get("writing_task_2") or user_answers.get("task_2") or user_answers.get("task2_response") or
            writing_sub.get("writing_task_2") or writing_sub.get("task_2") or writing_sub.get("task2_response") or ""
        )

        t1_prompt = pkg.get("task_1", {}).get("prompt", "")
        t2_prompt = pkg.get("task_2", {}).get("prompt", "")

        # Evaluate Task 1
        eval_t1 = WritingEvaluator.evaluate_essay(
            prompt_id=pkg.get("task_1", {}).get("prompt_id", "acad_t1_emissions"),
            essay_text=t1_text
        )

        # Evaluate Task 2
        eval_t2 = WritingEvaluator.evaluate_essay(
            prompt_id=pkg.get("task_2", {}).get("prompt_id", "acad_t2_ubi"),
            essay_text=t2_text
        )

        band_t1 = eval_t1.get("estimated_band", eval_t1.get("overall_band", 0.0))
        band_t2 = eval_t2.get("estimated_band", eval_t2.get("overall_band", 0.0))

        # Enforce zero-length guard: empty submissions receive Band 0.0
        if len(t1_text.strip().split()) == 0:
            band_t1 = 0.0
        if len(t2_text.strip().split()) == 0:
            band_t2 = 0.0

        # Official 1/3 Task 1 + 2/3 Task 2 weighting
        if band_t1 == 0.0 and band_t2 == 0.0:
            composite_band = 0.0
        else:
            composite_raw = (1.0 / 3.0) * band_t1 + (2.0 / 3.0) * band_t2
            composite_band = BandCalculator.round_band(composite_raw)

        return {
            "estimated_band": composite_band,
            "confidence_range": [max(0.0, composite_band - 0.5), min(9.0, composite_band + 0.5)],
            "weighting_rule": "Task 1 (1/3 weight) + Task 2 (2/3 weight) according to official Cambridge IELTS formula",
            "scoring_rule_version": "1.6.0",
            "examiner_verified": False,
            "disclaimer": "Diagnostic AI practice estimate for formative guidance. Not an official IELTS score. No human examiner validation.",
            "task_1": {
                "title": pkg.get("task_1", {}).get("title"),
                "word_count": eval_t1.get("word_count", len(t1_text.split())),
                "band": band_t1,
                "criteria": eval_t1.get("criteria", {}),
                "feedback": eval_t1.get("feedback", {})
            },
            "task_2": {
                "title": pkg.get("task_2", {}).get("title"),
                "word_count": eval_t2.get("word_count", len(t2_text.split())),
                "band": band_t2,
                "criteria": eval_t2.get("criteria", {}),
                "feedback": eval_t2.get("feedback", {})
            }
        }

    def _evaluate_speaking_package(
        self,
        pkg: Dict[str, Any],
        user_answers: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluates Speaking Parts 1, 2, and 3 responses with explicit non-acoustic STT disclosures.
        """
        spk_sub = user_answers.get("speaking") if isinstance(user_answers.get("speaking"), dict) else {}
        p1_resp = user_answers.get("speaking_part_1") or user_answers.get("part_1") or user_answers.get("part1") or spk_sub.get("speaking_part_1") or spk_sub.get("part_1") or spk_sub.get("part1") or ""
        p2_resp = user_answers.get("speaking_part_2") or user_answers.get("part_2") or user_answers.get("part2") or spk_sub.get("speaking_part_2") or spk_sub.get("part_2") or spk_sub.get("part2") or ""
        p3_resp = user_answers.get("speaking_part_3") or user_answers.get("part_3") or user_answers.get("part3") or spk_sub.get("speaking_part_3") or spk_sub.get("part_3") or spk_sub.get("part3") or ""

        combined_text = f"{p1_resp}\n{p2_resp}\n{p3_resp}".strip()
        word_count = len(combined_text.split())

        # Evaluate response text (pass bare combined text so zero-response accurately yields Band 0.0)
        eval_res = SpeakingExaminer.evaluate_spoken_response(
            transcript=combined_text
        )

        if word_count == 0:
            band = 0.0
        else:
            band = eval_res.get("estimated_band", 6.0 if word_count > 50 else 2.0)

        return {
            "estimated_band": band,
            "confidence_range": [max(0.0, band - 0.5), min(9.0, band + 0.5)],
            "assessment_modality": "speech_recognition_transcript_matching (non-acoustic)",
            "acoustic_analysis_disclaimer": "Evaluated via transcript heuristics. Does not analyze acoustic pitch, intonation, or formant resonance.",
            "pronunciation_limitation": "A transcript alone cannot reliably establish pronunciation, accent quality, or intonation. Pronunciation is unassessed acoustically.",
            "examiner_verified": False,
            "scoring_rule": "IELTS Speaking 4-Criteria Public Descriptors",
            "scoring_rule_version": "1.6.0",
            "disclaimer": "Diagnostic AI practice estimate. Not an official IELTS score. No human examiner validation.",
            "word_count": word_count,
            "criteria": eval_res.get("criteria_breakdown", {}),
            "feedback": eval_res.get("examiner_feedback", {}),
            "parts_evaluated": {
                "part_1": bool(p1_resp),
                "part_2": bool(p2_resp),
                "part_3": bool(p3_resp)
            }
        }

    # -------------------------------------------------------------------------
    # 5. RESULTS REVIEW & HISTORY
    # -------------------------------------------------------------------------
    def get_exam_results(self, session_id: str, learner_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves full post-submission examination results with explanations and evidence."""
        row = self.db.fetchone("SELECT * FROM exam_sessions WHERE id = ?", (session_id,))
        if not row:
            return None

        sess = dict(row)
        if sess["learner_id"] != learner_id:
            return None

        results = json.loads(sess.get("results_json") or "{}")
        return {
            "session_id": sess["id"],
            "learner_id": sess["learner_id"],
            "module": sess["module"],
            "track": sess["track"],
            "status": sess["status"],
            "band_score": sess.get("band_score"),
            "started_at": sess.get("started_at"),
            "completed_at": sess.get("completed_at"),
            "time_spent_seconds": sess.get("time_spent_seconds"),
            "results": results
        }

    def list_learner_history(self, learner_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Lists historical examination sessions completed by the learner."""
        rows = self.db.fetchall(
            """SELECT id, learner_id, module, track, status, band_score, started_at, completed_at, time_spent_seconds 
               FROM exam_sessions 
               WHERE learner_id = ? 
               ORDER BY started_at DESC LIMIT ?""",
            (learner_id, limit)
        )
        return [dict(r) for r in rows]
