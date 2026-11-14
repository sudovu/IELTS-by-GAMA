"""
Phase 14 Baseline Audit Script
Inspects:
- Reading engine, passages, question types, grading methods
- Listening engine, sections, audio assets, script concealment
- Writing evaluator, prompts, task types, criteria evaluation
- Speaking examiner, exam sets, parts 1-3, recording/STT status
- Database schema, exam_sessions table, repositories
- Server API routes and examination endpoints
- Frontend index.html and app.js exam modes
- Audio file availability on disk
"""

import os
import sys
import json
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.reading.reading_engine import ReadingEngine
from core.listening.listening_engine import ListeningEngine
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.database.db_manager import DatabaseManager
from core.database.migrations import MigrationManager
from core.database.repositories import ExamSessionRepository, TestResultRepository

def audit():
    report = {}

    # 1. Reading
    reading_passages = ReadingEngine.ORIGINAL_PASSAGES
    report["reading"] = {
        "passage_count": len(reading_passages),
        "passages": {}
    }
    for pid, p in reading_passages.items():
        qtypes = set(q.get("type", "unknown") for q in p.get("questions", []))
        report["reading"]["passages"][pid] = {
            "title": p.get("title"),
            "track": p.get("track"),
            "question_count": len(p.get("questions", [])),
            "question_types": sorted(list(qtypes))
        }

    # 2. Listening
    listening_sections = ListeningEngine.SECTIONS
    report["listening"] = {
        "section_count": len(listening_sections),
        "sections": {}
    }
    for sid, s in listening_sections.items():
        qtypes = set(q.get("type", "unknown") if isinstance(q, dict) else "unknown" for q in s.get("questions", []))
        report["listening"]["sections"][sid] = {
            "title": s.get("title"),
            "section_number": s.get("section_number"),
            "question_count": len(s.get("questions", [])),
            "has_audio_script": bool(s.get("audio_script"))
        }

    # 3. Audio Assets on Disk
    audio_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith(('.mp3', '.wav', '.ogg', '.m4a', '.aac')):
                audio_files.append(os.path.join(root, f))
    report["audio_files_on_disk"] = audio_files

    # 4. Writing
    writing_prompts = WritingEvaluator.ORIGINAL_PROMPTS
    report["writing"] = {
        "prompt_count": len(writing_prompts),
        "prompts": {}
    }
    for pr_id, pr in writing_prompts.items():
        report["writing"]["prompts"][pr_id] = {
            "title": pr.get("title"),
            "task_type": pr.get("task_type"),
            "track": pr.get("track"),
            "question_type": pr.get("question_type")
        }

    # 5. Speaking
    speaking_sets = SpeakingExaminer.EXAM_SETS
    report["speaking"] = {
        "exam_set_count": len(speaking_sets),
        "sets": []
    }
    for s in speaking_sets:
        report["speaking"]["sets"].append({
            "id": s.get("id"),
            "topic": s.get("topic"),
            "part_1_questions": len(s.get("part_1", [])),
            "has_part_2": bool(s.get("part_2")),
            "part_3_questions": len(s.get("part_3", []))
        })

    # 6. Database Exam Tables
    db = DatabaseManager()
    db.init_schema()
    mig = MigrationManager(db)
    mig.run_migrations()

    with db.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in cursor.fetchall()]
        report["database_tables"] = sorted(tables)

        cursor.execute("PRAGMA table_info(exam_sessions);")
        report["exam_sessions_columns"] = [r[1] for r in cursor.fetchall()]

    # 7. Frontend Panes
    with open('ui/static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    import re
    panes = re.findall(r'id=["\']tab-([a-zA-Z0-9_\-]+)["\']', html)
    report["frontend_tabs"] = panes

    return report

if __name__ == '__main__':
    rep = audit()
    print(json.dumps(rep, indent=2))
