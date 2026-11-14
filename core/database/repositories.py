"""
Repositories for IELTS by GAMA.
Encapsulates CRUD operations on SQLite for learners, mistakes, SRS, knowledge, tests,
curriculum lessons, vocabulary vault, exam sessions, writing drafts, and AI conversations.
"""

import json
import uuid
import datetime
from typing import Optional, List, Dict, Any
from .db_manager import DatabaseManager


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _now_dt() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class LearnerRepository:
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def get_learner(self, learner_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM learners WHERE id = ?", (learner_id,))
        return dict(row) if row else None

    def list_all_learners(self) -> List[Dict[str, Any]]:
        rows = self.db.fetchall("SELECT * FROM learners ORDER BY created_at ASC")
        return [dict(r) for r in rows]

    def get_or_create_default(self, learner_id: str = "default_learner", name: str = "Learner") -> Dict[str, Any]:
        existing = self.get_learner(learner_id)
        if existing:
            return existing
        now = _now_iso()
        self.db.execute(
            """INSERT INTO learners (id, name, target_band, current_band, cefr_level, track, daily_minutes, target_exam_date, native_language, target_sub_skills, notes, created_at, updated_at)
               VALUES (?, ?, 7.0, 5.5, 'B2', 'Academic', 30, NULL, 'English', '[]', NULL, ?, ?)""",
            (learner_id, name, now, now)
        )
        return self.get_learner(learner_id)

    def create_learner(
        self,
        name: str,
        target_band: float = 7.0,
        current_band: float = 5.5,
        cefr_level: str = "B2",
        track: str = "Academic",
        daily_minutes: int = 30,
        target_exam_date: Optional[str] = None,
        native_language: str = "English",
        target_sub_skills: Optional[List[str]] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        learner_id = f"learner_{uuid.uuid4().hex[:12]}"
        now = _now_iso()
        sub_skills_json = json.dumps(target_sub_skills or [])
        self.db.execute(
            """INSERT INTO learners (id, name, target_band, current_band, cefr_level, track, daily_minutes, target_exam_date, native_language, target_sub_skills, notes, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (learner_id, name, target_band, current_band, cefr_level, track, daily_minutes, target_exam_date, native_language, sub_skills_json, notes, now, now)
        )
        return self.get_learner(learner_id)

    def update_profile(self, learner_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        fields = []
        params = []
        allowed_fields = [
            "name", "target_band", "current_band", "cefr_level", "track", "daily_minutes",
            "target_exam_date", "native_language", "target_sub_skills", "notes"
        ]
        for k, v in updates.items():
            if k in allowed_fields:
                fields.append(f"{k} = ?")
                if k == "target_sub_skills" and isinstance(v, list):
                    params.append(json.dumps(v))
                else:
                    params.append(v)
        if not fields:
            return self.get_or_create_default(learner_id)
        params.append(_now_iso())
        params.append(learner_id)
        sql = f"UPDATE learners SET {', '.join(fields)}, updated_at = ? WHERE id = ?"
        self.db.execute(sql, tuple(params))
        return self.get_or_create_default(learner_id)

    def delete_learner(self, learner_id: str) -> bool:
        if learner_id == "default_learner":
            # Don't delete the default profile, reset it instead
            self.update_profile(learner_id, {
                "name": "Learner",
                "target_band": 7.0,
                "current_band": 5.5,
                "cefr_level": "B2",
                "track": "Academic",
                "daily_minutes": 30
            })
            return True
        cur = self.db.execute("DELETE FROM learners WHERE id = ?", (learner_id,))
        return (cur.rowcount > 0) if hasattr(cur, "rowcount") else True


class MistakeBookRepository:
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def record_mistake(
        self,
        learner_id: str,
        skill: str,
        category: str,
        original_text: str,
        corrected_text: str,
        explanation: str,
        subcategory: Optional[str] = None
    ) -> Dict[str, Any]:
        """Records a mistake. If matching category + original exists for learner, increments recurrence."""
        LearnerRepository(self.db).get_or_create_default(learner_id)
        now = _now_iso()
        existing = self.db.fetchone(
            """SELECT * FROM mistake_book 
               WHERE learner_id = ? AND skill = ? AND category = ? AND original_text = ?""",
            (learner_id, skill, category, original_text)
        )
        if existing:
            new_count = existing["recurrence_count"] + 1
            new_mastery = max(0.0, existing["mastery_score"] - 0.1)
            self.db.execute(
                """UPDATE mistake_book 
                   SET recurrence_count = ?, mastery_score = ?, status = 'needs_improvement', 
                       last_seen = ?, next_review = ?, explanation = ?
                   WHERE id = ?""",
                (new_count, new_mastery, now, now, explanation, existing["id"])
            )
            item = dict(existing)
            item["recurrence_count"] = new_count
            item["status"] = "needs_improvement"
            return item
        else:
            item_id = str(uuid.uuid4())
            self.db.execute(
                """INSERT INTO mistake_book 
                   (id, learner_id, skill, category, subcategory, original_text, corrected_text, explanation, recurrence_count, mastery_score, status, last_seen, next_review)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0.0, 'needs_improvement', ?, ?)""",
                (item_id, learner_id, skill, category, subcategory, original_text, corrected_text, explanation, now, now)
            )
            return {
                "id": item_id,
                "learner_id": learner_id,
                "skill": skill,
                "category": category,
                "subcategory": subcategory,
                "original_text": original_text,
                "corrected_text": corrected_text,
                "explanation": explanation,
                "recurrence_count": 1,
                "mastery_score": 0.0,
                "status": "needs_improvement"
            }

    def update_mastery(self, mistake_id: str, success: bool) -> Dict[str, Any]:
        row = self.db.fetchone("SELECT * FROM mistake_book WHERE id = ?", (mistake_id,))
        if not row:
            raise ValueError(f"Mistake with id {mistake_id} not found")
        mastery = row["mastery_score"]
        now = _now_dt()
        if success:
            mastery = min(1.0, mastery + 0.34)
        else:
            mastery = max(0.0, mastery - 0.25)
        
        status = "mastered" if mastery >= 0.95 else ("reviewing" if mastery >= 0.5 else "needs_improvement")
        days_ahead = 7 if status == "mastered" else (3 if status == "reviewing" else 1)
        next_review = (now + datetime.timedelta(days=days_ahead)).isoformat()
        
        self.db.execute(
            "UPDATE mistake_book SET mastery_score = ?, status = ?, next_review = ? WHERE id = ?",
            (mastery, status, next_review, mistake_id)
        )
        updated = dict(row)
        updated["mastery_score"] = mastery
        updated["status"] = status
        updated["next_review"] = next_review
        return updated

    def get_mistakes(self, learner_id: str, skill: Optional[str] = None, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        query = "SELECT * FROM mistake_book WHERE learner_id = ?"
        params: List[Any] = [learner_id]
        if skill:
            query += " AND skill = ?"
            params.append(skill)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY recurrence_count DESC, last_seen DESC LIMIT ?"
        params.append(limit)
        rows = self.db.fetchall(query, tuple(params))
        return [dict(r) for r in rows]

    get_mistakes_by_learner = get_mistakes

    def get_summary(self, learner_id: str) -> Dict[str, Any]:
        """Returns error frequency breakdowns by skill and category."""
        rows = self.db.fetchall(
            """SELECT skill, category, COUNT(*) as total_mistakes, SUM(recurrence_count) as total_occurrences,
                      SUM(CASE WHEN status = 'mastered' THEN 1 ELSE 0 END) as mastered_count
               FROM mistake_book
               WHERE learner_id = ?
               GROUP BY skill, category
               ORDER BY total_occurrences DESC""",
            (learner_id,)
        )
        return {
            "learner_id": learner_id,
            "categories": [dict(r) for r in rows]
        }


class SRSRepository:
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def add_or_get_item(
        self,
        learner_id: str,
        item_type: str,
        key_term: str,
        prompt: str,
        answer: str,
        notes: str = ""
    ) -> Dict[str, Any]:
        LearnerRepository(self.db).get_or_create_default(learner_id)
        existing = self.db.fetchone(
            "SELECT * FROM srs_items WHERE learner_id = ? AND item_type = ? AND key_term = ?",
            (learner_id, item_type, key_term)
        )
        if existing:
            return dict(existing)
        item_id = str(uuid.uuid4())
        now = _now_iso()
        self.db.execute(
            """INSERT INTO srs_items 
               (id, learner_id, item_type, key_term, prompt, answer, notes, repetition, interval_days, ease_factor, due_date, review_history)
               VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1.0, 2.5, ?, '[]')""",
            (item_id, learner_id, item_type, key_term, prompt, answer, notes, now)
        )
        return self.get_item(item_id)

    def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM srs_items WHERE id = ?", (item_id,))
        return dict(row) if row else None

    def get_due_items(self, learner_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        now = _now_iso()
        rows = self.db.fetchall(
            "SELECT * FROM srs_items WHERE learner_id = ? AND due_date <= ? ORDER BY due_date ASC LIMIT ?",
            (learner_id, now, limit)
        )
        return [dict(r) for r in rows]

    def record_review(self, item_id: str, grade: int) -> Dict[str, Any]:
        """
        Applies SM-2 algorithm:
        grade: 0-5 (0=blackout, 3=pass with effort, 5=perfect recall)
        """
        row = self.get_item(item_id)
        if not row:
            raise ValueError(f"SRS Item {item_id} not found")
        repetition = row["repetition"]
        interval = row["interval_days"]
        ef = row["ease_factor"]
        now = _now_dt()

        if grade >= 3:
            if repetition == 0:
                interval = 1.0
            elif repetition == 1:
                interval = 6.0
            else:
                interval = round(interval * ef, 1)
            repetition += 1
        else:
            repetition = 0
            interval = 1.0

        ef = ef + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
        if ef < 1.3:
            ef = 1.3

        due_date = (now + datetime.timedelta(days=interval)).isoformat()
        
        history = json.loads(row["review_history"] or "[]")
        history.append({
            "reviewed_at": now.isoformat(),
            "grade": grade,
            "interval": interval,
            "ef": ef
        })

        self.db.execute(
            """UPDATE srs_items 
               SET repetition = ?, interval_days = ?, ease_factor = ?, due_date = ?, review_history = ?
               WHERE id = ?""",
            (repetition, interval, ef, due_date, json.dumps(history[-20:]), item_id)
        )
        return self.get_item(item_id)


class KnowledgeRepository:
    """Stores permanent curated and online-distilled compact knowledge."""
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def upsert_knowledge(
        self,
        topic: str,
        query_trigger: str,
        compact_knowledge: str,
        subtopic: Optional[str] = None,
        source: str = "curated",
        confidence: float = 0.95,
        version: str = "1.0.0"
    ) -> Dict[str, Any]:
        now = _now_iso()
        existing = self.db.fetchone(
            "SELECT * FROM knowledge_base WHERE topic = ? AND query_trigger = ?",
            (topic, query_trigger)
        )
        if existing:
            self.db.execute(
                """UPDATE knowledge_base 
                   SET subtopic = ?, compact_knowledge = ?, source = ?, confidence = ?, version = ?, updated_at = ?
                   WHERE id = ?""",
                (subtopic, compact_knowledge, source, confidence, version, now, existing["id"])
            )
            item = dict(existing)
            item["compact_knowledge"] = compact_knowledge
            item["confidence"] = confidence
            return item
        else:
            item_id = str(uuid.uuid4())
            self.db.execute(
                """INSERT INTO knowledge_base 
                   (id, topic, subtopic, query_trigger, compact_knowledge, source, confidence, version, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (item_id, topic, subtopic, query_trigger, compact_knowledge, source, confidence, version, now, now)
            )
            return {
                "id": item_id,
                "topic": topic,
                "subtopic": subtopic,
                "query_trigger": query_trigger,
                "compact_knowledge": compact_knowledge,
                "source": source,
                "confidence": confidence,
                "version": version
            }

    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            """SELECT * FROM knowledge_base 
               WHERE query_trigger LIKE ? OR topic LIKE ? OR compact_knowledge LIKE ?
               ORDER BY confidence DESC LIMIT ?""",
            (f"%{query}%", f"%{query}%", f"%{query}%", limit)
        )
        return [dict(r) for r in rows]

    search_by_trigger = search_knowledge

    def get_all(self, limit: int = 1000) -> List[Dict[str, Any]]:
        rows = self.db.fetchall("SELECT * FROM knowledge_base ORDER BY created_at ASC LIMIT ?", (limit,))
        return [dict(r) for r in rows]


