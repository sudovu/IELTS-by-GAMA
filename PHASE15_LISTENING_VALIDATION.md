# PHASE 15 — LISTENING REAL AUDIO & MODALITY VALIDATION REPORT

**Project:** IELTS by GAMA  
**Phase:** 15 — Independent Product Verification  
**Auditor Role:** Audio & Speech Processing Engineer, QA Tester  

---

## 1. Modality Classification & Honest Disclosure

The listening implementation was audited to establish what audio technology is present on disk and in memory:

| Category | Definition | Present in IELTS by GAMA? |
|:---|:---|:---:|
| **A. Pre-recorded Studio Audio** | Pre-recorded human MP3/WAV/AAC audio files recorded by native voice actors in studio conditions. | **NO (0 bundled studio MP3 files)** |
| **B. Synthetic Speech (TTS)** | Spoken audio rendered in real-time from dialogue scripts using client-side Web Speech API (`SpeechSynthesisUtterance`) or OS TTS engines (`AndroidTTS`). | **YES (Primary Modality)** |
| **C. Transcript Practice** | Text-based reading and note-taking exercises without auditory playback. | **YES (Fallback Modality)** |

---

## 2. Reproduction of Phase 14 Audio Playback Defect

### 2.1 The Issue
In Phase 14, `ExamContentRepository.sanitize_for_client()` executed:
```python
if "sections" in sanitized:
    for s in sanitized["sections"]:
        s.pop("synonym_table", None)
        # Hide audio script in exam mode
        s.pop("audio_script", None)
```
Because `audio_script` was deleted from the pre-submission client payload, `item.stimulusAudioScript` on the client evaluated to `undefined` or `""`.  
When the learner clicked **"▶️ Play Audio"**, the frontend function `toggleExamAudioPlayback` checked:
```javascript
if (!scriptText || scriptText.trim().length === 0) {
    alert("No audio dialogue script available for this section.");
    return;
}
```
**Outcome:** The audio synthesizer failed with an alert, completely preventing any audio playback during the examination.

### 2.2 The Correction
1. In `core/exam/content_repository.py`: Preserved `audio_script` on sanitized section dictionaries so the browser TTS synthesizer has the speech text to read.
2. Verified that answer keys (`correct`, `acceptable`, `evidence`, `distractor_note`, `synonym_table`) remain strictly scrubbed.
3. In `ui/static/app.js`: Refactored `toggleExamAudioPlayback()` so that it directly pulls `item.stimulusAudioScript` from the in-memory question model rather than passing multi-paragraph text through inline HTML string interpolation.
4. Added `onerror` handler to gracefully reset the button state to `"▶️ Play Audio"` if browser speech synthesis encounters an interrupted state.

---

## 3. Playback Verification Under Various Device Conditions

| Test Condition | Expected Behavior | Observed Behavior | Status |
|:---|:---|:---|:---:|
| **Speech Playback Start** | Utterance begins, button toggles to `⏸️ Pause Audio` | Verified with British English voice (`en-GB`) at 0.95x speed | **PASS** |
| **Speech Playback Completion** | Utterance finishes, button reverts to `▶️ Play Audio` | `utterance.onend` triggered; UI reset cleanly | **PASS** |
| **Playback Interruption** | Clicking Pause or Stop cancels synthesis | `window.speechSynthesis.cancel()` called cleanly | **PASS** |
| **Browser Without Speech API** | Alert user and allow text fallback | Displays fallback notice; user can still input answers | **PASS** |
| **Simultaneous Timer Operation** | Exam countdown timer continues uninterrupted | Timer runs smoothly while audio speaks | **PASS** |
| **Answer Concealment** | Script is spoken; answer keys are NOT displayed | Dialogue is vocalized while question answers remain hidden | **PASS** |

---

## 4. Limitations & Recommendations for Real Learners

1. **Synthetic Voice Variations:** Web Speech synthesis uses the device's installed TTS engine. On Windows, it typically invokes Microsoft Natural voices; on Android, Google TTS; on iOS, Apple Siri/Samantha voices. Accents and naturalness vary by operating system.
2. **One-Time Listening Simulation:** In official IELTS Listening, audio is heard only once. While the interface permits replaying for study convenience, learners preparing for real exams are advised to attempt the questions after a single play.
3. **No Claim of Official Studio Audio:** The platform explicitly displays:  
   *"Audio Simulation (Web Speech Synthesizer) • Pre-recorded Cambridge studio audio files are not bundled."*
