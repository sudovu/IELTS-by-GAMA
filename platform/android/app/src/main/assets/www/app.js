/**
 * IELTS by GAMA - Frontend Client Application
 * Hybrid Online + Offline AI English Tutor
 * Features dual-mode networking: REST API with zero-network standalone offline fallback.
 */

const API_BASE = "";

// State
let appState = {
  currentTab: "dashboard",
  connectivity: "OFFLINE",
  forcedOffline: false,
  srsDeck: [],
  currentCardIdx: 0,
  speakingTimerInterval: null,
  speakingSeconds: 0
};

// -------------------------------------------------------------
// Offline Standalone Client Engine (for Android APK & No-Server runtimes)
// -------------------------------------------------------------
const OfflineLocalEngine = {
  getProfile() {
    const raw = localStorage.getItem("gama_profile");
    if (raw) return JSON.parse(raw);
    return {
      name: "Learner",
      current_band: 5.5,
      target_band: 7.0,
      cefr_level: "B2",
      daily_minutes: 30,
      track: "Academic"
    };
  },
  saveProfile(p) {
    localStorage.setItem("gama_profile", JSON.stringify(p));
  },
  getMistakes() {
    const raw = localStorage.getItem("gama_mistakes");
    return raw ? JSON.parse(raw) : [
      {
        id: "m_init",
        skill: "grammar",
        category: "Subject-Verb Agreement",
        original_text: "I am agree with this point",
        corrected_text: "I agree with this point",
        explanation: "'Agree' is an action verb in English and does not use 'am' in simple present.",
        recurrence_count: 2,
        mastery_score: 0.3,
        status: "needs_improvement"
      }
    ];
  },
  saveMistakes(m) {
    localStorage.setItem("gama_mistakes", JSON.stringify(m));
  },
  getSRS() {
    const raw = localStorage.getItem("gama_srs");
    return raw ? JSON.parse(raw) : [
      {
        id: "srs_1",
        item_type: "vocabulary",
        key_term: "substantial",
        prompt: "Define 'substantial' and provide an academic IELTS example.",
        answer: "Adjective: Of considerable importance, size, or worth.\nExample: 'There has been a substantial increase in public transport usage.'",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_2",
        item_type: "collocation",
        key_term: "make a decision",
        prompt: "Complete natural academic collocation: 'Citizens must _____ (make / do) a decision.'",
        answer: "Collocation: make a decision (unnatural: 'do a decision').",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_3",
        item_type: "phrasal_verb",
        key_term: "account for",
        prompt: "What is the meaning and formal alternative of 'account for'?",
        answer: "Meaning: To constitute or make up a proportion.\nFormal Alternative: constitute / comprise (e.g. 'Renewables accounted for 28% of total power').",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      }
    ];
  },
  saveSRS(deck) {
    localStorage.setItem("gama_srs", JSON.stringify(deck));
  },
  handleRequest(url, method = "GET", body = null) {
    const p = url.replace(API_BASE, "");

    if (p === "/api/status") {
      const isTablet = window.innerWidth >= 768;
      return {
        connectivity: appState.forcedOffline ? "● OFFLINE" : (navigator.onLine ? "● ONLINE" : "● OFFLINE"),
        is_online: !appState.forcedOffline && navigator.onLine,
        forced_offline: appState.forcedOffline,
        hardware_profile: isTablet ? "TABLET (Large Screen)" : "MOBILE",
        model_name: "GAM IELTS Nano (Offline)"
      };
    }

    if (p === "/api/dashboard") {
      const prof = this.getProfile();
      const mistakes = this.getMistakes();
      const srs = this.getSRS();
      const activeMistakes = mistakes.filter(m => m.status !== "mastered");
      return {
        dashboard: {
          learner_profile: prof,
          overall_band_estimate: prof.current_band,
          target_band: prof.target_band,
          cefr_level: prof.cefr_level,
          track: prof.track,
          skills_radar: {
            "Grammar": 6.5,
            "Vocabulary": 6.5,
            "Reading": 6.0,
            "Listening": 6.5,
            "Writing": prof.current_band,
            "Speaking": 6.0,
            "Fluency": 6.0,
            "Pronunciation": 6.5
          },
          mistake_book_metrics: {
            active_mistakes_count: activeMistakes.length,
            mastered_count: mistakes.length - activeMistakes.length,
            accuracy_rate_percent: mistakes.length ? Math.round(((mistakes.length - activeMistakes.length) / mistakes.length) * 100) : 100
          },
          srs_metrics: {
            items_due_today: srs.length
          }
        },
        daily_plan: {
          daily_greeting: `Good morning! You have ${prof.daily_minutes} minutes planned today. Estimated Band: ${prof.current_band} | Target: ${prof.target_band}. Ready to practice?`,
          tasks: [
            { title: "Vocabulary SRS Drills", duration_minutes: 10, description: "Review due SuperMemo SM-2 flashcards." },
            { title: "Targeted Weakness Practice", duration_minutes: 10, description: "Resolve flagged errors from your Mistake Book." },
            { title: "IELTS Core Module Practice", duration_minutes: 10, description: "Practice Reading passage or Speaking Part 2 cue card." }
          ]
        }
      };
    }

    if (p === "/api/srs/due") {
      return { items: this.getSRS() };
    }

    if (p === "/api/srs/review") {
      const deck = this.getSRS();
      const item = deck.find(c => c.id === body.item_id);
      if (item) {
        const grade = body.grade || 4;
        if (grade >= 3) {
          item.interval_days = item.repetition === 0 ? 1.0 : (item.repetition === 1 ? 6.0 : Math.round(item.interval_days * item.ease_factor));
          item.repetition++;
        } else {
          item.interval_days = 1.0;
          item.repetition = 0;
        }
        item.ease_factor = Math.max(1.3, item.ease_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02)));
        this.saveSRS(deck);
      }
      return { success: true };
    }

    if (p === "/api/mistakes") {
      const list = this.getMistakes();
      return {
        summary: { categories: [{ skill: "grammar", category: "Subject-Verb Agreement", total_occurrences: list.length, avg_mastery: 0.5 }] },
        active_mistakes: list
      };
    }

    if (p === "/api/mistakes/review") {
      const list = this.getMistakes();
      const item = list.find(m => m.id === body.mistake_id);
      if (item) {
        item.status = "mastered";
        item.mastery_score = 1.0;
        this.saveMistakes(list);
      }
      return { success: true };
    }

    if (p === "/api/reading") {
      return {
        id: "acad_p1",
        track: "Academic",
        title: "The Architecture of Deep-Sea Hydrothermal Ecosystems",
        text: "Deep-sea hydrothermal vents, discovered in 1977 along the Galapagos Rift, represent one of the most remarkable biological frontiers on Earth. Located thousands of meters beneath the oceanic surface where sunlight cannot penetrate, these geological formations dispel the historical assumption that all complex ecosystems rely fundamentally on solar photosynthesis. Instead, these abyssal biomes are sustained through chemosynthesis, a process mediated by specialized extremophilic bacteria.\n\nAs tectonic plates diverge, seawater infiltrates subterranean fissures, reaching temperatures exceeding 400 degrees Celsius near magma chambers. Saturated with dissolved minerals—predominantly hydrogen sulfide, iron, and copper—the superheated water precipitates violently upon encountering the frigid, near-freezing ambient ocean. This reaction constructs towering mineralized chimneys colloquially known as 'black smokers'.\n\nThe organisms flourishing around these vents exhibit astounding biological adaptations. Giant tube worms (Riftia pachyptila), which can reach lengths of over two meters, completely lack a digestive tract, mouth, or gut. Instead, they harbor billions of symbiotic sulfur-oxidizing bacteria within an organ called the trophosome. The tube worms extract hydrogen sulfide and oxygen from the hydrothermal fluid using vascularized red plumes, transferring these compounds to the endosymbionts, which synthesize organic nourishment for the host.\n\nNevertheless, these thriving oasis communities are exceptionally ephemeral. Because tectonic shifts and volcanic eruptions routinely seal hydrothermal conduits or open new subterranean fractures, vents can abruptly shut down within a matter of decades. Consequently, hydrothermal vent fauna have developed rapid larval dispersion mechanisms capable of traversing vast expanses of inhospitable abyssal desert to locate newly forming vents.",
        questions: [
          { num: 1, type: "TFNG", prompt: "Deep-sea hydrothermal ecosystems require solar radiation to produce fundamental nutrients." },
          { num: 2, type: "TFNG", prompt: "Giant tube worms absorb nourishment directly through their mouths." },
          { num: 3, type: "TFNG", prompt: "Vents remain active continuously for millions of years in the same location." },
          { num: 4, type: "Completion", prompt: "The mineral chimneys formed by superheated hydrothermal fluids are colloquially called _____ (NO MORE THAN TWO WORDS)." }
        ]
      };
    }

    if (p === "/api/reading/submit") {
      const ans = body.answers || {};
      let correct = 0;
      if ((ans["1"] || "").toLowerCase() === "false") correct++;
      if ((ans["2"] || "").toLowerCase() === "false") correct++;
      if ((ans["3"] || "").toLowerCase() === "false") correct++;
      if ((ans["4"] || "").toLowerCase().includes("black smoker")) correct++;
      const band = correct === 4 ? 8.0 : (correct === 3 ? 7.0 : (correct >= 2 ? 6.0 : 5.0));
      return {
        estimated_band: band,
        correct_answers: correct,
        total_questions: 4,
        disclaimer: "Practice estimate only. Not an official IELTS result."
      };
    }

    if (p === "/api/listening") {
      return {
        id: "sec_1",
        section_number: 1,
        title: "University Campus Accommodation Booking",
        audio_script: "OFFICER: Good morning, Campus Housing Office. How can I help you today?\nSTUDENT: Hello. I'd like to inquire about booking a room in the university halls for the upcoming semester.\nOFFICER: Certainly. Could I first take your full name, please?\nSTUDENT: Yes, it's Julian Sterling. That's S-T-E-R-L-I-N-G.\nOFFICER: Thank you, Julian. And what faculty are you enrolled in?\nSTUDENT: I'm starting a master's program in Biomedical Science.\nOFFICER: Excellent. Now, regarding room preferences, we have standard single rooms with shared facilities or en-suite studio rooms.\nSTUDENT: I'd strongly prefer an en-suite room if possible. I need a quiet study environment.\nOFFICER: Right. An en-suite room in Oakwood Lodge is available. The standard price is 240 pounds per week, but because you are booking for the full academic term, a student subsidy applies, bringing it down to 210 pounds per week.\nSTUDENT: 210 pounds sounds very reasonable. And when would the tenancy officially commence?\nOFFICER: Key collection starts on the 18th of September, though orientation begins three days earlier.\nSTUDENT: Wonderful. I'll reserve that.",
        questions: [
          { num: 1, prompt: "Applicant's surname: _____" },
          { num: 2, prompt: "Preferred room type: _____ room" },
          { num: 3, prompt: "Discounted weekly rent: £_____" },
          { num: 4, prompt: "Date of key collection: 18th of _____" }
        ]
      };
    }

    if (p === "/api/listening/submit") {
      const ans = body.answers || {};
      let correct = 0;
      if ((ans["1"] || "").toLowerCase().includes("sterling")) correct++;
      if ((ans["2"] || "").toLowerCase().includes("suite")) correct++;
      if ((ans["3"] || "").includes("210")) correct++;
      if ((ans["4"] || "").toLowerCase().includes("september")) correct++;
      const band = correct === 4 ? 8.0 : (correct === 3 ? 7.0 : (correct >= 2 ? 6.0 : 5.0));
      return {
        estimated_band: band,
        correct_answers: correct,
        total_questions: 4,
        disclaimer: "Practice estimate only. Not an official IELTS result."
      };
    }

    if (p === "/api/writing/evaluate") {
      const text = body.essay_text || "";
      const words = text.trim().split(/\s+/).filter(w => w.length > 0);
      const wordCount = words.length;

      let tr = wordCount >= 250 ? 7.0 : 5.5;
      let cc = text.toLowerCase().includes("furthermore") || text.toLowerCase().includes("in conclusion") ? 7.0 : 6.0;
      let lr = text.toLowerCase().includes("crucial") || text.toLowerCase().includes("significant") ? 7.0 : 6.0;
      let gra = 6.5;

      const formative = [];
      if (text.toLowerCase().includes("i am agree")) {
        gra = 5.5;
        formative.push({
          original: "I am agree with this idea",
          correction: "I agree with this idea",
          why: "'Agree' is an action verb in English and does not use the auxiliary 'am' in simple present.",
          better_alternative: "I strongly subscribe to this perspective / I concur with this notion.",
          practice_exercise: "Choose: 'I _____ (agree / am agree) that education fosters social mobility.'"
        });
      }

      const rawAvg = (tr + cc + lr + gra) / 4.0;
      const roundedBand = Math.round(rawAvg * 2) / 2;

      return {
        estimated_band: roundedBand,
        word_count: wordCount,
        underlength_penalty: wordCount < 250 ? 1.0 : 0.0,
        criteria: {
          "Task Response": tr,
          "Coherence and Cohesion": cc,
          "Lexical Resource": lr,
          "Grammatical Range and Accuracy": gra
        },
        formative_corrections: formative,
        disclaimer: "Practice estimate only. Not an official IELTS result."
      };
    }

    if (p === "/api/speaking/evaluate") {
      const transcript = body.transcript || "";
      const duration = body.duration_seconds || 60.0;
      const words = transcript.trim().split(/\s+/).filter(w => w.length > 0);
      const wpm = Math.round((words.length / (duration / 60.0)));
      const fillers = (transcript.match(/\b(um|uh|like|you know|basically)\b/gi) || []).length;
      const fc = wpm >= 115 && wpm <= 165 ? 7.0 : 6.0;

      return {
        estimated_band: fc,
        fluency_metrics: {
          words_per_minute: wpm,
          target_wpm_range: "120 - 150 WPM",
          total_filler_words: fillers,
          filler_percentage: words.length ? Math.round((fillers / words.length) * 100) : 0,
          feedback: wpm >= 115 ? "Smooth speaking cadence and natural pacing." : "Work on continuous expression to avoid hesitant pauses."
        },
        disclaimer: "Practice estimate only. Not an official IELTS result."
      };
    }

    if (p === "/api/diagnostic/questions") {
      return {
        questions: [
          { id: "g1", skill: "grammar", category: "Tenses & Conditionals", prompt: "If funding _____ (increase) next year, scientists will expand clinical trials.", options: ["increases", "will increase", "increased", "would increase"] },
          { id: "g2", skill: "grammar", category: "Subject-Verb Agreement", prompt: "The collection of historical artifacts _____ (has/have) been archived.", options: ["has", "have", "are", "were"] },
          { id: "v1", skill: "vocabulary", category: "Collocations", prompt: "The survey revealed a _____ (profound/deep) discrepancy in demographic patterns.", options: ["profound", "deep", "heavy", "dense"] },
          { id: "v2", skill: "vocabulary", category: "Phrasal Verbs", prompt: "The committee agreed to _____ (carry out / give in) the recommendations.", options: ["carry out", "give in", "look on", "take up"] },
          { id: "r1", skill: "reading", category: "Inference", prompt: "Passage: 'Solar adoption surged in cities, but rural zones rely on biomass.' True, False, or Not Given: Rural areas primarily use solar power.", options: ["False", "True", "Not Given"] },
          { id: "l1", skill: "listening", category: "Form Completion", prompt: "Speaker: 'The venue is Henderson Auditorium.' Question: The venue is Henderson _____.", options: ["Auditorium", "Hall", "Library", "Center"] }
        ]
      };
    }

    if (p === "/api/diagnostic/submit") {
      const answers = body.answers || {};
      let correct = 0;
      if (answers["g1"] === "increases") correct++;
      if (answers["g2"] === "has") correct++;
      if (answers["v1"] === "profound") correct++;
      if (answers["v2"] === "carry out") correct++;
      if (answers["r1"] === "False") correct++;
      if (answers["l1"] === "Auditorium") correct++;

      const pct = Math.round((correct / 6) * 100);
      const estBand = correct >= 5 ? 7.0 : (correct >= 4 ? 6.5 : (correct >= 3 ? 5.5 : 4.5));
      const cefr = correct >= 5 ? "C1" : (correct >= 4 ? "B2" : (correct >= 3 ? "B1" : "A2"));

      const prof = this.getProfile();
      prof.current_band = estBand;
      prof.cefr_level = cefr;
      this.saveProfile(prof);

      return {
        accuracy_percent: pct,
        correct_count: correct,
        total_questions: 6,
        estimated_cefr: cefr,
        estimated_ielts_range: `${estBand} - ${estBand + 0.5}`,
        estimated_band: estBand,
        strengths: ["Reading Comprehension", "Vocabulary Recognition"],
        priority_skills: ["Academic Writing Task 2", "Complex Grammar Inversion"],
        recommended_study_plan: `Focus on Writing Task 2 and daily Spaced Repetition flashcards to advance toward Band ${prof.target_band}.`
      };
    }

    if (p === "/api/grammar/adaptive") {
      return {
        target_category: "Subject-Verb Agreement",
        message: "Personalized focus: Mastering complex subject-verb concordance in IELTS essays.",
        lesson: {
          title: "Subject-Verb Concordance in Academic Clauses",
          rules: [
            "Intervening prepositional phrases do not change subject plurality: 'The quality of the essays is exceptional.'",
            "Quantified expressions like 'each of' and 'neither of' take a singular verb.",
            "Compound subjects connected by 'and' take a plural verb."
          ],
          academic_tip: "Double-check clauses where the noun adjacent to the verb is plural but the head subject is singular."
        }
      };
    }

    if (p === "/api/chat") {
      const msg = (body.message || "").toLowerCase();
      const mistakes = [];

      if (msg.includes("i am agree")) {
        mistakes.push({
          original: "I am agree",
          correction: "I agree",
          why: "'Agree' is a full verb in English and does not use the auxiliary 'am' in simple present."
        });
      }

      let reply = "I am ready to help you prepare for IELTS. What would you like to practice: Grammar, Vocabulary, Reading, Writing, or Speaking?";

      if (msg.includes("affect") && msg.includes("effect")) {
        reply = "**'Affect' vs 'Effect'**:\n\n• **Affect** is almost always a **verb** meaning 'to influence':\n  *\"Technological changes directly affect the workforce.\"*\n\n• **Effect** is almost always a **noun** meaning 'the result':\n  *\"The legislation had a profound effect on emissions.\"*\n\n**Memory Tip (RAVEN)**:\n**R**emember: **A**ffect = **V**erb, **E**ffect = **N**oun.";
      } else if (msg.includes("task 2") || msg.includes("writing prompt")) {
        reply = "**IELTS Academic Writing Task 2 Prompt**:\n\n> *Some educationalists argue that high school curricula should prioritize STEM subjects over artistic fields. To what extent do you agree or disagree?*\n\nAim for 250+ words with a clear thesis and supporting examples.";
      } else if (msg.includes("part 2") || msg.includes("cue card")) {
        reply = "**IELTS Speaking Part 2 Cue Card**:\n\n**Describe an ambitious goal you achieved.**\n• What the goal was\n• When you pursued it\n• What challenges arose\n• Why it was meaningful to you.";
      } else if (mistakes.length > 0) {
        reply = "I noticed a grammatical structure to refine:\n\n• **Original:** *\"I am agree\"*\n• **Correction:** *\"I agree\"*\n• **Better Alternative:** *\"I strongly concur with this point of view.\"*";
      }

      return {
        reply,
        provider: "Offline Local Engine",
        is_offline: true,
        detected_mistakes: mistakes
      };
    }

    if (p === "/api/settings/offline_toggle") {
      appState.forcedOffline = body.forced_offline;
      return {
        forced_offline: appState.forcedOffline,
        status: appState.forcedOffline ? "● OFFLINE" : (navigator.onLine ? "● ONLINE" : "● OFFLINE")
      };
    }

    if (p === "/api/export") {
      return {
        data: JSON.stringify({
          profile: this.getProfile(),
          mistakes: this.getMistakes(),
          srs: this.getSRS()
        }, null, 2)
      };
    }

    if (p === "/api/import") {
      try {
        const parsed = JSON.parse(body.data);
        if (parsed.profile) this.saveProfile(parsed.profile);
        if (parsed.mistakes) this.saveMistakes(parsed.mistakes);
        if (parsed.srs) this.saveSRS(parsed.srs);
        return { restored_mistakes: (parsed.mistakes || []).length };
      } catch (e) {
        return { restored_mistakes: 0 };
      }
    }

    return {};
  }
};

