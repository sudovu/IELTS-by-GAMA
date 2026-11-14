"""
Local Web Server and REST API for IELTS by GAMA.
Built on Python's standard library ThreadingHTTPServer.
Runs 100% offline with zero external pip dependencies.
"""

import os
import sys
import json
import mimetypes
from typing import Optional, Dict, Any, List
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository, SettingsRepository, TestResultRepository
from core.chatbot.tutor_bot import UnifiedAITutor
from core.reading.reading_engine import ReadingEngine
from core.listening.listening_engine import ListeningEngine
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.speaking.pronunciation_coach import PronunciationCoach
from core.progress.mistake_book import MistakeBook
from core.progress.srs import SpacedRepetitionSystem
from core.progress.study_planner import StudyPlanner
from core.progress.analytics import LearningAnalytics
from core.grammar.adaptive_grammar import AdaptiveGrammar
from core.grammar.grammar_engine import GrammarEngine
from core.curriculum.curriculum_engine import CurriculumEngine
from core.vocabulary.vocabulary_vault import VocabularyVault
from core.scoring.cefr_diagnostic import CEFRDiagnostic
from core.sync.connectivity import ConnectivityManager
from core.device.profile_manager import ProfileManager
from core.exam import ExamContentRepository, ExamManager
from core.auth.auth_manager import AuthManager
from core.review.review_manager import ReviewManager
from core.review.double_marking import DoubleMarkingManager
from core.benchmark.benchmark_manager import BenchmarkManager
from core.benchmark.calibration_engine import CalibrationEngine
from core.beta.beta_manager import BetaManager


