# PHASE 16 KNOWN LIMITATIONS & DISCLOSURES
**Project:** IELTS by GAMA  
**Version:** 1.6.0  
**Phase:** 16 — Supervised Beta Pilot, Human Scoring Calibration & Teacher Review Toolkit  
**Date:** November 15, 2026  
**Status:** Transparent Risk Disclosure & Future Roadmap  

---

## 1. Executive Summary

In adherence to scientific integrity and software engineering transparency, this document details the known technical, operational, and assessment limitations of IELTS by GAMA version 1.6.0. 

No system limitation is concealed or minimized. These disclosures outline the boundaries of the software and define requirements for subsequent development phases.

---

## 2. Assessment & Scoring Limitations

### 2.1 Pending Human Calibration Data ($N=0$)
- **Current State:** The assessment calibration engine reports `status: "pending_human_calibration"` and `valid_samples: 0`.
- **Reason:** No artificial benchmark records have been fabricated. Real calibration metrics (MAE, Mean Signed Bias, $\pm 0.5$ agreement) require real candidates in the beta cohorts to complete submissions and real examiners to execute double-marking.
- **Classification:** `PENDING HUMAN VALIDATION`.
- **Impact:** Automated scores are practice approximations (version 1.6.0) and should not be relied upon as official band predictions until empirical calibration curves are calculated.

### 2.2 Speaking Pronunciation Evaluation Modality
- **Limitation:** In web browser environments without acoustic audio feature extraction, speech-to-text engines only provide transcripts.
- **Pedagogical Boundary:** While lexical, grammatical, and fluency metrics can be approximated from transcript timing and vocabulary, true acoustic pronunciation (phonological intonation, sentence stress, rhythm) cannot be evaluated from text alone.
- **Mitigation Implemented:** Human examiners must explicitly tag `assessment_mode: "audio"`, `"transcript"`, or `"both"`. The UI prohibits claiming acoustic pronunciation validation if only transcript text was reviewed.

### 2.3 Non-Official Status Disclaimer
- **Mandatory Disclosure:** IELTS by GAMA is an independent preparation and diagnostic platform. It is **not affiliated with, endorsed by, or validated by Cambridge University Press & Assessment, the British Council, or IDP: IELTS Australia**. All practice examinations and scores are practice estimates and do not constitute official IELTS certification.

---

## 3. Platform & Hardware Limitations

### 3.1 iOS Physical Hardware Testing
- **Current State:** All iOS distribution files (`.mobileconfig`, `manifest.plist`, `sw.js`, `manifest.webmanifest`, and `ielts-by-gama.ipa` binary) have been generated, tested in Chromium/WebKit emulators, and deployed to the web portal.
- **Classification:** `PENDING PHYSICAL DEVICE VERIFICATION`.
- **Reason:** Apple's proprietary security model on physical iOS devices enforces certificate trust requirements for enterprise OTA (`itms-services://`) installations. Testing on physical Apple iPhone/iPad hardware requires user-side testing or MDM device enrollment.

### 3.2 Offline Heuristics vs. Cloud LLM Reasoning
- **Current State:** In Forced Offline Mode, the system uses deterministic rule-based algorithms, lexical frequency lookup tables, and syntactic heuristics.
- **Limitation:** Heuristic engines lack the deep contextual semantic nuance of 70B+ cloud LLMs when analyzing subtle irony, figurative language, or philosophical discourse in high-band Writing Task 2 essays.
- **Trade-off:** Offline heuristics guarantee absolute candidate privacy, zero operational server cost, and instant execution without internet access.

---

## 4. Operational & Governance Boundaries

### 4.1 Cohort Capacity Bounds
- **Current State:** The system enforces a strict 50-participant cap across the four seeded cohorts.
- **Reason:** Controlled manual review by teachers requires reasonable workload limits. Large-scale unconstrained registration without teacher staffing would result in unreviewed queues.

### 4.2 Single-Node SQLite Concurrency
- **Current State:** The backend operates on a local SQLite database (`data/ielts_gama.db`).
- **Limitation:** SQLite is optimized for single-host or local deployments. While SQLite supports high read concurrency via WAL (Write-Ahead Logging), high-frequency concurrent writes from thousands of simultaneous remote examiners would require migration to PostgreSQL.

---

## 5. Mitigation & Roadmap Strategy

| Limitation | Severity | Target Resolution Phase |
| :--- | :---: | :--- |
| $N=0$ Calibration Data | Medium | Phase 17: Post-cohort empirical calibration report |
| Acoustic Pronunciation | Low | Future native audio DSP feature extraction pipeline |
| Physical iOS MDM Testing | Low | Continuous candidate feedback through beta pilot |
| SQLite Write Concurrency | Low | Cloud microservice backend if scaling beyond 500 concurrent candidates |

---

## 6. Disclosure Sign-Off

These known limitations represent documented engineering boundaries, not software defects. The application operates reliably within its defined design parameters.
