"""Vocabulary subsystem package for IELTS by GAMA."""
from .vocab_engine import VocabEngine
from .semantic_synonyms import SemanticSynonyms
from .vocabulary_vault import VocabularyVault

__all__ = ["VocabEngine", "SemanticSynonyms", "VocabularyVault"]
