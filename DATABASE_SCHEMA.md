# Database Schema Specification — IELTS by GAMA

## Overview
IELTS by GAMA utilizes an offline-first, embedded SQLite database (`data/ielts_gama.db`) with Write-Ahead Logging (`WAL`), strict foreign keys (`PRAGMA foreign_keys = ON;`), and parameterized queries for thread-safe local data persistence.

---

## 1. Existing Tables & Schema (v1.5.3)

### `learners`
Stores learner profiles and primary test targets.
```sql
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
```

### `mistake_book`
Unified error ledger across all four skills and grammatical categories.
```sql
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
```

### `srs_items`
SuperMemo SM-2 Spaced Repetition items for vocabulary and grammar retention.
```sql
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
```

### `knowledge_base`
Compact curated curriculum and distilled knowledge for Local RAG and offline AI queries.
```sql
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
```

### `study_plans`
Personalized daily, weekly, and monthly study plans.
```sql
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
```

### `test_results`
Mock and practice test scores across skills.
```sql
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
```

### `smart_cache`
Disk cache for API responses and distilled content.
```sql
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
```

### `system_settings`
System preferences, offline mode flags, and content versions.
```sql
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 2. Phase 1 Extended Schema (Curriculum, Vocabulary, Exam Sessions)

To fulfill the requirements of the Master Project Directive, the database schema is extended with non-destructive migrations:

### `curriculum_lessons`
Structured CEFR A1–C2 English Learning Academy lessons.
```sql
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
```

### `lesson_progress`
Learner completion tracking for each lesson.
```sql
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
```

### `vocabulary_vault`
Comprehensive lexical repository with complete linguistic metadata.
```sql
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
```

### `exam_sessions`
Full 40-question mock exams and practice sessions with question navigation, timer, and state.
```sql
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
```

### `writing_drafts`
Writing submissions, autosaved drafts, criterion feedback, and version history.
```sql
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
```

### `ai_conversations`
Persistent learner-tutor dialogue history for contextual educational memory.
```sql
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
```

---

## 3. Migration Architecture
Migrations are managed in `core/database/migrations.py`. Each migration is transactional and checks for table existence, ensuring existing learner data is never lost or corrupted.
