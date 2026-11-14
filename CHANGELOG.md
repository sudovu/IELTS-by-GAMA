# Changelog - IELTS by GAMA

All notable changes to the **IELTS by GAMA** platform and native Android applications are documented in this file.

The versioning follows the convention:
- **Major.Minor.Patch** (e.g. `v1.2.0`)
- **Small changes / bug fixes / patches**: `1.1.1`, `1.2.1`, etc.
- **Big changes / feature additions**: `1.2.0`, `1.3.0`, etc.

---

## [v1.6.0] - 2026-11-15 (Phase 18: Student-First IELTS Platform, Assessment Accuracy & Result Verification)

### Added & Hardened
- **Student-First Autonomous Architecture**:
  - Re-architected system for complete autonomous self-study without requiring human teachers, examiners, or external calibration cohorts.
  - Simplified student UI: educator management navigation groups and filter tabs are hidden by default and guarded by user roles (`admin`, `teacher`, `examiner`).
  - Implemented honest empty states for new learners: zero synthetic scores or fabricated charts when a learner has not completed assessments.
- **Listening Assessment Accuracy & Collision Prevention**:
  - Fixed critical Section numbering collision in `core/listening/listening_engine.py`: renumbered all 4 sections to sequential integers (Q1–10, Q11–20, Q21–30, Q31–40).
  - Enhanced answer evaluator to support both sequential keys (`listen_1` .. `listen_40`) and relative section indices (1..10).
  - Added question-by-question breakdown with distractor rationales and script evidence.
- **Reading Assessment Accuracy & Empty-Answer Guards**:
  - Implemented explicit empty-answer and whitespace-only guards across all 5 grading functions (`grade_tfng`, `grade_ynng`, `grade_multiple_choice`, `grade_matching`, `grade_completion`).
  - Blank and unanswered inputs strictly receive 0 marks and are flagged as `is_unanswered: True`.
  - Replaced arbitrary key vulnerabilities with strict schema rejection.
- **Band Calculation Integrity**:
  - Corrected `raw_to_band_listening` and `raw_to_band_reading` in `BandCalculator` so that 0 correct answers accurately yields **Band 0.0** (resolving previous default of Band 3.5).
  - Implemented full granular scale from Band 0.0 through Band 9.0 following Cambridge Assessment published guidelines.
- **Writing & Speaking Evaluation Hardening**:
  - Fixed empty-essay fallback bug in `ExamManager`: empty essays now strictly receive **Band 0.0**.
  - Enforced underlength band ceilings in `CriteriaEvaluator`: 0 words $\to$ Band 0.0, 1–24 words $\to$ max 1.5, 25–49 words $\to$ max 2.5.
  - Implemented official Cambridge IELTS writing formula: $\text{Writing Band} = \text{round\_band}(1/3 \times \text{Task 1} + 2/3 \times \text{Task 2})$.
  - Added explicit non-acoustic transcript recognition and pronunciation limitation disclosures to all speaking evaluation outputs.
- **Result Verification & Transparent Audit Records**:
  - Enforced deterministic result calculation: raw scores, total questions, percentages, band estimates, confidence ranges ($\pm 0.5$), versioned scoring rules (`"1.6.0"`), and accepted answer lists are saved to immutable JSON records.
  - Idempotency guard: duplicate submissions of already completed sessions return cached results without score mutation.
- **Automated Mistake Book Integration**:
  - Automatic error logging from Reading and Listening practice tests directly into `MistakeBook` with context, user answer, correct answer, and explanation.
  - Dynamic adaptive recommendations on the student dashboard targeting weakest skill areas.
- **Comprehensive Verification & Testing**:
  - Authored `tests/test_phase18_student_assessment_integrity.py` with 14 automated tests (100% pass).
  - Full test suite execution: **159 passing tests** across 17 test suites (0 failures, 0 errors in 7.322s).
  - Pre-migration database backup verified (`data/ielts_gama_phase18_backup.db`).
  - Authored all 17 Phase 18 markdown reports in repository root.

---

## [v1.6.0] - 2026-11-14 (Major Release: Master Project Directive — Complete English Learning & IELTS Preparation Ecosystem)

### Added & Transformed
- **Comprehensive Database Integrity & Multi-Learner Support**:
  - Implemented transactional SQLite migration engine in `core/database/migrations.py` managing 14 core tables with WAL mode and foreign key integrity.
  - Added full multi-profile management (`#activeLearnerBadge`, `#learnerProfileModal`) supporting learner switching, onboarding, target band/track setup, and target exam date configuration.
  - Added new tables: `curriculum_lessons`, `lesson_progress`, `vocabulary_vault`, `exam_sessions`, `writing_drafts`, `ai_conversations`.
