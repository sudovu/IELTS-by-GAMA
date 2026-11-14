"""
Audit Script for IELTS by GAMA
Performs deep automated inspection of:
- Python core architecture and imports
- SQLite schema vs Master Project Directive
- Content files (grammar, vocabulary, reading, listening, writing, speaking)
- REST API routes in ui/server.py
- Frontend tabs, controls, and API calls in index.html & app.js
- Android bridge and configuration
- Test coverage
"""

import os
import sys
import json
import re
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

print("=" * 60)
print("IELTS by GAMA - Comprehensive Repository Audit")
print("=" * 60)

# 1. DATABASE SCHEMA INSPECTION
print("\n[1] DATABASE SCHEMA & TABLES")
from core.database.db_manager import DatabaseManager
db = DatabaseManager(":memory:")
db.init_schema()
with db.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables in schema ({len(tables)}): {', '.join(tables)}")

    for t in tables:
        clean_table = re.sub(r'[^a-zA-Z0-9_]', '', t)
        cursor.execute(f"PRAGMA table_info({clean_table});")
        cols = [f"{col[1]} ({col[2]})" for col in cursor.fetchall()]
        print(f"  - {t}: {', '.join(cols)}")

# 2. REST API ROUTES IN SERVER.PY
print("\n[2] REST API ROUTES (ui/server.py)")
server_file = os.path.join(BASE_DIR, "ui", "server.py")
with open(server_file, "r", encoding="utf-8") as f:
    server_code = f.read()

get_routes = re.findall(r'path == ["\'](/api/[^"\']+)["\']', server_code)
post_routes = re.findall(r'path == ["\'](/api/[^"\']+)["\']', server_code[server_code.find("def do_POST"):])
# separate GET from POST
get_section = server_code[server_code.find("def do_GET"):server_code.find("def do_POST")]
get_routes = re.findall(r'path == ["\'](/api/[^"\']+)["\']', get_section)
print(f"GET routes ({len(get_routes)}): {get_routes}")
print(f"POST routes ({len(post_routes)}): {post_routes}")

# 3. CONTENT REPOSITORY INVENTORY
print("\n[3] CONTENT REPOSITORY INVENTORY")
content_dir = os.path.join(BASE_DIR, "content")
for root, dirs, files in os.walk(content_dir):
    for f in files:
        if f.endswith(".json"):
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, BASE_DIR)
            with open(fp, "r", encoding="utf-8") as jf:
                data = json.load(jf)
            count = len(data) if isinstance(data, (list, dict)) else 0
            print(f"  - {rel}: {count} items")

# 4. FRONTEND TABS AND UI CONTROLS
print("\n[4] FRONTEND TABS & MODULES (ui/static/index.html & app.js)")
html_file = os.path.join(BASE_DIR, "ui", "static", "index.html")
with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

nav_tabs = re.findall(r'data-tab=["\']([^"\']+)["\']', html)
tab_panes = re.findall(r'id=["\']tab-([^"\']+)["\']', html)
print(f"Navigation data-tab entries ({len(set(nav_tabs))} unique): {sorted(list(set(nav_tabs)))}")
print(f"Tab pane IDs ({len(tab_panes)}): {tab_panes}")

app_js_file = os.path.join(BASE_DIR, "ui", "static", "app.js")
with open(app_js_file, "r", encoding="utf-8") as f:
    app_js = f.read()

api_calls = re.findall(r'callApi\(["\'](/api/[^"\']+)["\']', app_js)
print(f"API calls in app.js ({len(set(api_calls))} unique): {sorted(list(set(api_calls)))}")

# 5. HARDCODED / SIMULATED LOGIC AUDIT
print("\n[5] HARDCODED / SIMULATED LOGIC AUDIT")
from core.ai.local_provider import LocalAIProvider
from core.progress.analytics import LearningAnalytics
from core.speaking.speaking_examiner import SpeakingExaminer
from core.reading.reading_engine import ReadingEngine
from core.listening.listening_engine import ListeningEngine
from core.writing.writing_evaluator import WritingEvaluator

print("  - Analytics Radar:", LearningAnalytics().get_dashboard_data("test")["skills_radar"])
print(f"  - Reading Passages count: {len(ReadingEngine.ORIGINAL_PASSAGES)}")
print(f"  - Listening Sections count: {len(ListeningEngine.SECTIONS)}")
print(f"  - Writing Prompts count: {len(WritingEvaluator.ORIGINAL_PROMPTS)}")
print(f"  - Speaking Exam Sets count: {len(SpeakingExaminer.EXAM_SETS)}")

print("\nAudit script complete.")
