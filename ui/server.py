"""
Local Web Server and REST API for IELTS by GAMA.
Built on Python's standard library ThreadingHTTPServer.
Runs 100% offline with zero external pip dependencies.
"""

import os
import sys
import json
import mimetypes
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository, SettingsRepository
from core.chatbot.tutor_bot import UnifiedAITutor
from core.reading.reading_engine import ReadingEngine
from core.listening.listening_engine import ListeningEngine
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.progress.mistake_book import MistakeBook
from core.progress.srs import SpacedRepetitionSystem
from core.progress.study_planner import StudyPlanner
from core.progress.analytics import LearningAnalytics
from core.grammar.adaptive_grammar import AdaptiveGrammar
from core.grammar.grammar_engine import GrammarEngine
from core.scoring.cefr_diagnostic import CEFRDiagnostic
from core.sync.connectivity import ConnectivityManager
from core.device.profile_manager import ProfileManager


class GAMAHTTPRequestHandler(BaseHTTPRequestHandler):
    """Handles static web requests and REST API queries."""

    # Shared instances
    db = DatabaseManager()
    tutor = UnifiedAITutor(db)
    learner_repo = LearnerRepository(db)
    settings_repo = SettingsRepository(db)
    reading = ReadingEngine()
    listening = ListeningEngine()
    writing = WritingEvaluator()
    speaking = SpeakingExaminer()
    mistake_book = MistakeBook(db)
    srs = SpacedRepetitionSystem(db)
    planner = StudyPlanner(db)
    analytics = LearningAnalytics(db)
    adaptive_grammar = AdaptiveGrammar(db)
    connectivity = ConnectivityManager()

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

        if path == "/api/status":
            cfg = ProfileManager.get_hardware_config()
            self._send_json({
                "connectivity": self.connectivity.get_ui_indicator(),
                "is_online": self.connectivity.is_online,
                "forced_offline": self.connectivity.is_forced_offline,
                "hardware_profile": cfg["profile"],
                "model_name": cfg["model_name"]
            })

        elif path == "/api/dashboard":
            learner_id = "default_learner"
            dash = self.analytics.get_dashboard_data(learner_id)
            daily = self.planner.generate_daily_plan(learner_id)
            self._send_json({"dashboard": dash, "daily_plan": daily})

        elif path == "/api/mistakes":
            learner_id = "default_learner"
            summary = self.mistake_book.get_summary_report(learner_id)
            active = self.mistake_book.get_due_mistakes(learner_id)
            self._send_json({"summary": summary, "active_mistakes": active})

        elif path == "/api/srs/due":
            due = self.srs.get_due_deck("default_learner")
            self._send_json({"items": due})

        elif path == "/api/reading/passages":
            passages = self.reading.list_passages()
            self._send_json({"passages": passages})

        elif path == "/api/reading":
            pid = "acad_p1"
            if "passage_id=" in parsed.query:
                pid = parsed.query.replace("passage_id=", "").split("&")[0].strip()
            passage = self.reading.get_passage(pid) or self.reading.get_passage("acad_p1")
            self._send_json(passage)

        elif path == "/api/listening":
            sec_id = parsed.query.replace("sec_id=", "").strip() if "sec_id=" in parsed.query else "sec_1"
            sec = self.listening.get_section(sec_id or "sec_1", show_transcript=True)
            self._send_json(sec or self.listening.get_section("sec_1", show_transcript=True))

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

        elif path == "/api/writing/prompts":
            prompts = self.writing.list_prompts()
            self._send_json({"prompts": prompts})

        elif path == "/api/grammar/adaptive":
            session = self.adaptive_grammar.generate_adaptive_session("default_learner")
            self._send_json(session)

        elif path == "/api/grammar/fillups":
            category = None
            if "category=" in parsed.query:
                category = parsed.query.replace("category=", "").split("&")[0].strip()
            drills = GrammarEngine.get_fill_up_drills(category)
            self._send_json({"drills": drills})

        elif path == "/api/diagnostic/questions":
            self._send_json({"questions": CEFRDiagnostic.DIAGNOSTIC_QUESTIONS})

        else:
            # Serve static files from ui/static
            self._serve_static(path)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_json_body()

        if path == "/api/chat":
            msg = body.get("message", "")
            learner_id = body.get("learner_id", "default_learner")
            res = self.tutor.process_message(learner_id, msg)
            self._send_json(res)

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
            user_answers = {int(k): v for k, v in answers_raw.items()}
            res = self.reading.evaluate_test(pid, user_answers)
            self._send_json(res)

        elif path == "/api/listening/submit":
            answers_raw = body.get("answers", {})
            sec_id = body.get("section_id", "sec_1")
            user_answers = {int(k): v for k, v in answers_raw.items()}
            res = self.listening.evaluate_submission(sec_id, user_answers)
            self._send_json(res)

        elif path == "/api/writing/evaluate":
            prompt_id = body.get("prompt_id", "acad_t2_stem")
            essay_text = body.get("essay_text", "")
            res = self.writing.evaluate_essay(prompt_id, essay_text)
            self._send_json(res)

        elif path == "/api/grammar/fillups/submit":
            drill_id = body.get("drill_id", "")
            user_answer = body.get("user_answer", "")
            res = GrammarEngine.evaluate_fill_up(drill_id, user_answer)
            self._send_json(res)

        elif path == "/api/speaking/evaluate":
            transcript = body.get("transcript", "")
            duration = float(body.get("duration_seconds", 60.0))
            res = self.speaking.evaluate_spoken_response(transcript, duration_seconds=duration)
            self._send_json(res)

        elif path == "/api/diagnostic/submit":
            answers = body.get("answers", {})
            res = CEFRDiagnostic.grade_diagnostic(answers)
            self._send_json(res)

        else:
            self._send_json({"error": "Unknown API route"}, status=404)

    def _serve_static(self, path: str):
        if path in ("/", ""):
            path = "/index.html"

        # Sanitize path
        clean_rel = os.path.normpath(path.lstrip("/"))
        file_path = os.path.join(BASE_DIR, "ui", "static", clean_rel)

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