// Unified API Caller (Server First, Offline Client Engine Fallback)
async function callApi(endpoint, method = "GET", data = null) {
  // If forced offline, on file: protocol, or server unreachable -> use OfflineLocalEngine
  if (appState.forcedOffline || window.location.protocol === "file:" || !API_BASE) {
    try {
      if (window.location.protocol !== "file:") {
        const res = await fetch(`${API_BASE}${endpoint}`, {
          method,
          headers: { "Content-Type": "application/json" },
          body: data ? JSON.stringify(data) : null
        });
        if (res.ok) return await res.json();
      }
    } catch (err) {
      // Graceful fallback to client engine
    }
    return OfflineLocalEngine.handleRequest(endpoint, method, data);
  }

  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      method,
      headers: { "Content-Type": "application/json" },
      body: data ? JSON.stringify(data) : null
    });
    if (res.ok) return await res.json();
  } catch (e) {
    // Fall back to offline engine
  }
  return OfflineLocalEngine.handleRequest(endpoint, method, data);
}

// -------------------------------------------------------------
// DOM Lifecycle & Controller Initializations
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  initScreenSizeManager();
  initNavigation();
  initThemeToggle();
  initOfflineToggle();
  initChat();
  initDashboard();
  initDiagnostic();
  initGrammar();
  initVocabSRS();
  initReading();
  initListening();
  initWriting();
  initSpeaking();
  initMistakeBook();
  initSettings();

  checkStatus();
  setInterval(checkStatus, 6000);
});

