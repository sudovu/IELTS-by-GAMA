# Changelog - IELTS by GAMA

All notable changes to the **IELTS by GAMA** platform and native Android applications are documented in this file.

The versioning follows the convention:
- **Major.Minor.Patch** (e.g. `v1.2.0`)
- **Small changes / bug fixes / patches**: `1.1.1`, `1.2.1`, etc.
- **Big changes / feature additions**: `1.2.0`, `1.3.0`, etc.

---

## [v1.2.0] - 2026-10-04 (Big Changes: IELTS Advantage & Content Expansion)

### Added
- **IELTS Advantage Questionnaire Studio (`#tab-advantage`)**:
  - *Question Breakdown Questionnaire*: Dissects prompts into Broad Topic, Micro-Topic, and Task Words/Traps using Chris Pell's 100% Rule.
  - *Coffee Shop Idea Generator*: Fast, high-clarity idea development avoiding over-complication or ungrounded claims.
  - *PEEL Paragraph Blueprint*: Body paragraph structure (Point, Explain, Example, Link/Result).
  - *10-Point Pre-Submission Self-Assessment Checklist*: Comprehensive 10-point audit covering TA, CC, LR, and GRA with live submission readiness score.
  - *3-Step Speaking Strategy*: Direct Answer -> Reason/Extension -> Example/Anecdote integration.
- **Grammar Fill-Up Cloze Drills**:
  - Interactive cloze drills testing Conditionals, Inversion, Passive Voice, Participle Clauses, and Hedging.
  - Real-time grammatical evaluation with band-targeted feedback notes.
- **Vocabulary Training & Topic Vaults**:
  - 10 High-frequency IELTS domain vaults (*Environment, Technology, Education, Health, Economy, Crime, Globalisation, Urbanisation, Media, Arts*).
  - Interactive Collocation Matcher drill.
  - Lexical Upgrade Clinic converting Band 6 phrasing into Band 8+ academic substitutes.
- **Cambridge Academic Test Modules Expansion**:
  - Reading: Expanded to 3 complete academic passages (*Hydrothermal Ecosystems*, *Cognitive Bilingualism*, *Urban Heat Islands*) with 13 questions each and Keyword & Synonym Mapping tables.
  - Speaking: Expanded from 3 to 6 official Cambridge Exam Sets with cue card timers, live audio transcripts, and Band 9 models.
  - Writing: Expanded to 5 Task 2 essay types with sample PEEL outlines.
  - Diagnostic: Expanded from 6 to 12 CEFR assessment questions.
- **System & Deployment**:
  - Displayed version badge (`v1.2.0`) across app header, sidebar, and Settings pane.
  - Updated Android `versionCode` to `2` and `versionName` to `"1.2.0"`.

---

## [v1.0.0] - 2026-10-04 (Initial Production Release)

### Added
- **Hybrid Online + Offline AI English & IELTS Tutor Architecture**:
  - Pure Python standard library backend with zero cloud lock-in.
  - Standalone Android APK with 100% offline local evaluation engine.
- **Certified AI Speaking Examiner Room**:
  - 3-part Cambridge interview simulation with Dr. Harrison.
  - Realistic British English TTS prosody and live speech recognition.
  - Band 8/9 optimization coaching and cue card countdown timer.
- **Formative Writing Studio**:
  - 4-criterion assessment (Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy).
  - 'Teach Through Correction' diagnostic feedback.
- **Academic Listening Module**:
  - Cambridge Sections 1-4 with interactive questions and audio playback.
- **Spaced Repetition (SRS) Vocabulary & Mistake Book**:
  - Leitner box intervals for academic collocations and tracked error diagnostics.
- **Adaptive Android UI**:
  - Responsive layouts for Android 11+ phones and widescreen tablets.
  - Custom 3D glowing launcher icon.
  - Production release keystore signing (APK Signature Scheme v1, v2, v3).