class GAMAHTTPRequestHandler(BaseHTTPRequestHandler):
    """Handles static web requests and REST API queries."""

    # Shared instances
    db = DatabaseManager()
    tutor = UnifiedAITutor(db)
    learner_repo = LearnerRepository(db)
    settings_repo = SettingsRepository(db)
    test_repo = TestResultRepository(db)
    curriculum = CurriculumEngine(db)
    reading = ReadingEngine()
    listening = ListeningEngine()
    writing = WritingEvaluator()
    speaking = SpeakingExaminer()
    vocab_vault = VocabularyVault(db)
    mistake_book = MistakeBook(db)
    srs = SpacedRepetitionSystem(db)
    planner = StudyPlanner(db)
    analytics = LearningAnalytics(db)
    adaptive_grammar = AdaptiveGrammar(db)
    connectivity = ConnectivityManager()
    exam_manager = ExamManager(db)
    auth_mgr = AuthManager(db)
    review_mgr = ReviewManager(db)
    double_marking_mgr = DoubleMarkingManager(db)
    benchmark_mgr = BenchmarkManager(db)
    calibration_engine = CalibrationEngine(db)
    beta_mgr = BetaManager(db)

    def _get_auth_token(self) -> Optional[str]:
        tok = self.headers.get("X-Session-Token")
        if tok:
            return tok.strip()
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            return auth[7:].strip()
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if "token" in qs and qs["token"]:
            return qs["token"][0].strip()
        return None

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0:
            return {}
        raw = self.rfile.read(content_len).decode("utf-8")
        return json.loads(raw) if raw else {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/api/status", "/api/health"]:
            cfg = ProfileManager.get_hardware_config()
            self._send_json({
                "status": "healthy",
                "version": "1.6.0",
                "connectivity": self.connectivity.get_ui_indicator(),
                "is_online": self.connectivity.is_online,
                "forced_offline": self.connectivity.is_forced_offline,
                "hardware_profile": cfg["profile"],
                "model_name": cfg["model_name"]
            })

        elif path == "/api/learners":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learners = self.learner_repo.list_all_learners()
            self._send_json({
                "learners": learners,
                "active_learner_id": active_id
            })

        elif path == "/api/learners/current":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            profile = self.learner_repo.get_or_create_default(active_id)
            self._send_json(profile)

        elif path == "/api/dashboard":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = parsed.query.replace("learner_id=", "").split("&")[0].strip() if "learner_id=" in parsed.query else active_id
            dash = self.analytics.get_dashboard_data(learner_id)
            daily = self.planner.generate_daily_plan(learner_id)
            self._send_json({"dashboard": dash, "daily_plan": daily})

        elif path == "/api/planner/daily":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = parsed.query.replace("learner_id=", "").split("&")[0].strip() if "learner_id=" in parsed.query else active_id
            plan = self.planner.generate_daily_plan(learner_id)
            self._send_json(plan)

        elif path == "/api/planner/weekly":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = parsed.query.replace("learner_id=", "").split("&")[0].strip() if "learner_id=" in parsed.query else active_id
            plan = self.planner.generate_weekly_plan(learner_id)
            self._send_json(plan)

        elif path == "/api/planner/adaptive":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = parsed.query.replace("learner_id=", "").split("&")[0].strip() if "learner_id=" in parsed.query else active_id
            plan = self.planner.generate_adaptive_study_plan(learner_id)
            self._send_json(plan)

        elif path == "/api/mistakes":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = parsed.query.replace("learner_id=", "").split("&")[0].strip() if "learner_id=" in parsed.query else active_id
            summary = self.mistake_book.get_summary_report(learner_id)
            active = self.mistake_book.get_due_mistakes(learner_id)
            self._send_json({"summary": summary, "active_mistakes": active})

        elif path == "/api/srs/due":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = parsed.query.replace("learner_id=", "").split("&")[0].strip() if "learner_id=" in parsed.query else active_id
            due = self.srs.get_due_deck(learner_id)
            self._send_json({"items": due})

        elif path == "/api/chat/history":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = parsed.query.replace("learner_id=", "").split("&")[0].strip() if "learner_id=" in parsed.query else active_id
            history = self.tutor.get_conversation_history(learner_id)
            self._send_json({"history": history})

        elif path == "/api/reading/passages":
            track = None
            if "track=" in parsed.query:
                track = parsed.query.replace("track=", "").split("&")[0].strip()
            passages = self.reading.list_passages(track=track)
            self._send_json({"passages": passages})

        elif path == "/api/reading/mock":
            track = "Academic"
            if "track=" in parsed.query:
                track = parsed.query.replace("track=", "").split("&")[0].strip()
            mock = self.reading.generate_full_mock(track=track)
            self._send_json(mock)

        elif path == "/api/reading":
            pid = "acad_p1"
            if "passage_id=" in parsed.query:
                pid = parsed.query.replace("passage_id=", "").split("&")[0].strip()
            show_ans = "show_answers=true" in parsed.query.lower()
            passage = self.reading.get_passage(pid, show_answers=show_ans) or self.reading.get_passage("acad_p1", show_answers=show_ans)
            self._send_json(passage)

        elif path == "/api/listening/sections":
            sections = self.listening.list_sections()
            self._send_json({"sections": sections})

        elif path == "/api/listening/mock":
            show_t = "show_transcript=true" in parsed.query.lower()
            mock = self.listening.generate_full_listening_mock(show_transcripts=show_t)
            self._send_json(mock)

        elif path == "/api/listening":
            sec_id = "sec_1"
            if "sec_id=" in parsed.query:
                sec_id = parsed.query.replace("sec_id=", "").split("&")[0].strip()
            show_t = "show_transcript=true" in parsed.query.lower()
            sec = self.listening.get_section(sec_id or "sec_1", show_transcript=show_t)
            self._send_json(sec or self.listening.get_section("sec_1", show_transcript=show_t))

        elif path == "/api/speaking/sets":
            sets = self.speaking.get_exam_sets()
            self._send_json({"sets": sets})

        elif path == "/api/speaking/prompts":
            card_idx = 0
            if "card_idx=" in parsed.query:
                try:
                    card_idx = int(parsed.query.replace("card_idx=", "").split("&")[0].strip())
                except ValueError:
                    card_idx = 0
            prompts = self.speaking.get_test_prompts(card_idx)
            self._send_json(prompts)

        elif path == "/api/speaking/pronunciation/minimal-pairs":
            self._send_json({"pairs": PronunciationCoach.list_minimal_pairs()})

        elif path == "/api/speaking/pronunciation/stress":
            self._send_json({"drills": PronunciationCoach.list_syllable_stress_drills()})

        elif path == "/api/speaking/pronunciation/connected":
            self._send_json({"drills": PronunciationCoach.list_connected_speech_drills()})

        elif path == "/api/writing/prompts":
            track = None
            task_type = None
            if "track=" in parsed.query:
                track = parsed.query.split("track=")[1].split("&")[0].strip()
            if "task_type=" in parsed.query:
                task_type = parsed.query.split("task_type=")[1].split("&")[0].strip()
            prompts = self.writing.list_prompts(track=track, task_type=task_type)
            self._send_json({"prompts": prompts})

        elif path == "/api/writing/drafts":
            learner_id = self.settings_repo.get("active_learner_id", "default_learner")
            if "learner_id=" in parsed.query:
                learner_id = parsed.query.split("learner_id=")[1].split("&")[0].strip()
            drafts = self.writing.get_learner_drafts(learner_id, db=self.db)
            self._send_json({"drafts": drafts})

        elif path == "/api/grammar/adaptive":
            session = self.adaptive_grammar.generate_adaptive_session("default_learner")
            self._send_json(session)

        elif path == "/api/grammar/fillups":
            category = None
            if "category=" in parsed.query:
                category = parsed.query.replace("category=", "").split("&")[0].strip()
            drills = GrammarEngine.get_fill_up_drills(category)
            self._send_json({"drills": drills})

        elif path == "/api/vocabulary/words":
            query = ""
            cefr = None
            if "q=" in parsed.query:
                query = parsed.query.split("q=")[1].split("&")[0].strip()
            if "cefr=" in parsed.query:
                cefr = parsed.query.split("cefr=")[1].split("&")[0].strip()
            words = self.vocab_vault.search_words(query=query, cefr_level=cefr)
            self._send_json({"words": words})

        elif path.startswith("/api/vocabulary/word/"):
            word = path.replace("/api/vocabulary/word/", "").strip()
            word_data = self.vocab_vault.get_word(word)
            self._send_json(word_data or {"error": "Word not found"})

        elif path == "/api/vocabulary/srs/due":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = parsed.query.replace("learner_id=", "").split("&")[0].strip() if "learner_id=" in parsed.query else active_id
            due = self.vocab_vault.get_due_srs_deck(learner_id)
            self._send_json({"due_cards": due})

        elif path == "/api/diagnostic/questions":
            self._send_json({"questions": CEFRDiagnostic.DIAGNOSTIC_QUESTIONS})

        elif path == "/api/curriculum/map":
            from core.curriculum.content_manager import ContentManager
            self._send_json(ContentManager.get_curriculum_map())

        elif path == "/api/curriculum/recommendations":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = parsed.query.replace("learner_id=", "").split("&")[0].strip() if "learner_id=" in parsed.query else active_id
            recs = self.curriculum.recommend_review_lessons(learner_id)
            self._send_json({"recommendations": recs})

        elif path == "/api/curriculum/prerequisites":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = active_id
            lesson_id = ""
            for pair in parsed.query.split("&"):
                if "lesson_id=" in pair:
                    lesson_id = pair.split("=")[1].strip()
                elif "learner_id=" in pair:
                    learner_id = pair.split("=")[1].strip()
            res = self.curriculum.check_prerequisites(learner_id, lesson_id)
            self._send_json(res)

        elif path == "/api/curriculum/validation":
            from core.curriculum.content_manager import ContentManager
            from core.curriculum.validator import ContentValidator
            lessons = ContentManager.load_curriculum_lessons()
            themes = ContentManager.load_vocabulary_themes()
            self._send_json({
                "curriculum": ContentValidator.validate_curriculum(lessons),
                "vocabulary": ContentValidator.validate_vocabulary_themes(themes)
            })

        elif path == "/api/vocabulary/themes":
            from core.curriculum.content_manager import ContentManager
            self._send_json({"themes": ContentManager.list_vocabulary_themes()})

        elif path == "/api/vocabulary/quiz":
            theme = None
            cefr = None
            if "theme=" in parsed.query:
                theme = parsed.query.split("theme=")[1].split("&")[0].strip()
            if "cefr=" in parsed.query:
                cefr = parsed.query.split("cefr=")[1].split("&")[0].strip()
            quiz = self.vocab_vault.generate_vocab_quiz(theme=theme, cefr_level=cefr)
            self._send_json({"quiz": quiz})

        elif path == "/api/curriculum/lessons":
            query_params = {}
            if parsed.query:
                for pair in parsed.query.split("&"):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        query_params[k.strip().lower()] = v.strip()
            level = query_params.get("level") or query_params.get("cefr_level")
            module = query_params.get("module") or query_params.get("module_type")
            lid = self.settings_repo.get("active_learner_id", "default_learner")
            lessons = self.curriculum.list_lessons(cefr_level=level, module_type=module, learner_id=lid)
            self._send_json({"lessons": lessons, "active_learner_id": lid})

        elif path.startswith("/api/curriculum/lesson/"):
            lesson_id = path.replace("/api/curriculum/lesson/", "").strip()
            lid = self.settings_repo.get("active_learner_id", "default_learner")
            lesson = self.curriculum.get_lesson(lesson_id, learner_id=lid)
            if lesson:
                self._send_json({"lesson": lesson})
            else:
                self._send_json({"error": "Lesson not found"}, status=404)

        elif path == "/api/exam/library":
            exams = ExamContentRepository.list_available_exams()
            self._send_json({"exams": exams})

        elif path == "/api/exam/session":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            if "learner_id=" in parsed.query:
                active_id = parsed.query.split("learner_id=")[1].split("&")[0].strip()
            active_sess = self.exam_manager.get_active_session(active_id)
            self._send_json({"active_session": active_sess})

        elif path == "/api/exam/results":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            session_id = ""
            if "session_id=" in parsed.query:
                session_id = parsed.query.split("session_id=")[1].split("&")[0].strip()
            if "learner_id=" in parsed.query:
                active_id = parsed.query.split("learner_id=")[1].split("&")[0].strip()
            res = self.exam_manager.get_exam_results(session_id, active_id)
            if res:
                self._send_json(res)
            else:
                self._send_json({"error": "Exam results not found"}, status=404)

        elif path == "/api/exam/history":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            if "learner_id=" in parsed.query:
                active_id = parsed.query.split("learner_id=")[1].split("&")[0].strip()
            limit = 20
            if "limit=" in parsed.query:
                try:
                    limit = int(parsed.query.split("limit=")[1].split("&")[0].strip())
                except ValueError:
                    limit = 20
            history = self.exam_manager.list_learner_history(active_id, limit=limit)
            self._send_json({"history": history, "learner_id": active_id})

        # -------------------------------------------------------------
        # PHASE 16: RBAC, TEACHER TOOLKIT, BENCHMARK & BETA (GET)
        # -------------------------------------------------------------
        elif path == "/api/auth/me":
            token = self._get_auth_token()
            user = self.auth_mgr.validate_session(token)
            if user:
                self._send_json({"authenticated": True, "user": user})
            else:
                self._send_json({"authenticated": False, "role": "learner", "user": None})

        elif path == "/api/teacher/dashboard":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["teacher", "admin"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                qs = parse_qs(parsed.query)
                teacher_id = qs.get("teacher_id", [user["user_id"]])[0] if user["role"] == "admin" else user["user_id"]
                data = self.review_mgr.get_teacher_dashboard(teacher_id)
                self._send_json(data)

        elif path == "/api/teacher/assignment":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["teacher", "admin", "examiner"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                qs = parse_qs(parsed.query)
                assign_id = qs.get("id", [""])[0]
                assign = self.review_mgr.get_assignment(assign_id, reviewer_id=user["user_id"])
                if assign:
                    self._send_json(assign)
                else:
                    self._send_json({"error": "Assignment not found or unauthorized reviewer."}, status=404)

        elif path == "/api/examiner/assignments":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["examiner", "admin"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                rows = self.db.fetchall(
                    """SELECT a.*, l.name as learner_name
                       FROM review_assignments a
                       LEFT JOIN learners l ON a.learner_id = l.id
                       WHERE a.assigned_to = ? OR ? = 'admin'
                       ORDER BY a.created_at DESC""",
                    (user["user_id"], user["role"])
                )
                items = []
                for r in rows:
                    it = dict(r)
                    it["content"] = json.loads(it.get("content_json") or "{}")
                    items.append(it)
                self._send_json({"examiner_id": user["user_id"], "assignments": items})

        elif path == "/api/examiner/double_marking":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["examiner", "admin", "teacher"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                qs = parse_qs(parsed.query)
                sub_id = qs.get("submission_id", [""])[0]
                data = self.double_marking_mgr.get_double_marked_evaluations(
                    submission_id=sub_id,
                    requesting_reviewer_id=user["user_id"],
                    user_role=user["role"]
                )
                self._send_json(data)

        elif path == "/api/benchmark/list":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["examiner", "admin", "teacher"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                records = self.benchmark_mgr.list_benchmark_records()
                self._send_json({"total_records": len(records), "records": records})

        elif path == "/api/benchmark/calibration":
            qs = parse_qs(parsed.query)
            atype = qs.get("type", [None])[0]
            calib = self.calibration_engine.run_calibration_analysis(assessment_type=atype)
            self._send_json(calib)

        elif path == "/api/beta/cohorts":
            cohorts = self.beta_mgr.list_cohorts()
            self._send_json({"cohorts": cohorts})

        elif path == "/api/beta/analytics":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["admin", "teacher"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                stats = self.beta_mgr.get_beta_analytics()
                self._send_json(stats)

        else:
            # Serve static files from ui/static
            self._serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        if path == "/api/learners/switch":
            lid = body.get("learner_id", "default_learner")
            self.settings_repo.set("active_learner_id", lid)
            profile = self.learner_repo.get_or_create_default(lid)
            self._send_json({"success": True, "active_learner": profile})

        elif path == "/api/learners/save":
            lid = body.get("learner_id")
            if not lid or lid == "new":
                profile = self.learner_repo.create_learner(
                    name=body.get("name", "Learner"),
                    target_band=float(body.get("target_band", 7.0)),
                    current_band=float(body.get("current_band", 5.5)),
                    cefr_level=body.get("cefr_level", "B2"),
                    track=body.get("track", "Academic"),
                    daily_minutes=int(body.get("daily_minutes", 30)),
                    target_exam_date=body.get("target_exam_date"),
                    native_language=body.get("native_language", "English"),
                    target_sub_skills=body.get("target_sub_skills", []),
                    notes=body.get("notes")
                )
                self.settings_repo.set("active_learner_id", profile["id"])
            else:
                profile = self.learner_repo.update_profile(lid, body)
                self.settings_repo.set("active_learner_id", lid)
            self._send_json({"success": True, "profile": profile})

        elif path == "/api/learners/delete":
            lid = body.get("learner_id")
            if lid:
                self.learner_repo.delete_learner(lid)
                current_active = self.settings_repo.get("active_learner_id")
                if current_active == lid:
                    self.settings_repo.set("active_learner_id", "default_learner")
            self._send_json({"success": True, "active_learner_id": self.settings_repo.get("active_learner_id", "default_learner")})

        elif path == "/api/chat":
            msg = body.get("message", "")
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = body.get("learner_id", active_id)
            res = self.tutor.process_message(learner_id, msg)
            self._send_json(res)

        elif path == "/api/chat/clear":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = body.get("learner_id", active_id)
            self.tutor.clear_conversation_history(learner_id)
            self._send_json({"success": True})

        elif path == "/api/settings/offline_toggle":
            forced = body.get("forced_offline", False)
            self.connectivity.set_forced_offline(forced)
            self._send_json({
                "forced_offline": self.connectivity.is_forced_offline,
                "status": self.connectivity.get_ui_indicator()
            })

        elif path == "/api/settings/save":
            for k, v in body.items():
                self.settings_repo.set(k, str(v))
            self._send_json({"success": True})

        elif path == "/api/srs/review":
            item_id = body.get("item_id")
            grade = int(body.get("grade", 4))
            updated = self.srs.review_card(item_id, grade)
            self._send_json(updated)

        elif path == "/api/mistakes/review":
            mistake_id = body.get("mistake_id")
            success = bool(body.get("success", True))
            updated = self.mistake_book.review_mistake(mistake_id, success)
            self._send_json(updated)

        elif path == "/api/reading/submit":
            pid = body.get("passage_id", "acad_p1")
            answers_raw = body.get("answers", {})
            user_answers = {int(k) if str(k).isdigit() else k: v for k, v in answers_raw.items()}
            res = self.reading.evaluate_test(pid, user_answers)
            lid = body.get("learner_id") or self.settings_repo.get("active_learner_id", "default_learner")
            try:
                self.test_repo.record_result(
                    learner_id=lid,
                    test_type="reading",
                    track=res.get("track", "Academic"),
                    overall_band=float(res.get("estimated_band", 6.0)),
                    reading_band=float(res.get("estimated_band", 6.0)),
                    details=res
                )
            except Exception as e:
                pass
            self._send_json(res)

        elif path == "/api/listening/submit":
            answers_raw = body.get("answers", {})
            sec_id = body.get("section_id", "sec_1")
            user_answers = {int(k) if str(k).isdigit() else k: v for k, v in answers_raw.items()}
            res = self.listening.evaluate_submission(sec_id, user_answers)
            lid = body.get("learner_id") or self.settings_repo.get("active_learner_id", "default_learner")
            try:
                self.test_repo.record_result(
                    learner_id=lid,
                    test_type="listening",
                    track="Academic",
                    overall_band=float(res.get("estimated_band", 6.0)),
                    listening_band=float(res.get("estimated_band", 6.0)),
                    details=res
                )
            except Exception as e:
                pass
            self._send_json(res)

        elif path == "/api/writing/evaluate":
            prompt_id = body.get("prompt_id", "acad_t2_stem")
            essay_text = body.get("essay_text", "")
            learner_id = body.get("learner_id") or self.settings_repo.get("active_learner_id", "default_learner")
            draft_id = body.get("draft_id")
            res = self.writing.evaluate_essay(prompt_id, essay_text, learner_id=learner_id, draft_id=draft_id, db=self.db)
            self._send_json(res)

        elif path == "/api/writing/draft/save":
            learner_id = body.get("learner_id") or self.settings_repo.get("active_learner_id", "default_learner")
            prompt_id = body.get("prompt_id", "acad_t2_stem")
            draft_text = body.get("draft_text", "")
            draft_id = body.get("draft_id")
            saved = self.writing.save_draft(learner_id, prompt_id, draft_text, draft_id=draft_id, db=self.db)
            self._send_json(saved)

        elif path == "/api/grammar/fillups/submit":
            drill_id = body.get("drill_id", "")
            user_answer = body.get("user_answer", "")
            res = GrammarEngine.evaluate_fill_up(drill_id, user_answer)
            self._send_json(res)

        elif path == "/api/speaking/evaluate":
            transcript = body.get("transcript", "")
            duration = float(body.get("duration_seconds", 60.0))
            learner_id = body.get("learner_id") or self.settings_repo.get("active_learner_id", "default_learner")
            res = self.speaking.evaluate_spoken_response(transcript, duration_seconds=duration, learner_id=learner_id, db=self.db)
            self._send_json(res)

        elif path == "/api/speaking/pronunciation/evaluate":
            drill_type = body.get("drill_type", "minimal_pair")
            target_word = body.get("target_word", "")
            spoken_transcript = body.get("spoken_transcript", "")
            res = PronunciationCoach.evaluate_drill_attempt(drill_type, target_word, spoken_transcript)
            self._send_json(res)

        elif path == "/api/vocabulary/srs/add":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = body.get("learner_id", active_id)
            word = body.get("word", "")
            card = self.vocab_vault.add_word_to_srs(learner_id, word)
            self._send_json(card)

        elif path == "/api/vocabulary/srs/review":
            item_id = body.get("item_id", "")
            grade = int(body.get("grade", 4))
            updated = self.vocab_vault.review_card(item_id, grade)
            self._send_json(updated)

        elif path == "/api/vocabulary/quiz/submit":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            learner_id = body.get("learner_id", active_id)
            quiz = body.get("quiz", {})
            answers = body.get("answers", {})
            result = self.vocab_vault.evaluate_quiz_submission(learner_id, quiz, answers)
            self._send_json(result)

        elif path == "/api/diagnostic/submit":
            answers = body.get("answers", {})
            res = CEFRDiagnostic.grade_diagnostic(answers)
            self._send_json(res)

        elif path == "/api/curriculum/submit":
            lid = body.get("learner_id") or self.settings_repo.get("active_learner_id", "default_learner")
            lesson_id = body.get("lesson_id", "")
            answers = body.get("answers", {})
            res = self.curriculum.evaluate_submission(lid, lesson_id, answers)
            self._send_json(res)

        elif path == "/api/exam/start":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            lid = body.get("learner_id") or active_id
            track = body.get("track", "Academic")
            module = body.get("module", "full_mock")
            exam_id = body.get("exam_id")
            try:
                res = self.exam_manager.start_exam(lid, track=track, module=module, exam_id=exam_id)
                self._send_json(res)
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)

        elif path == "/api/exam/autosave":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            lid = body.get("learner_id") or active_id
            session_id = body.get("session_id", "")
            answers = body.get("answers", {})
            flagged = body.get("flagged", [])
            curr_sec = body.get("current_section")
            curr_q = body.get("current_question")
            time_spent = body.get("time_spent_seconds")
            res = self.exam_manager.autosave_answers(
                session_id=session_id,
                learner_id=lid,
                answers=answers,
                flagged_questions=flagged,
                current_section=curr_sec,
                current_question=curr_q,
                time_spent_seconds=time_spent
            )
            self._send_json(res, status=200 if res.get("success") else 400)

        elif path == "/api/exam/submit":
            active_id = self.settings_repo.get("active_learner_id", "default_learner")
            lid = body.get("learner_id") or active_id
            session_id = body.get("session_id", "")
            final_answers = body.get("final_answers") or body.get("answers")
            res = self.exam_manager.submit_exam(session_id=session_id, learner_id=lid, final_answers=final_answers)
            self._send_json(res, status=200 if res.get("success") else 400)

        # -------------------------------------------------------------
        # PHASE 16: RBAC, TEACHER TOOLKIT, BENCHMARK & BETA (POST)
        # -------------------------------------------------------------
        elif path == "/api/auth/login":
            uname = body.get("username", "")
            pwd = body.get("password", "")
            user = self.auth_mgr.authenticate(uname, pwd)
            if user:
                token = self.auth_mgr.create_session(user["id"])
                self._send_json({"success": True, "token": token, "user": user})
            else:
                self._send_json({"success": False, "error": "Invalid username or password."}, status=401)

        elif path == "/api/auth/logout":
            token = self._get_auth_token()
            if token:
                self.auth_mgr.revoke_session(token)
            self._send_json({"success": True, "message": "Signed out successfully."})

        elif path == "/api/teacher/review/save":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["teacher", "admin", "examiner"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                res = self.review_mgr.save_evaluation(
                    assignment_id=body.get("assignment_id", ""),
                    reviewer_id=user["user_id"],
                    reviewer_role=user["role"],
                    overall_band=float(body.get("overall_band", 0.0)),
                    criteria_scores=body.get("criteria_scores", {}),
                    criterion_feedback=body.get("criterion_feedback"),
                    general_comments=body.get("general_comments"),
                    assessment_mode=body.get("assessment_mode", "transcript"),
                    status="draft"
                )
                self._send_json(res, status=200 if res.get("success") else 400)

        elif path == "/api/teacher/review/submit":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["teacher", "admin"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                res = self.review_mgr.save_evaluation(
                    assignment_id=body.get("assignment_id", ""),
                    reviewer_id=user["user_id"],
                    reviewer_role="teacher",
                    overall_band=float(body.get("overall_band", 0.0)),
                    criteria_scores=body.get("criteria_scores", {}),
                    criterion_feedback=body.get("criterion_feedback"),
                    general_comments=body.get("general_comments"),
                    assessment_mode=body.get("assessment_mode", "transcript"),
                    status="submitted"
                )
                self._send_json(res, status=200 if res.get("success") else 400)

        elif path == "/api/examiner/review":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["examiner", "admin"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                res = self.review_mgr.save_evaluation(
                    assignment_id=body.get("assignment_id", ""),
                    reviewer_id=user["user_id"],
                    reviewer_role="examiner",
                    overall_band=float(body.get("overall_band", 0.0)),
                    criteria_scores=body.get("criteria_scores", {}),
                    criterion_feedback=body.get("criterion_feedback"),
                    general_comments=body.get("general_comments"),
                    assessment_mode=body.get("assessment_mode", "transcript"),
                    status=body.get("status", "submitted")
                )
                self._send_json(res, status=200 if res.get("success") else 400)

        elif path == "/api/examiner/reconcile":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["admin", "senior_examiner", "examiner"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                res = self.double_marking_mgr.submit_reconciliation(
                    submission_id=body.get("submission_id", ""),
                    reconciler_id=user["user_id"],
                    reconciled_band=float(body.get("reconciled_band", 0.0)),
                    reconciled_criteria=body.get("reconciled_criteria", {}),
                    comments=body.get("comments", "")
                )
                self._send_json(res, status=200 if res.get("success") else 400)

        elif path == "/api/benchmark/enroll":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["admin", "teacher", "examiner"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                res = self.benchmark_mgr.enroll_benchmark_submission(
                    assessment_type=body.get("assessment_type", "writing"),
                    content=body.get("content", ""),
                    task_type=body.get("task_type"),
                    track=body.get("track"),
                    recording_ref=body.get("recording_ref"),
                    has_consent=bool(body.get("has_consent", True)),
                    dataset_version=body.get("dataset_version", "1.0.0")
                )
                self._send_json(res, status=200 if res.get("success") else 400)

        elif path == "/api/benchmark/withdraw":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["admin", "teacher", "learner"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                bench_id = body.get("benchmark_id", "")
                res = self.benchmark_mgr.withdraw_consent(bench_id)
                self._send_json(res)

        elif path == "/api/beta/cohorts/create":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["admin"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                res = self.beta_mgr.create_cohort(
                    name=body.get("name", "New Beta Cohort"),
                    track_or_level=body.get("track_or_level", "Academic"),
                    start_date=body.get("start_date", "2026-12-01"),
                    end_date=body.get("end_date", "2027-01-15"),
                    max_participants=int(body.get("max_participants", 50))
                )
                self._send_json(res, status=200 if res.get("success") else 400)

        elif path == "/api/beta/participants/enroll":
            token = self._get_auth_token()
            ok, user, err = self.auth_mgr.authorize_request(token, ["admin", "teacher", "learner"])
            if not ok:
                self._send_json({"error": err}, status=403 if user else 401)
            else:
                res = self.beta_mgr.enroll_participant(
                    cohort_id=body.get("cohort_id", ""),
                    user_id=body.get("user_id", user["user_id"]),
                    email=body.get("email", user.get("email")),
                    has_consent=bool(body.get("has_consent", True))
                )
                self._send_json(res, status=200 if res.get("success") else 400)

        elif path == "/api/beta/feedback":
            res = self.beta_mgr.submit_feedback(
                cohort_id=body.get("cohort_id", "cohort_acad_1"),
                category=body.get("category", "usability"),
                rating=int(body.get("rating", 5)),
                comments=body.get("comments", ""),
                participant_id=body.get("participant_id"),
                is_anonymous=bool(body.get("is_anonymous", False))
            )
            self._send_json(res, status=200 if res.get("success") else 400)

        elif path == "/api/beta/bugs":
            res = self.beta_mgr.report_bug(
                cohort_id=body.get("cohort_id", "cohort_acad_1"),
                title=body.get("title", ""),
                description=body.get("description", ""),
                severity=body.get("severity", "medium"),
                steps_to_reproduce=body.get("steps_to_reproduce"),
                reporter_id=body.get("reporter_id")
            )
            self._send_json(res, status=200 if res.get("success") else 400)

        else:
            self._send_json({"error": "Unknown API route"}, status=404)

    def _serve_static(self, path: str):
        if path in ("/", ""):
            path = "/index.html"

        # Sanitize and resolve path securely
        static_dir = os.path.abspath(os.path.join(BASE_DIR, "ui", "static"))
        clean_rel = os.path.normpath(path.lstrip("/\\"))
        file_path = os.path.abspath(os.path.join(static_dir, clean_rel))

        # Enforce strict root boundary check to block directory traversal
        if not file_path.startswith(static_dir):
            self.send_error(403, "Access Forbidden")
            return

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            self.send_error(404, f"File Not Found: {clean_rel}")
            return

        content_type, _ = mimetypes.guess_type(file_path)
        content_type = content_type or "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")


def run_server(port: int = 8080):
    server_address = ("127.0.0.1", port)
    httpd = ThreadingHTTPServer(server_address, GAMAHTTPRequestHandler)
    print(f"GAMA Hybrid Local Server active at http://127.0.0.1:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down GAMA server.")
        httpd.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