// -------------------------------------------------------------
// Dynamic Screen Size Grabber & Universal Layout Adapter
// -------------------------------------------------------------
function initScreenSizeManager() {
  function updateScreenMetrics() {
    const w = window.innerWidth || document.documentElement.clientWidth;
    const h = window.innerHeight || document.documentElement.clientHeight;
    const dpr = (window.devicePixelRatio || 1).toFixed(1);
    const isLandscape = w > h;
    const orientation = isLandscape ? "landscape" : "portrait";

    // Set dynamic viewport CSS variables for pixel-perfect viewport fitting
    document.documentElement.style.setProperty("--app-width", `${w}px`);
    document.documentElement.style.setProperty("--app-height", `${h}px`);
    document.documentElement.style.setProperty("--vh", `${h * 0.01}px`);

    let tier = "desktop";
    let tierLabel = "DESKTOP";
    if (w < 600) {
      tier = "phone";
      tierLabel = "PHONE";
    } else if (w < 768) {
      tier = "mobile-large";
      tierLabel = "PHABLET";
    } else if (w < 1024) {
      tier = "tablet";
      tierLabel = "TABLET";
    } else if (w < 1440) {
      tier = "tablet-landscape";
      tierLabel = "TABLET HD";
    }

    document.body.setAttribute("data-screen-tier", tier);
    document.body.setAttribute("data-orientation", orientation);

    // Live update in sidebar footer
    const devLabel = document.getElementById("deviceProfileLabel");
    if (devLabel) {
      devLabel.textContent = `${tierLabel} (${w}×${h})`;
    }

    // Live update in Developed by GAMA card
    const devSpec = document.getElementById("devScreenSpec");
    if (devSpec) {
      devSpec.textContent = `${w}×${h} px (${tierLabel} • ${dpr}x DPR)`;
    }

    // Live subtitle badge in header
    const screenBadge = document.getElementById("screenDimensionBadge");
    if (screenBadge) {
      screenBadge.textContent = `${tierLabel} • ${w}×${h} • Offline-Ready`;
    }
  }

  updateScreenMetrics();

  window.addEventListener("resize", () => {
    updateScreenMetrics();
  }, { passive: true });

  window.addEventListener("orientationchange", () => {
    setTimeout(updateScreenMetrics, 150);
  });

  if (window.visualViewport) {
    window.visualViewport.addEventListener("resize", () => {
      updateScreenMetrics();
    }, { passive: true });
  }
}

