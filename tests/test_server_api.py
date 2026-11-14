"""
Unit tests for ui/server.py REST API routes and security path traversal prevention.
"""

import unittest
import json
import urllib.request
import urllib.error
import threading
import time
from ui.server import run_server, GAMAHTTPRequestHandler
from core.database.db_manager import DatabaseManager


class TestServerAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8899
        cls.server_thread = threading.Thread(target=run_server, args=(cls.port,), daemon=True)
        cls.server_thread.start()
        time.sleep(1.0)  # wait for server to warm up

    def _get(self, path: str):
        url = f"http://127.0.0.1:{self.port}{path}"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def _post(self, path: str, data: dict):
        url = f"http://127.0.0.1:{self.port}{path}"
        body = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def test_learners_endpoints(self):
        # 1. GET /api/learners
        status, data = self._get("/api/learners")
        self.assertEqual(status, 200)
        self.assertIn("learners", data)
        self.assertIn("active_learner_id", data)

        # 2. GET /api/learners/current
        status, current = self._get("/api/learners/current")
        self.assertEqual(status, 200)
        self.assertIn("name", current)

        # 3. POST /api/learners/save (new learner)
        status, res = self._post("/api/learners/save", {
            "learner_id": "new",
            "name": "Integration Learner",
            "target_band": 7.5,
            "current_band": 6.0,
            "track": "Academic",
            "daily_minutes": 45,
            "target_exam_date": "2027-03-01",
            "native_language": "Spanish"
        })
        self.assertEqual(status, 200)
        self.assertTrue(res["success"])
        new_lid = res["profile"]["id"]
        self.assertEqual(res["profile"]["name"], "Integration Learner")

        # 4. POST /api/learners/switch
        status, switch_res = self._post("/api/learners/switch", {"learner_id": "default_learner"})
        self.assertEqual(status, 200)
        self.assertEqual(switch_res["active_learner"]["id"], "default_learner")

        # 5. POST /api/learners/delete
        status, del_res = self._post("/api/learners/delete", {"learner_id": new_lid})
        self.assertEqual(status, 200)
        self.assertTrue(del_res["success"])

    def test_curriculum_endpoints(self):
        # 1. GET /api/curriculum/lessons
        status, data = self._get("/api/curriculum/lessons")
        self.assertEqual(status, 200)
        self.assertIn("lessons", data)
        self.assertGreaterEqual(len(data["lessons"]), 18)

        # 2. GET /api/curriculum/lessons?level=B2&module=grammar
        status, b2_data = self._get("/api/curriculum/lessons?level=B2&module=grammar")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(b2_data["lessons"]), 1)

        # 3. GET /api/curriculum/lesson/curric_b2_gram_conditionals
        status, lesson_data = self._get("/api/curriculum/lesson/curric_b2_gram_conditionals")
        self.assertEqual(status, 200)
        self.assertIn("lesson", lesson_data)
        self.assertEqual(lesson_data["lesson"]["id"], "curric_b2_gram_conditionals")

        # 4. POST /api/curriculum/submit
        status, submit_res = self._post("/api/curriculum/submit", {
            "lesson_id": "curric_b2_gram_conditionals",
            "answers": {"b2_as_1": 1}
        })
        self.assertEqual(status, 200)
        self.assertTrue(submit_res["success"])
        self.assertIn("score", submit_res)

        # 5. GET /api/curriculum/map
        status, cmap = self._get("/api/curriculum/map")
        self.assertEqual(status, 200)
        self.assertIn("total_lessons", cmap)
        self.assertGreaterEqual(cmap["total_lessons"], 54)

        # 6. GET /api/curriculum/validation
        status, val_report = self._get("/api/curriculum/validation")
        self.assertEqual(status, 200)
        self.assertIn("curriculum", val_report)
        self.assertEqual(val_report["curriculum"]["quality_score_percent"], 100.0)

        # 7. GET /api/vocabulary/themes
        status, themes_data = self._get("/api/vocabulary/themes")
        self.assertEqual(status, 200)
        self.assertIn("themes", themes_data)
        self.assertEqual(len(themes_data["themes"]), 15)

        # 8. GET /api/vocabulary/quiz & POST /api/vocabulary/quiz/submit
        status, qdata = self._get("/api/vocabulary/quiz?theme=technology")
        self.assertEqual(status, 200)
        self.assertIn("quiz", qdata)
        quiz = qdata["quiz"]
        q1 = quiz["questions"][0]
        status, sub_eval = self._post("/api/vocabulary/quiz/submit", {
            "quiz": quiz,
            "answers": {q1["id"]: q1["correct_index"]}
        })
        self.assertEqual(status, 200)
        self.assertIn("score_percent", sub_eval)

    def test_path_traversal_blocked(self):
        # Test directory traversal attack blocked with 403 or 404
        url = f"http://127.0.0.1:{self.port}/..%2f..%2f..%2f..%2fWindows%2fwin.ini"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                self.assertNotEqual(resp.status, 200)
        except urllib.error.HTTPError as e:
            self.assertIn(e.code, [403, 404])


if __name__ == "__main__":
    unittest.main()
