# Changelog

All notable changes to **IELTS by GAMA** will be documented in this file.

## [1.0.0] - 2026-09-13

### Added
- **Hybrid-First Architecture**: Dual OFFLINE and ONLINE modes with `ConnectivityManager` and live UI badges.
- **Local AI & Local RAG**: Zero-dependency offline linguistic intelligence and TF-IDF cosine similarity search on SQLite.
- **Online-to-Offline Knowledge Loop**: Compact web extraction that caches and embeds distilled research for future offline usage.
- **CEFR Diagnostic Assessment**: Baseline diagnostic covering all 4 skills with CEFR and IELTS band mappings.
- **IELTS Core Modules**:
  - Academic & General Reading with TFNG and completion graders.
  - Section 1-4 Listening with distractor analysis and audio script delivery.
  - Writing Task 1 & 2 evaluator with 4-criterion band scoring and "Teach Through Correction" 5-point formative feedback.
  - Speaking Examiner simulation with fluency/WPM pacing and filler word tracking.
- **Adaptive Learning Engine**:
  - Mistake Book tracking error recurrence and mastery scores.
  - SuperMemo SM-2 Spaced Repetition System (SRS).
  - Adaptive Grammar drills focusing on student's most frequent mistakes.
  - Daily, Weekly, and Monthly personalized study plans.
- **Dual User Interfaces**:
  - Terminal CLI (`ielts_cli.py`).
  - Local Web UI (`run_ui.py`) with responsive desktop/tablet layout and Web Speech API audio support.
- **Zero Telemetry & Local Privacy**: SQLite storage with export/import in open JSON format.