function initNavigation() {
  const items = document.querySelectorAll(".nav-item");
  items.forEach(item => {
    item.addEventListener("click", () => {
      const targetTab = item.getAttribute("data-tab");
      switchTab(targetTab);
    });
  });
}

function switchTab(tabId) {
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
  document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));

  const targetNav = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
  const targetPane = document.getElementById(`tab-${tabId}`);
  if (targetNav && targetPane) {
    targetNav.classList.add("active");
    targetPane.classList.add("active");
    appState.currentTab = tabId;

    if (tabId === "dashboard") loadDashboard();
    if (tabId === "vocab") loadSRSDeck();
    if (tabId === "mistakes") loadMistakes();
  }
}

async function checkStatus() {
  const data = await callApi("/api/status");
  if (data) {
    updateStatusBadge(data.connectivity, data.forced_offline);
    document.getElementById("deviceProfileLabel").innerText = data.hardware_profile;
    document.getElementById("modelNameLabel").innerText = data.model_name;
  }
}

function updateStatusBadge(indicator, forced) {
  const badge = document.getElementById("connectivityBadge");
  const text = document.getElementById("statusText");
  const btn = document.getElementById("toggleOfflineBtn");
  text.innerText = indicator.replace("● ", "");

  if (indicator.includes("ONLINE")) {
    badge.className = "status-badge";
  } else {
    badge.className = "status-badge offline";
  }

  appState.forcedOffline = forced;
  btn.innerText = `Force Offline: ${forced ? "ON" : "OFF"}`;
  btn.className = forced ? "btn btn-danger btn-sm" : "btn btn-secondary btn-sm";
}

