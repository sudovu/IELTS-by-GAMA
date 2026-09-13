"""
Smart Cache Manager for IELTS by GAMA.
Implements TTL (Time-To-Live) and LRU (Least Recently Used) cache eviction
on SQLite for temporary research, generated audio, intermediate analyses, and context.
"""

import hashlib
import json
import datetime
from typing import Any, Optional, Dict
from ..database.db_manager import DatabaseManager


class CacheManager:
    """Manages temporary cached data with expiration and size-bounded LRU eviction."""

    def __init__(self, db: DatabaseManager = None, max_cache_bytes: int = 50 * 1024 * 1024):  # 50MB default
        self.db = db or DatabaseManager()
        self.max_cache_bytes = max_cache_bytes

    def _hash_key(self, raw_key: str) -> str:
        return hashlib.sha256(raw_key.strip().lower().encode("utf-8")).hexdigest()

    def set(
        self,
        key: str,
        data: Any,
        ttl_seconds: int = 3600,  # 1 hour default
        data_type: str = "general",
        priority: int = 1
    ) -> str:
        cache_key = self._hash_key(key)
        data_json = json.dumps(data)
        size_bytes = len(data_json.encode("utf-8"))
        now = datetime.datetime.utcnow()
        expires_at = (now + datetime.timedelta(seconds=ttl_seconds)).isoformat()
        now_iso = now.isoformat()

        # Enforce storage limits before insert
        self.cleanup_expired()
        self._enforce_max_size(size_bytes)

        self.db.execute(
            """INSERT INTO smart_cache 
               (cache_key, data_json, data_type, size_bytes, priority, created_at, last_accessed, expires_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(cache_key) DO UPDATE SET
                   data_json = excluded.data_json,
                   data_type = excluded.data_type,
                   size_bytes = excluded.size_bytes,
                   priority = excluded.priority,
                   last_accessed = excluded.last_accessed,
                   expires_at = excluded.expires_at""",
            (cache_key, data_json, data_type, size_bytes, priority, now_iso, now_iso, expires_at)
        )
        return cache_key

    def get(self, key: str) -> Optional[Any]:
        cache_key = self._hash_key(key)
        now_iso = datetime.datetime.utcnow().isoformat()
        row = self.db.fetchone(
            "SELECT data_json, expires_at FROM smart_cache WHERE cache_key = ?",
            (cache_key,)
        )
        if not row:
            return None

        if row["expires_at"] < now_iso:
            # Expired
            self.delete(key)
            return None

        # Update last_accessed timestamp (LRU)
        self.db.execute(
            "UPDATE smart_cache SET last_accessed = ? WHERE cache_key = ?",
            (now_iso, cache_key)
        )
        return json.loads(row["data_json"])

    def delete(self, key: str):
        cache_key = self._hash_key(key)
        self.db.execute("DELETE FROM smart_cache WHERE cache_key = ?", (cache_key,))

    def cleanup_expired(self) -> int:
        """Removes all cache entries whose expiration date is in the past."""
        now_iso = datetime.datetime.utcnow().isoformat()
        cur = self.db.execute("DELETE FROM smart_cache WHERE expires_at < ?", (now_iso,))
        return cur.rowcount if hasattr(cur, "rowcount") else 0

    def _enforce_max_size(self, incoming_bytes: int):
        row = self.db.fetchone("SELECT COALESCE(SUM(size_bytes), 0) as total FROM smart_cache")
        current_total = row["total"] if row else 0

        if current_total + incoming_bytes > self.max_cache_bytes:
            # Evict least recently accessed with lowest priority
            rows = self.db.fetchall(
                "SELECT cache_key, size_bytes FROM smart_cache ORDER BY priority ASC, last_accessed ASC"
            )
            for r in rows:
                self.db.execute("DELETE FROM smart_cache WHERE cache_key = ?", (r["cache_key"],))
                current_total -= r["size_bytes"]
                if current_total + incoming_bytes <= self.max_cache_bytes:
                    break

    def get_stats(self) -> Dict[str, Any]:
        row = self.db.fetchone(
            "SELECT COUNT(*) as count, COALESCE(SUM(size_bytes), 0) as total_bytes FROM smart_cache"
        )
        return {
            "entries_count": row["count"] if row else 0,
            "total_bytes": row["total_bytes"] if row else 0,
            "max_allowed_bytes": self.max_cache_bytes
        }

    def clear_all(self):
        self.db.execute("DELETE FROM smart_cache")
