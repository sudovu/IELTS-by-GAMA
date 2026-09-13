"""
Unit tests for Grammar Engine, Adaptive Grammar, and Vocabulary.
"""

import unittest
from core.grammar.grammar_engine import GrammarEngine
from core.vocabulary.vocab_engine import VocabEngine
from core.vocabulary.semantic_synonyms import SemanticSynonyms


class TestGrammarAndVocab(unittest.TestCase):
    def test_grammar_error_detection_and_formative_feedback(self):
        sentence = "I am agree with your opinion because he gave me a information."
        errors = GrammarEngine.check_sentence(sentence)
        self.assertTrue(len(errors) >= 2)

        categories = [e["category"] for e in errors]
        self.assertIn("Subject-Verb Agreement", categories)
        self.assertIn("Articles", categories)

        # Test prompt-mandated 5-point formative explanation
        formatted = GrammarEngine.format_teach_through_correction(errors[0])
        self.assertIn("ORIGINAL:", formatted)
        self.assertIn("CORRECTION:", formatted)
        self.assertIn("WHY:", formatted)
        self.assertIn("BETTER ALTERNATIVE", formatted)
        self.assertIn("PRACTICE EXERCISE:", formatted)

    def test_vocabulary_engine_word_families_and_collocations(self):
        word_data = VocabEngine.get_word("substantial")
        self.assertIsNotNone(word_data)
        self.assertEqual(word_data["pos"], "adjective")
        self.assertIn("substantially", word_data["word_family"].values())
        self.assertTrue(len(word_data["collocations"]) > 0)

        # Collocation exercise
        colloc_ex = VocabEngine.get_collocation_exercise()
        self.assertEqual(colloc_ex["correct"], "make")

    def test_semantic_synonyms_nuance(self):
        nuance = SemanticSynonyms.explain_nuance("important", "crucial")
        self.assertIsNotNone(nuance)
        self.assertIn("formality", nuance)
        self.assertIn("intensity", nuance)
        self.assertIn("collocations", nuance)


if __name__ == "__main__":
    unittest.main()
