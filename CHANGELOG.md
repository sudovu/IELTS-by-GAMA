# Changelog - IELTS by GAMA

All notable changes to the **IELTS by GAMA** platform and native Android applications are documented in this file.

The versioning follows the convention:
- **Major.Minor.Patch** (e.g. `v1.2.0`)
- **Small changes / bug fixes / patches**: `1.1.1`, `1.2.1`, etc.
- **Big changes / feature additions**: `1.2.0`, `1.3.0`, etc.

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
