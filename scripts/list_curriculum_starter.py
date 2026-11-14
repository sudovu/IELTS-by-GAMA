import sys, os
sys.path.insert(0, os.path.abspath("."))
from core.curriculum.curriculum_engine import STARTER_LESSONS

print(f"Total starter lessons: {len(STARTER_LESSONS)}")
for l in STARTER_LESSONS:
    print(f"- {l['id']} [{l['cefr_level']}] ({l['module_type']}): {l['title']}")