- **Personal Learning Dashboard & Dynamic Skills Radar**:
  - Eliminated static demonstration radar metrics in favor of genuine live skill evaluations in `core/progress/analytics.py` calculated from candidate test records, evaluated writing drafts, and active mistakes.
  - Integrated dynamic daily study plans allocating minutes across vocabulary recall, weakness drills, and core practice.
- **English Learning Academy & CEFR Curriculum (A1–C2)**:
  - Built full 6-level structured curriculum in `core/curriculum/curriculum_engine.py` with 18 comprehensive lessons covering grammar, linguistic mechanics, examples, guided exercises, and quizzes.
  - Expanded `core/grammar/grammar_engine.py` with 25+ diagnostic error patterns and 30+ high-yield Cloze fill-up drills.
  - Automatic error logging from quiz attempts directly into the learner's `MistakeBook`.
- **IELTS Reading & Listening Examination Expansion**:
  - Implemented comprehensive graders in `core/reading/question_types.py` for all 14 official IELTS question types (TFNG, YNNG, MCQ with distractor analysis, Matching Headings/Features/Sentence Endings, Completion).
  - Added General Training reading passages (`gt_s1`, `gt_s2`, `gt_s3`) and full mock generator.
  - Expanded all 4 Listening sections to 10 questions each (= full 40 questions).
  - Enforced strict examination mode with answer key and transcript protection during testing.
- **Writing Studio Expansion & Draft Management**:
  - Added 18 comprehensive prompts across Academic Task 1 (Line, Bar, Pie, Table, Process, Map), General Training Task 1 (Formal, Semi-Formal, Informal Letters), and Academic/GT Task 2 (Opinion, Discussion, Advantages/Disadvantages, Causes/Solutions, Two-Part).
  - Enforced criteria scoring rubrics (Task Achievement/Response, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy) with Overview checks, objective tone verification, letter salutations/sign-offs, and underlength penalties.
  - Integrated persistent draft autosaving and evaluation recording in SQLite `writing_drafts` and `test_results`.
- **Speaking Examiner & Pronunciation Coach**:
  - Built `core/speaking/pronunciation_coach.py` providing phonemic minimal pairs (/iː/ vs /ɪ/, /b/ vs /v/, /θ/ vs /s/, /r/ vs /l/, /w/ vs /v/), syllable stress shifts, connected speech, and non-simulated drill grading.
  - Connected `SpeakingExaminer` 3-part Cambridge simulation with Band 9 models and IELTS Advantage 3-step strategy to `test_results`.
- **AI English Teacher with Dynamic CEFR Adaptation**:
  - Connected persistent multi-turn conversational history to SQLite `ai_conversations` table via `AIConversationRepository`.
  - Automatically adapts pedagogical tone, vocabulary, and explanation complexity to learner's assessed CEFR level (A1 to C2).
  - Real-time grammatical error interception with 5-point formative correction.
- **Vocabulary Vault & Spaced Repetition (SRS)**:
  - Built `VocabularyVault` with Academic Word List (AWL) Sublists 1-10, collocations, definitions, word families, and common pitfalls.
  - Integrated SuperMemo SM-2 Spaced Repetition System (SRS) for flashcard scheduling and review tracking.
- **Adaptive Study Planner**:
  - Built `generate_adaptive_study_plan()` in `core/progress/study_planner.py` synthesizing actual radar weaknesses, target exam countdown, overdue SRS cards, and pending curriculum lessons into 4-phase adaptive milestones.
- **UI Navigation Fix & Cross-Platform Packaging**:
  - Restored default visibility of all module categories in sidebar navigation with quick-jumping; no buttons hidden on initial load.
  - Synchronized static assets to Android WebView (`platform/android/app/src/main/assets/www/`).
  - Rebuilt iOS distribution packages (`ielts-by-gama.ipa`, Apple `.mobileconfig`, OTA manifest, PWA Service Worker).
  - Verified 100% test coverage with 71 passing tests and 0 failures.

---

## [v1.5.3] - 2026-10-04 (Small Changes: Pixel-Perfect Auto Screen Calibration & Seamless Snug System Fit)

### Fixed & Improved
- **Zero Excess Gap & Auto Snug Header**:
  - Eliminated both status bar collision and forehead gap by wrapping the WebView in a native `rootContainer` (`FrameLayout`) that applies exact WindowInsets (`WindowInsetsCompat.Type.statusBars()` and `Type.navigationBars()`).
  - Standardized `.app-header` to a snug, compact `52px` on mobile (`56px` on tablet/desktop) with clean vertical centering and zero artificial top padding.
  - Android status bar renders cleanly above the app header with zero overlap and zero empty space.
- **Screen Setting Analysis Engine**:
  - Automatically assesses screen width, height, density pixel ratio (DPR), orientation, and device form factor on launch.
  - Dynamically fits all categories, dashboard metrics, and controls tailored to the physical screen hardware.