function initOfflineToggle() {
  const btn = document.getElementById("toggleOfflineBtn");
  btn.addEventListener("click", async () => {
    const nextState = !appState.forcedOffline;
    const data = await callApi("/api/settings/offline_toggle", "POST", { forced_offline: nextState });
    if (data) updateStatusBadge(data.status, data.forced_offline);
  });
}

function initThemeToggle() {
  const btn = document.getElementById("themeToggleBtn");
  btn.addEventListener("click", () => {
    document.body.classList.toggle("light-theme");
  });
}

// Dashboard
async function initDashboard() {
  await loadDashboard();
}

async function loadDashboard() {
  const data = await callApi("/api/dashboard");
  if (data) {
    const d = data.dashboard;
    const p = data.daily_plan;

    document.getElementById("dailyGreetingText").innerText = p.daily_greeting;
    document.getElementById("currentBandMetric").innerText = d.overall_band_estimate;
    document.getElementById("targetBandMetric").innerText = d.target_band;
    document.getElementById("cefrMetric").innerText = `CEFR Level: ${d.cefr_level}`;
    document.getElementById("srsDueMetric").innerText = d.srs_metrics.items_due_today;
    document.getElementById("activeMistakesMetric").innerText = d.mistake_book_metrics.active_mistakes_count;
    document.getElementById("accuracyRateMetric").innerText = `Accuracy: ${d.mistake_book_metrics.accuracy_rate_percent}%`;

    const taskList = document.getElementById("dailyPlanTasksList");
    taskList.innerHTML = "";
    p.tasks.forEach(t => {
      const div = document.createElement("div");
      div.className = "task-item";
      div.innerHTML = `<strong>${t.title} (${t.duration_minutes}m)</strong><p>${t.description}</p>`;
      taskList.appendChild(div);
    });

    const radarBox = document.getElementById("skillsRadarBox");
    radarBox.innerHTML = "";
    for (const [skill, score] of Object.entries(d.skills_radar)) {
      const row = document.createElement("div");
      row.className = "radar-bar-row";
      const pct = Math.round((score / 9.0) * 100);
      row.innerHTML = `
        <span style="width: 100px;">${skill}</span>
        <div class="bar-track"><div class="bar-fill" style="width: ${pct}%;"></div></div>
        <span>Band ${score}</span>
      `;
      radarBox.appendChild(row);
    }
  }
}