class TestResultRepository:
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def record_result(
        self,
        learner_id: str,
        test_type: str = "practice",
        track: str = "Academic",
        overall_band: float = 6.0,
        listening_band: Optional[float] = None,
        reading_band: Optional[float] = None,
        writing_band: Optional[float] = None,
        speaking_band: Optional[float] = None,
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        LearnerRepository(self.db).get_or_create_default(learner_id)
        item_id = str(uuid.uuid4())
        now = _now_iso()
        details_json = json.dumps(details or {})
        self.db.execute(
            """INSERT INTO test_results 
               (id, learner_id, test_type, track, overall_band, listening_band, reading_band, writing_band, speaking_band, details_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (item_id, learner_id, test_type, track, overall_band, listening_band, reading_band, writing_band, speaking_band, details_json, now)
        )
        return {
            "id": item_id,
            "learner_id": learner_id,
            "test_type": test_type,
            "track": track,
            "overall_band": overall_band,
            "listening_band": listening_band,
            "reading_band": reading_band,
            "writing_band": writing_band,
            "speaking_band": speaking_band,
            "created_at": now
        }

    def get_history(self, learner_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            "SELECT * FROM test_results WHERE learner_id = ? ORDER BY created_at DESC LIMIT ?",
            (learner_id, limit)
        )
        results = []
        for r in rows:
            d = dict(r)
            d["details"] = json.loads(d.get("details_json") or "{}")
            results.append(d)
        return results

    get_recent_tests = get_history


class SettingsRepository:
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        row = self.db.fetchone("SELECT value FROM system_settings WHERE key = ?", (key,))
        return row["value"] if row else default

    def set(self, key: str, value: str):
        now = _now_iso()
        self.db.execute(
            """INSERT INTO system_settings (key, value, updated_at)
               VALUES (?, ?, ?)
               ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at""",
            (key, value, now)
        )

    def get_all(self) -> Dict[str, str]:
        rows = self.db.fetchall("SELECT key, value FROM system_settings")
        return {r["key"]: r["value"] for r in rows}


# -------------------------------------------------------------
# Phase 1 Extended Repositories
# -------------------------------------------------------------

class CurriculumRepository:
    """Manages structured CEFR A1-C2 English Learning Academy lessons and progress."""
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def upsert_lesson(
        self,
        lesson_id: str,
        cefr_level: str,
        module_type: str,
        title: str,
        order_index: int,
        objectives: List[str],
        explanation_markdown: str,
        examples: List[Dict[str, Any]],
        guided_exercises: List[Dict[str, Any]],
        interactive_practice: List[Dict[str, Any]],
        assessment: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        self.db.execute(
            """INSERT INTO curriculum_lessons 
               (id, cefr_level, module_type, title, order_index, objectives_json, explanation_markdown, examples_json, guided_exercises_json, interactive_practice_json, assessment_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                   cefr_level = excluded.cefr_level,
                   module_type = excluded.module_type,
                   title = excluded.title,
                   order_index = excluded.order_index,
                   objectives_json = excluded.objectives_json,
                   explanation_markdown = excluded.explanation_markdown,
                   examples_json = excluded.examples_json,
                   guided_exercises_json = excluded.guided_exercises_json,
                   interactive_practice_json = excluded.interactive_practice_json,
                   assessment_json = excluded.assessment_json""",
            (
                lesson_id, cefr_level.upper(), module_type.lower(), title, order_index,
                json.dumps(objectives), explanation_markdown, json.dumps(examples),
                json.dumps(guided_exercises), json.dumps(interactive_practice), json.dumps(assessment)
            )
        )
        return self.get_lesson(lesson_id)

    def get_lesson(self, lesson_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM curriculum_lessons WHERE id = ?", (lesson_id,))
        if not row:
            return None
        d = dict(row)
        d["objectives"] = json.loads(d.get("objectives_json") or "[]")
        d["examples"] = json.loads(d.get("examples_json") or "[]")
        d["guided_exercises"] = json.loads(d.get("guided_exercises_json") or "[]")
        d["interactive_practice"] = json.loads(d.get("interactive_practice_json") or "[]")
        d["assessment"] = json.loads(d.get("assessment_json") or "[]")
        return d

    def list_lessons(self, cefr_level: Optional[str] = None, module_type: Optional[str] = None) -> List[Dict[str, Any]]:
        query = "SELECT id, cefr_level, module_type, title, order_index FROM curriculum_lessons WHERE 1=1"
        params = []
        if cefr_level:
            query += " AND cefr_level = ?"
            params.append(cefr_level.upper())
        if module_type:
            query += " AND module_type = ?"
            params.append(module_type.lower())
        query += " ORDER BY cefr_level ASC, order_index ASC"
        rows = self.db.fetchall(query, tuple(params))
        return [dict(r) for r in rows]

    def record_progress(self, learner_id: str, lesson_id: str, score: float, status: str = "completed") -> Dict[str, Any]:
        LearnerRepository(self.db).get_or_create_default(learner_id)
        row = self.db.fetchone(
            "SELECT * FROM lesson_progress WHERE learner_id = ? AND lesson_id = ?",
            (learner_id, lesson_id)
        )
        now = _now_iso()
        if row:
            attempts = row["attempts"] + 1
            highest_score = max(row["score"], score)
            self.db.execute(
                """UPDATE lesson_progress 
                   SET status = ?, score = ?, attempts = ?, completed_at = ?
                   WHERE id = ?""",
                (status, highest_score, attempts, now, row["id"])
            )
            item = dict(row)
            item["status"] = status
            item["score"] = highest_score
            item["attempts"] = attempts
            return item
        else:
            prog_id = str(uuid.uuid4())
            self.db.execute(
                """INSERT INTO lesson_progress (id, learner_id, lesson_id, status, score, attempts, completed_at)
                   VALUES (?, ?, ?, ?, ?, 1, ?)""",
                (prog_id, learner_id, lesson_id, status, score, now)
            )
            return {
                "id": prog_id,
                "learner_id": learner_id,
                "lesson_id": lesson_id,
                "status": status,
                "score": score,
                "attempts": 1,
                "completed_at": now
            }

    def get_progress(self, learner_id: str, lesson_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone(
            "SELECT * FROM lesson_progress WHERE learner_id = ? AND lesson_id = ?",
            (learner_id, lesson_id)
        )
        return dict(row) if row else None

    def get_learner_progress(self, learner_id: str) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            """SELECT p.*, l.title, l.cefr_level, l.module_type 
               FROM lesson_progress p
               JOIN curriculum_lessons l ON p.lesson_id = l.id
               WHERE p.learner_id = ?
               ORDER BY p.completed_at DESC""",
            (learner_id,)
        )
        return [dict(r) for r in rows]


class VocabularyVaultRepository:
    """Manages the rich lexical dictionary and word family database."""
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def upsert_word(
        self,
        word: str,
        pos: str,
        cefr_level: str,
        band_tier: str,
        simple_definition: str,
        advanced_definition: str,
        example_sentences: List[str],
        synonyms: List[str],
        antonyms: List[str],
        word_family: Dict[str, str],
        collocations: List[str],
        common_mistakes: List[str],
        pronunciation: Optional[str] = None,
        ipa: Optional[str] = None,
        academic_usage: Optional[str] = None
    ) -> Dict[str, Any]:
        item_id = str(uuid.uuid4())
        w_clean = word.strip().lower()
        self.db.execute(
            """INSERT INTO vocabulary_vault 
               (id, word, pos, pronunciation, ipa, cefr_level, band_tier, simple_definition, advanced_definition, example_sentences_json, synonyms_json, antonyms_json, word_family_json, collocations_json, common_mistakes_json, academic_usage)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(word) DO UPDATE SET
                   pos = excluded.pos,
                   pronunciation = excluded.pronunciation,
                   ipa = excluded.ipa,
                   cefr_level = excluded.cefr_level,
                   band_tier = excluded.band_tier,
                   simple_definition = excluded.simple_definition,
                   advanced_definition = excluded.advanced_definition,
                   example_sentences_json = excluded.example_sentences_json,
                   synonyms_json = excluded.synonyms_json,
                   antonyms_json = excluded.antonyms_json,
                   word_family_json = excluded.word_family_json,
                   collocations_json = excluded.collocations_json,
                   common_mistakes_json = excluded.common_mistakes_json,
                   academic_usage = excluded.academic_usage""",
            (
                item_id, w_clean, pos, pronunciation, ipa, cefr_level.upper(), band_tier,
                simple_definition, advanced_definition, json.dumps(example_sentences),
                json.dumps(synonyms), json.dumps(antonyms), json.dumps(word_family),
                json.dumps(collocations), json.dumps(common_mistakes), academic_usage
            )
        )
        return self.get_word(w_clean)

    def get_word(self, word: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM vocabulary_vault WHERE word = ?", (word.strip().lower(),))
        if not row:
            return None
        d = dict(row)
        d["example_sentences"] = json.loads(d.get("example_sentences_json") or "[]")
        d["synonyms"] = json.loads(d.get("synonyms_json") or "[]")
        d["antonyms"] = json.loads(d.get("antonyms_json") or "[]")
        d["word_family"] = json.loads(d.get("word_family_json") or "{}")
        d["collocations"] = json.loads(d.get("collocations_json") or "[]")
        d["common_mistakes"] = json.loads(d.get("common_mistakes_json") or "[]")
        return d

    def search_words(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            """SELECT * FROM vocabulary_vault 
               WHERE word LIKE ? OR simple_definition LIKE ? OR advanced_definition LIKE ? 
                  OR synonyms_json LIKE ? OR collocations_json LIKE ? OR example_sentences_json LIKE ? OR academic_usage LIKE ?
               ORDER BY word ASC LIMIT ?""",
            (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", limit)
        )
        results = []
        for r in rows:
            d = dict(r)
            d["example_sentences"] = json.loads(d.get("example_sentences_json") or "[]")
            d["collocations"] = json.loads(d.get("collocations_json") or "[]")
            results.append(d)
        return results


    def get_by_cefr(self, cefr_level: str, limit: int = 50) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            "SELECT * FROM vocabulary_vault WHERE cefr_level = ? ORDER BY word ASC LIMIT ?",
            (cefr_level.upper(), limit)
        )
        return [dict(r) for r in rows]


class ExamSessionRepository:
    """Manages active and historical examination sessions (Reading, Listening, Writing, Speaking)."""
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def start_session(self, learner_id: str, module: str, track: str, time_limit_seconds: int) -> Dict[str, Any]:
        LearnerRepository(self.db).get_or_create_default(learner_id)
        session_id = f"exam_{uuid.uuid4().hex[:12]}"
        now = _now_iso()
        self.db.execute(
            """INSERT INTO exam_sessions 
               (id, learner_id, module, track, status, time_limit_seconds, time_spent_seconds, answers_json, results_json, started_at)
               VALUES (?, ?, ?, ?, 'in_progress', ?, 0, '{}', '{}', ?)""",
            (session_id, learner_id, module, track, time_limit_seconds, now)
        )
        return self.get_session(session_id)

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone("SELECT * FROM exam_sessions WHERE id = ?", (session_id,))
        if not row:
            return None
        d = dict(row)
        d["answers"] = json.loads(d.get("answers_json") or "{}")
        d["results"] = json.loads(d.get("results_json") or "{}")
        return d

    def update_answers(self, session_id: str, answers: Dict[str, Any], time_spent_seconds: int) -> Dict[str, Any]:
        self.db.execute(
            "UPDATE exam_sessions SET answers_json = ?, time_spent_seconds = ? WHERE id = ?",
            (json.dumps(answers), time_spent_seconds, session_id)
        )
        return self.get_session(session_id)

    def complete_session(self, session_id: str, results: Dict[str, Any], band_score: float) -> Dict[str, Any]:
        now = _now_iso()
        self.db.execute(
            """UPDATE exam_sessions 
               SET status = 'submitted', results_json = ?, band_score = ?, completed_at = ?
               WHERE id = ?""",
            (json.dumps(results), band_score, now, session_id)
        )
        return self.get_session(session_id)

    def list_learner_sessions(self, learner_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            "SELECT * FROM exam_sessions WHERE learner_id = ? ORDER BY started_at DESC LIMIT ?",
            (learner_id, limit)
        )
        results = []
        for r in rows:
            d = dict(r)
            d["answers"] = json.loads(d.get("answers_json") or "{}")
            d["results"] = json.loads(d.get("results_json") or "{}")
            results.append(d)
        return results

    def get_active_session(self, learner_id: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetchone(
            "SELECT * FROM exam_sessions WHERE learner_id = ? AND status = 'in_progress' ORDER BY started_at DESC LIMIT 1",
            (learner_id,)
        )
        if not row:
            return None
        d = dict(row)
        d["answers"] = json.loads(d.get("answers_json") or "{}")
        d["results"] = json.loads(d.get("results_json") or "{}")
        return d

    def abandon_session(self, session_id: str) -> bool:
        now = _now_iso()
        self.db.execute(
            "UPDATE exam_sessions SET status = 'abandoned', completed_at = ? WHERE id = ?",
            (now, session_id)
        )
        return True



class WritingDraftRepository:
    """Manages student essay drafts, autosaves, and criterion evaluations."""
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def save_draft(
        self,
        learner_id: str,
        prompt_id: str,
        task_type: str,
        track: str,
        draft_text: str,
        word_count: int,
        draft_id: Optional[str] = None
    ) -> Dict[str, Any]:
        LearnerRepository(self.db).get_or_create_default(learner_id)
        now = _now_iso()
        if draft_id:
            self.db.execute(
                """UPDATE writing_drafts 
                   SET draft_text = ?, word_count = ?, updated_at = ?
                   WHERE id = ?""",
                (draft_text, word_count, now, draft_id)
            )
            item_id = draft_id
        else:
            item_id = str(uuid.uuid4())
            self.db.execute(
                """INSERT INTO writing_drafts 
                   (id, learner_id, prompt_id, task_type, track, draft_text, word_count, status, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?)""",
                (item_id, learner_id, prompt_id, task_type, track, draft_text, word_count, now, now)
            )
        row = self.db.fetchone("SELECT * FROM writing_drafts WHERE id = ?", (item_id,))
        return dict(row)

    def record_evaluation(
        self,
        draft_id: str,
        ta_score: float,
        cc_score: float,
        lr_score: float,
        gra_score: float,
        overall_band: float,
        feedback: Dict[str, Any]
    ) -> Dict[str, Any]:
        now = _now_iso()
        self.db.execute(
            """UPDATE writing_drafts 
               SET status = 'evaluated', ta_score = ?, cc_score = ?, lr_score = ?, gra_score = ?, 
                   overall_band = ?, feedback_json = ?, updated_at = ?
               WHERE id = ?""",
            (ta_score, cc_score, lr_score, gra_score, overall_band, json.dumps(feedback), now, draft_id)
        )
        row = self.db.fetchone("SELECT * FROM writing_drafts WHERE id = ?", (draft_id,))
        d = dict(row)
        d["feedback"] = json.loads(d.get("feedback_json") or "{}")
        return d

    def get_learner_drafts(self, learner_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            "SELECT * FROM writing_drafts WHERE learner_id = ? ORDER BY updated_at DESC LIMIT ?",
            (learner_id, limit)
        )
        results = []
        for r in rows:
            d = dict(r)
            if d.get("feedback_json"):
                d["feedback"] = json.loads(d["feedback_json"])
            results.append(d)
        return results


class AIConversationRepository:
    """Stores multi-turn learner-tutor dialogues for contextual educational continuity."""
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def add_message(
        self,
        learner_id: str,
        role: str,
        message: str,
        detected_errors: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        LearnerRepository(self.db).get_or_create_default(learner_id)
        msg_id = str(uuid.uuid4())
        now = _now_iso()
        errors_json = json.dumps(detected_errors or [])
        meta_json = json.dumps(metadata or {})
        self.db.execute(
            """INSERT INTO ai_conversations (id, learner_id, role, message, detected_errors_json, metadata_json, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (msg_id, learner_id, role, message, errors_json, meta_json, now)
        )
        return {
            "id": msg_id,
            "learner_id": learner_id,
            "role": role,
            "message": message,
            "detected_errors": detected_errors or [],
            "metadata": metadata or {},
            "created_at": now
        }

    def get_conversation_history(self, learner_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        rows = self.db.fetchall(
            """SELECT * FROM ai_conversations 
               WHERE learner_id = ? 
               ORDER BY created_at ASC LIMIT ?""",
            (learner_id, limit)
        )
        results = []
        for r in rows:
            d = dict(r)
            d["detected_errors"] = json.loads(d.get("detected_errors_json") or "[]")
            d["metadata"] = json.loads(d.get("metadata_json") or "{}")
            results.append(d)
        return results

    def clear_history(self, learner_id: str):
        self.db.execute("DELETE FROM ai_conversations WHERE learner_id = ?", (learner_id,))
