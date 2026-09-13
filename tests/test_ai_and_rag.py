"""
Unit tests for Local AI, Local RAG, and Task Router.
"""

import unittest
import os
import tempfile
from core.database.db_manager import DatabaseManager
from core.database.repositories import KnowledgeRepository
from core.ai.local_rag import LocalRAG
from core.ai.local_provider import LocalAIProvider
from core.ai.task_router import TaskRouter, TaskType
from core.sync.connectivity import ConnectivityState


class TestAIAndRAG(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.db = DatabaseManager(self.temp_path)
        self.db.init_schema()

        # Seed knowledge
        repo = KnowledgeRepository(self.db)
        repo.upsert_knowledge(
            topic="Affect vs Effect",
            query_trigger="difference between affect and effect",
            compact_knowledge="Affect is a verb. Effect is a noun."
        )
        self.rag = LocalRAG(self.db)
        self.rag.refresh()
        self.local_ai = LocalAIProvider(self.db)

    def tearDown(self):
        self.db.close()
        try:
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)
        except Exception:
            pass

    def test_local_rag_retrieval(self):
        docs, confidence = self.rag.query("difference between affect and effect")
        self.assertTrue(len(docs) > 0)
        self.assertIn("Affect vs Effect", docs[0]["topic"])
        self.assertGreaterEqual(confidence, 0.7)

    def test_local_ai_generation_offline(self):
        resp = self.local_ai.generate("Explain affect vs effect")
        self.assertTrue(resp.is_offline)
        self.assertIn("Affect", resp.text)
        self.assertIn("Effect", resp.text)
        self.assertGreaterEqual(resp.confidence, 0.8)

    def test_task_router_logic(self):
        # Offline always routes to local
        target = TaskRouter.decide_target(
            task_type=TaskType.WRITING_EVAL,
            connectivity_state=ConnectivityState.OFFLINE,
            cloud_ai_enabled=True
        )
        self.assertEqual(target, "local")

        # Grammar is always local
        target = TaskRouter.decide_target(
            task_type=TaskType.GRAMMAR,
            connectivity_state=ConnectivityState.ONLINE,
            cloud_ai_enabled=True
        )
        self.assertEqual(target, "local")

        # Complex writing when user opts into cloud and online
        target = TaskRouter.decide_target(
            task_type=TaskType.WRITING_EVAL,
            connectivity_state=ConnectivityState.ONLINE,
            cloud_ai_enabled=True,
            local_confidence=0.5
        )
        self.assertEqual(target, "cloud")


if __name__ == "__main__":
    unittest.main()