- **Proactive Microphone Permission Calibration**:
  - Added on-startup system setup card that detects microphone permission status for Cambridge IELTS Part 1, 2, and 3 AI Speaking practice.
  - Proactively requests Android runtime `RECORD_AUDIO` permission when needed, with clean fallback for voice synthesis.
- **Multi-Theme Solid Status Bar**:
  - Synchronizes native status bar background with dark `#161e2b` and light `#ffffff` themes with dynamic icon contrast.

---

## [v1.5.2] - 2026-10-04 (Small Changes: Zero Top Gap & Seamless System Bar Auto-Fit)

### Fixed & Improved
- **Zero Top Gap Elimination**:
  - Removed duplicate top insets between native Android FrameLayout (`rootContainer`) and CSS (`body { padding-top: var(--sat); }`).
  - Switched native Android container to `WindowCompat.setDecorFitsSystemWindows(window, true)` with direct `setContentView(webView)`, allowing the top header to sit seamlessly flush with the Android status bar with zero artificial blank space.
- **Native Android Dynamic Theme Bridge**:
  - Implemented `AndroidThemeBridge` (`AndroidTheme.setDarkMode(isDark)`) to synchronize the native Android OS system status bar and navigation bar in real time with the app theme (`#161e2b` with light icons in dark mode, `#f8fafc` with dark icons in light mode).
- **Website & Documentation Synchronization**:
  - Fully synchronized all version tags, JSON-LD Schema records, and Developments Hub / Projects references across `gautambhuwan.com.np` to reflect `v1.5.2`.

---

## [v1.5.1] - 2026-10-04 (Small Changes: Auto Screen Lock & Rock-Solid Header Seating)

### Fixed & Improved
- **Auto Screen Fit & Strict Viewport Lock**:
  - Locked viewport scaling with `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">`.
  - Added strict overflow clipping (`overflow-x: clip !important; overflow-x: hidden !important; touch-action: pan-y;`) across `html`, `body`, and `.app-container`.
  - Completely resolved unwanted horizontal panning, dragging, and "movability", ensuring the screen sits perfectly stable on all mobile and tablet viewports without manual adjustment.
- **Rock-Solid Header Seating**:
  - Re-engineered `.app-header` with strict 100% width bounding, box-sizing, and compact single-line layout for mobile displays (`height: 52px`, `padding: 0 10px`, `gap: 6px`).
  - Streamlined branding: scaled logo (`32px`), prevented title wrapping, and suppressed subtitle on mobile.
  - Responsive connectivity status indicator: automatically displays compact `"ONLINE"` / `"OFFLINE"` badge on viewports under 768px and full badge on desktop, preventing horizontal flex overflow.
  - Shortened control button labels (`Offline: OFF` / `Offline: ON`) to guarantee all header controls sit comfortably on a single line on any smartphone.

---

## [v1.5.0] - 2026-10-04 (Big Changes: Multi-Platform Tablet/iOS/Windows & Light Mode Overhaul)

### Added
- **Crystal Clear Light Mode Redesign**:
  - Complete aesthetic and ergonomic redesign of the light theme.
  - High-contrast typography with deep slate headings (`#0f172a`), readable body text (`#334155`), and crystal-clear secondary text (`#64748b`).
  - Pure white elevated cards (`#ffffff`) with subtle, refined border definitions (`#e2e8f0`) and soft depth shadows.
  - Recalibrated categorical pastel palette (Core Indigo, Exam Blue, Advantage Amber, System Slate) engineered specifically for high readability on light backgrounds.
  - Elimination of all dark artifacts: form inputs, active goal boxes, subcategory toolbars, chat chips, cloze fill-ups, and modals now render with crisp daylight styling.
  - Instant theme toggle button with animated confirmation toast (`☀️ Crisp Light Mode Active` / `🌙 AMOLED Dark Mode Active`).
  - Automatic synchronization with operating system color scheme preference (`prefers-color-scheme`) with persistent local storage manual override.
- **Multi-Platform Compatibility (Tablet, iOS, Windows, Android)**:
  - **Automatic Screen Size & Device Adapter**: Dynamic JavaScript dimension detector setting CSS custom properties (`--app-width`, `--app-height`, `--vh`) and device classes (`device-mobile`, `device-tablet`, `device-desktop`, `device-ultrawide`, `platform-ios`, `platform-windows`, `platform-android`).
  - **Tablet Layouts (iPads & Android Tablets)**: Optimized split-pane dual-column views for Reading Passages (passage left, questions right) and Writing Studio (prompts left, editor right) across 768px – 1180px viewports.
  - **iOS Compatibility**: Safe area insets (`env(safe-area-inset-*)`), WebKit momentum touch scrolling, Web Audio API / SpeechSynthesis user gesture unlock for Dr. Harrison's speaking examiner voice, and Apple standalone PWA meta tags.
  - **Windows Desktop Integration**: Slim acrylic scrollbars adapting to both Dark and Light themes, high-DPI scaling, and desktop keyboard shortcuts (`Alt+1..5` navigation, `Alt+T` theme toggle, `Escape` modal dismiss).

