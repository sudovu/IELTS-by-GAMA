"""
Unit tests for Writing Evaluator and Speaking Examiner.
"""

import unittest
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.speaking.fluency_tracker import FluencyTracker


class TestWritingAndSpeaking(unittest.TestCase):
    def test_writing_evaluation_and_criteria(self):
        sample_essay = (
            "In contemporary society, education plays a vital role in determining individual success. "
            "Some educationalists argue that high school curricula should prioritize STEM subjects over artistic fields. "
            "Although scientific skills are crucial for national economic competitiveness, I believe artistic studies "
            "are equally indispensable for developing creative thinking.\n\n"
            "To begin with, technological development requires robust training in engineering and mathematics. "
            "Consequently, students equipped with quantitative competence can innovate modern digital infrastructure.\n\n"
            "On the other hand, humanities and literature cultivate empathy and ethical judgment. "
            "Furthermore, modern industries increasingly demand individuals with strong communication skills.\n\n"
            "In conclusion, while STEM domains provide practical utility, a balanced educational curriculum is essential."
        )

        res = WritingEvaluator.evaluate_essay("acad_t2_stem", sample_essay)
        self.assertIn("estimated_band", res)
        self.assertIn("Task Response", res["criteria"])
        self.assertIn("Coherence and Cohesion", res["criteria"])
        self.assertIn("Lexical Resource", res["criteria"])
        self.assertIn("Grammatical Range and Accuracy", res["criteria"])
        self.assertGreaterEqual(res["estimated_band"], 6.0)

    def test_fluency_tracker_metrics(self):
        speech = "I would like to describe um an ambitious goal that I achieved last year. It was basically very challenging."
        metrics = FluencyTracker.analyze_fluency(speech, duration_seconds=10.0)
        self.assertGreater(metrics["words_per_minute"], 50)
        self.assertIn("um", metrics["filler_breakdown"])
        self.assertIn("basically", metrics["filler_breakdown"])

    def test_speaking_examiner_simulation(self):
        transcript = "I pursued my dream of learning foreign languages because it opens up remarkable opportunities worldwide."
        report = SpeakingExaminer.evaluate_spoken_response(transcript, duration_seconds=30.0)
        self.assertIn("estimated_band", report)
        self.assertIn("Fluency and Coherence", report["criteria"])
        self.assertIn("Pronunciation", report["criteria"])


if __name__ == "__main__":
    unittest.main()
