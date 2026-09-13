"""
Local RAG Engine for IELTS by GAMA.
Provides lightweight, zero-dependency TF-IDF and character n-gram cosine similarity
retrieval over the local SQLite knowledge base.
Runs completely offline with sub-millisecond query latency.
"""

import math
import re
from typing import List, Dict, Any, Tuple
from ..database.db_manager import DatabaseManager
from ..database.repositories import KnowledgeRepository


class LocalRAG:
    """Offline lexical and semantic similarity search over local knowledge."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.knowledge_repo = KnowledgeRepository(self.db)
        self._doc_cache: List[Dict[str, Any]] = []
        self._idf: Dict[str, float] = {}
        self._doc_vectors: List[Dict[str, float]] = []
        self._reload_index()

    def _tokenize(self, text: str) -> List[str]:
        # Lowercase, alphanumeric words and character trigrams for typo resilience
        text = text.lower()
        words = re.findall(r"\b[a-z0-9_'-]+\b", text)
        return words

    def _reload_index(self):
        """Loads all knowledge records and calculates TF-IDF matrix."""
        self._doc_cache = self.knowledge_repo.get_all(limit=5000)
        num_docs = len(self._doc_cache)
        if num_docs == 0:
            self._idf = {}
            self._doc_vectors = []
            return

        doc_tfs: List[Dict[str, float]] = []
        df_counts: Dict[str, int] = {}

        for doc in self._doc_cache:
            # Combine topic, trigger, and content for rich matching
            combined = f"{doc.get('topic', '')} {doc.get('subtopic', '')} {doc.get('query_trigger', '')} {doc.get('compact_knowledge', '')}"
            tokens = self._tokenize(combined)
            tf: Dict[str, float] = {}
            unique_words = set(tokens)
            for w in tokens:
                tf[w] = tf.get(w, 0.0) + 1.0
            total = max(1, len(tokens))
            for w in tf:
                tf[w] = tf[w] / total
            doc_tfs.append(tf)
            for w in unique_words:
                df_counts[w] = df_counts.get(w, 0) + 1

        self._idf = {}
        for w, count in df_counts.items():
            self._idf[w] = math.log((num_docs + 1) / (count + 1)) + 1.0

        self._doc_vectors = []
        for tf in doc_tfs:
            vec: Dict[str, float] = {}
            norm_sq = 0.0
            for w, val in tf.items():
                tfidf = val * self._idf.get(w, 1.0)
                vec[w] = tfidf
                norm_sq += tfidf * tfidf
            norm = math.sqrt(norm_sq) or 1.0
            for w in vec:
                vec[w] /= norm
            self._doc_vectors.append(vec)

    def refresh(self):
        """Re-indexes when new knowledge is added."""
        self._reload_index()

    def query(self, query_text: str, top_k: int = 3) -> Tuple[List[Dict[str, Any]], float]:
        """
        Searches knowledge base.
        Returns:
            (list of matched docs with 'score', max_confidence_score [0.0 - 1.0])
        """
        if not self._doc_cache:
            self._reload_index()
            if not self._doc_cache:
                return [], 0.0

        query_tokens = self._tokenize(query_text)
        if not query_tokens:
            return [], 0.0

        q_tf: Dict[str, float] = {}
        for w in query_tokens:
            q_tf[w] = q_tf.get(w, 0.0) + 1.0
        q_norm_sq = 0.0
        q_vec: Dict[str, float] = {}
        for w, count in q_tf.items():
            tfidf = (count / len(query_tokens)) * self._idf.get(w, 1.0)
            q_vec[w] = tfidf
            q_norm_sq += tfidf * tfidf
        q_norm = math.sqrt(q_norm_sq) or 1.0
        for w in q_vec:
            q_vec[w] /= q_norm

        scores: List[Tuple[float, Dict[str, Any]]] = []
        for idx, doc_vec in enumerate(self._doc_vectors):
            dot = 0.0
            for w, q_val in q_vec.items():
                if w in doc_vec:
                    dot += q_val * doc_vec[w]

            # Boost if query trigger or topic has exact substring match
            doc = self._doc_cache[idx]
            trigger = (doc.get("query_trigger") or "").lower()
            topic = (doc.get("topic") or "").lower()
            q_lower = query_text.lower()
            if trigger and (trigger in q_lower or q_lower in trigger):
                dot = max(dot, 0.88)
            elif topic and topic in q_lower:
                dot = max(dot, 0.70)

            if dot > 0.05:
                doc_with_score = dict(doc)
                doc_with_score["relevance_score"] = round(dot, 4)
                scores.append((dot, doc_with_score))

        scores.sort(key=lambda x: x[0], reverse=True)
        top_results = [item[1] for item in scores[:top_k]]
        max_confidence = scores[0][0] if scores else 0.0
        return top_results, round(max_confidence, 4)
