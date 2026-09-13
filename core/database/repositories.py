"""
Repositories for IELTS by GAMA.
Encapsulates CRUD operations on SQLite for learners, mistakes, SRS, knowledge, and tests.
"""

import json
import uuid
import datetime
from typing import Optional, List, Dict, Any
from .db_manager import DatabaseManager


class LearnerRepository:
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def get_or_create_default(self, learner_id: str = "default_learner", name: str = "Learner") -> Dict[str, Any]:
        row = self.db.fetchone("SELECT * FROM learners WHERE id = ?", (learner_id,))
        if row:
            return dict(row)
        now = datetime.datetime.utcnow().isoformat()
        self.db.execute(
            """INSERT INTO learners (id, name, target_band, current_band, cefr_level, track, daily_minutes, created_at, updated_at)
               VALUES (?, ?, 7.0, 5.5, 'B2', 'Academic', 30, ?, ?)""",
            (learner_id, name, now, now)
        )
        return self.get_or_create_default(learner_id, name)

    def update_profile(self, learner_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        fields = []
        params = []
        for k, v in updates.items():
            if k in ["name", "target_band", "current_band", "cefr_level", "track", "daily_minutes"]:
                fields.append(f"{k} = ?")
                params.append(v)
        if not fields:
            return self.get_or_create_default(learner_id)
        params.append(datetime.datetime.utcnow().isoformat())
        params.append(learner_id)
        sql = f"UPDATE learners SET {', '.join(fields)}, updated_at = ? WHERE id = ?"
        self.db.execute(sql, tuple(params))
        return self.get_or_create_default(learner_id)


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
        now = datetime.datetime.utcnow().isoformat()
        existing = self.db.fetchone(
            """SELECT * FROM mistake_book 
               WHERE learner_id = ? AND skill = ? AND category = ? AND original_text = ?""",
            (learner_id, skill, category, original_text)
        )
        if existing:
            new_count = existing["recurrence_count"] + 1
            # Recurrence pushes next review closer and drops mastery score slightly
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
        now = datetime.datetime.utcnow()
        if success:
            mastery = min(1.0, mastery + 0.34)
        else:
            mastery = max(0.0, mastery - 0.25)
        
        status = "mastered" if mastery >= 0.95 else ("reviewing" if mastery >= 0.5 else "needs_improvement")
        # Compute next review date using light interval
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

    def get_summary(self, learner_id: str) -> Dict[str, Any]:
        rows = self.db.fetchall(
            """SELECT skill, category, COUNT(*) as total, SUM(recurrence_count) as total_occurrences,
                      AVG(mastery_score) as avg_mastery,
                      SUM(CASE WHEN status = 'mastered' THEN 1 ELSE 0 END) as mastered_count
               FROM mistake_book 
               WHERE learner_id = ?
               GROUP BY skill, category
               ORDER BY total_occurrences DESC""",
            (learner_id,)
        )
        return {"categories": [dict(r) for r in rows]}


class SRSRepository:
    """SuperMemo SM-2 Spaced Repetition repository."""
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
        now = datetime.datetime.utcnow().isoformat()
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
        now = datetime.datetime.utcnow().isoformat()
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
        now = datetime.datetime.utcnow()

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
        now = datetime.datetime.utcnow().isoformat()
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
        # Fast SQL LIKE search; local RAG enhances this with semantic ranker
        param = f"%{query.strip()}%"
        rows = self.db.fetchall(
            """SELECT * FROM knowledge_base 
               WHERE query_trigger LIKE ? OR topic LIKE ? OR subtopic LIKE ? OR compact_knowledge LIKE ?
               ORDER BY confidence DESC LIMIT ?""",
            (param, param, param, param, limit)
        )
        return [dict(r) for r in rows]

    def get_all(self, limit: int = 1000) -> List[Dict[str, Any]]:
        rows = self.db.fetchall("SELECT * FROM knowledge_base ORDER BY topic, subtopic LIMIT ?", (limit,))
        return [dict(r) for r in rows]


class TestResultRepository:
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def record_test(
        self,
        learner_id: str,
        test_type: str,
        track: str,
        overall_band: float,
        listening_band: Optional[float] = None,
        reading_band: Optional[float] = None,
        writing_band: Optional[float] = None,
        speaking_band: Optional[float] = None,
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        LearnerRepository(self.db).get_or_create_default(learner_id)
        item_id = str(uuid.uuid4())
        now = datetime.datetime.utcnow().isoformat()
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


class SettingsRepository:
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        row = self.db.fetchone("SELECT value FROM system_settings WHERE key = ?", (key,))
        return row["value"] if row else default

    def set(self, key: str, value: str):
        now = datetime.datetime.utcnow().isoformat()
        self.db.execute(
            """INSERT INTO system_settings (key, value, updated_at)
               VALUES (?, ?, ?)
               ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at""",
            (key, value, now)
        )

    def get_all(self) -> Dict[str, str]:
        rows = self.db.fetchall("SELECT key, value FROM system_settings")
        return {r["key"]: r["value"] for r in rows}
