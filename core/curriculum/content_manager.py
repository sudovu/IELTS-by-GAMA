"""
content_manager.py
Modular content management system for IELTS by GAMA.
Loads, validates, indexes, and queries structured curriculum and vocabulary content
from JSON repositories in content/ with offline fallback.
"""

import os
import json
from typing import Dict, Any, List, Optional
from ..database.db_manager import DatabaseManager
from ..database.repositories import CurriculumRepository, VocabularyVaultRepository


class ContentManager:
    """Manages external JSON content repositories with robust caching and database integration."""

    _cached_curriculum: Optional[List[Dict[str, Any]]] = None
    _cached_vocab_themes: Optional[Dict[str, List[Dict[str, Any]]]] = None

    @classmethod
    def get_content_dir(cls) -> str:
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base, "content")

    @classmethod
    def load_curriculum_lessons(cls, force_reload: bool = False) -> List[Dict[str, Any]]:
        """Loads all curriculum lessons across CEFR levels from content/curriculum/."""
        if cls._cached_curriculum is not None and not force_reload:
            return cls._cached_curriculum

        curriculum_dir = os.path.join(cls.get_content_dir(), "curriculum")
        lessons = []

        if os.path.exists(curriculum_dir):
            for level in ["a1", "a2", "b1", "b2", "c1", "c2"]:
                fpath = os.path.join(curriculum_dir, f"{level}.json")
                if os.path.exists(fpath):
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                lessons.extend(data)
                    except Exception as e:
                        print(f"[ContentManager] Error loading {fpath}: {e}")

        # If no lessons loaded from filesystem, import the starter lessons as fallback
        if not lessons:
            from .curriculum_engine import STARTER_LESSONS
            lessons = list(STARTER_LESSONS)

        # Sort by level and order_index
        level_order = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}
        lessons.sort(key=lambda x: (level_order.get(x.get("cefr_level", "A1").upper(), 99), x.get("order_index", 0)))

        cls._cached_curriculum = lessons
        return lessons

    @classmethod
    def get_lesson_by_id(cls, lesson_id: str) -> Optional[Dict[str, Any]]:
        """Finds a specific lesson by unique identifier."""
        lessons = cls.load_curriculum_lessons()
        for l in lessons:
            if l.get("id") == lesson_id:
                return l
        return None

    @classmethod
    def filter_lessons(
        cls,
        cefr_level: Optional[str] = None,
        module_type: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Filters curriculum lessons by CEFR level, module type, and keyword search."""
        lessons = cls.load_curriculum_lessons()
        results = []

        for l in lessons:
            if cefr_level and l.get("cefr_level", "").upper() != cefr_level.upper():
                continue
            if module_type and l.get("module_type", "").lower() != module_type.lower():
                continue
            if search_query:
                q = search_query.lower()
                text_to_search = (
                    l.get("title", "") + " " +
                    " ".join(l.get("objectives", [])) + " " +
                    l.get("explanation_markdown", "")
                ).lower()
                if q not in text_to_search:
                    continue
            results.append(l)

        return results

    @classmethod
    def get_curriculum_map(cls) -> Dict[str, Any]:
        """Constructs a comprehensive curriculum map across all levels and modules."""
        lessons = cls.load_curriculum_lessons()
        levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
        level_map = {lvl: {} for lvl in levels}

        for l in lessons:
            lvl = l.get("cefr_level", "A1").upper()
            mod = l.get("module_type", "grammar").lower()
            if lvl not in level_map:
                level_map[lvl] = {}
            if mod not in level_map[lvl]:
                level_map[lvl][mod] = []

            level_map[lvl][mod].append({
                "id": l.get("id"),
                "title": l.get("title"),
                "order_index": l.get("order_index"),
                "prerequisites": l.get("prerequisites", []),
                "estimated_minutes": l.get("estimated_minutes", 25),
                "objectives_count": len(l.get("objectives", [])),
                "has_guided_exercises": len(l.get("guided_exercises", [])) > 0,
                "has_interactive_practice": len(l.get("interactive_practice", [])) > 0,
                "assessment_question_count": len(l.get("assessment", [])),
                "completion_threshold": "60% for completion, 80% for mastery"
            })

        return {
            "total_levels": len(levels),
            "total_lessons": len(lessons),
            "levels": level_map,
            "pedagogical_modules": [
                "grammar", "vocabulary", "reading", "listening",
                "writing", "speaking", "pronunciation", "functional", "review"
            ]
        }

    # -------------------------------------------------------------------------
    # THEMED VOCABULARY MANAGEMENT
    # -------------------------------------------------------------------------
    @classmethod
    def load_vocabulary_themes(cls, force_reload: bool = False) -> Dict[str, List[Dict[str, Any]]]:
        """Loads all themed vocabulary collections from content/vocabulary/themes.json."""
        if cls._cached_vocab_themes is not None and not force_reload:
            return cls._cached_vocab_themes

        themes_path = os.path.join(cls.get_content_dir(), "vocabulary", "themes.json")
        data = {}

        if os.path.exists(themes_path):
            try:
                with open(themes_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"[ContentManager] Error loading {themes_path}: {e}")

        cls._cached_vocab_themes = data
        return data

    @classmethod
    def list_vocabulary_themes(cls) -> List[Dict[str, Any]]:
        """Returns metadata list of all available vocabulary themes and word counts."""
        themes = cls.load_vocabulary_themes()
        result = []
        for theme_key, words in themes.items():
            result.append({
                "theme_id": theme_key,
                "title": theme_key.replace("_", " ").title(),
                "word_count": len(words),
                "cefr_levels": sorted(list({w.get("cefr_level", "B1") for w in words}))
            })
        return result

    @classmethod
    def get_theme_words(cls, theme_id: str) -> List[Dict[str, Any]]:
        """Retrieves words belonging to a specific theme."""
        themes = cls.load_vocabulary_themes()
        return themes.get(theme_id, [])

    @classmethod
    def search_all_vocabulary(
        cls,
        query: Optional[str] = None,
        cefr_level: Optional[str] = None,
        theme_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Searches across all vocabulary themes."""
        themes = cls.load_vocabulary_themes()
        results = []

        for tid, words in themes.items():
            if theme_id and tid != theme_id:
                continue
            for w in words:
                if cefr_level and w.get("cefr_level", "").upper() != cefr_level.upper():
                    continue
                if query:
                    q = query.lower()
                    haystack = (
                        w.get("word", "") + " " +
                        w.get("definition", "") + " " +
                        " ".join(w.get("synonyms", [])) + " " +
                        " ".join(w.get("collocations", []))
                    ).lower()
                    if q not in haystack:
                        continue
                item = dict(w)
                item["theme"] = tid
                results.append(item)

        return results

    # -------------------------------------------------------------------------
    # DATABASE SEEDING
    # -------------------------------------------------------------------------
    @classmethod
    def seed_database_curriculum(cls, db: DatabaseManager) -> int:
        """Seeds or updates curriculum_lessons in SQLite from structured JSON content."""
        repo = CurriculumRepository(db)
        lessons = cls.load_curriculum_lessons()
        count = 0

        for l in lessons:
            repo.upsert_lesson(
                lesson_id=l["id"],
                cefr_level=l.get("cefr_level", "A1"),
                module_type=l.get("module_type", "grammar"),
                title=l.get("title", ""),
                order_index=l.get("order_index", 1),
                objectives=l.get("objectives", []),
                explanation_markdown=l.get("explanation_markdown", ""),
                examples=l.get("examples", []),
                guided_exercises=l.get("guided_exercises", []),
                interactive_practice=l.get("interactive_practice", []),
                assessment=l.get("assessment", [])
            )
            count += 1

        return count

    @classmethod
    def seed_database_vocabulary(cls, db: DatabaseManager) -> int:
        """Seeds vocabulary_vault in SQLite from structured JSON themes."""
        repo = VocabularyVaultRepository(db)
        themes = cls.load_vocabulary_themes()
        count = 0

        for theme_id, words in themes.items():
            for w in words:
                repo.upsert_word(
                    word=w["word"],
                    pos=w.get("pos", "noun"),
                    cefr_level=w.get("cefr_level", "B1"),
                    band_tier=w.get("band_tier", "Band 6.0-7.0"),
                    pronunciation=w.get("pronunciation", ""),
                    ipa=w.get("ipa", ""),
                    simple_definition=w.get("simple_definition", w.get("definition", "")),
                    advanced_definition=w.get("advanced_definition", w.get("definition", "")),
                    example_sentences=w.get("example_sentences", [w.get("contextual_example", "")]),
                    synonyms=w.get("synonyms", []),
                    antonyms=w.get("antonyms", []),
                    word_family=w.get("word_family", {}),
                    collocations=w.get("collocations", []),
                    common_mistakes=w.get("common_mistakes", []),
                    academic_usage=w.get("ielts_usefulness", "")
                )
                count += 1

        return count
