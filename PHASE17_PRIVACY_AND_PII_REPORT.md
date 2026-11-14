# Phase 17 Privacy & Personally Identifiable Information (PII) Report

**Project:** IELTS by GAMA  
**Application Version:** 1.6.0  
**Phase:** 17 — Security Hardening, Privacy Audit & Controlled Beta Launch Gate  
**Date:** 2026-11-15  
**Author:** QA & Security Architecture Team  

---

## 1. Executive Summary

A comprehensive privacy and data governance audit was conducted across all learner interaction channels, examination workflows, database schemas, and AI tutoring components. The primary objective was to ensure that candidate identity and submission data are collected with informed consent, minimized according to purpose, pseudonymized prior to research or calibration usage, and protected against unauthorized disclosure.

---

## 2. Pseudonymization vs. Anonymization Definition

The application documentation and architecture explicitly distinguish between **pseudonymization** and **absolute anonymization**:

- **Pseudonymization & Redaction:** The process of stripping direct identifiers (names, emails, phone numbers, postal addresses, candidate IDs) and replacing them with standardized category tokens (`[EMAIL REDACTED]`, `[PHONE REDACTED]`, etc.). This substantially reduces privacy risks but does not mathematically eliminate all indirect stylistic or contextual re-identification risks inherent in free-form natural language essays or acoustic speech recordings.
- **Regulatory Clarity:** In accordance with GDPR Article 4(5) and standard privacy engineering principles, benchmark and beta research corpora are classified as **pseudonymized data**, requiring appropriate organizational safeguards and consent controls.

---

## 3. Multi-Entity Pseudonymization Pipeline

The redaction engine in `core/benchmark/benchmark_manager.py: pseudonymize_text()` executes a multi-stage sequential filter:

| PII Category | Detection Logic / Pattern | Replacement Token |
| :--- | :--- | :--- |
| **Email Addresses** | RFC-compliant standard email regex: `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z\|a-z]{2,}\b` | `[EMAIL REDACTED]` |
| **Telephone Numbers** | International formats, domestic numbers with area codes, and 7-digit local phone patterns: `\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b` and `\b\d{3}[-.\s]?\d{4}\b` | `[PHONE REDACTED]` |
| **Candidate & Student IDs** | Prefixed and formatted identification codes: `\b(?:Candidate\|Student\|Learner\|Passport\|ID\|Desk)\s*(?:ID\|Number\|No\.?\|#)?\s*(?:is\s*)?[:=\-]?\s*[A-Za-z0-9\-]{4,20}\b` and `\b(?:CAND\|STU\|PASSPORT\|IELTS\|STUDENT\|CANDIDATE)-[A-Za-z0-9]{4,12}\b` | `[ID REDACTED]` |
| **Postal & Street Addresses** | Numbered building addresses with road/street/lane/terrace suffixes: `\b\d{1,5}\s+(?:[A-Z][a-z]+\s+)*(?:Street\|St\.?\|Road\|Rd\.?\|Avenue\|Ave\.?\|Boulevard\|Blvd\.?\|Lane\|Ln\.?\|Drive\|Dr\.?\|Terrace\|Terr\.?\|Way\|Court\|Ct\.?\|Place\|Pl\.?\|Close\|Square\|Sq\.?)\b` | `[ADDRESS REDACTED]` |
| **Salutations & Sign-offs** | Letter opening and closing formulas containing proper names: `\b(Dear\|Sincerely\|Regards\|Yours faithfully\|Yours sincerely\|Best wishes)[,\s]+(?:Mr\.?\|Mrs\.?\|Ms\.?\|Dr\.?\|Prof\.?)?\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b` | `\1 [NAME REDACTED]` |
| **Standalone Honorifics** | Titles preceding capitalized names: `\b(?:Mr\.?\|Mrs\.?\|Ms\.?\|Dr\.?\|Prof\.?)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b` | `[NAME REDACTED]` |

---

## 4. Audio Biometrics & Speaking Recordings

Audio recordings captured during IELTS Speaking examination simulations represent biometric data:

1. **Storage Isolation:** Audio files are saved as temporary `.wav` or `.webm` blobs in isolated data directories.
2. **Access Control:** Audio references are never exposed via unauthenticated public GET endpoints.
3. **Acoustic Scoring Safeguard:** The application currently refrains from automated acoustic grading without supervised human calibration. Speaking examinations are evaluated on transcription analysis for lexical, grammatical, and structural markers, preventing uncalibrated acoustic scoring claims.

---

## 5. Data Minimization & Retention

1. **Local-First Principle:** In standard standalone deployment, all learner records remain on the learner's local machine within `data/ielts_gama.db`.
2. **Beta Pilot Cohorts:** Participants admitted to the controlled beta pilot are notified that their anonymized feedback, error logs, and consented mock submissions will be reviewed exclusively for pedagogical refinement and scoring calibration.
3. **No Third-Party Analytics:** The application contains zero third-party commercial trackers, telemetry SDKs, or external advertising scripts.
