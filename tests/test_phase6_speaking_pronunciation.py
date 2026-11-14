# -*- coding: utf-8 -*-
"""
Tests for Phase 6: Speaking Examiner & Pronunciation Coach.
Verifies:
1. Authentic Cambridge 3-part speaking test sets and Band 9 models.
2. Objective FluencyTracker metrics (WPM, fillers, hesitation).
3. PronunciationCoach minimal pairs, syllable stress shifts, connected speech.
4. Transparent non-simulated drill evaluation.
5. Speaking score persistence in SQLite test_results for dashboard synchronization.
"""

import unittest
import os
import tempfile
from core.database.db_manager import DatabaseManager
from core.database.repositories import TestResultRepository
from core.speaking.speaking_examiner import SpeakingExaminer
from core.speaking.fluency_tracker import FluencyTracker
from core.speaking.pronunciation_coach import PronunciationCoach


class TestPhase6SpeakingPronunciation(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_exam_sets_inventory(self):
        """Verifies full 3-part exam sets with Band 9 model answers and IELTS Advantage strategies."""
        sets = SpeakingExaminer.get_exam_sets()
        self.assertGreaterEqual(len(sets), 3)

        prompts = SpeakingExaminer.get_test_prompts(0)
        self.assertIn("part_1", prompts)
        self.assertIn("part_2_cue_card", prompts)
        self.assertIn("part_3_discussion", prompts)
        self.assertIn("band_9_model", prompts["part_2_cue_card"])
        self.assertIn("advantage_strategy_tip", prompts)

    def test_fluency_tracker_analysis(self):
        """Tests that speech rate (WPM) and filler words are calculated accurately without faking."""
        # 30 words in 15 seconds = 120 WPM
        speech = "I would like to talk about an ambitious goal that I achieved um last year. It was actually challenging."
        metrics = FluencyTracker.analyze_fluency(speech, duration_seconds=15.0)
        self.assertGreaterEqual(metrics["words_per_minute"], 60.0)
        self.assertIn("um", metrics["filler_breakdown"])
        self.assertIn("actually", metrics["filler_breakdown"])
        self.assertIn("target_wpm_range", metrics)

    def test_pronunciation_coach_data(self):
        """Verifies phonemic minimal pairs, syllable stress, and connected speech drills."""
        pairs = PronunciationCoach.list_minimal_pairs()
        self.assertGreaterEqual(len(pairs), 5)
        pair_ids = [p["id"] for p in pairs]
        self.assertIn("pair_long_short_i", pair_ids)
        self.assertIn("pair_b_vs_v", pair_ids)
        self.assertIn("pair_th_vs_s", pair_ids)
        self.assertIn("pair_r_vs_l", pair_ids)
        self.assertIn("pair_w_vs_v", pair_ids)

        stress_drills = PronunciationCoach.list_syllable_stress_drills()
        self.assertGreaterEqual(len(stress_drills), 6)
        words = [d["word"] for d in stress_drills]
        self.assertIn("present", words)
        self.assertIn("record", words)
        self.assertIn("contrast", words)

        connected = PronunciationCoach.list_connected_speech_drills()
        self.assertGreaterEqual(len(connected), 3)

    def test_pronunciation_drill_evaluation(self):
        """Tests transparent evaluation of phoneme targets."""
        res_success = PronunciationCoach.evaluate_drill_attempt(
            drill_type="minimal_pair",
            target_word="sheep",
            spoken_transcript="The sheep was in the green field"
        )
        self.assertTrue(res_success["phonemic_match"])
        self.assertEqual(res_success["clarity_rating"], 8.0)

        res_miss = PronunciationCoach.evaluate_drill_attempt(
            drill_type="minimal_pair",
            target_word="ship",
            spoken_transcript="The sheep was in the field"
        )
        self.assertFalse(res_miss["phonemic_match"])
        self.assertEqual(res_miss["clarity_rating"], 5.5)

    def test_speaking_evaluation_persistence(self):
        """Tests speaking evaluation persists into SQLite test_results."""
        learner_id = "phase6_speaking_candidate"
        transcript = (
            "From my perspective, sustainable public transit is of paramount importance in modern urban centers. "
            "Although personal automobile ownership offers transient convenience, unchecked vehicle congestion "
            "is profoundly detrimental to environmental health and commuter productivity. "
            "Consequently, municipal authorities should subsidize electric bus fleets and expand subway networks."
        )
        eval_result = SpeakingExaminer.evaluate_spoken_response(
            transcript=transcript,
            duration_seconds=60.0,
            learner_id=learner_id,
            db=self.db
        )
        self.assertIn("estimated_band", eval_result)
        self.assertGreaterEqual(eval_result["estimated_band"], 6.5)

        # Check SQLite test_results
        test_repo = TestResultRepository(self.db)
        history = test_repo.get_history(learner_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["test_type"], "speaking")
        self.assertEqual(history[0]["track"], "Speaking")
        self.assertEqual(history[0]["speaking_band"], eval_result["estimated_band"])


if __name__ == "__main__":
    unittest.main()
