# PHASE 19: HOSTING ARCHITECTURE REPORT
**Project:** IELTS by GAMA  
**Current Application Version:** 1.6.0  
**Focus:** Production Hosting Topology, Static vs Dynamic Constraints & Hybrid Architecture  
**Execution Date:** November 15, 2026  
**Auditor:** Cloud Infrastructure & Systems Architect  

---

## 1. Executive Summary

This report establishes the verified hosting architecture for IELTS by GAMA, addressing the relationship between the public web deployment at [`https://gautambhuwan.com.np/ielts/`](https://gautambhuwan.com.np/ielts/) and the local/private Python backend engine.

### Key Architectural Constraint:
- The website domain `gautambhuwan.com.np` is hosted via **GitHub Pages** (static hosting with `.nojekyll` and `CNAME`).
- GitHub Pages natively serves static HTML, CSS, JavaScript, WebAssembly, and media assets. It **cannot** execute arbitrary server-side Python processes or host an active SQLite database server.
- **Architectural Solution:** IELTS by GAMA was purposefully architected as a **Dual-Mode Hybrid Application**:
  1. **Autonomous Client-Side PWA Mode (Live on GitHub Pages / Website):** The frontend contains an embedded `OfflineLocalEngine` executing in JavaScript, with local persistence in browser `localStorage`. It delivers the complete student experience (Curriculum, Flashcards, Diagnostics, Mock Tests, Mistake Book, and Analytics) client-side with zero external server dependencies.
  2. **Connected Hybrid Server Mode (Desktop & Private VPS):** When run locally or on a private server (`python run_ui.py`), `callApi()` communicates over HTTP with the Python `ThreadingHTTPServer` (`ui/server.py`), storing records in SQLite (`data/ielts_gama.db`).

---

## 2. End-to-End Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            STUDENT BROWSER                                  │
│             (Desktop Chrome / Safari iOS PWA / Android WebView)             │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                        Single Page App (SPA)                        │   │
│   │   - Modern Responsive UI (Plus Jakarta Sans & JetBrains Mono)       │   │
│   │   - Tab Navigation Engine (Dashboard, Academy, Exam Suite, Drills)  │   │
│   │   - Web Speech API (Native Speech Synthesis & Speech Recognition)   │   │
│   └──────────────────────────────────┬──────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                  Service Worker Cache ('v1.6.0')                    │   │
│   │   - Precaching: index.html, app.js, styles.css, manifest, icons     │   │
│   │   - Stale-While-Revalidate Caching for Instant Loading              │   │
│   └──────────────────────────────────┬──────────────────────────────────┘   │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
      [Autonomous Client-Side Mode]           [Connected Hybrid Server Mode]
     (Live on gautambhuwan.com.np/ielts/)        (Local Python / Private Server)
                    │                                     │
                    ▼                                     ▼
      ┌───────────────────────────┐         ┌───────────────────────────┐
      │    OfflineLocalEngine     │         │      HTTPS REST API       │
      │  - Client-side Graders    │         │  - Header: X-Session-Token│
      │  - Built-in Mock Tests    │         │  - Rate Limiting & Auth   │
      │  - Local Mistake Book     │         └─────────────┬─────────────┘
      └─────────────┬─────────────┘                       │
                    │                                     ▼
                    ▼                       ┌───────────────────────────┐
      ┌───────────────────────────┐         │    Python 3 Server Engine │
      │   Browser localStorage    │         │       (ui/server.py)      │
      │  - gama_learners          │         └─────────────┬─────────────┘
      │  - gama_active_learner_id │                       │
      │  - gama_mistakes          │                       ▼
      │  - gama_exam_history      │         ┌───────────────────────────┐
      └───────────────────────────┘         │  SQLite 3 ACID Database   │
                                            │    (data/ielts_gama.db)   │
                                            └───────────────────────────┘
```

---

## 3. Operational Advantages of the Hybrid Topology

1. **Zero Hosting Cost for Students:** Students can access the complete practice platform on the public website without requiring high-cost cloud computing servers.
2. **True Offline Functionality:** Once loaded, the student can disconnect from the internet entirely. The PWA Service Worker serves all assets, and `OfflineLocalEngine` grades answers locally.
3. **Data Privacy by Default:** In client-side mode, student essays, speaking transcripts, and test scores remain on the student's personal device.
4. **Local Server Available for Power Users:** Students who want to run the full Python backend with centralized SQLite storage can do so locally via `python run_ui.py`.

---

## 4. Conclusion

The hosting architecture is robust, cost-effective, privacy-preserving, and perfectly matched to the capabilities of the hosting target (`gautambhuwan.com.np`).
