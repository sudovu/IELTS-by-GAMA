# IELTS by GAMA
### Hybrid Online + Offline AI English Tutor & IELTS Preparation System

![Mode](https://img.shields.io/badge/Mode-Offline--First-green.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_Default-success.svg)

**IELTS by GAMA** is a dedicated, production-grade AI English-learning and IELTS preparation platform engineered with a **hybrid-first architecture**. It operates with complete autonomy in **100% Offline Mode** while seamlessly utilizing Internet connectivity in **Online Mode** to enhance local knowledge.

---

## 🏛️ Architecture Overview

```
                         IELTS by GAMA
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
            OFFLINE MODE                ONLINE MODE
                 │                           │
        Local AI + Local DB          Local AI + Internet
        Local RAG                   Web/Cloud AI optional
        Local exercises             Fresh IELTS knowledge
        Local speech                Content updates
        Local progress              Model/content updates
                 │                           │
                 └─────────────┬─────────────┘
                               │
                         Unified AI Tutor
                               │
                 ┌─────────────┴─────────────┐
                 ↓                           ↓
          English Learning              IELTS Preparation
```

### The Transition Between Online and Offline
```
              ┌─────────────────┐
              │   USER QUESTION │
              └────────┬────────┘
                       ↓
                LOCAL KNOWLEDGE
                       ↓
                 LOCAL CACHE
                       ↓
                 LOCAL AI
                       ↓
              Is confidence enough?
                 /             \
               YES             NO
                ↓               ↓
             ANSWER         INTERNET?
                              /    \
                            NO      YES
                            ↓        ↓
                         ANSWER    SEARCH
                                    ↓
                               EXTRACT ONLY
                               NEEDED DATA
                                    ↓
                                 VERIFY
                                    ↓
                               ANSWER USER
                                    ↓
                           SAVE COMPACT DATA
                                    ↓
                            FUTURE OFFLINE USE
```

---

## ✨ Key Features

1. **Hybrid Connectivity & Mode Supervisor**
   - Live status indicator: `● OFFLINE`, `● ONLINE`, or `● SYNCING`.
   - Explicit **Force Offline Mode** switch for zero-transmission privacy guarantees.

2. **Zero-Dependency Local AI & Local RAG**
   - Built-in deterministic linguistic intelligence and sub-millisecond TF-IDF cosine similarity retrieval over SQLite.
   - Grounded in curated grammar, vocabulary, and IELTS assessment rubrics.
   - Pluggable support for quantized local models (llama.cpp, ONNX) and optional Cloud AI (Gemini).

3. **Formative "Teach Through Correction" Engine**
   - Never rewrites essays blindly. Evaluates errors using the 5-point formative structure:
     `ORIGINAL` → `CORRECTION` → `WHY` → `BETTER ALTERNATIVE` → `PRACTICE EXERCISE`.

4. **100% Original, Copyright-Compliant IELTS Practice**
   - Academic and General Training practice for **Listening, Reading, Writing, and Speaking**.
   - Strict adherence to copyright law (no copied Cambridge examination papers).
   - Clear disclaimers: *"Practice estimate only. Not an official IELTS result."*

5. **Personalized Mistake Book & SuperMemo SM-2 Spaced Repetition**
   - Tracks error recurrence across 24 grammatical syllabus categories.
   - Dynamically schedules retention intervals for Academic Word List vocabulary, collocations, and idioms.

6. **Adaptive Study Planner & Diagnostics**
   - Initial CEFR diagnostic test (A1 to C2) mapped to IELTS band estimates.
   - Daily, weekly, and monthly targeted plans matching student daily study limits.

7. **Multi-Platform Interfaces**
   - **Interactive Terminal CLI**: `python ielts_cli.py`
   - **Local Web/Desktop Responsive UI**: `python run_ui.py` (served on `http://127.0.0.1:8080` with Web Speech API integration).
   - **Android 11+ & Tablet Application**: Self-contained offline APK with responsive split-screen tablet layout and hardware-accelerated WebView (`dist/ielts-by-gama-tablet-android11+.apk`).

---

## 📱 Android App (Android 11+ & Tablets)

The project includes an Android APK built for **Android 11+ (API 30+)** optimized for both phones and **Android tablets** (portrait and landscape orientations):
- **Direct APK Download**: [`dist/ielts-by-gama-tablet-android11+.apk`](dist/ielts-by-gama-tablet-android11+.apk)
- **Features**:
  - Tablet-optimized split-screen layout for Reading (Passage + Questions side-by-side) and Writing (Task + Essay Editor).
  - 100% offline-first engine bundled into assets—no server or Python runtime required on device.
  - Microphone and speech synthesis support for Speaking section practice.
  - Back-button navigation and hardware acceleration.
- **Build from Source**:
  ```bash
  cd platform/android
  ./gradlew assembleDebug
  ```

---

## 🚀 Quick Start

### 1. Initialize Database & Seed Content
```bash
python scripts/init_db.py
```

### 2. Launch Interactive Terminal CLI
```bash
python ielts_cli.py
```

### 3. Launch Local Responsive Web App
```bash
python run_ui.py
# Open browser at http://127.0.0.1:8080
```

---

## 🧪 Testing

Run the automated test suite covering all modules:
```bash
python -m unittest discover tests
```

---

## 🔒 Privacy & Security

- **Strictly Local-First**: Voice recordings, essays, conversations, and progress records remain on the local machine in SQLite.
- **No Automatic Telemetry**: Telemetry is completely disabled.
- **SSRF & Injection Hardening**: All SQL queries use parameterization. Online research sanitizes inputs and strictly restricts outbound domains.

---

## 📜 License
Distributed under the GNU Affero General Public License v3.0 (AGPLv3). See [`LICENSE`](LICENSE) for more information.
