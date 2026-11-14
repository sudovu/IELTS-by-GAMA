# PHASE 18: KNOWN LIMITATIONS REPORT
**Project:** IELTS by GAMA  
**Current Version:** 1.6.0  
**Focus:** Explicit Disclosure of Technical & Pedagogical Boundaries  
**Audit Date:** November 15, 2026  
**Auditor:** Quality Assurance Lead & Educational Assessment Auditor  

---

## 1. Executive Summary

In adherence to the core non-negotiable guidelines of IELTS by GAMA, all practice results, automated scorings, and system capabilities must be described honestly. The application explicitly refrains from claiming official accreditation or capabilities that cannot be technically delivered.

---

## 2. Technical & Pedagogical Limitations

### 1. Diagnostic Practice Status (Not an Official IELTS Score)
- **Limitation:** IELTS by GAMA is an independent educational training software. It is **not** endorsed by, affiliated with, or accredited by Cambridge Assessment English, IDP: IELTS Australia, or the British Council.
- **Learner Impact:** Practice scores provide a reliable diagnostic estimate ($\pm 0.5$ to $\pm 1.0$ band margin of error) for self-study preparation, but cannot serve as official language proficiency certificates for immigration, academic admissions, or professional licensing.
- **Disclosure Mechanism:** Visible disclaimers are rendered on the Dashboard, exam submission screens, and individual result reports.

### 2. Speech Evaluation via Non-Acoustic Transcript Recognition
- **Limitation:** The speaking examiner analyzes speech-to-text transcripts and timing metadata. It does **not** perform acoustic spectral, formant, or phonemic frequency analysis.
- **Learner Impact:** The system accurately evaluates lexical choice, grammatical complexity, fluency pacing (words per minute), and hesitation markers. However, it cannot evaluate accent quality, phonemic articulation errors, word stress, or sentence intonation.
- **Disclosure Mechanism:** Clear disclaimer prominently embedded in Speaking evaluation results:
  > *"A transcript alone cannot reliably assess pronunciation, accent quality, or intonation. The displayed pronunciation rating is a neutral baseline and is unassessed via acoustic analysis."*

### 3. Speech Synthesis Audio Playback
- **Limitation:** Listening section audio currently relies on high-quality text-to-speech (TTS) speech synthesis rather than studio-recorded native human speaker casts.
- **Learner Impact:** Audio scripts are authentic and accurately reflect IELTS exam dialogues, accents, and distractor patterns. However, acoustic pacing and natural background acoustic ambience may differ slightly from studio recordings.
- **Mitigation:** The complete audio script is accessible for reading and replay, and the question structure strictly mirrors authentic IELTS sections.

### 4. Automated Writing Scoring Bounds
- **Limitation:** In the absence of human examiners, Writing evaluation uses heuristic rule-based feature extraction (AWL vocabulary matching, syntactic complexity detection, paragraph structure, and discourse marker tracking).
- **Learner Impact:** Highly effective for diagnosing structural errors, underlength responses, and vocabulary weaknesses. However, highly sophisticated nuances (e.g. subtle irony, rhetorical flair) may not receive the full credit that an expert human examiner might award.

---

## 3. Transparency Commitment

The system makes zero claims of human calibration, zero claims of official examination status, and provides 100% visible evidence and accepted answers for every question scored.
