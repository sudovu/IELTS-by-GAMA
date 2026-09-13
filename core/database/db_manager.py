"""
Database Manager for SQLite in IELTS by GAMA.
Handles thread-safe connections, WAL mode, foreign keys, and safe schema initialization.
"""

import os
import sqlite3
import threading
from contextlib import contextmanager
from typing import Generator, Any
from .schema import SCHEMA_SQL


class DatabaseManager:
    """Manages SQLite database connections and transactions safely."""

    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, db_path: str = None):
        if db_path is None:
            # Default database location under user workspace or local data folder
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_dir = os.path.join(base_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, "ielts_gama.db")

        with cls._lock:
            if db_path not in cls._instances:
                instance = super(DatabaseManager, cls).__new__(cls)
                instance._init(db_path)
                cls._instances[db_path] = instance
            return cls._instances[db_path]

    def _init(self, db_path: str):
        self.db_path = db_path
        self._local = threading.local()
        self.init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.row_factory = sqlite3.Row
            # Performance & integrity pragmas
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA synchronous = NORMAL;")
            conn.execute("PRAGMA temp_store = MEMORY;")
            self._local.conn = conn
        return self._local.conn

    @contextmanager
    def connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Provides a database connection with auto-commit or rollback."""
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    @contextmanager
    def cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Provides a database cursor inside a managed transaction."""
        with self.connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
            finally:
                cursor.close()

    def init_schema(self):
        """Executes schema initialization script safely."""
        with self.connection() as conn:
            conn.executescript(SCHEMA_SQL)

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Executes a single parameterized query."""
        with self.connection() as conn:
            return conn.execute(sql, params)

    def executemany(self, sql: str, params_seq: list) -> sqlite3.Cursor:
        """Executes parameterized query for multiple parameter sets."""
        with self.connection() as conn:
            return conn.executemany(sql, params_seq)

    def fetchone(self, sql: str, params: tuple = ()) -> Any:
        """Executes query and returns one row as a dictionary-like Row object."""
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchone()

    def fetchall(self, sql: str, params: tuple = ()) -> list:
        """Executes query and returns all rows."""
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()

    def close(self):
        """Closes thread-local connection if open."""
        if hasattr(self._local, "conn") and self._local.conn is not None:
            try:
                self._local.conn.close()
            except Exception:
                pass
            self._local.conn = None
