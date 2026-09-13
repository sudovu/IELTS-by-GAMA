"""
Unit tests for Database Manager, Repositories, and Smart Cache (TTL & LRU).
"""

import unittest
import os
import tempfile
import time
from core.database.db_manager import DatabaseManager
from core.database.repositories import (
    LearnerRepository,
    MistakeBookRepository,
    SRSRepository,
    KnowledgeRepository,
    SettingsRepository
)
from core.memory.cache_manager import CacheManager


class TestDatabaseAndCache(unittest.TestCase):
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

    def test_learner_repository(self):
        repo = LearnerRepository(self.db)
        learner = repo.get_or_create_default("test_user", "Test Student")
        self.assertEqual(learner["name"], "Test Student")
        self.assertEqual(learner["target_band"], 7.0)

        updated = repo.update_profile("test_user", {"target_band": 8.0, "current_band": 6.5})
        self.assertEqual(updated["target_band"], 8.0)
        self.assertEqual(updated["current_band"], 6.5)

    def test_knowledge_repository(self):
        repo = KnowledgeRepository(self.db)
        item = repo.upsert_knowledge(
            topic="Articles",
            query_trigger="uncountable nouns",
            compact_knowledge="Uncountable nouns do not take 'a/an'."
        )
        self.assertEqual(item["topic"], "Articles")

        matches = repo.search_knowledge("uncountable")
        self.assertTrue(len(matches) > 0)
        self.assertIn("Articles", matches[0]["topic"])

    def test_smart_cache_ttl_and_lru(self):
        cache = CacheManager(self.db, max_cache_bytes=1024)  # Small 1KB limit
        cache.set("key1", {"value": "first"}, ttl_seconds=1)
        self.assertEqual(cache.get("key1")["value"], "first")

        # Sleep past 1 second TTL
        time.sleep(1.1)
        self.assertIsNone(cache.get("key1"))

        # Test LRU size capping
        cache.set("item_a", {"content": "X" * 300}, ttl_seconds=3600, priority=1)
        cache.set("item_b", {"content": "Y" * 300}, ttl_seconds=3600, priority=1)
        cache.set("item_c", {"content": "Z" * 500}, ttl_seconds=3600, priority=2)

        # Old item with lowest priority should be evicted to stay within budget
        stats = cache.get_stats()
        self.assertLessEqual(stats["total_bytes"], 1024)


if __name__ == "__main__":
    unittest.main()
