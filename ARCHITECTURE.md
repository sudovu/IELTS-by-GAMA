# System Architecture — IELTS by GAMA
## Multi-Platform Hybrid AI English Tutor & IELTS Preparation System

```
+-----------------------------------------------------------------------------------------+
|                                    IELTS by GAMA UI                                     |
|  (Adaptive Responsive Interface: Desktop, Mobile Web, iOS Safari PWA, Android WebView) |
+-----------------------------------------------------------------------------------------+
                                             |
            +--------------------------------+--------------------------------+
            |                                                                 |
            v (Local HTTP REST API)                                           v (Direct JS Fallback)
+-----------------------------------------+             +-----------------------------------------+
|       Python Local Backend Engine       |             |           OfflineLocalEngine            |
|        (ThreadingHTTPServer:8080)       |             |         (Zero-Python Android &          |
+-----------------------------------------+             |          iOS Safari Standalone)         |
  |             |             |             |           +-----------------------------------------+
  v             v             v             v                                 |
+---------+   +---------+   +---------+   +---------+                         |
| Scoring |   | Writing |   | Reading |   |Speaking |                         v
| & CEFR  |   | & PEEL  |   | & Listen|   |Examiner |                 +---------------+
+---------+   +---------+   +---------+   +---------+                 | LocalStorage  |
  |                 \             /             /                     | & IndexedDB   |
  |                  \           /             /                      +---------------+
  v                   v         v             v
+---------------------------------------------------+
|               Unified AI Tutor Bot                |
|  (Interception, Formative Correction, Local RAG)  |
+---------------------------------------------------+
  |                         |                     |
  v                         v                     v
+-------------------+ +-------------------+ +-------------------+
| LocalAIProvider   | | Mistake Book      | | Spaced Repetition |
| & Local RAG       | | (Unified Ledger)  | | (SuperMemo SM-2)  |
+-------------------+ +-------------------+ +-------------------+
  |                         |                     |
  +-------------------------+---------------------+
                            |
                            v
+---------------------------------------------------+
|              SQLite Storage Engine                |
|         (data/ielts_gama.db, WAL Mode)            |
+---------------------------------------------------+
```

---

## 1. Architectural Principles

1. **100% Offline-First by Default**:
   All core educational capabilities (curriculum, grammar rules, vocabulary vault, diagnostic evaluation, reading passages, listening audio synthesis, writing evaluation, speaking simulations, mistake tracking, and spaced repetition) function entirely offline with zero external network connectivity.

2. **Dual-Execution Engine**:
   - **Mode A (Full Hybrid Server)**: Python local backend (`ui/server.py`) serving REST endpoints with SQLite storage, Local RAG vector indexing, and optional cloud AI augmentation.
   - **Mode B (Client Standalone)**: Embedded JavaScript engine (`OfflineLocalEngine` in `ui/static/app.js`) enabling self-contained operation inside Android APK WebViews, iOS Safari WebClips, or static PWA deployments without requiring a local Python server.

3. **Formative "Teach Through Correction"**:
   Rather than rewriting student work or generating passive answers, the tutor intercepts errors and generates targeted 5-point feedback:
   `ORIGINAL` → `CORRECTION` → `WHY` → `BETTER ALTERNATIVE` → `PRACTICE EXERCISE`.

4. **Authentic IELTS Advantage & Cambridge Framework**:
   - The 100% Rule (Topic, Micro-Topic, and Traps).
   - The Coffee Shop Idea Generation method.
   - PEEL Body Paragraph Blueprint (Point, Explain, Example, Link).
   - 10-Point Pre-Submission Self-Assessment Checklist.
   - 3-Step Speaking Strategy (Direct Answer → Reason → Example).

---

## 2. Core Subsystems

### A. Learner Management & Personalization (`core/device/profile_manager.py`)
- Manages learner profiles, target band (1.0–9.0), track (Academic or General Training), target exam date, and daily study budget.
- Tracks multi-learner profiles in SQLite with active profile switching.

### B. CEFR English Learning Academy (`core/curriculum/`)
- Comprehensive structured curriculum from A1 (Beginner) to C2 (Proficiency).
- 24 Grammatical Syllabus categories with interactive Cloze drills and syntax analysis.
- Rich Vocabulary Vault (Academic Word List, collocations, phrasal verbs, idioms, word families).

### C. IELTS Examination Centre (`core/reading/`, `core/listening/`, `core/writing/`, `core/speaking/`)
- **Reading**: Academic and General Training with 14 question types, keyword synonym mapping tables, and timed 60-minute mock tests.
- **Listening**: 4 Examination sections with natural speech synthesis, distractor analyses, and post-test transcript protection.
- **Writing**: Task 1 (Academic visual data reports & GT letters) and Task 2 (Opinion, Discussion, Adv/Disadv, Problem/Solution, Two-part) with criterion scoring (TA, CC, LR, GRA).
- **Speaking**: 3-Part examiner simulation with Dr. Harrison, cue card countdown timers, live speech transcription, and multi-criterion evaluation.

### D. Progress & Adaptive Intelligence (`core/progress/`)
- **Personalized Mistake Book**: Multi-skill error tracking with recurrence counting and mastery scores.
- **Spaced Repetition (SRS)**: SuperMemo SM-2 algorithm scheduling cards by ease factor, intervals, and review grades.
- **Adaptive Study Planner**: Dynamic daily and weekly schedules prioritizing learner weaknesses and due items.
- **Learning Analytics**: Real-time progress computation, true skill radar mapping, and complete JSON export/import.

### E. AI English Teacher (`core/chatbot/`, `core/ai/`)
- Unified teaching intelligence with multi-turn hot memory and Local RAG.
- Intercepts grammar mistakes during conversational practice and logs them to the learner's mistake book.
- Adapts explanations to the learner's CEFR level.

---

## 3. Multi-Platform Support & Responsive Design
- **Android**: Signed production APK for Android 11+ with `AndroidTTS`, `AndroidSTT`, and `AndroidTheme` JavaScript bridges.
- **iOS**: Apple WebClip Profile (`.mobileconfig`), direct `.ipa` sideloading package, Apple OTA manifest (`manifest.plist`), and PWA Service Worker (`sw.js`).
- **Windows / Desktop**: Fluent responsive layout, keyboard shortcuts (`Alt+1..5`, `Alt+T`), and custom acrylic scrollbars.
- **Tablets**: Adaptive split-screen layouts for reading passages and writing studio.
