"""
SQLite Database Schema for IELTS by GAMA
Provides definitions for learners, mistake tracking, spaced repetition (SRS),
compact knowledge base, smart cache, test sessions, and system configuration.
"""

SCHEMA_SQL = """
-- Learner profiles
CREATE TABLE IF NOT EXISTS learners (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    target_band REAL NOT NULL DEFAULT 7.0,
    current_band REAL NOT NULL DEFAULT 5.5,
    cefr_level TEXT NOT NULL DEFAULT 'B2',
    track TEXT NOT NULL DEFAULT 'Academic', -- 'Academic' or 'General Training'
    daily_minutes INTEGER NOT NULL DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Persistent Mistake Book
CREATE TABLE IF NOT EXISTS mistake_book (
    id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    skill TEXT NOT NULL, -- 'grammar', 'vocabulary', 'writing', 'speaking', 'reading', 'listening'
    category TEXT NOT NULL, -- e.g. 'Articles', 'Subject-Verb Agreement', 'Collocation'
    subcategory TEXT,
    original_text TEXT NOT NULL,
    corrected_text TEXT NOT NULL,
    explanation TEXT NOT NULL,
    recurrence_count INTEGER DEFAULT 1,
    mastery_score REAL DEFAULT 0.0, -- 0.0 to 1.0
    status TEXT DEFAULT 'needs_improvement', -- 'needs_improvement', 'reviewing', 'mastered'
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    next_review TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id)
);

-- Spaced Repetition System (SuperMemo SM-2)
CREATE TABLE IF NOT EXISTS srs_items (
    id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    item_type TEXT NOT NULL, -- 'vocabulary', 'grammar', 'phrasal_verb', 'collocation', 'idiom'
    key_term TEXT NOT NULL,
    prompt TEXT NOT NULL,
    answer TEXT NOT NULL,
    notes TEXT,
    repetition INTEGER DEFAULT 0,
    interval_days REAL DEFAULT 1.0,
    ease_factor REAL DEFAULT 2.5,
    due_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    review_history TEXT, -- JSON array of reviews
    FOREIGN KEY (learner_id) REFERENCES learners(id)
);

-- Permanent Compact Knowledge Base (Local RAG + Online-to-Offline persistence)
CREATE TABLE IF NOT EXISTS knowledge_base (
    id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    subtopic TEXT,
    query_trigger TEXT NOT NULL,
    compact_knowledge TEXT NOT NULL,
    source TEXT DEFAULT 'curated', -- 'curated', 'online_distilled', 'user_saved'
    confidence REAL DEFAULT 0.95,
    version TEXT DEFAULT '1.0.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Personalized Study Plans
CREATE TABLE IF NOT EXISTS study_plans (
    id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    plan_type TEXT NOT NULL, -- 'daily', 'weekly', 'monthly'
    target_date TEXT NOT NULL,
    tasks_json TEXT NOT NULL,
    completed_json TEXT DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id)
);

-- Mock & Practice Test Results
CREATE TABLE IF NOT EXISTS test_results (
    id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    test_type TEXT NOT NULL, -- 'diagnostic', 'mock_full', 'reading', 'listening', 'writing', 'speaking'
    track TEXT NOT NULL DEFAULT 'Academic',
    overall_band REAL NOT NULL,
    listening_band REAL,
    reading_band REAL,
    writing_band REAL,
    speaking_band REAL,
    details_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES learners(id)
);

-- Smart Disk Cache (TTL + LRU)
CREATE TABLE IF NOT EXISTS smart_cache (
    cache_key TEXT PRIMARY KEY,
    data_json TEXT NOT NULL,
    data_type TEXT NOT NULL,
    size_bytes INTEGER NOT NULL,
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

-- System Settings & Preferences
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indices for rapid querying
CREATE INDEX IF NOT EXISTS idx_mistakes_learner_skill ON mistake_book (learner_id, skill, status);
CREATE INDEX IF NOT EXISTS idx_srs_due ON srs_items (learner_id, due_date);
CREATE INDEX IF NOT EXISTS idx_knowledge_topic ON knowledge_base (topic, query_trigger);
CREATE INDEX IF NOT EXISTS idx_cache_expires ON smart_cache (expires_at);
CREATE INDEX IF NOT EXISTS idx_cache_accessed ON smart_cache (last_accessed);
"""
