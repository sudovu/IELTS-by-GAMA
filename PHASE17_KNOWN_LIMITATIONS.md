# Phase 17 Known Limitations & Assessment Boundary Disclosure

**Project:** IELTS by GAMA  
**Application Version:** 1.6.0  
**Phase:** 17 — Security Hardening, Privacy Audit & Controlled Beta Launch Gate  
**Date:** 2026-11-15  
**Author:** QA & Security Architecture Team  

---

## 1. Overview & Ethical Assessment Disclosure

In accordance with academic integrity and ethical AI principles, this document provides a comprehensive, unvarnished inventory of known limitations, boundary conditions, and architectural constraints in IELTS by GAMA (v1.6.0). 

These limitations must be clearly communicated to beta participants, educational coordinators, and evaluators.

---

## 2. Assessment & Scoring Limitations

### 2.1 Practice Estimates vs. Official IELTS Scores
- **Practice Approximation Only:** All automated band scores generated for Writing and Speaking are heuristic practice estimates intended for diagnostic guidance and structured self-study.
- **No Official Endorsement:** The application is NOT an official IELTS assessment platform and is neither endorsed nor accredited by IELTS partners (British Council, IDP: IELTS Australia, Cambridge University Press & Assessment). Automated scores must never be represented as official IELTS results.
- **Human Calibration Pending:** Statistical scoring alignment with certified IELTS examiners is currently awaiting data collection through the supervised beta pilot.

### 2.2 Speaking Modality Constraints
- **Transcription-Based Evaluation:** Speaking examinations in v1.6.0 evaluate transcribed speech for fluency markers, lexical resource, grammatical accuracy, and structural response coherence.
- **Acoustic Phonetics:** Fine-grained acoustic phonetic modeling (e.g., intonation contours, phonemic stress, voice onset time) is intentionally restricted from automated band calculation until certified human examiner acoustic calibration datasets are established.

---

## 3. Architecture & Infrastructure Limitations

### 3.1 Single-Instance SQLite Database
- **Concurrency Scope:** The application utilizes SQLite in WAL mode, which provides exceptional read performance and reliable single-writer transactions for local execution and controlled pilot cohorts (up to 50–100 concurrent participants).
- **Scale Limitation:** It is not engineered for horizontally scaled, multi-region distributed deployments. An enterprise-scale public rollout will require migrating the backend repository layer to PostgreSQL and introducing Redis for distributed session caching.

### 3.2 In-Memory Sliding-Window Rate Limiting
- The sliding-window rate limiter in `AuthManager` operates within Python process memory.
- If the server process is restarted, the in-memory failed attempt history resets. In production server deployments with multiple worker processes, rate limiting state should be backed by a persistent key-value store (e.g., Redis).

---

## 4. Privacy & Data Limitations

### 4.1 Pseudonymization vs. Mathematical Zero-Entropy Anonymization
- The pseudonymization pipeline in `BenchmarkManager` strips direct identifiers (emails, phone numbers, student/candidate IDs, postal street addresses, personal salutations).
- However, natural language writing samples may still contain indirect stylistic markers, uncommon biographical narratives, or specialized vocabulary that could theoretically allow contextual deduction by persons familiar with the author. Candidates must be informed of this inherent characteristic of natural language research datasets.

### 4.2 Offline Service Worker Capabilities
- The Progressive Web App (PWA) Service Worker caches static assets, curriculum lessons, and offline diagnostic quizzes, enabling fully offline study for core reading, listening, and grammar modules.
- However, dynamic AI tutor interactions and automated evaluation of free-form essays require network access to local or remote LLM inference endpoints.
