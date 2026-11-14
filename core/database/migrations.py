"""
Database Migration Manager for IELTS by GAMA.
Ensures non-destructive, versioned, transactional migrations of the SQLite schema.
Preserves existing learner records, test results, and knowledge base.
"""

import sqlite3
import datetime
import re
from typing import List, Tuple
from .db_manager import DatabaseManager


class MigrationManager:
    """Applies schema migrations safely and idempotently."""

    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def _ensure_migration_table(self, conn: sqlite3.Connection):
        conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

    def get_applied_versions(self, conn: sqlite3.Connection) -> List[int]:
        self._ensure_migration_table(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT version FROM schema_migrations ORDER BY version ASC;")
        return [row[0] for row in cursor.fetchall()]

    def run_migrations(self, verbose: bool = False) -> int:
        """Runs all pending migrations in order. Returns count of applied migrations."""
        applied_count = 0
        with self.db.connection() as conn:
            self._ensure_migration_table(conn)
            applied = set(self.get_applied_versions(conn))

            migrations: List[Tuple[int, str, callable]] = [
                (1, "extend_learner_and_create_core_tables", self._migration_001_core_expansion),
                (2, "phase16_rbac_review_benchmark_and_beta_tables", self._migration_002_phase16_tables),
            ]

            for version, name, migration_fn in migrations:
                if version not in applied:
                    if verbose:
                        print(f"[Migration] Applying migration v{version}: {name}...")
                    migration_fn(conn)
                    now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
                    conn.execute(
                        "INSERT INTO schema_migrations (version, name, applied_at) VALUES (?, ?, ?);",
                        (version, name, now_str)
                    )
                    applied_count += 1
                    if verbose:
                        print(f"[Migration] Successfully applied migration v{version}: {name}")

        return applied_count

    def _column_exists(self, conn: sqlite3.Connection, table_name: str, column_name: str) -> bool:
        if not re.match(r"^[a-zA-Z0-9_]+$", table_name):
            raise ValueError(f"Invalid table name: {table_name}")
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        cols = [row[1] for row in cursor.fetchall()]
        return column_name in cols

    def _migration_001_core_expansion(self, conn: sqlite3.Connection):
        """
        Adds:
        - Extended columns to learners (target_exam_date, native_language, target_sub_skills, notes)
        - curriculum_lessons table
        - lesson_progress table
        - vocabulary_vault table
        - exam_sessions table
        - writing_drafts table
        - ai_conversations table
        """
        # 1. Extend learners table
        if not self._column_exists(conn, "learners", "target_exam_date"):
            conn.execute("ALTER TABLE learners ADD COLUMN target_exam_date TEXT;")
        if not self._column_exists(conn, "learners", "native_language"):
            conn.execute("ALTER TABLE learners ADD COLUMN native_language TEXT DEFAULT 'English';")
        if not self._column_exists(conn, "learners", "target_sub_skills"):
            conn.execute("ALTER TABLE learners ADD COLUMN target_sub_skills TEXT DEFAULT '[]';")
        if not self._column_exists(conn, "learners", "notes"):
            conn.execute("ALTER TABLE learners ADD COLUMN notes TEXT;")

        # 2. curriculum_lessons
        conn.execute("""
        CREATE TABLE IF NOT EXISTS curriculum_lessons (
            id TEXT PRIMARY KEY,
            cefr_level TEXT NOT NULL, -- 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'
            module_type TEXT NOT NULL, -- 'grammar', 'vocabulary', 'reading', 'listening', 'speaking', 'writing'
            title TEXT NOT NULL,
            order_index INTEGER NOT NULL,
            objectives_json TEXT NOT NULL,
            explanation_markdown TEXT NOT NULL,
            examples_json TEXT NOT NULL,
            guided_exercises_json TEXT NOT NULL,
            interactive_practice_json TEXT NOT NULL,
            assessment_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_curriculum_level ON curriculum_lessons(cefr_level, module_type, order_index);")

        # 3. lesson_progress
        conn.execute("""
        CREATE TABLE IF NOT EXISTS lesson_progress (
            id TEXT PRIMARY KEY,
            learner_id TEXT NOT NULL,
            lesson_id TEXT NOT NULL,
            status TEXT DEFAULT 'not_started', -- 'not_started', 'in_progress', 'completed'
            score REAL DEFAULT 0.0,
            attempts INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(id),
            FOREIGN KEY (lesson_id) REFERENCES curriculum_lessons(id)
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lesson_progress ON lesson_progress(learner_id, lesson_id);")

        # 4. vocabulary_vault
        conn.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary_vault (
            id TEXT PRIMARY KEY,
            word TEXT NOT NULL UNIQUE,
            pos TEXT NOT NULL,
            pronunciation TEXT,
            ipa TEXT,
            cefr_level TEXT NOT NULL, -- 'A1' - 'C2'
            band_tier TEXT NOT NULL, -- e.g. 'Band 7-8'
            simple_definition TEXT NOT NULL,
            advanced_definition TEXT NOT NULL,
            example_sentences_json TEXT NOT NULL,
            synonyms_json TEXT NOT NULL,
            antonyms_json TEXT NOT NULL,
            word_family_json TEXT NOT NULL,
            collocations_json TEXT NOT NULL,
            common_mistakes_json TEXT NOT NULL,
            academic_usage TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_vocab_word ON vocabulary_vault(word);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_vocab_cefr ON vocabulary_vault(cefr_level);")

        # 5. exam_sessions
        conn.execute("""
        CREATE TABLE IF NOT EXISTS exam_sessions (
            id TEXT PRIMARY KEY,
            learner_id TEXT NOT NULL,
            module TEXT NOT NULL, -- 'reading', 'listening', 'writing', 'speaking', 'full_mock'
            track TEXT NOT NULL, -- 'Academic', 'General Training'
            status TEXT NOT NULL, -- 'in_progress', 'submitted', 'abandoned'
            time_limit_seconds INTEGER NOT NULL,
            time_spent_seconds INTEGER DEFAULT 0,
            answers_json TEXT DEFAULT '{}',
            results_json TEXT DEFAULT '{}',
            band_score REAL,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(id)
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_exam_sessions_learner ON exam_sessions(learner_id, module, status);")

        # 6. writing_drafts
        conn.execute("""
        CREATE TABLE IF NOT EXISTS writing_drafts (
            id TEXT PRIMARY KEY,
            learner_id TEXT NOT NULL,
            prompt_id TEXT NOT NULL,
            task_type TEXT NOT NULL, -- 'task_1', 'task_2'
            track TEXT NOT NULL, -- 'Academic', 'General Training'
            draft_text TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            status TEXT DEFAULT 'draft', -- 'draft', 'evaluated'
            ta_score REAL,
            cc_score REAL,
            lr_score REAL,
            gra_score REAL,
            overall_band REAL,
            feedback_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(id)
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_writing_drafts_learner ON writing_drafts(learner_id, prompt_id);")

        # 7. ai_conversations
        conn.execute("""
        CREATE TABLE IF NOT EXISTS ai_conversations (
            id TEXT PRIMARY KEY,
            learner_id TEXT NOT NULL,
            role TEXT NOT NULL, -- 'user', 'tutor', 'system'
            message TEXT NOT NULL,
            detected_errors_json TEXT,
            metadata_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(id)
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ai_conv_learner ON ai_conversations(learner_id, created_at);")

    def _migration_002_phase16_tables(self, conn: sqlite3.Connection):
        """
        Phase 16 Schema Expansion:
        1. users & user_sessions (RBAC: learner, teacher, examiner, admin)
        2. teacher_assignments
        3. review_assignments & human_evaluations (blind double-marking & criteria grading)
        4. benchmark_records (human benchmark dataset management)
        5. beta_cohorts, beta_participants, beta_feedback & beta_bug_reports
        """
        import hashlib, os, secrets

        # 1. users
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL, -- 'learner', 'teacher', 'examiner', 'admin'
            full_name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);")

        # 2. user_sessions
        conn.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_token TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id);")

        # 3. teacher_assignments
        conn.execute("""
        CREATE TABLE IF NOT EXISTS teacher_assignments (
            id TEXT PRIMARY KEY,
            teacher_id TEXT NOT NULL,
            learner_id TEXT NOT NULL,
            assigned_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES users(id),
            FOREIGN KEY (learner_id) REFERENCES learners(id)
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_teacher_learner ON teacher_assignments(teacher_id, learner_id);")

        # 4. review_assignments
        conn.execute("""
        CREATE TABLE IF NOT EXISTS review_assignments (
            id TEXT PRIMARY KEY,
            submission_id TEXT NOT NULL,
            submission_type TEXT NOT NULL, -- 'writing', 'speaking'
            learner_id TEXT NOT NULL,
            task_type TEXT, -- 'task_1', 'task_2', 'speaking_full'
            track TEXT, -- 'Academic', 'General Training'
            content_json TEXT NOT NULL,
            assigned_to TEXT NOT NULL,
            assigned_role TEXT NOT NULL, -- 'teacher', 'examiner'
            status TEXT DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'reconciled'
            is_benchmark INTEGER DEFAULT 0,
            benchmark_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_to) REFERENCES users(id)
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_review_assign_user ON review_assignments(assigned_to, status);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_review_submission ON review_assignments(submission_id);")

        # 5. human_evaluations
        conn.execute("""
        CREATE TABLE IF NOT EXISTS human_evaluations (
            id TEXT PRIMARY KEY,
            assignment_id TEXT NOT NULL,
            submission_id TEXT NOT NULL,
            reviewer_id TEXT NOT NULL,
            reviewer_role TEXT NOT NULL, -- 'teacher', 'examiner', 'senior_examiner'
            overall_band REAL NOT NULL,
            criteria_scores_json TEXT NOT NULL,
            assessment_mode TEXT DEFAULT 'transcript', -- 'audio', 'transcript', 'both'
            criterion_feedback_json TEXT,
            general_comments TEXT,
            status TEXT DEFAULT 'submitted', -- 'draft', 'submitted', 'reconciled'
            revision INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            submitted_at TIMESTAMP,
            FOREIGN KEY (assignment_id) REFERENCES review_assignments(id),
            FOREIGN KEY (reviewer_id) REFERENCES users(id)
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_human_eval_assign ON human_evaluations(assignment_id);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_human_eval_sub ON human_evaluations(submission_id);")

        # 6. benchmark_records
        conn.execute("""
        CREATE TABLE IF NOT EXISTS benchmark_records (
            id TEXT PRIMARY KEY,
            assessment_type TEXT NOT NULL, -- 'writing', 'speaking'
            task_type TEXT,
            track TEXT,
            anonymized_content TEXT NOT NULL,
            recording_ref TEXT,
            consent_status TEXT DEFAULT 'consented', -- 'consented', 'withdrawn', 'pending'
            consent_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            dataset_version TEXT DEFAULT '1.0.0',
            consensus_human_band REAL,
            consensus_criteria_json TEXT,
            double_marked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_bench_type ON benchmark_records(assessment_type, task_type);")

        # 7. beta_cohorts
        conn.execute("""
        CREATE TABLE IF NOT EXISTS beta_cohorts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            track_or_level TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            max_participants INTEGER DEFAULT 50,
            status TEXT DEFAULT 'active', -- 'active', 'closed'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 8. beta_participants
        conn.execute("""
        CREATE TABLE IF NOT EXISTS beta_participants (
            id TEXT PRIMARY KEY,
            cohort_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            email TEXT,
            consent_status TEXT DEFAULT 'consented',
            status TEXT DEFAULT 'active', -- 'invited', 'active', 'completed', 'dropped'
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cohort_id) REFERENCES beta_cohorts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_beta_part_cohort ON beta_participants(cohort_id, user_id);")

        # 9. beta_feedback
        conn.execute("""
        CREATE TABLE IF NOT EXISTS beta_feedback (
            id TEXT PRIMARY KEY,
            cohort_id TEXT NOT NULL,
            participant_id TEXT,
            is_anonymous INTEGER DEFAULT 0,
            category TEXT NOT NULL,
            rating INTEGER,
            comments TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cohort_id) REFERENCES beta_cohorts(id)
        );
        """)

        # 10. beta_bug_reports
        conn.execute("""
        CREATE TABLE IF NOT EXISTS beta_bug_reports (
            id TEXT PRIMARY KEY,
            cohort_id TEXT NOT NULL,
            reporter_id TEXT,
            severity TEXT NOT NULL, -- 'critical', 'high', 'medium', 'low'
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            steps_to_reproduce TEXT,
            status TEXT DEFAULT 'open', -- 'open', 'investigating', 'resolved'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cohort_id) REFERENCES beta_cohorts(id)
        );
        """)

        # Schema created for users and sessions.
        # Note (Phase 17 Hardening): Automatic seeding of privileged user accounts
        # with hardcoded default passwords has been removed from migrations.
        # Initial administrators must be provisioned via scripts/provision_admin.py.

        # Seed initial 4 Beta Cohorts if empty
        cohort_count = conn.execute("SELECT COUNT(*) FROM beta_cohorts;").fetchone()[0]
        if cohort_count == 0:
            cohorts = [
                ("cohort_acad_1", "IELTS Academic Pilot Cohort A", "Academic", "2026-12-01", "2027-01-15", 30),
                ("cohort_gt_1", "IELTS General Training Pilot Cohort B", "General Training", "2026-12-01", "2027-01-15", 30),
                ("cohort_acad_a1_b1", "English Academy Foundations (A1-B1) Cohort", "Academy A1-B1", "2026-12-05", "2027-01-20", 40),
                ("cohort_acad_b2_c2", "English Academy Advanced (B2-C2) Cohort", "Academy B2-C2", "2026-12-05", "2027-01-20", 40),
            ]
            for cid, cname, ctrack, sdate, edate, max_p in cohorts:
                conn.execute(
                    "INSERT INTO beta_cohorts (id, name, track_or_level, start_date, end_date, max_participants) VALUES (?, ?, ?, ?, ?, ?);",
                    (cid, cname, ctrack, sdate, edate, max_p)
                )