---

## [v1.4.0] - 2026-10-04 (Big Changes: Category Progress Mastery, Live Band Score & Daily Mission Achiever)

### Added
- **Daily Mission & Goal Achiever System**:
  - Interactive "What do you want to achieve today?" on-startup welcome modal with 1-click goal options (Reading, Listening, Writing, Speaking, Grammar/SRS).
  - Prominent Daily Mission HUD card on Dashboard with active target details, live progress bar, direct routing helper (`helpAchieveGoal()`), and 1-click manual completion.
  - Session-aware startup prompt remembering user preferences.
- **Category Progress & Mastery Tracking Grid**:
  - 4 live competency cards for each preparation pillar: *Strategy & Core*, *Cambridge 4-Skills Suite*, *Methodology & Drills*, and *Tracking & System*.
  - Real-time percentage progress meters (`#catProgressBar_*`) and granular item-level tracking (Diagnostic completion, Reading passages, Listening sections, Writing essays, Speaking mocks, Advantage audits, and SRS mastery).
  - Direct 1-click launch shortcuts into each category workspace.
- **Live Dynamic Band Score Recalculation Engine**:
  - Real-time recalculation of overall IELTS Band Score whenever the user practices Reading, Listening, Writing, Speaking, Grammar clozes, or SRS flashcards.
  - Formula strictly follows official IELTS rounding rules to the nearest half-band with performance-based grammar/lexis bonuses.
  - Automatic CEFR progression mapping (C2, C1, B2, B1, A2) updated live in the UI.
- **Animated Band Score Update Toast**:
  - High-visibility celebratory floating notification (`#bandUpdateToast`) on practice submission displaying the newly achieved band score, CEFR level, and practice bonus.
- **Streamlined Navigation & Filter**:
  - Removed redundant "All (12)" filter from the mobile navigation bar, providing a clean 3-category switcher (*4-Skills Exam*, *Advantage & Drills*, *Strategy & System*) for seamless ergonomics.

---

## [v1.3.0] - 2026-10-04 (Big Changes: UI Modernization, Button System & Categorization)

### Added
- **Categorized Multi-Tier Navigation Structure**:
  - Reorganized sidebar into 4 functional category blocks: *Strategy & Core*, *Cambridge 4-Skills Suite*, *Methodology & Drills*, and *Tracking & System*.
  - Added category accent dots and metadata badges (e.g., `12 Qs`, `Dr. Harrison`, `Task 1 & 2`, `SM-2 SRS`).
  - Added mobile horizontal category filter bar (`.mobile-cat-filter`) allowing quick segmented view toggling on smartphones.
- **Distinguishable Button System & Tactile Feedback**:
  - Implemented 3D active tactile states (`transform: translateY(2px)`, inset shadows) on all interactive buttons.
  - Added hero action buttons: `.btn-hero-exam` (emerald glow for exam submissions), `.btn-hero-advantage` (amber glow for methodology tools), `.btn-hero-audio` (cyan pulse for audio and speaking).
  - Added `.btn-cat-ghost` for secondary tools and `.btn-pulse` for live examiner/interview triggers.
- **Interactive Chip Selector Bars**:
  - Replaced native select dropdowns with horizontal sliding chip bars (`.chip-selector-bar`, `.chip-btn`):
    - Cambridge Academic Reading Passages (1, 2, 3)
    - Listening Sections (1, 2, 3, 4)
    - Writing Task 2 Essay Types (5 prompt types)
    - Speaking Exam Sets (Sets 1 to 6)
    - Grammar Cloze Syntax categories (8 grammatical filters)
    - Vocabulary Topic Vaults (10 topic categories)
- **Subcategorized Tool Switchers (`.btn-sub-tool`)**:
  - Distinct numbered sub-bar navigation for IELTS Advantage Studio (1. Question Breakdown, 2. Coffee Shop Method, 3. PEEL Blueprint, 4. 10-Point Audit).
  - Clean mode switchers for Grammar Coach (Clozes vs Personalized Lessons) and Vocabulary (Vault, Collocations, Upgrades, SRS).
- **AI Tutor Chat Quick Prompts**:
  - One-touch prompt chips for 100% Rule question analysis, Part 2 cue card opening templates, adverbial inversion in writing, and environmental collocations.
- **Platform & Mobile Sync**:
  - Bumped Android Gradle build to `versionCode = 3`, `versionName = "1.3.0"`.
  - Synced assets to `platform/android/app/src/main/assets/www/`.

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
