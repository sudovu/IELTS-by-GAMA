# IELTS by GAMA
### Production-Grade Student-First AI English Learning & IELTS Preparation Ecosystem

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%203-lightgrey.svg)](https://www.sqlite.org/)
[![Security](https://img.shields.io/badge/Security-OWASP%20scrypt-success.svg)](https://cheatsheetseries.owasp.org/)
[![License](https://img.shields.io/badge/License-AGPL%20v3-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Web%20%7C%20iOS%20%7C%20Android%20%7C%20Desktop-purple.svg)](https://gautambhuwan.com.np/ielts/)

**IELTS by GAMA** is an autonomous, comprehensive English-learning and IELTS preparation platform. It offers an end-to-end educational curriculum spanning CEFR levels **A1 through C2**, complete **IELTS Academic** and **General Training** examination practice across all four skills (Listening, Reading, Writing, and Speaking), an automated **Mistake Book**, spaced repetition vocabulary training, and personal analytics.

---

## 🏛️ Hosting & System Architecture

IELTS by GAMA operates in two complementary deployment modes:

1. **Autonomous Client-Side & PWA Mode (Static Web / Mobile):**
   - The web application hosted at [`https://gautambhuwan.com.np/ielts/`](https://gautambhuwan.com.np/ielts/) runs client-side with an embedded `OfflineLocalEngine` and Service Worker (`sw.js`).
   - Learner profiles, practice tests, vocabulary flashcards, and mistake logs persist safely in browser `localStorage`.
   - Functions autonomously without requiring a remote server connection.
2. **Hybrid Local / Private Server Mode (Desktop & Dedicated Hosting):**
   - Python 3 `ui/server.py` serving a local REST API backed by an ACID-compliant SQLite database (`data/ielts_gama.db`).
   - Enforces defense-in-depth security: OWASP scrypt password hashing ($N=16384, r=8, p=1$), constant-time anti-enumeration, sliding-window rate limiting, and HTTP header-only session tokens.

```
┌─────────────────────────────────────────────────────────────┐
│                       Student Browser                       │
│      (Desktop Chrome / Safari iOS PWA / Android WebView)    │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
    [Standalone Web App / PWA]       [HTTPS API Requests]
      - Embedded Offline Engine        - Header: X-Session-Token
      - Service Worker Cache           - Parameterized SQL
      - localStorage Persistence       - Rate-Limited Endpoints
               │                              │
               └──────────────┬───────────────┘
                              ▼
                 ┌──────────────────────────┐
                 │   Python Server Engine   │
                 │      (ui/server.py)      │
                 └────────────┬─────────────┘
                              ▼
                 ┌──────────────────────────┐
                 │  Local SQLite 3 Database │
                 │    (data/ielts_gama.db)  │
                 └──────────────────────────┘
```

---

## ✨ Core Student Capabilities

### 1. English Academy Curriculum (CEFR A1 to C2)
- **54 Structured Lessons:** Spanning 6 CEFR bands (A1 Breakthrough, A2 Waystage, B1 Threshold, B2 Vantage, C1 Operational Proficiency, C2 Mastery).
- **Instructional Depth:** Every lesson features targeted learning objectives, grammatical explanations, authentic examples, common learner error analyses, vocabulary in context, and 5 interactive practice questions with immediate feedback.

### 2. Full IELTS Examination Simulation (Academic & General Training)
- **Reading:** 40 authentic questions across 3 passages (Academic) or 3 sections (General Training), covering all 14 question types: True/False/Not Given, Yes/No/Not Given, Multiple Choice, Matching Headings, Information Matching, Sentence Completion, and Summary Completion.
- **Listening:** 40 sequential questions across 4 authentic sections (Campus Booking, Community Center Monologue, Academic Tutorial, Hydrothermal Vents Lecture) with distractor analyses.
- **Writing Studio:** 18 comprehensive prompts across Academic Task 1, General Training Task 1, and Academic/GT Task 2. Evaluated using official Cambridge weighting ($\frac{1}{3} \text{ Task 1} + \frac{2}{3} \text{ Task 2}$).
- **Speaking Examiner:** 3-part Cambridge interview simulation with pacing trackers, filler-word counters, and lexical upgrade suggestions.

### 3. Automated Mistake Book & Adaptive Drills
- Errors made during Reading, Listening, Grammar, or Curriculum quizzes are automatically logged in the student's personal **Mistake Book**.
- Tracks error recurrence count and mastery score.
- Generates targeted review drills directly from past mistakes.

### 4. Vocabulary Vault & Spaced Repetition (SRS)
- 15 comprehensive vocabulary themes (Environment, Education, Science, Urbanization, Technology, etc.).
- SuperMemo SM-2 Spaced Repetition System schedules retention reviews based on candidate recall.

---

## 🔒 Privacy, Security & Data Storage

- **Local-First & Multi-Learner Isolation:** All student data, exam histories, drafts, and mistake logs are strictly isolated by learner ID.
- **No Third-Party Trackers:** Zero external advertising trackers or analytics telemetry.
- **OWASP-Grade Authentication:** Passwords hashed with scrypt. Session tokens transmitted exclusively in `X-Session-Token` headers; query parameter token transport is rejected with HTTP 401.

---

## ⚠️ Practice Scoring & Assessment Disclaimers

IELTS by GAMA is an independent educational training software designed for formative self-study.

1. **Not an Official IELTS Result:**
   - Scores produced by this application are **automated diagnostic estimates** ($\pm 0.5$ band margin of error) for self-study preparation.
   - This software is **not** endorsed by, accredited by, or affiliated with Cambridge Assessment English, IDP: IELTS Australia, or the British Council.
   - Internally generated scores cannot be used for university admissions, visa applications, or official accreditation.
2. **Synthetic Listening Audio:**
   - Listening audio exercises utilize high-quality speech synthesis playback of authentic IELTS dialogue scripts.
3. **Transcript-Based Speaking Limitations:**
   - Speaking evaluation operates on speech-to-text transcript recognition and fluency tracker pacing.
   - The system does **not** conduct acoustic spectral, formant, or phonemic pitch analysis.
   - Pronunciation ratings represent a neutral baseline and are unassessed via acoustic analysis.

---

## 📱 Installation & Cross-Platform Access

### 1. Web Application & Progressive Web App (PWA)
- **Live URL:** [https://gautambhuwan.com.np/ielts/](https://gautambhuwan.com.np/ielts/)
- **Installation:** Open in Chrome or Safari $\to$ click **Install App** or **Add to Home Screen**.
- Offline-ready via Service Worker asset caching.

### 2. Apple iOS (iPhone & iPad)
- **1-Click Profile (.mobileconfig):** [Download Profile](https://gautambhuwan.com.np/downloads/ielts-by-gama/ielts-by-gama.mobileconfig)
- **Native .IPA Package:** [Download .IPA (3.7 MB)](https://gautambhuwan.com.np/downloads/ielts-by-gama/ielts-by-gama.ipa) for AltStore, Sideloadly, or TrollStore.
- **Wireless Over-The-Air (OTA):** Available via enterprise manifest.

### 3. Android (Phone & Tablet)
- **Direct APK Download:** [Download Android APK (23.9 MB)](https://gautambhuwan.com.np/downloads/ielts-by-gama/ielts-by-gama-release.apk)
- **Tablet Edition:** Responsive dual-pane layouts for tablets.

---

## 🚀 Running Locally from Source

### Prerequisites
- Python 3.9 or higher
- SQLite 3.35 or higher

### Setup & Launch
```bash
# Clone the repository
git clone https://github.com/sudovu/IELTS-by-GAMA.git
cd IELTS-by-GAMA

# Launch the hybrid local server
python run_ui.py
# Open your browser at http://127.0.0.1:8080
```

### Running Automated Tests
```bash
python -m unittest discover tests
```

---

## 🤝 Support & Issue Reporting

If you encounter an issue or have a suggestion:
- **GitHub Issues:** [https://github.com/sudovu/IELTS-by-GAMA/issues](https://github.com/sudovu/IELTS-by-GAMA/issues)
- **Website:** [https://gautambhuwan.com.np](https://gautambhuwan.com.np)

---

## 📜 License
Distributed under the GNU Affero General Public License v3.0 (AGPLv3). See [`LICENSE`](LICENSE) for complete terms.
