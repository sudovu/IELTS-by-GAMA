"""
End-to-End System Tests for IELTS by GAMA.
Verifies:
1. Section 71: Strict Offline Functionality
2. Section 72 & 73: Online-to-Offline Knowledge Feedback & Research Reuse
3. Section 74: Smart Cache TTL & Permanent Knowledge Preservation
4. Section 75: Low-Resource Device Profile Adaptation & Memory Pressure
"""

import unittest
import os
import tempfile
import time
from core.database.db_manager import DatabaseManager
from core.database.repositories import KnowledgeRepository
from core.chatbot.tutor_bot import UnifiedAITutor
from core.sync.connectivity import ConnectivityManager, ConnectivityState
from core.research.research_planner import ResearchPlanner
from core.research.knowledge_saver import KnowledgeSaver
from core.memory.cache_manager import CacheManager
from core.device.profile_manager import ProfileManager, DeviceProfile
from core.reading.reading_engine import ReadingEngine
from core.listening.listening_engine import ListeningEngine
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.scoring.band_calculator import BandCalculator


class TestOfflineWorkflowAndResearchReuse(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()

        self.connectivity = ConnectivityManager()
        self.connectivity.set_forced_offline(True)  # Strictly Offline
        self.tutor = UnifiedAITutor(self.db)

    def tearDown(self):
        self.db.close()
        self.connectivity.set_forced_offline(False)
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_section_71_offline_independence(self):
        """Disables network and verifies all modules execute cleanly offline."""
        self.connectivity.set_forced_offline(True)
        self.assertFalse(self.connectivity.is_online)

        # 1. Chatbot offline
        chat_res = self.tutor.process_message("test_learner", "I am agree with your statement.")
        self.assertTrue(chat_res["is_offline"])
        self.assertIn("OFFLINE", chat_res["connectivity"])
        self.assertTrue(len(chat_res["detected_mistakes"]) > 0)

        # 2. Reading offline
        reading_res = ReadingEngine.evaluate_test("acad_p1", {1: "False", 2: "False"})
        self.assertGreaterEqual(reading_res["correct_answers"], 2)

        # 3. Listening offline
        listening_res = ListeningEngine.evaluate_submission("sec_1", {1: "Sterling", 2: "en-suite"})
        self.assertEqual(listening_res["correct_answers"], 2)

        # 4. Writing offline
        writing_res = WritingEvaluator.evaluate_essay("acad_t2_stem", "Education is important for students.")
        self.assertIn("estimated_band", writing_res)

        # 5. Speaking offline
        speaking_res = SpeakingExaminer.evaluate_spoken_response("I achieved my goal.", duration_seconds=15.0)
        self.assertIn("estimated_band", speaking_res)

    def test_section_73_research_reuse_test(self):
        """
        Step 1: Simulate Online mode -> Research 'affect and effect' -> Store compact knowledge.
        Step 2: Disconnect Internet (100% Offline).
        Step 3: Query 'Explain affect and effect' -> Answers from local knowledge with zero internet.
        """
        # Step 1: Online Mode
        self.connectivity.set_forced_offline(False)
        self.connectivity.set_state(ConnectivityState.ONLINE)

        saver = KnowledgeSaver(self.db, self.tutor.ai.local_provider.rag)
        saver.save_distilled_knowledge(
            topic="Affect vs Effect",
            query_trigger="explain affect and effect",
            compact_knowledge="Affect is a verb meaning to influence. Effect is a noun meaning the consequence.",
            source="Online Research Synthesis",
            confidence=0.98
        )

        # Step 2: Disconnect Internet (Forced Offline)
        self.connectivity.set_forced_offline(True)
        self.assertFalse(self.connectivity.is_online)

        # Step 3: Ask question offline
        offline_response = self.tutor.process_message("test_learner", "explain affect and effect")
        self.assertTrue(offline_response["is_offline"])
        self.assertIn("verb", offline_response["reply"].lower())
        self.assertIn("noun", offline_response["reply"].lower())

    def test_section_74_cache_ttl_and_permanent_knowledge(self):
        """Temporary cache is evicted on TTL; permanent knowledge remains."""
        cache = CacheManager(self.db)
        repo = KnowledgeRepository(self.db)

        # Permanent knowledge
        repo.upsert_knowledge(
            topic="Permanent Grammar Rule",
            query_trigger="permanent rule",
            compact_knowledge="This rule must never be deleted."
        )

        # Temporary research cache with 1-second TTL
        cache.set("temp_research_query", {"results": "temporary text"}, ttl_seconds=1)
        self.assertIsNotNone(cache.get("temp_research_query"))

        # Wait for TTL to expire
        time.sleep(1.1)
        self.assertIsNone(cache.get("temp_research_query"))

        # Verify permanent knowledge is intact
        persisted = repo.search_knowledge("permanent rule")
        self.assertEqual(len(persisted), 1)
        self.assertEqual(persisted[0]["topic"], "Permanent Grammar Rule")

    def test_section_75_resource_pressure_and_device_profiles(self):
        """Device capability adaptation for low-memory devices."""
        # Ultra-low profile selection
        config_ultra = ProfileManager.get_hardware_config(DeviceProfile.ULTRA_LOW)
        self.assertEqual(config_ultra["model_name"], "GAM IELTS Nano")
        self.assertLessEqual(config_ultra["max_context_turns"], 4)

        # Desktop profile
        config_desktop = ProfileManager.get_hardware_config(DeviceProfile.DESKTOP)
        self.assertEqual(config_desktop["model_name"], "GAM IELTS Standard")

        # Resource pressure event
        cache = CacheManager(self.db)
        cache.set("old_cached_turn", {"data": "filler"}, ttl_seconds=3600)
        action_report = ProfileManager.handle_resource_pressure(cache)
        self.assertEqual(action_report["pressure_action"], "cache_trimmed")


if __name__ == "__main__":
    unittest.main()