// Chat
function initChat() {
  const input = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendMessageBtn");
  const voiceBtn = document.getElementById("voiceInputBtn");

  sendBtn.addEventListener("click", sendChatMessage);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendChatMessage();
  });

  if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognizer = new SpeechRecognition();
    recognizer.lang = "en-US";
    recognizer.continuous = false;

    voiceBtn.addEventListener("click", () => {
      voiceBtn.innerText = "🔴 Listening...";
      recognizer.start();
    });

    recognizer.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      input.value = transcript;
      voiceBtn.innerText = "🎙️";
      sendChatMessage();
    };
    recognizer.onerror = () => { voiceBtn.innerText = "🎙️"; };
    recognizer.onend = () => { voiceBtn.innerText = "🎙️"; };
  } else {
    voiceBtn.style.display = "none";
  }
}

async function sendChatMessage() {
  const input = document.getElementById("chatInput");
  const text = input.value.trim();
  if (!text) return;
  input.value = "";

  appendChatMessage("user", text);

  const data = await callApi("/api/chat", "POST", { message: text });
  if (data) {
    appendChatMessage("tutor", data.reply, data.detected_mistakes);
    speakText(data.reply.slice(0, 140));
  }
}

function appendChatMessage(role, content, mistakes = []) {
  const container = document.getElementById("chatMessages");
  const msgDiv = document.createElement("div");
  msgDiv.className = `message ${role}`;

  let mistakeAlert = "";
  if (mistakes && mistakes.length > 0) {
    mistakeAlert = `<div style="margin-top: 8px; padding: 6px 10px; background: rgba(239, 68, 68, 0.15); border-left: 3px solid #ef4444; border-radius: 4px; font-size: 0.8rem;">
      <strong>Mistake Intercepted:</strong> "${mistakes[0].original}" -> <em>"${mistakes[0].correction}"</em>
    </div>`;
  }

  msgDiv.innerHTML = `<div class="msg-bubble">${escapeHtml(content)}${mistakeAlert}</div>`;
  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function speakText(text) {
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[*_#>`]/g, "");
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.lang = "en-GB";
    window.speechSynthesis.speak(utterance);
  }
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Diagnostic
async function initDiagnostic() {
  const data = await callApi("/api/diagnostic/questions");
  if (data && data.questions) {
    const container = document.getElementById("diagnosticQuestionsContainer");
    container.innerHTML = "";
    data.questions.forEach((q, idx) => {
      const div = document.createElement("div");
      div.className = "mb-3";
      div.innerHTML = `
        <p><strong>Q${idx + 1} [${q.skill.toUpperCase()} - ${q.category}]:</strong> ${q.prompt}</p>
        <div class="options-group mt-1">
          ${q.options.map(opt => `
            <label style="display: block; margin: 4px 0;">
              <input type="radio" name="diag_${q.id}" value="${opt}"> ${opt}
            </label>
          `).join("")}
        </div>
      `;
      container.appendChild(div);
    });
  }

  document.getElementById("submitDiagnosticBtn").addEventListener("click", async () => {
    const answers = {};
    document.querySelectorAll("input[name^='diag_']:checked").forEach(input => {
      const qid = input.name.replace("diag_", "");
      answers[qid] = input.value;
    });

    const report = await callApi("/api/diagnostic/submit", "POST", { answers });
    if (report) {
      const repBox = document.getElementById("diagnosticReport");
      repBox.style.display = "block";
      repBox.innerHTML = `
        <h3>Diagnostic Results</h3>
        <p><strong>Accuracy:</strong> ${report.accuracy_percent}% (${report.correct_count}/${report.total_questions})</p>
        <p><strong>Estimated CEFR:</strong> ${report.estimated_cefr} | <strong>Practice IELTS Range:</strong> ${report.estimated_ielts_range}</p>
        <p><strong>Strengths:</strong> ${report.strengths.join(", ")}</p>
        <p><strong>Priority Focus:</strong> ${report.priority_skills.join(", ")}</p>
        <p><strong>Recommended Study Plan:</strong> ${report.recommended_study_plan}</p>
      `;
      loadDashboard();
    }
  });
}

// Adaptive Grammar
async function initGrammar() {
  const data = await callApi("/api/grammar/adaptive");
  if (data && data.lesson) {
    const container = document.getElementById("grammarSessionContent");
    container.innerHTML = `
      <h3>Targeted Focus: ${data.target_category}</h3>
      <p class="subtitle">${data.message}</p>
      <div class="rule-box mt-3" style="background: rgba(255,255,255,0.03); padding: 14px; border-radius: 8px;">
        <h4>${data.lesson.title}</h4>
        <ul>${data.lesson.rules.map(r => `<li>${r}</li>`).join("")}</ul>
        <p class="mt-2" style="color: var(--primary-accent);"><strong>Academic Tip:</strong> ${data.lesson.academic_tip}</p>
      </div>
    `;
  }
}

// Vocabulary & SRS
async function initVocabSRS() {
  document.getElementById("revealCardBtn").addEventListener("click", () => {
    document.getElementById("cardAnswerBox").style.display = "block";
    document.getElementById("revealCardBtn").style.display = "none";
  });
  await loadSRSDeck();
}

async function loadSRSDeck() {
  const data = await callApi("/api/srs/due");
  if (data) {
    appState.srsDeck = data.items || [];
    appState.currentCardIdx = 0;
    showCurrentCard();
  }
}

function showCurrentCard() {
  const promptEl = document.getElementById("cardPrompt");
  const answerEl = document.getElementById("cardAnswer");
  const answerBox = document.getElementById("cardAnswerBox");
  const revealBtn = document.getElementById("revealCardBtn");

  answerBox.style.display = "none";
  revealBtn.style.display = "inline-block";

  if (!appState.srsDeck || appState.srsDeck.length === 0 || appState.currentCardIdx >= appState.srsDeck.length) {
    promptEl.innerText = "No more cards due for review today! Excellent work!";
    revealBtn.style.display = "none";
    return;
  }

  const card = appState.srsDeck[appState.currentCardIdx];
  promptEl.innerText = card.prompt;
  answerEl.innerText = card.answer;
}

window.gradeCard = async function(grade) {
  const card = appState.srsDeck[appState.currentCardIdx];
  if (!card) return;
  await callApi("/api/srs/review", "POST", { item_id: card.id, grade });
  appState.currentCardIdx++;
  showCurrentCard();
  loadDashboard();
};

// Reading
async function initReading() {
  const passage = await callApi("/api/reading");
  if (passage) {
    document.getElementById("readingTitle").innerText = `${passage.title} (${passage.track})`;
    document.getElementById("readingText").innerText = passage.text;

    const qList = document.getElementById("readingQuestionsList");
    qList.innerHTML = "";
    (passage.questions || []).forEach(q => {
      const div = document.createElement("div");
      div.className = "mb-2";
      div.innerHTML = `
        <p><strong>Q${q.num} [${q.type}]:</strong> ${q.prompt}</p>
        <input type="text" id="read_ans_${q.num}" class="mt-1" style="width: 100%;" placeholder="Enter answer..." />
      `;
      qList.appendChild(div);
    });
  }

  document.getElementById("submitReadingBtn").addEventListener("click", async () => {
    const answers = {};
    document.querySelectorAll("input[id^='read_ans_']").forEach(input => {
      const num = input.id.replace("read_ans_", "");
      answers[num] = input.value;
    });

    const rep = await callApi("/api/reading/submit", "POST", { answers });
    if (rep) {
      const repBox = document.getElementById("readingScoreReport");
      repBox.style.display = "block";
      repBox.innerHTML = `
        <h3>Reading Score: Band ${rep.estimated_band}</h3>
        <p>Correct: ${rep.correct_answers} / ${rep.total_questions}</p>
        <p><em>${rep.disclaimer}</em></p>
      `;
    }
  });
}

// Listening
async function initListening() {
  let audioScript = "";
  const sec = await callApi("/api/listening");
  if (sec) {
    document.getElementById("listeningTitle").innerText = `Section ${sec.section_number}: ${sec.title}`;
    audioScript = sec.audio_script || "";
    document.getElementById("listeningTranscriptBox").innerText = audioScript;

    const qList = document.getElementById("listeningQuestionsList");
    qList.innerHTML = "";
    (sec.questions || []).forEach(q => {
      const div = document.createElement("div");
      div.className = "mb-2";
      div.innerHTML = `
        <p><strong>Q${q.num}:</strong> ${q.prompt}</p>
        <input type="text" id="list_ans_${q.num}" class="mt-1" style="width: 100%;" placeholder="Enter answer..." />
      `;
      qList.appendChild(div);
    });
  }

  document.getElementById("playAudioScriptBtn").addEventListener("click", () => {
    speakText(audioScript);
  });

  document.getElementById("toggleTranscriptBtn").addEventListener("click", () => {
    const box = document.getElementById("listeningTranscriptBox");
    box.style.display = box.style.display === "none" ? "block" : "none";
  });

  document.getElementById("submitListeningBtn").addEventListener("click", async () => {
    const answers = {};
    document.querySelectorAll("input[id^='list_ans_']").forEach(input => {
      const num = input.id.replace("list_ans_", "");
      answers[num] = input.value;
    });

    const rep = await callApi("/api/listening/submit", "POST", { answers });
    if (rep) {
      const repBox = document.getElementById("listeningScoreReport");
      repBox.style.display = "block";
      repBox.innerHTML = `
        <h3>Listening Score: Band ${rep.estimated_band}</h3>
        <p>Correct: ${rep.correct_answers} / ${rep.total_questions}</p>
        <p><em>${rep.disclaimer}</em></p>
      `;
    }
  });
}

// Writing
function initWriting() {
  const essayInput = document.getElementById("essayInput");
  const wordCountLabel = document.getElementById("wordCountLabel");

  essayInput.addEventListener("input", () => {
    const words = essayInput.value.trim().split(/\s+/).filter(w => w.length > 0);
    wordCountLabel.innerText = words.length;
  });

  document.getElementById("evaluateWritingBtn").addEventListener("click", async () => {
    const text = essayInput.value.trim();
    if (!text) return;

    const rep = await callApi("/api/writing/evaluate", "POST", { prompt_id: "acad_t2_stem", essay_text: text });
    if (rep) {
      const repBox = document.getElementById("writingEvalReport");
      repBox.style.display = "block";

      let criteriaHtml = "";
      for (const [cName, cScore] of Object.entries(rep.criteria)) {
        criteriaHtml += `<li><strong>${cName}:</strong> Band ${cScore}</li>`;
      }

      let formativeHtml = "";
      if (rep.formative_corrections && rep.formative_corrections.length > 0) {
        formativeHtml = "<h4 class='mt-3'>Teach Through Correction Feedback:</h4>";
        rep.formative_corrections.forEach(err => {
          formativeHtml += `<div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px; margin-top: 6px;">
            <p><strong>Original:</strong> "${err.original}"</p>
            <p><strong>Correction:</strong> "${err.correction}"</p>
            <p><strong>Why:</strong> ${err.why}</p>
            <p><strong>Better Alternative:</strong> <em>${err.better_alternative}</em></p>
          </div>`;
        });
      }

      repBox.innerHTML = `
        <h3>Estimated Overall Writing Band: ${rep.estimated_band}</h3>
        <p>Word Count: ${rep.word_count} words (Penalty: ${rep.underlength_penalty})</p>
        <ul>${criteriaHtml}</ul>
        ${formativeHtml}
        <p class='mt-2'><em>${rep.disclaimer}</em></p>
      `;
    }
  });
}

// Speaking
function initSpeaking() {
  const cueContent = document.getElementById("cueCardContent");
  cueContent.innerHTML = `
    <strong>Topic: Describe an ambitious goal you have achieved.</strong>
    <p>• What the goal was<br>• When and why you pursued it<br>• What challenges arose<br>• Why it was meaningful to you.</p>
  `;

  const recordBtn = document.getElementById("startSpeechRecordBtn");
  const stopBtn = document.getElementById("stopSpeechRecordBtn");
  const timerEl = document.getElementById("speakingTimer");
  const transcriptEl = document.getElementById("speakingTranscriptInput");

  let recognizer = null;
  if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognizer = new SpeechRecognition();
    recognizer.continuous = true;
    recognizer.interimResults = true;
    recognizer.lang = "en-US";

    recognizer.onresult = (e) => {
      let finalStr = "";
      for (let i = 0; i < e.results.length; ++i) {
        finalStr += e.results[i][0].transcript + " ";
      }
      transcriptEl.value = finalStr;
    };
  }

  recordBtn.addEventListener("click", () => {
    appState.speakingSeconds = 0;
    timerEl.innerText = "00:00";
    recordBtn.disabled = true;
    stopBtn.disabled = false;

    if (recognizer) recognizer.start();

    appState.speakingTimerInterval = setInterval(() => {
      appState.speakingSeconds++;
      const m = String(Math.floor(appState.speakingSeconds / 60)).padStart(2, "0");
      const s = String(appState.speakingSeconds % 60).padStart(2, "0");
      timerEl.innerText = `${m}:${s}`;
    }, 1000);
  });

  stopBtn.addEventListener("click", () => {
    clearInterval(appState.speakingTimerInterval);
    recordBtn.disabled = false;
    stopBtn.disabled = true;
    if (recognizer) recognizer.stop();
  });

  document.getElementById("evaluateSpeakingBtn").addEventListener("click", async () => {
    const transcript = transcriptEl.value.trim();
    if (!transcript) return;
    const duration = Math.max(15, appState.speakingSeconds || 60);

    const rep = await callApi("/api/speaking/evaluate", "POST", { transcript, duration_seconds: duration });
    if (rep) {
      const repBox = document.getElementById("speakingEvalReport");
      repBox.style.display = "block";
      repBox.innerHTML = `
        <h3>Estimated Speaking Band: ${rep.estimated_band}</h3>
        <p><strong>Speech Rate:</strong> ${rep.fluency_metrics.words_per_minute} WPM (Target: ${rep.fluency_metrics.target_wpm_range})</p>
        <p><strong>Filler Words Detected:</strong> ${rep.fluency_metrics.total_filler_words} (${rep.fluency_metrics.filler_percentage}%)</p>
        <p><strong>Feedback:</strong> ${rep.fluency_metrics.feedback}</p>
        <p><em>${rep.disclaimer}</em></p>
      `;
    }
  });
}

// Mistake Book
async function initMistakeBook() {
  await loadMistakes();
}

async function loadMistakes() {
  const data = await callApi("/api/mistakes");
  if (data) {
    const sumBox = document.getElementById("mistakeBookSummary");
    const listEl = document.getElementById("mistakeBookList");

    sumBox.innerHTML = `
      <p>Active error categories: <strong>${(data.summary && data.summary.categories) ? data.summary.categories.length : 0}</strong></p>
    `;

    listEl.innerHTML = "";
    (data.active_mistakes || []).forEach(m => {
      const div = document.createElement("div");
      div.className = "task-item mb-2";
      div.innerHTML = `
        <strong>[${m.skill.toUpperCase()}] ${m.category} (Seen ${m.recurrence_count}x)</strong>
        <p>Original: <em>"${m.original_text}"</em></p>
        <p>Correction: <strong>"${m.corrected_text}"</strong></p>
        <p>Explanation: ${m.explanation}</p>
        <button class="btn btn-sm btn-success mt-1" onclick="resolveMistake('${m.id}')">Mark Resolved (Mastered)</button>
      `;
      listEl.appendChild(div);
    });
  }
}

window.resolveMistake = async function(id) {
  await callApi("/api/mistakes/review", "POST", { mistake_id: id, success: true });
  loadMistakes();
  loadDashboard();
};

// Settings & Export/Import
function initSettings() {
  const forcedOff = document.getElementById("settingForcedOffline");
  forcedOff.addEventListener("change", async () => {
    const data = await callApi("/api/settings/offline_toggle", "POST", { forced_offline: forcedOff.checked });
    if (data) updateStatusBadge(data.status, data.forced_offline);
  });

  const exportBtn = document.getElementById("exportDataBtn");
  const importBtn = document.getElementById("importDataBtn");
  const transferArea = document.getElementById("dataTransferArea");

  exportBtn.addEventListener("click", async () => {
    const res = await callApi("/api/export", "POST");
    if (res) transferArea.value = res.data;
  });

  importBtn.addEventListener("click", async () => {
    const raw = transferArea.value.trim();
    if (!raw) return;
    const rep = await callApi("/api/import", "POST", { data: raw });
    if (rep) {
      alert(`Imported successfully! Restored ${rep.restored_mistakes} mistakes.`);
      loadDashboard();
      loadMistakes();
    }
  });
}
