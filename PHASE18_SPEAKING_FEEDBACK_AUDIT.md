# PHASE 18: SPEAKING FEEDBACK AUDIT REPORT
**Project:** IELTS by GAMA  
**Current Version:** 1.6.0  
**Focus:** Speaking Examiner Simulation, Fluency Tracking, Transcript Limitations & Acoustic Disclaimers  
**Audit Date:** November 15, 2026  
**Auditor:** Assessment Accuracy Lead & Speech Technology Specialist  

---

## 1. Executive Summary

This audit evaluated the automated Speaking examination pipeline across `core/speaking/speaking_examiner.py`, `core/speaking/fluency_tracker.py`, and `CriteriaEvaluator.evaluate_speaking`.

Because IELTS by GAMA operates in hybrid and self-study environments without an accredited IELTS examiner, **transparency regarding acoustic analysis limitations is essential**. The system must evaluate what it can genuinely assess (transcript content, lexical range, fluency metrics, pacing) while clearly disclosing what it cannot assess (acoustic phonetics, pitch variation, stress, and intonation).

---

## 2. Speaking Examination Architecture

The simulation mirrors the 3-part IELTS Speaking interview:
1. **Part 1 (Introduction & Interview):** 4–5 questions on familiar topics (hometown, studies, hobbies).
2. **Part 2 (Individual Long Turn):** Candidate cue card with 1 minute preparation and 1–2 minutes speaking.
3. **Part 3 (Two-way Discussion):** In-depth abstract questions connected to the Part 2 theme.

---

## 3. Assessment Modality & Fluency Metrics

The evaluation engine leverages two primary modalities:

1. **Speech-to-Text Transcript Analysis:**
   - **Grammatical Range & Accuracy:** Detects sentence length, subordinate clauses, tense consistency.
   - **Lexical Resource:** Identifies Band 7/8/9 vocabulary and suggests lexical upgrades (e.g. replacing *"very important"* with *"crucial"* or *"indispensable"*).
2. **Fluency Tracker (`core/speaking/fluency_tracker.py`):**
   - **Words per Minute (WPM):** Tracks speaking rate against optimal IELTS range (110–150 WPM).
   - **Filler Word Detection:** Counts hesitation markers (`um`, `uh`, `like`, `you know`, `basically`).
   - **Pause Frequency & Ratio:** Measures silence vs speech duration.

---

## 4. Assessment Limitations & Non-Acoustic Disclosure

In compliance with Phase 18 standards, all Speaking evaluation outputs include mandatory limitation disclosures:

1. **Acoustic Disclaimer:**
   > *"This evaluation does not perform acoustic spectral, formant, or acoustic phoneme analysis; assessments reflect speech-to-text transcript recognition and fluency tracker pacing."*
2. **Pronunciation Limitation:**
   > *"A transcript alone cannot reliably assess pronunciation, accent quality, or intonation. The displayed pronunciation rating is a neutral baseline and is unassessed via acoustic analysis."*
3. **Assessment Modality Tag:**
   `assessment_modality: "speech_to_text_transcript_recognition (non-acoustic)"`
4. **Examiner Verification:**
   `examiner_verified: False`
5. **Empty Transcript Guard:**
   Empty or silent speaking submissions strictly receive **Band 0.0**.

---

## 5. Result Verification Metadata

The Speaking result object returned to students contains:
- `estimated_band`: Overall band score estimate.
- `confidence_range`: $\pm 0.5$ band margin of error.
- `criteria`: Individual sub-scores for:
  - Fluency and Coherence
  - Lexical Resource
  - Grammatical Range and Accuracy
  - Pronunciation (disclosed as unassessed baseline)
- `fluency_metrics`: WPM, filler frequency, speech duration.
- `lexical_upgrades`: Actionable recommendations for more academic vocabulary.

---

## 6. Conclusion

Speaking evaluation provides valuable lexical, structural, and fluency practice for independent candidates while upholding complete academic honesty regarding pronunciation and acoustic analysis limitations.
