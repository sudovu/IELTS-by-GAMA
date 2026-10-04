/**
 * IELTS by GAMA - Frontend Client Application
 * Hybrid Online + Offline AI English Tutor
 * Features dual-mode networking: REST API with zero-network standalone offline fallback.
 * Incorporates Chris Pell's IELTS Advantage Methodology & Question Analysis Framework.
 */

const API_BASE = "";
const APP_VERSION = "1.5.3";

// Global State
let appState = {
  version: APP_VERSION,
  currentTab: "dashboard",
  connectivity: "OFFLINE",
  forcedOffline: false,
  srsDeck: [],
  currentCardIdx: 0,
  currentListeningSection: "sec_1",
  currentReadingPassage: "acad_p1",
  currentWritingPrompt: "acad_t2_stem",
  currentSpeakingSetIdx: 0,
  grammarMode: "fillup",
  vocabMode: "vault",
  fillupScore: 0,
  fillupStreak: 0,
  speakingTimerInterval: null,
  speakingSeconds: 0,
  speakingInterview: {
    active: false,
    stage: "idle", // 'part1', 'part2_prep', 'part2_speak', 'part3', 'done'
    examSetIdx: 0,
    examData: null,
    part1QuestionIdx: 0,
    part3QuestionIdx: 0,
    prepTimerInterval: null,
    prepSecondsLeft: 60,
    currentQuestionText: "",
    dialogueHistory: [],
    candidateFullTranscript: ""
  }
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
      current_band: 6.0,
      target_band: 7.5,
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
  addMistake(skill, category, original, correction, explanation) {
    const list = this.getMistakes();
    const existing = list.find(m => m.original_text.toLowerCase() === original.toLowerCase());
    if (existing) {
      existing.recurrence_count++;
      existing.mastery_score = Math.max(0.0, existing.mastery_score - 0.2);
      existing.status = "needs_improvement";
    } else {
      list.push({
        id: "m_" + Date.now(),
        skill: skill,
        category: category,
        original_text: original,
        corrected_text: correction,
        explanation: explanation,
        recurrence_count: 1,
        mastery_score: 0.0,
        status: "needs_improvement"
      });
    }
    this.saveMistakes(list);
  },
  getSRS() {
    const raw = localStorage.getItem("gama_srs");
    if (raw) return JSON.parse(raw);

    // High-yield 24-card SuperMemo deck
    return [
      {
        id: "srs_1",
        item_type: "vocabulary",
        category: "Environment",
        key_term: "curb carbon emissions",
        prompt: "Collocation: To significantly reduce emissions produced by factories and vehicles.",
        answer: "Collocation: curb carbon emissions (e.g. 'Strict environmental legislation was passed to curb carbon emissions.')",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_2",
        item_type: "collocation",
        category: "Technology",
        key_term: "streamline workflows",
        prompt: "Collocation: To make an organization or industrial system more efficient by using digital software.",
        answer: "Collocation: streamline operational workflows (e.g. 'Automation helps corporations streamline complex workflows.')",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_3",
        item_type: "vocabulary",
        category: "Education",
        key_term: "foster critical thinking",
        prompt: "Collocation: To encourage students to evaluate arguments rather than memorizing facts.",
        answer: "Collocation: foster critical thinking skills (e.g. 'Liberal arts curricula aim to foster critical thinking.')",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_4",
        item_type: "grammar",
        category: "Inversion",
        key_term: "Not only... but also",
        prompt: "Inversion: Rewrite using inversion: 'Renewables reduce costs and they cut emissions.'",
        answer: "'Not only do renewables reduce costs, but they also cut emissions.'",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_5",
        item_type: "lexical_upgrade",
        category: "Precision",
        key_term: "paramount",
        prompt: "Lexical Upgrade: Replace 'very important' with Band 8+ academic register.",
        answer: "Band 8+: of paramount importance / pivotal / indispensable (e.g. 'Data security is of paramount importance.')",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_6",
        item_type: "lexical_upgrade",
        category: "Precision",
        key_term: "substantial",
        prompt: "Lexical Upgrade: Replace 'a lot of' with academic wording.",
        answer: "Band 8+: a substantial proportion of / an abundance of",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_7",
        item_type: "collocation",
        category: "Health",
        key_term: "sedentary lifestyle",
        prompt: "Collocation: A lifestyle characterized by prolonged sitting and lack of exercise.",
        answer: "Collocation: sedentary lifestyle (e.g. 'A sedentary lifestyle precipitates cardiovascular ailments.')",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_8",
        item_type: "vocabulary",
        category: "Crime",
        key_term: "potent deterrent",
        prompt: "Collocation: A punishment strong enough to discourage potential criminals.",
        answer: "Collocation: serve as a potent deterrent (e.g. 'Rigorous penalties serve as a potent deterrent.')",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_9",
        item_type: "grammar",
        category: "Mixed Conditional",
        key_term: "Mixed Conditional",
        prompt: "Complete mixed conditional: 'If the council had planned earlier, traffic _____ (not be) so terrible today.'",
        answer: "'...would not be so terrible today' (Past unreal condition -> Present outcome)",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_10",
        item_type: "phrasal_verb",
        category: "Formal Substitute",
        key_term: "account for",
        prompt: "What is the formal Latinate synonym of 'account for' (proportion)?",
        answer: "Synonym: constitute / comprise / represent (e.g. 'Nuclear energy accounts for 20% of output.')",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_11",
        item_type: "collocation",
        category: "Urbanization",
        key_term: "alleviate congestion",
        prompt: "Collocation: What verb pairs naturally with 'traffic congestion' to mean reduce?",
        answer: "Collocations: alleviate / mitigate / ease traffic congestion",
        repetition: 0,
        interval_days: 1.0,
        ease_factor: 2.5
      },
      {
        id: "srs_12",
        item_type: "methodology",
        category: "IELTS Advantage",
        key_term: "Coffee Shop Method",
        prompt: "What is the core premise of Chris Pell's 'Coffee Shop Method' in Writing Task 2?",
        answer: "Express arguments simply and logically as if explaining to a friend in a coffee shop, avoiding panic and artificial 'big words'.",
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
        model_name: "GAM IELTS Nano (Offline RAG)"
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
            "Grammar": 7.0,
            "Vocabulary": 7.0,
            "Reading": 6.5,
            "Listening": 7.0,
            "Writing": prof.current_band,
            "Speaking": 6.5,
            "Fluency": 6.5,
            "Pronunciation": 7.0
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
          daily_greeting: `Welcome back! You have ${prof.daily_minutes} minutes planned. Current Band: ${prof.current_band} | Target: ${prof.target_band}. Ready to excel?`,
          tasks: [
            { title: "IELTS Advantage Question Analysis", duration_minutes: 10, description: "Break down micro-topics and formulate PEEL blueprints." },
            { title: "Grammar Fill-Up Clozes", duration_minutes: 10, description: "Master conditionals, inversion, and impersonal passive clauses." },
            { title: "Vocabulary & SRS Drills", duration_minutes: 10, description: "Review due SuperMemo SM-2 flashcards and collocations." }
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
        summary: { categories: [{ skill: "grammar", category: "Subject-Verb Agreement", total_occurrences: list.length, avg_mastery: 0.6 }] },
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

    // Reading Passages
    if (p.startsWith("/api/reading/passages")) {
      return {
        passages: [
          { id: "acad_p1", title: "The Architecture of Deep-Sea Hydrothermal Ecosystems", track: "Academic", question_count: 4 },
          { id: "acad_p2", title: "The Cognitive Architecture of Bilingualism & Executive Function", track: "Academic", question_count: 4 },
          { id: "acad_p3", title: "Urban Heat Islands and Microclimate Architecture", track: "Academic", question_count: 4 }
        ]
      };
    }

    if (p.startsWith("/api/reading")) {
      const pid = (p.includes("passage_id=") ? p.split("passage_id=")[1] : "acad_p1").split("&")[0];
      const passages = {
        "acad_p1": {
          id: "acad_p1",
          track: "Academic",
          title: "The Architecture of Deep-Sea Hydrothermal Ecosystems",
          text: "Deep-sea hydrothermal vents, discovered in 1977 along the Galapagos Rift, represent one of the most remarkable biological frontiers on Earth. Located thousands of meters beneath the oceanic surface where sunlight cannot penetrate, these geological formations dispel the historical assumption that all complex ecosystems rely fundamentally on solar photosynthesis. Instead, these abyssal biomes are sustained through chemosynthesis, a process mediated by specialized extremophilic bacteria.\n\nAs tectonic plates diverge, seawater infiltrates subterranean fissures, reaching temperatures exceeding 400 degrees Celsius near magma chambers. Saturated with dissolved minerals—predominantly hydrogen sulfide, iron, and copper—the superheated water precipitates violently upon encountering the frigid, near-freezing ambient ocean. This reaction constructs towering mineralized chimneys colloquially known as 'black smokers'.\n\nThe organisms flourishing around these vents exhibit astounding biological adaptations. Giant tube worms (Riftia pachyptila), which can reach lengths of over two meters, completely lack a digestive tract, mouth, or gut. Instead, they harbor billions of symbiotic sulfur-oxidizing bacteria within an organ called the trophosome. The tube worms extract hydrogen sulfide and oxygen from the hydrothermal fluid using vascularized red plumes, transferring these compounds to the endosymbionts, which synthesize organic nourishment for the host.\n\nNevertheless, these thriving oasis communities are exceptionally ephemeral. Because tectonic shifts and volcanic eruptions routinely seal hydrothermal conduits or open new subterranean fractures, vents can abruptly shut down within a matter of decades. Consequently, hydrothermal vent fauna have developed rapid larval dispersion mechanisms capable of traversing vast expanses of inhospitable abyssal desert to locate newly forming vents.",
          questions: [
            { num: 1, type: "TFNG", prompt: "Deep-sea hydrothermal ecosystems require solar radiation to produce fundamental nutrients." },
            { num: 2, type: "TFNG", prompt: "Giant tube worms absorb nourishment directly through their mouths." },
            { num: 3, type: "TFNG", prompt: "Vents remain active continuously for millions of years in the same location." },
            { num: 4, type: "Completion", prompt: "The mineral chimneys formed by superheated hydrothermal fluids are colloquially called _____ (NO MORE THAN TWO WORDS)." }
          ],
          synonym_table: [
            { question_keyword: "solar radiation", passage_synonym: "sunlight / solar photosynthesis" },
            { question_keyword: "fundamental nutrients", passage_synonym: "organic nourishment" },
            { question_keyword: "absorb nourishment", passage_synonym: "synthesize organic nourishment for the host" },
            { question_keyword: "continuously active", passage_synonym: "ephemeral / shut down within decades" }
          ]
        },
        "acad_p2": {
          id: "acad_p2",
          track: "Academic",
          title: "The Cognitive Architecture of Bilingualism & Executive Function",
          text: "For much of the twentieth century, clinical educators cautioned parents against raising children in bilingual households, asserting that juggling two grammatical systems would cause cognitive confusion and impede linguistic development. However, modern neuroimaging and psycholinguistic experiments have thoroughly debunked this deficit hypothesis. Far from hindering intellect, acquiring multiple languages reshapes neural pathways and fortifies the brain's executive control center.\n\nExecutive function refers to a constellation of higher-order cognitive operations overseen predominantly by the prefrontal cortex. These include cognitive flexibility, inhibitory control, working memory, and selective attention. When a bilingual individual communicates, both language systems remain perpetually active in the brain. Even when conducting a conversation entirely in Spanish, the English lexical network is primed and competes for activation. To prevent interference, the brain must continuously exert inhibitory control to suppress the irrelevant language while maintaining attentional focus on the target vernacular.\n\nThis relentless neural workout produces measurable neuroplastic advantages across the lifespan. In laboratory experiments such as the Simon task and the Stroop color-word test, bilingual participants consistently outperform monolingual peers in resolving conflicting stimuli and executing rapid task-switching protocols. Crucially, this advantage is not restricted to linguistic tasks; it manifests robustly across spatial reasoning and abstract problem-solving.\n\nPerhaps the most profound implication of bilingualism is its neuroprotective capacity against age-related cognitive decline. Longitudinal epidemiological studies led by cognitive neuroscientists demonstrate that lifelong bilinguals manifest symptoms of neurodegenerative disorders, such as Alzheimer's disease, an average of four to five years later than monolingual cohorts with equivalent neuropathological brain damage. This phenomenon is known as 'cognitive reserve'—the brain's enhanced resilience and capability to improvise alternative neural routes around damaged areas.",
          questions: [
            { num: 1, type: "TFNG", prompt: "Early twentieth-century educators encouraged families to raise multilingual children." },
            { num: 2, type: "TFNG", prompt: "When a bilingual speaks one language, their other language system is entirely shut down." },
            { num: 3, type: "TFNG", prompt: "The cognitive benefits of bilingualism are strictly confined to verbal and language-based tests." },
            { num: 4, type: "Completion", prompt: "The brain's ability to resist neurodegenerative symptoms by finding alternate neural circuits is termed _____ (NO MORE THAN TWO WORDS)." }
          ],
          synonym_table: [
            { question_keyword: "encouraged families", passage_synonym: "cautioned parents against" },
            { question_keyword: "entirely shut down", passage_synonym: "perpetually active / competes for activation" },
            { question_keyword: "strictly confined to verbal", passage_synonym: "not restricted to linguistic tasks" },
            { question_keyword: "alternate neural circuits", passage_synonym: "improvise alternative neural routes" }
          ]
        },
        "acad_p3": {
          id: "acad_p3",
          track: "Academic",
          title: "Urban Heat Islands and Microclimate Architecture",
          text: "Urban Heat Islands (UHIs) represent a pronounced meteorological phenomenon whereby metropolitan centers experience surface and ambient air temperatures substantially higher than their surrounding rural peripheries. This thermal discrepancy, which can reach up to 10 degrees Celsius in densely populated capitals during nighttime hours, is primarily driven by the extensive replacement of vegetative terrain with impermeable artificial surfaces such as asphalt, concrete, and masonry. These materials possess high thermal mass and low albedo, enabling them to absorb copious solar irradiance during daytime hours and reradiate it as sensible heat after dusk.\n\nFurthermore, urban canyons formed by towering high-rise developments impede natural wind ventilation, trapping anthropogenic heat generated by industrial machinery, vehicular exhausts, and air-conditioning refrigeration units. The consequences of unmitigated UHIs are severe, exacerbating heat-related cardiovascular mortality, amplifying smog photochemistry, and triggering immense spikes in electrical energy consumption for cooling systems.\n\nTo counter these escalating urban microclimates, contemporary municipal architects and urban planners are implementing multi-layered passive cooling strategies. Central to these interventions is the widespread integration of living architecture, such as vegetative green roofs and extensive vertical facade gardens. Vegetative surfaces cool the ambient microclimate through evapotranspiration—a biophysical process where plants transpire moisture while solar energy evaporates water from soil matrices, thereby dissipating latent heat without raising temperature.\n\nConcurrently, civil engineers are retrofitting road networks with permeable, high-albedo cool pavements. By reflecting upwards of 40% of incident solar radiation compared to the standard 10% reflected by aged asphalt, cool pavements prevent initial thermal absorption. When combined with strategic urban forestry corridors that channel prevailing oceanic breezes, these sustainable architectural interventions can suppress peak localized temperatures by several critical degrees.",
          questions: [
            { num: 1, type: "TFNG", prompt: "Rural peripheral regions typically experience higher temperatures than city centers." },
            { num: 2, type: "TFNG", prompt: "Urban canyon high-rises can hinder atmospheric airflow and trap heat." },
            { num: 3, type: "TFNG", prompt: "Standard aged asphalt reflects over 40% of incoming solar radiation." },
            { num: 4, type: "Completion", prompt: "Plants lower ambient air temperatures without heating through the process of _____ (ONE WORD ONLY)." }
          ],
          synonym_table: [
            { question_keyword: "higher temperatures in rural areas", passage_synonym: "city centers substantially higher than rural peripheries" },
            { question_keyword: "hinder atmospheric airflow", passage_synonym: "impede natural wind ventilation" },
            { question_keyword: "standard aged asphalt reflects 40%", passage_synonym: "standard 10% reflected by aged asphalt" },
            { question_keyword: "cooling process", passage_synonym: "evapotranspiration / dissipating latent heat" }
          ]
        }
      };
      return passages[pid] || passages["acad_p1"];
    }

    if (p === "/api/reading/submit") {
      const pid = body.passage_id || "acad_p1";
      const ans = body.answers || {};
      let correct = 0;
      if (pid === "acad_p1") {
        if ((ans["1"] || "").toLowerCase() === "false") correct++;
        if ((ans["2"] || "").toLowerCase() === "false") correct++;
        if ((ans["3"] || "").toLowerCase() === "false") correct++;
        if ((ans["4"] || "").toLowerCase().includes("black smoker")) correct++;
      } else if (pid === "acad_p2") {
        if ((ans["1"] || "").toLowerCase() === "false") correct++;
        if ((ans["2"] || "").toLowerCase() === "false") correct++;
        if ((ans["3"] || "").toLowerCase() === "false") correct++;
        if ((ans["4"] || "").toLowerCase().includes("cognitive reserve")) correct++;
      } else if (pid === "acad_p3") {
        if ((ans["1"] || "").toLowerCase() === "false") correct++;
        if ((ans["2"] || "").toLowerCase() === "true") correct++;
        if ((ans["3"] || "").toLowerCase() === "false") correct++;
        if ((ans["4"] || "").toLowerCase().includes("evapotranspiration")) correct++;
      }
      const band = correct === 4 ? 8.5 : (correct === 3 ? 7.5 : (correct === 2 ? 6.5 : 5.0));
      return {
        estimated_band: band,
        correct_answers: correct,
        total_questions: 4,
        disclaimer: "Practice estimate only. Not an official IELTS result."
      };
    }

    // Listening Sections
    if (p.startsWith("/api/listening")) {
      const secId = (p.includes("sec_id=") ? p.split("sec_id=")[1] : "sec_1").split("&")[0];
      const sections = {
        "sec_1": {
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
        },
        "sec_2": {
          id: "sec_2",
          section_number: 2,
          title: "Greendale Community Arts Centre & Gallery Tour",
          audio_script: "GUIDE: Good afternoon everyone, and welcome to Greendale Arts Centre. Before we tour the studios, let me outline key visitor details. The centre was founded in 1994, although major renovations took place in 2018. Our ceramic pottery workshop is located on the ground floor next to the courtyard garden. Opening hours on weekdays are 9 AM to 8 PM, while weekend entry closes earlier at 6 PM. Membership for local residents costs 45 pounds annually, which grants free admission to special exhibitions. For visitors arriving by public transport, bus route number 14 stops directly in front of the main entrance.",
          questions: [
            { num: 1, prompt: "Year of major centre renovations: _____" },
            { num: 2, prompt: "Pottery workshop location: next to the _____ garden" },
            { num: 3, prompt: "Weekend closing time: _____ PM" },
            { num: 4, prompt: "Direct bus route number: _____" }
          ]
        },
        "sec_3": {
          id: "sec_3",
          section_number: 3,
          title: "Academic Tutorial: Renewable Microgrid Projects",
          audio_script: "TUTOR: Good afternoon, Liam and Clara. Let's discuss your engineering fieldwork proposal.\nCLARA: Thanks, Professor. We decided to investigate solar microgrids installed on university rooftops.\nLIAM: Yes, we initially thought about wind turbines, but building height regulations made solar photovoltaic panels far more viable.\nTUTOR: An astute decision. And what primary variable will you measure over the six-month trial?\nCLARA: We are analyzing peak storage efficiency, specifically measuring battery discharge rates under cloudy conditions.\nTUTOR: Excellent. Keep in mind that your interim progress report must be submitted by November 12th.\nLIAM: Understood. We have already calibrated our digital telemetry sensors.",
          questions: [
            { num: 1, prompt: "Chosen renewable technology: solar _____ panels" },
            { num: 2, prompt: "Primary measured variable: peak storage _____" },
            { num: 3, prompt: "Interim report deadline: _____ 12th" }
          ]
        },
        "sec_4": {
          id: "sec_4",
          section_number: 4,
          title: "Academic Lecture: Cetacean Bioacoustics in Polar Oceans",
          audio_script: "PROFESSOR: Welcome back to Marine Biology 402. Today we examine acoustic communication in Arctic cetaceans, specifically beluga whales and narwhals. In frozen ocean environments where solar illumination is virtually absent for months, sound waves represent the primary sensory modality for navigation, social cohesion, and prey localization. Beluga vocalizations encompass a dynamic acoustic spectrum ranging from low-frequency groans to ultrasonic clicks reaching 120 kilohertz. Recent bioacoustic telemetry indicates that anthropogenic noise from commercial shipping vessels causes significant acoustic masking, which forces pods to increase their call amplitude—a physiological adaptation known as the Lombard effect. Furthermore, the warming of sea ice has accelerated ambient underwater noise levels by nearly three decibels per decade.",
          questions: [
            { num: 1, prompt: "Primary sensory modality in Arctic waters: _____ waves" },
            { num: 2, prompt: "Maximum frequency of beluga ultrasonic clicks: _____ kilohertz" },
            { num: 3, prompt: "Vocal elevation under ambient noise is known as the _____ effect" }
          ]
        }
      };
      return sections[secId] || sections["sec_1"];
    }

    if (p === "/api/listening/submit") {
      const ans = body.answers || {};
      const secId = body.section_id || "sec_1";
      let correct = 0;
      let total = 4;
      if (secId === "sec_1") {
        if ((ans["1"] || "").toLowerCase().includes("sterling")) correct++;
        if ((ans["2"] || "").toLowerCase().includes("suite")) correct++;
        if ((ans["3"] || "").includes("210")) correct++;
        if ((ans["4"] || "").toLowerCase().includes("september")) correct++;
      } else if (secId === "sec_2") {
        if ((ans["1"] || "").includes("2018")) correct++;
        if ((ans["2"] || "").toLowerCase().includes("courtyard")) correct++;
        if ((ans["3"] || "").includes("6")) correct++;
        if ((ans["4"] || "").includes("14")) correct++;
      } else if (secId === "sec_3") {
        total = 3;
        if ((ans["1"] || "").toLowerCase().includes("photovoltaic")) correct++;
        if ((ans["2"] || "").toLowerCase().includes("efficiency")) correct++;
        if ((ans["3"] || "").toLowerCase().includes("november")) correct++;
      } else if (secId === "sec_4") {
        total = 3;
        if ((ans["1"] || "").toLowerCase().includes("sound")) correct++;
        if ((ans["2"] || "").includes("120")) correct++;
        if ((ans["3"] || "").toLowerCase().includes("lombard")) correct++;
      }
      const band = (correct / total) >= 0.9 ? 8.0 : ((correct / total) >= 0.7 ? 7.0 : ((correct / total) >= 0.5 ? 6.0 : 5.0));
      return {
        estimated_band: band,
        correct_answers: correct,
        total_questions: total,
        disclaimer: "Practice estimate only. Not an official IELTS result."
      };
    }

    // Speaking Sets (6 Cambridge-Standard Sets)
    if (p.startsWith("/api/speaking/prompts")) {
      const idx = p.includes("card_idx=") ? parseInt(p.split("card_idx=")[1]) || 0 : 0;
      const examSets = [
        {
          id: "topic_ambition",
          title: "Exam Set 1: Career, Goals & Ambition",
          part_1: [
            "Good morning. My name is Dr. Harrison. Can you state your full name, please?",
            "Could you tell me where you come from and what you enjoy most about your hometown?",
            "Do you currently work, or are you a student? What are your daily responsibilities?",
            "How do you usually unwind and spend your free time after a busy day?"
          ],
          part_2_cue_card: {
            id: "cue_ambition",
            topic: "Describe a significant achievement or ambitious goal you reached.",
            prompts: [
              "What the achievement or goal was",
              "When you first decided to pursue it",
              "What obstacles or challenges you faced along the way",
              "And explain why reaching this goal was personally meaningful to you."
            ],
            band_9_model: "I'd like to describe successfully creating an educational platform for students in remote regions. I conceived this idea during university after observing how digital disparity restricted learning opportunities. The primary challenge was optimizing software to execute offline with zero budget. Overcoming this barrier was deeply meaningful because it validated that perseverance and thoughtful architecture can bridge socioeconomic divides."
          },
          part_3_discussion: [
            "Do young people today face greater pressure to succeed in their careers than earlier generations?",
            "How can educational institutions better prepare students for practical life challenges?",
            "Why do some individuals lose motivation when pursuing long-term objectives?",
            "Should personal fulfillment be valued more highly than financial prosperity in modern careers?"
          ]
        },
        {
          id: "topic_environment",
          title: "Exam Set 2: Sustainable Living & Urban Heritage",
          part_1: [
            "Hello. Welcome to the IELTS Speaking test. May I see your identification, please?",
            "Let's talk about where you live. Is your neighborhood noisy or quiet?",
            "Do you prefer living in a bustling metropolitan area or a peaceful countryside setting?",
            "How have cities in your country changed over the past ten years?"
          ],
          part_2_cue_card: {
            id: "cue_heritage",
            topic: "Describe a historical building or architectural landmark that left a strong impression on you.",
            prompts: [
              "Where this building or landmark is located",
              "What architectural features or history it possesses",
              "When and with whom you visited it",
              "And explain why you think preserving such heritage is important for future generations."
            ],
            band_9_model: "A landmark that made a lasting impression on me is the 19th-century municipal library in our historic quarter. Architecturally, it boasts vaulted limestone masonry, natural light wells, and passive ventilation shafts designed long before air conditioning. I visited it with my grandfather during my school years. Preserving such heritage is vital because it anchors modern communities to their cultural lineage."
          },
          part_3_discussion: [
            "Why is it essential for governments to preserve ancient architecture alongside modern high-rises?",
            "How does sustainable green architecture influence public health in densely populated cities?",
            "Should historical monuments be free for citizens to visit, or should admission fees fund restoration?",
            "In what ways can urban planners prevent historic districts from succumbing to commercialization?"
          ]
        },
        {
          id: "topic_technology",
          title: "Exam Set 3: Artificial Intelligence, Automation & Media",
          part_1: [
            "Good afternoon. I am your examiner today. Could you please confirm your full name?",
            "How reliant are you on digital devices for your everyday communication?",
            "Do you prefer reading news from printed newspapers or digital applications?",
            "What kind of modern technology do you find most indispensable in your daily life?"
          ],
          part_2_cue_card: {
            id: "cue_technology",
            topic: "Describe a technological innovation or digital tool that dramatically changed how you work or study.",
            prompts: [
              "What the innovation or software application is",
              "How you first became aware of it",
              "How frequently you incorporate it into your routine",
              "And explain how it has augmented your productivity and learning efficiency."
            ],
            band_9_model: "I would like to highlight an offline linguistic analysis engine that I discovered during my postgraduate dissertation. It performs syntactic parsing and formative checking completely on-device without cloud latency. It transformed my productivity by allowing me to maintain deep focus in environments with zero internet access."
          },
          part_3_discussion: [
            "Will automated artificial intelligence systems eventually diminish the demand for human analytical skills?",
            "How can governments ensure ethical standards in algorithmic decision-making and data privacy?",
            "What impact has constant digital connectivity had on face-to-face interpersonal relationships?",
            "Are older demographics being unfairly marginalized by the rapid shift toward cashless, app-only services?"
          ]
        },
        {
          id: "topic_tourism",
          title: "Exam Set 4: International Tourism & Overtourism",
          part_1: [
            "Good morning. Let's discuss travel and holidays. How often do you travel during vacation periods?",
            "Do you prefer visiting famous tourist destinations or exploring secluded off-the-beaten-track locations?",
            "What factors do you consider when choosing a holiday destination?",
            "Do you think tourism brings more economic advantages or environmental challenges to your region?"
          ],
          part_2_cue_card: {
            id: "cue_tourism",
            topic: "Describe an unforgettable journey or trip you took to an unfamiliar destination.",
            prompts: [
              "Where you went and how you traveled there",
              "Who accompanied you on this journey",
              "What memorable activities you engaged in",
              "And explain what valuable insights or lessons you gleaned from the experience."
            ],
            band_9_model: "I will describe a low-carbon trekking journey through the northern highlands with two university companions. We traversed mountainous valleys by electric bicycle and stayed at community eco-lodges. What stood out was the indigenous community's zero-waste ethos. It demonstrated that sustainable tourism can empower local commerce without destroying pristine ecology."
          },
          part_3_discussion: [
            "Should governments place statutory caps on daily visitor numbers to safeguard delicate historical monuments?",
            "How does mass commercial tourism alter the authentic traditions and linguistic identity of host communities?",
            "Do you believe virtual reality simulations could ever substitute physical international travel?",
            "In what ways can travelers minimize their environmental footprint when visiting fragile natural reserves?"
          ]
        },
        {
          id: "topic_education",
          title: "Exam Set 5: Modern Education & Practical Skills",
          part_1: [
            "Good afternoon. Let's talk about education. What was your favorite subject in secondary school?",
            "Did you have an inspirational teacher who significantly influenced your educational journey?",
            "Do you find learning in an interactive classroom or online self-study more effective?",
            "Are practical vocational skills sufficiently taught in modern secondary schools?"
          ],
          part_2_cue_card: {
            id: "cue_education",
            topic: "Describe a difficult skill or subject you successfully mastered through deliberate practice.",
            prompts: [
              "What the skill or subject was",
              "Why you initially found it formidable or challenging",
              "What study methods or resources you leveraged to master it",
              "And explain how mastering this skill enhanced your personal or academic confidence."
            ],
            band_9_model: "A formidable subject I worked hard to master was statistical econometrics. Initially, mathematical regression models seemed bewilderingly abstract until I began applying them to empirical environmental datasets. Establishing a daily 45-minute problem-solving routine demystified the principles and taught me that complex disciplines yield to structured consistency."
          },
          part_3_discussion: [
            "Should tertiary higher education be funded entirely by taxpayers, or should students contribute tuition fees?",
            "To what extent will artificial intelligence tutors replace traditional classroom educators?",
            "Why are soft skills like emotional intelligence and teamwork becoming more coveted by employers?",
            "How can school curricula bridge the growing divide between theoretical academia and industry demands?"
          ]
        },
        {
          id: "topic_health",
          title: "Exam Set 6: Public Health & Fast-Paced Lifestyles",
          part_1: [
            "Hello. Let's discuss daily habits and health. What healthy habits do you try to maintain every day?",
            "How do you manage stress and psychological pressure during intense examination periods?",
            "Do you prefer engaging in outdoor team sports or individual physical workouts?",
            "Has public awareness regarding balanced nutrition improved in your home country recently?"
          ],
          part_2_cue_card: {
            id: "cue_health",
            topic: "Describe a positive lifestyle modification you implemented to boost your physical or mental health.",
            prompts: [
              "What the modification or new habit was",
              "What triggered or motivated you to make this change",
              "How challenging it was to sustain in the initial stages",
              "And explain the lasting benefits you noticed in your well-being."
            ],
            band_9_model: "I would like to highlight my commitment to a 30-minute daily morning jog and an evening digital curfew. The catalyst was persistent daytime fatigue caused by late-night screen exposure. Once I disconnected notifications after 9 PM, my sleep quality rebounded dramatically, leaving me far more focused and energized during academic tasks."
          },
          part_3_discussion: [
            "Should municipal authorities penalize junk food manufacturers by levying sugar and saturated fat taxes?",
            "Why are modern sedentary white-collar professions experiencing an epidemic of postural and cardiovascular ailments?",
            "Is individual personal discipline or state regulation more effective in curbing national obesity rates?",
            "How can corporations structure working hours to prevent employee burnout and mental exhaustion?"
          ]
        }
      ];
      return examSets[idx % examSets.length];
    }

    // Writing Evaluator with IELTS Advantage Checklist
    if (p === "/api/writing/evaluate") {
      const text = body.essay_text || "";
      const words = text.trim().split(/\s+/).filter(w => w.length > 0);
      const wordCount = words.length;

      let tr = wordCount >= 250 ? 7.0 : 5.5;
      let cc = (text.toLowerCase().includes("furthermore") || text.toLowerCase().includes("in conclusion") || text.toLowerCase().includes("on balance")) ? 7.0 : 6.0;
      let lr = (text.toLowerCase().includes("substantial") || text.toLowerCase().includes("crucial") || text.toLowerCase().includes("paramount") || text.toLowerCase().includes("detrimental")) ? 7.5 : 6.0;
      let gra = (text.toLowerCase().includes("if") || text.toLowerCase().includes("which") || text.toLowerCase().includes("although")) ? 7.0 : 6.0;

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

      const checklist = [
        { item: "Answered all parts of the question prompt", passed: wordCount >= 250 },
        { item: "Clear thesis position stated in intro and conclusion", passed: text.toLowerCase().includes("in conclusion") || text.toLowerCase().includes("my opinion") || text.toLowerCase().includes("i argue") },
        { item: "Substantial word count (Sweet spot: 260-290 words)", passed: wordCount >= 250 && wordCount <= 320 },
        { item: "Cohesive linkers and discourse signposts present", passed: cc >= 7.0 },
        { item: "Topic-specific academic vocabulary utilized", passed: lr >= 7.0 },
        { item: "Complex subordinate and conditional clauses present", passed: gra >= 7.0 },
        { item: "Absence of basic grammatical errors (e.g. 'I am agree')", passed: formative.length === 0 }
      ];

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
        advantage_checklist: checklist,
        disclaimer: "Practice estimate only. Not an official IELTS result."
      };
    }

    // Speaking Evaluator
    if (p === "/api/speaking/evaluate") {
      const transcript = body.transcript || "";
      const duration = body.duration_seconds || 60.0;
      const words = transcript.trim().split(/\s+/).filter(w => w.length > 0);
      const wpm = Math.round((words.length / (duration / 60.0)));
      const fillers = (transcript.match(/\b(um|uh|like|you know|basically)\b/gi) || []).length;
      let fc = wpm >= 115 && wpm <= 165 ? 7.0 : 6.0;
      let lr = 6.5;
      let gra = 6.5;

      const lower = transcript.toLowerCase();
      if (lower.includes("substantial") || lower.includes("paramount") || lower.includes("consequently") || lower.includes("perspective") || lower.includes("indispensable")) {
        lr += 1.0;
      }

      const upgrades = [];
      const upgradeMap = [
        ["i think", "from my perspective / I am inclined to argue that"],
        ["a lot of", "a substantial proportion of / an abundance of"],
        ["very important", "of paramount importance / pivotal / indispensable"],
        ["good", "exemplary / profoundly beneficial"],
        ["bad", "detrimental / adverse"],
        ["big problem", "formidable dilemma / pressing challenge"],
        ["help", "facilitate / bolster / expedite"],
        ["hard", "arduous / multifaceted"]
      ];

      for (const [colloq, adv] of upgradeMap) {
        if (lower.includes(colloq)) {
          upgrades.push({
            original: colloq,
            band_9_upgrade: adv,
            tip: `Upgrade colloquial '${colloq}' to higher-tier academic phrasing.`
          });
          if (upgrades.length >= 3) break;
        }
      }

      if (upgrades.length === 0) {
        upgrades.push({
          original: "conversational signposts",
          band_9_upgrade: "Integrate discourse markers: 'To put this into perspective', 'Notwithstanding that fact', 'In the broader scheme of things'",
          tip: "Cohesive discourse markers elevate fluency from Band 6.5 to Band 8.0."
        });
      }

      const overall = Math.round(((fc + lr + gra + 6.5) / 4.0) * 2) / 2;

      return {
        estimated_band: overall,
        criteria: {
          "Fluency and Coherence": fc,
          "Lexical Resource": lr,
          "Grammatical Range and Accuracy": gra,
          "Pronunciation": 6.5
        },
        fluency_metrics: {
          words_per_minute: wpm,
          target_wpm_range: "120 - 150 WPM",
          total_filler_words: fillers,
          filler_percentage: words.length ? Math.round((fillers / words.length) * 100) : 0,
          feedback: wpm >= 115 ? "Smooth speaking cadence and natural pacing." : "Work on continuous expression to avoid hesitant pauses."
        },
        band_upgrades: upgrades,
        actionable_tips: [
          "Follow the IELTS Advantage 3-Step Formula: 1. Answer Directly -> 2. The 'Why' -> 3. Concrete Example.",
          "Elaborate thoroughly with personal reflections rather than single-sentence answers."
        ],
        disclaimer: "Practice estimate only. Not an official IELTS result."
      };
    }

    // 12-Question Diagnostic Test
    if (p === "/api/diagnostic/questions") {
      return {
        questions: [
          { id: "g1", skill: "grammar", category: "Conditionals", prompt: "If government funding _____ (increase) next year, researchers will expand their clinical trials.", options: ["increases", "will increase", "increased", "would increase"] },
          { id: "g2", skill: "grammar", category: "Subject-Verb Agreement", prompt: "The collection of historical artifacts _____ (have/has) been preserved in the national archives.", options: ["has", "have", "are having", "were"] },
          { id: "g3", skill: "grammar", category: "Inversion", prompt: "Not only _____ the new policy reduce carbon emissions, but it also stimulated clean tech employment.", options: ["did", "does", "had", "will"] },
          { id: "g4", skill: "grammar", category: "Articles & Countability", prompt: "The academic supervisor offered invaluable _____ regarding the thesis methodology.", options: ["advice", "an advice", "advices", "a piece of advices"] },
          { id: "v1", skill: "vocabulary", category: "Collocations", prompt: "The statistical analysis revealed a _____ (profound / deep) discrepancy in the demographic data.", options: ["profound", "deep", "heavy", "dense"] },
          { id: "v2", skill: "vocabulary", category: "Phrasal Verbs", prompt: "The university committee decided to _____ (account for / carry out) the new campus sustainability guidelines.", options: ["carry out", "account for", "give in", "look into"] },
          { id: "v3", skill: "vocabulary", category: "Lexical Upgrades", prompt: "Which phrasing represents a Band 8+ academic upgrade for 'a big change' in IELTS Writing?", options: ["a substantial transformation", "a huge difference", "a super big shift", "a massive modification"] },
          { id: "v4", skill: "vocabulary", category: "Academic Verbs", prompt: "Wind and solar energy now _____ for approximately 28% of national electrical capacity.", options: ["account", "amount", "constitute for", "represent of"] },
          { id: "r1", skill: "reading", category: "Inference", prompt: "Passage: 'While solar energy adoption surged by 40% in urban regions, rural electrification still predominantly relies on biomass.' True, False, or Not Given: Rural areas primarily use solar power.", options: ["False", "True", "Not Given"] },
          { id: "r2", skill: "reading", category: "TFNG Distractors", prompt: "Passage: 'The high-speed rail line opened in 2021 and carries 50,000 commuters daily.' True, False, or Not Given: The high-speed rail line is faster than previous diesel engines.", options: ["Not Given", "True", "False"] },
          { id: "l1", skill: "listening", category: "Form Completion", prompt: "Speaker: 'The seminar will take place in the Henderson Auditorium on Thursday, 14th of October.' Question: The venue is the Henderson _____.", options: ["Auditorium", "Hall", "Library", "Center"] },
          { id: "m1", skill: "methodology", category: "IELTS Advantage Strategy", prompt: "According to the IELTS Advantage methodology, what is the crucial first step before writing any Task 2 essay?", options: ["Analyze general topic, micro-topic, and task instruction words", "Immediately start writing introductory sentences to save time", "Memorize 10 complicated idioms to impress the examiner", "Write down as many synonyms as possible"] }
        ]
      };
    }

    if (p === "/api/diagnostic/submit") {
      const answers = body.answers || {};
      let correct = 0;
      if (answers["g1"] === "increases") correct++;
      if (answers["g2"] === "has") correct++;
      if (answers["g3"] === "did") correct++;
      if (answers["g4"] === "advice") correct++;
      if (answers["v1"] === "profound") correct++;
      if (answers["v2"] === "carry out") correct++;
      if (answers["v3"] === "a substantial transformation") correct++;
      if (answers["v4"] === "account") correct++;
      if (answers["r1"] === "False") correct++;
      if (answers["r2"] === "Not Given") correct++;
      if (answers["l1"] === "Auditorium") correct++;
      if (answers["m1"] === "Analyze general topic, micro-topic, and task instruction words") correct++;

      const pct = Math.round((correct / 12) * 100);
      const estBand = correct >= 10 ? 7.5 : (correct >= 8 ? 7.0 : (correct >= 6 ? 6.0 : (correct >= 4 ? 5.0 : 4.0)));
      const cefr = correct >= 10 ? "C1" : (correct >= 8 ? "B2" : (correct >= 6 ? "B1" : "A2"));

      const prof = this.getProfile();
      prof.current_band = estBand;
      prof.cefr_level = cefr;
      this.saveProfile(prof);

      return {
        accuracy_percent: pct,
        correct_count: correct,
        total_questions: 12,
        estimated_cefr: cefr,
        estimated_ielts_range: `${estBand} - ${estBand + 0.5}`,
        estimated_band: estBand,
        strengths: ["Reading Comprehension", "Academic Vocabulary Recognition"],
        priority_skills: ["Conditionals & Inversion", "IELTS Advantage Task 2 Questionnaire"],
        recommended_study_plan: `Prioritize the IELTS Advantage Question Analysis Studio and daily Grammar Fill-Up clozes to achieve Band ${prof.target_band}.`
      };
    }

    // 12 Grammar Fill-Up Clozes
    if (p.startsWith("/api/grammar/fillups")) {
      const category = (p.includes("category=") ? p.split("category=")[1] : "all").split("&")[0];
      const allDrills = [
        {
          id: "fill_cond_1",
          category: "Conditionals",
          prompt: "If municipal authorities _____ (invest) in efficient light rail a decade ago, traffic congestion would not be so acute today.",
          acceptable: ["had invested"],
          explanation: "Mixed conditional: Past unreal condition ('had invested') producing a present consequence ('would not be so acute').",
          band_note: "Mixed conditionals are a hallmark indicator of Band 8+ Grammatical Range."
        },
        {
          id: "fill_cond_2",
          category: "Conditionals",
          prompt: "If the government were to raise carbon taxes, corporations _____ (seek) cleaner manufacturing alternatives.",
          acceptable: ["would seek"],
          explanation: "Second conditional: 'were to + verb' in the condition requires 'would + base verb' in the main clause.",
          band_note: "Ideal for formulating balanced hypothetical proposals in Task 2."
        },
        {
          id: "fill_pass_1",
          category: "Passive Voice & Impersonal Structures",
          prompt: "It is widely _____ (argue) by educationalists that early childhood literacy bridges socioeconomic divides.",
          acceptable: ["argued", "contended", "believed"],
          explanation: "Impersonal passive reporting: 'It is + past participle + that-clause' establishes objective academic register.",
          band_note: "Replaces informal 'People think that' with Band 7+ academic elegance."
        },
        {
          id: "fill_pass_2",
          category: "Passive Voice & Impersonal Structures",
          prompt: "Comprehensive clinical trials must be _____ (carry out) before new pharmaceuticals receive market authorization.",
          acceptable: ["carried out", "conducted"],
          explanation: "Modal passive: 'must be + past participle'. Note 'carried out' is the past participle of 'carry out'.",
          band_note: "Maintains formal passive distance when discussing policy standards."
        },
        {
          id: "fill_sva_1",
          category: "Subject-Verb Agreement",
          prompt: "The rapid expansion of metropolitan transit networks _____ (have / has) reduced average commuting times.",
          acceptable: ["has"],
          explanation: "The true head subject is 'The rapid expansion' (singular), not the intervening plural noun 'networks'.",
          band_note: "Classic IELTS trap: never let an intervening prepositional noun alter verb concord."
        },
        {
          id: "fill_sva_2",
          category: "Subject-Verb Agreement",
          prompt: "Each of the experimental cohorts _____ (was / were) observed under rigorous environmental controls.",
          acceptable: ["was"],
          explanation: "'Each of + plural noun' always takes a singular verb in standard formal English.",
          band_note: "Essential precision rule for both Task 1 reports and Task 2 essays."
        },
        {
          id: "fill_inv_1",
          category: "Inversion",
          prompt: "Not only _____ (do / does / did) automated robotics increase production velocity, but they also minimize industrial injuries.",
          acceptable: ["do"],
          explanation: "Negative adverbial inversion: 'Not only + auxiliary verb (do) + plural subject (robotics) + main verb'.",
          band_note: "Inversion structures demonstrate Band 8+ rhetorical mastery to examiners."
        },
        {
          id: "fill_inv_2",
          category: "Inversion",
          prompt: "Seldom _____ (have / has / do) economists witnessed such rapid technological disruption in employment sectors.",
          acceptable: ["have"],
          explanation: "Adverbial inversion with 'Seldom': auxiliary 'have' precedes the plural subject 'economists'.",
          band_note: "Adds dramatic emphasis to high-impact thesis statements."
        },
        {
          id: "fill_rel_1",
          category: "Relative & Participle Clauses",
          prompt: "_____ (Having / Have / Had) scrutinized the empirical telemetry, the research committee authorized the trial.",
          acceptable: ["Having"],
          explanation: "Perfect participle clause ('Having + past participle') denotes an action completed prior to the main clause verb.",
          band_note: "Seamlessly synthesizes complex causes without overusing repetitive linkers like 'because' or 'so'."
        },
        {
          id: "fill_prep_1",
          category: "Prepositions & Concordance",
          prompt: "Heavy commercial traffic exerts a profoundly detrimental impact _____ (on / in / at) urban air quality.",
          acceptable: ["on", "upon"],
          explanation: "The noun 'impact' takes the dependent preposition 'on' (or 'upon').",
          band_note: "Correct prepositional collocations are vital for Band 7+ Lexical and Grammatical descriptors."
        },
        {
          id: "fill_hedge_1",
          category: "Hedging & Modality",
          prompt: "The survey results tend to _____ (suggest / suggests / suggesting) that remote work bolsters employee retention.",
          acceptable: ["suggest"],
          explanation: "'Tend to + base infinitive verb' is an academic hedging structure preventing unsubstantiated over-generalization.",
          band_note: "IELTS examiners penalize sweeping absolutes. Hedging with 'tends to suggest' aligns with Band 8+ style."
        },
        {
          id: "fill_art_1",
          category: "Articles & Countability",
          prompt: "Professor Vance offered invaluable _____ (advice / advices) regarding methodology design.",
          acceptable: ["advice"],
          explanation: "'Advice' is strictly uncountable in English and can never take a plural '-s' or indefinite 'an'.",
          band_note: "Frequent error penalized by examiners: never write 'an advice' or 'advices'."
        }
      ];

      if (category && category !== "all") {
        return { drills: allDrills.filter(d => d.category.toLowerCase().includes(category.toLowerCase())) };
      }
      return { drills: allDrills };
    }

    if (p === "/api/grammar/fillups/submit") {
      const drillId = body.drill_id || "";
      const userAns = (body.user_answer || "").trim().toLowerCase();
      const allDrills = this.handleRequest("/api/grammar/fillups").drills;
      const drill = allDrills.find(d => d.id === drillId);
      if (!drill) return { is_correct: false, error: "Drill not found" };

      const isCorrect = drill.acceptable.some(acc => acc.toLowerCase() === userAns);
      if (!isCorrect) {
        this.addMistake("grammar", drill.category, userAns || "(blank)", drill.acceptable[0], drill.explanation);
      }
      return {
        is_correct: isCorrect,
        acceptable_answers: drill.acceptable,
        explanation: drill.explanation,
        band_note: drill.band_note
      };
    }

    if (p === "/api/grammar/adaptive") {
      return {
        target_category: "Subject-Verb Agreement",
        message: "Personalized focus: Mastering complex subject-verb concordance in IELTS clauses.",
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
      let reply = "I am ready to help you prepare for IELTS. What would you like to practice: IELTS Advantage Question Analysis, Grammar Fill-Up Clozes, Topic Vocabulary Vault, Reading, Writing, or Speaking?";

      if (msg.includes("affect") && msg.includes("effect")) {
        reply = "**'Affect' vs 'Effect'**:\n\n• **Affect** is almost always a **verb** meaning 'to influence':\n  *\"Technological changes directly affect the workforce.\"*\n\n• **Effect** is almost always a **noun** meaning 'the result':\n  *\"The legislation had a profound effect on emissions.\"*\n\n**Memory Tip (RAVEN)**:\n**R**emember: **A**ffect = **V**erb, **E**ffect = **N**oun.";
      } else if (msg.includes("i am agree")) {
        reply = "⚠️ **Grammar Slip Detected**: 'I am agree' is incorrect in English.\n\n• **Correction**: *'I agree with this perspective.'*\n• **Band 8+ Academic Upgrade**: *'I strongly concur with this notion / I subscribe to this viewpoint.'*\n• **Reason**: 'Agree' is a full active verb and does not use 'am' in simple present.";
      } else if (msg.includes("advantage") || msg.includes("questionnaire") || msg.includes("chris pell")) {
        reply = "**IELTS Advantage Core Methodology (Chris Pell)**:\n\n1. **Question Analysis (The 100% Rule)**: Never write before isolating the General Topic, Micro-Topic, and exact Task Words.\n2. **The Coffee Shop Method**: Brainstorm simple, logical ideas as if chatting with a friend in a coffee shop.\n3. **PEEL Structure**: Point -> Explain (Why) -> Example (Real world) -> Link (Result).\n4. **3-Step Speaking Strategy**: Direct Answer -> Reason -> Example/Anecdote.";
      }
      return { reply: reply };
    }

    return { error: "Unknown route" };
  }
};

// -------------------------------------------------------------
// Unified API Call Bridge (Online REST or Standalone Local)
// -------------------------------------------------------------
async function callApi(url, method = "GET", body = null) {
  if (appState.forcedOffline) {
    return OfflineLocalEngine.handleRequest(url, method, body);
  }

  try {
    const opts = { method: method, headers: { "Content-Type": "application/json" } };
    if (body && (method === "POST" || method === "PUT")) {
      opts.body = JSON.stringify(body);
    }
    const res = await fetch(API_BASE + url, opts);
    if (!res.ok) throw new Error("HTTP error " + res.status);
    return await res.json();
  } catch (err) {
    // Graceful offline fallback
    return OfflineLocalEngine.handleRequest(url, method, body);
  }
}

// -------------------------------------------------------------
// Universal Audio & Speech Engine (Android Native Bridge + Web Speech)
// -------------------------------------------------------------
let isCurrentlySpeaking = false;

function speakText(text, btnElement) {
  if (!text) return;

  if (isCurrentlySpeaking) {
    stopAudioSpeech(btnElement);
    return;
  }

  const cleanText = text.replace(/[#*_>`•\[\]]/g, " ").replace(/\s+/g, " ").trim();

  // 1. Android Native TTS Bridge (Pixel Phone & Tablet APK)
  if (window.AndroidTTS && typeof window.AndroidTTS.speak === "function") {
    isCurrentlySpeaking = true;
    if (btnElement) btnElement.innerHTML = "⏹️ Stop Audio";

    window.onTTSStarted = () => {
      isCurrentlySpeaking = true;
      if (btnElement) btnElement.innerHTML = "⏹️ Stop Audio";
    };
    window.onTTSFinished = () => {
      isCurrentlySpeaking = false;
      if (btnElement) btnElement.innerHTML = "🔊 Play Audio Script";
    };
    window.onTTSError = () => {
      isCurrentlySpeaking = false;
      if (btnElement) btnElement.innerHTML = "🔊 Play Audio Script";
    };

    window.AndroidTTS.speak(cleanText);
    return;
  }

  // 2. Desktop & Mobile Browser Web Speech API fallback
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(cleanText);
    utt.lang = "en-GB";
    utt.rate = 0.95;

    utt.onstart = () => {
      isCurrentlySpeaking = true;
      if (btnElement) btnElement.innerHTML = "⏹️ Stop Audio";
    };
    utt.onend = () => {
      isCurrentlySpeaking = false;
      if (btnElement) btnElement.innerHTML = "🔊 Play Audio Script";
    };
    utt.onerror = () => {
      isCurrentlySpeaking = false;
      if (btnElement) btnElement.innerHTML = "🔊 Play Audio Script";
    };

    window.speechSynthesis.speak(utt);
    return;
  }

  alert("Audio speech output is not supported on this device/browser.");
}

function stopAudioSpeech(btnElement) {
  isCurrentlySpeaking = false;
  if (window.AndroidTTS && typeof window.AndroidTTS.stop === "function") {
    window.AndroidTTS.stop();
  }
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }
  if (btnElement) btnElement.innerHTML = "🔊 Play Audio Script";
}

// -------------------------------------------------------------
// Screen Dimension & Multi-Platform Adaptive Engine (v1.5.0)
// -------------------------------------------------------------
function updateScreenDimensions() {
  const w = window.innerWidth;
  const h = window.innerHeight;
  const dpr = window.devicePixelRatio || 1;

  // Set CSS custom properties for pixel-perfect dynamic layouts
  document.documentElement.style.setProperty("--app-width", `${w}px`);
  document.documentElement.style.setProperty("--app-height", `${h}px`);
  document.documentElement.style.setProperty("--vh", `${h * 0.01}px`);

  // Detect Device Category
  const isCompactMobile = w < 480;
  const isMobile = w < 768;
  const isTablet = w >= 768 && w <= 1180;
  const isDesktop = w > 1180 && w <= 1600;
  const isUltrawide = w > 1600;
  const isLandscape = window.matchMedia("(orientation: landscape)").matches;

  // Detect Platform & OS
  const ua = navigator.userAgent || "";
  const platform = navigator.platform || "";
  const isIOS = /iPad|iPhone|iPod/.test(ua) || (platform === "MacIntel" && navigator.maxTouchPoints > 1);
  const isWindows = /Win/i.test(ua) || /Win/i.test(platform);
  const isAndroid = /Android/i.test(ua);
  const isMac = /Mac/i.test(ua) && !isIOS;

  // Sync classes on body
  document.body.classList.toggle("device-compact", isCompactMobile);
  document.body.classList.toggle("device-mobile", isMobile);
  document.body.classList.toggle("device-tablet", isTablet);
  document.body.classList.toggle("device-desktop", isDesktop);
  document.body.classList.toggle("device-ultrawide", isUltrawide);
  document.body.classList.toggle("orientation-landscape", isLandscape);
  document.body.classList.toggle("orientation-portrait", !isLandscape);
  document.body.classList.toggle("platform-ios", isIOS);
  document.body.classList.toggle("platform-windows", isWindows);
  document.body.classList.toggle("platform-android", isAndroid);
  document.body.classList.toggle("platform-mac", isMac);

  // Determine user-friendly profile label
  let osLabel = "Windows";
  if (isIOS) osLabel = isTablet ? "iPadOS" : "iOS";
  else if (isAndroid) osLabel = isTablet ? "Android Tablet" : "Android Phone";
  else if (isWindows) osLabel = "Windows";
  else if (isMac) osLabel = "macOS";

  let devLabel = "Mobile";
  if (isTablet) devLabel = "Tablet";
  else if (isDesktop) devLabel = "Desktop";
  else if (isUltrawide) devLabel = "Ultrawide PC";

  const badge = document.getElementById("screenDimensionBadge");
  const devScreen = document.getElementById("devScreenSpec");
  const deviceLabel = document.getElementById("deviceProfileLabel");

  const badgeText = `${osLabel} • ${w}×${h} (${devLabel})`;
  if (badge) badge.innerHTML = `${badgeText} • <span class="version-tag" id="headerVersionBadge">v1.5.2</span>`;
  if (devScreen) devScreen.innerText = `${badgeText} @ ${dpr.toFixed(1)}x DPR`;
  if (deviceLabel) deviceLabel.innerText = `${devLabel.toUpperCase()} (${osLabel})`;

  // Ensure connectivity badge text fits the current screen size
  updateConnectivityStatus();
}

window.addEventListener("resize", updateScreenDimensions);
window.addEventListener("orientationchange", () => {
  setTimeout(updateScreenDimensions, 100);
});

// iOS Audio Unlock on first user gesture
function initIOSAudioUnlock() {
  const unlockAudio = () => {
    if (window.speechSynthesis) {
      const silent = new SpeechSynthesisUtterance("");
      silent.volume = 0;
      window.speechSynthesis.speak(silent);
    }
    window.removeEventListener("touchstart", unlockAudio);
    window.removeEventListener("click", unlockAudio);
  };
  window.addEventListener("touchstart", unlockAudio, { passive: true, once: true });
  window.addEventListener("click", unlockAudio, { passive: true, once: true });
}

// Windows Keyboard Shortcuts
function initWindowsShortcuts() {
  window.addEventListener("keydown", (e) => {
    // Alt + 1..6 navigation
    if (e.altKey && !e.ctrlKey && !e.shiftKey) {
      if (e.key === "1") { e.preventDefault(); navigateToTab("dashboard"); }
      else if (e.key === "2") { e.preventDefault(); navigateToTab("reading"); }
      else if (e.key === "3") { e.preventDefault(); navigateToTab("writing"); }
      else if (e.key === "4") { e.preventDefault(); navigateToTab("speaking"); }
      else if (e.key === "5") { e.preventDefault(); navigateToTab("listening"); }
      else if (e.key.toLowerCase() === "t") { e.preventDefault(); toggleTheme(); }
    }
    // Escape closes modals
    if (e.key === "Escape") {
      const modal = document.getElementById("goalWelcomeModal");
      if (modal && modal.classList.contains("open")) {
        modal.classList.remove("open");
      }
    }
  });
}

// -------------------------------------------------------------
// Light / Dark Theme Manager with System Preference Sync
// -------------------------------------------------------------
function initTheme() {
  const savedTheme = localStorage.getItem("ielts_theme");
  const systemPrefersLight = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches;
  const isLight = savedTheme === "light" || (!savedTheme && systemPrefersLight);

  if (isLight) {
    document.body.classList.add("light-theme");
  } else {
    document.body.classList.remove("light-theme");
  }
  updateThemeUI();

  // Listen to OS system theme changes if not manually locked
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: light)").addEventListener("change", (e) => {
      if (!localStorage.getItem("ielts_theme")) {
        if (e.matches) {
          document.body.classList.add("light-theme");
        } else {
          document.body.classList.remove("light-theme");
        }
        updateThemeUI();
      }
    });
  }
}

function updateThemeUI() {
  const isLight = document.body.classList.contains("light-theme");
  const btn = document.getElementById("themeToggleBtn");
  const metaThemeColor = document.getElementById("metaThemeColor");

  if (btn) {
    btn.innerHTML = isLight ? "🌞" : "🌙";
    btn.title = isLight ? "Switch to Dark AMOLED Theme (Alt+T)" : "Switch to Crisp Light Theme (Alt+T)";
  }
  if (metaThemeColor) {
    metaThemeColor.setAttribute("content", isLight ? "#f8fafc" : "#0f141c");
  }

  // Synchronize native Android system status bar and navigation bar seamlessly
  if (window.AndroidTheme && typeof window.AndroidTheme.setDarkMode === 'function') {
    try {
      window.AndroidTheme.setDarkMode(!isLight);
    } catch (e) {
      console.warn("Could not sync Android native theme:", e);
    }
  }
}

function toggleTheme() {
  const isLight = document.body.classList.toggle("light-theme");
  localStorage.setItem("ielts_theme", isLight ? "light" : "dark");
  updateThemeUI();
  showBandToast(
    isLight ? "☀️ Crisp Light Mode Active" : "🌙 AMOLED Dark Mode Active",
    isLight ? "High-contrast daylight theme enabled" : "Deep contrast night theme enabled"
  );
}

// -------------------------------------------------------------
// Navigation Tabs & Categorization
// -------------------------------------------------------------
function initNavigation() {
  const navItems = document.querySelectorAll(".nav-item");
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      navItems.forEach(n => n.classList.remove("active"));
      item.classList.add("active");

      const tabId = item.getAttribute("data-tab");
      appState.currentTab = tabId;

      document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
      const target = document.getElementById("tab-" + tabId);
      if (target) target.classList.add("active");

      // Auto-trigger tab data initialization
      if (tabId === "dashboard") loadDashboard();
      if (tabId === "grammar") initGrammar();
      if (tabId === "vocab") initVocabulary();
      if (tabId === "reading") loadReading();
      if (tabId === "listening") loadListening();
      if (tabId === "mistakes") loadMistakes();
      if (tabId === "advantage") loadAdvantagePrompt("stem");
    });
  });

  // Mobile Category Filter Strip
  initMobileCategoryFilter();

  // Connectivity toggle
  const toggleBtn = document.getElementById("toggleOfflineBtn");
  toggleBtn.addEventListener("click", () => {
    appState.forcedOffline = !appState.forcedOffline;
    toggleBtn.innerText = `Force Offline: ${appState.forcedOffline ? "ON" : "OFF"}`;
    updateConnectivityStatus();
    loadDashboard();
  });

  // Theme toggle button click
  const themeBtn = document.getElementById("themeToggleBtn");
  if (themeBtn) {
    themeBtn.addEventListener("click", toggleTheme);
  }
}

function initMobileCategoryFilter() {
  const filterBtns = document.querySelectorAll(".cat-filter-btn");
  const navGroups = document.querySelectorAll(".nav-category-group");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const filter = btn.getAttribute("data-filter");
      navGroups.forEach(group => {
        const groupCat = group.getAttribute("data-group");
        if (filter === "all") {
          group.style.display = "";
        } else if (filter === "exam") {
          group.style.display = groupCat === "exam" ? "" : "none";
        } else if (filter === "advantage") {
          group.style.display = groupCat === "advantage" ? "" : "none";
        } else if (filter === "core") {
          group.style.display = (groupCat === "core" || groupCat === "system") ? "" : "none";
        } else {
          group.style.display = groupCat === filter ? "" : "none";
        }
      });
    });
  });
}

// Quick AI Tutor Chat Prompt helper
window.sendQuickPrompt = function(promptText) {
  const input = document.getElementById("chatInput");
  if (input) {
    input.value = promptText;
    const sendBtn = document.getElementById("sendMessageBtn");
    if (sendBtn) sendBtn.click();
  }
};

// Chip Selector Bridge Functions
window.selectAdvantageChip = function(promptKey, btn) {
  const container = document.getElementById("advantagePromptChips");
  if (container) {
    container.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
  }
  if (btn) btn.classList.add("active");
  const sel = document.getElementById("advantagePromptSelect");
  if (sel) sel.value = promptKey;
  loadAdvantagePrompt(promptKey);
};

window.selectGrammarFilter = function(category, btn) {
  const container = document.getElementById("grammarClozeFilterChips");
  if (container) {
    container.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
  }
  if (btn) btn.classList.add("active");
  const sel = document.getElementById("clozeCategorySelect");
  if (sel) sel.value = category;
  filterFillupDrills(category);
};

window.selectVocabTopicChip = function(topicKey, btn) {
  const container = document.getElementById("vocabTopicFilterChips");
  if (container) {
    container.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
  }
  if (btn) btn.classList.add("active");
  const sel = document.getElementById("vocabTopicSelect");
  if (sel) sel.value = topicKey;
  renderVocabTopic(topicKey);
};

window.selectReadingPassageChip = function(passageId, btn) {
  const container = document.getElementById("readingPassageChips");
  if (container) {
    container.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
  }
  if (btn) btn.classList.add("active");
  const sel = document.getElementById("readingPassageSelect");
  if (sel) sel.value = passageId;
  switchReadingPassage(passageId);
};

window.selectListeningSectionChip = function(secId, btn) {
  const container = document.getElementById("listeningSectionChips");
  if (container) {
    container.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
  }
  if (btn) btn.classList.add("active");
  switchListeningSection(secId);
};

window.selectWritingPromptChip = function(promptId, btn) {
  const container = document.getElementById("writingPromptChips");
  if (container) {
    container.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
  }
  if (btn) btn.classList.add("active");
  const sel = document.getElementById("writingPromptSelect");
  if (sel) sel.value = promptId;
  switchWritingPrompt(promptId);
};

window.selectSpeakingSetChip = function(setId, btn) {
  const container = document.getElementById("speakingExamChips");
  if (container) {
    container.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
  }
  if (btn) btn.classList.add("active");
  const sel = document.getElementById("speakingExamSetSelect");
  if (sel) {
    sel.value = setId;
    if (window.onSpeakingSetChanged) window.onSpeakingSetChanged(setId);
  }
};

function updateConnectivityStatus() {
  const badge = document.getElementById("connectivityBadge");
  const text = document.getElementById("statusText");
  const toggleBtn = document.getElementById("toggleOfflineBtn");
  const isMobile = window.innerWidth < 768;

  if (appState.forcedOffline) {
    if (badge) badge.className = "status-badge offline";
    if (badge) badge.title = "Offline Engine: Forced Offline (100% Private)";
    if (text) text.innerText = isMobile ? "OFFLINE" : "OFFLINE (Private)";
    if (toggleBtn) toggleBtn.innerText = isMobile ? "Offline: ON" : "Force Offline: ON";
  } else if (navigator.onLine) {
    if (badge) badge.className = "status-badge online";
    if (badge) badge.title = "Hybrid Online + Offline AI Engine Ready";
    if (text) text.innerText = isMobile ? "ONLINE" : "ONLINE (Hybrid)";
    if (toggleBtn) toggleBtn.innerText = isMobile ? "Offline: OFF" : "Force Offline: OFF";
  } else {
    if (badge) badge.className = "status-badge offline";
    if (badge) badge.title = "Local Offline RAG Active";
    if (text) text.innerText = isMobile ? "OFFLINE" : "OFFLINE (Local RAG)";
    if (toggleBtn) toggleBtn.innerText = isMobile ? "Offline: OFF" : "Force Offline: OFF";
  }
}

// -------------------------------------------------------------
// Daily Goal & Category Progress Mastery System (v1.4.0)
// -------------------------------------------------------------
const GOAL_DEFINITIONS = {
  speaking: {
    icon: "🎙️",
    title: "Complete 1 Official Speaking Interview",
    desc: "Practice with Dr. Harrison in the 3-Part Examiner Room using the 3-Step Strategy (Direct Answer -> Reason -> Concrete Example).",
    targetTab: "speaking",
    targetCount: 1,
    unit: "interview",
    buttonLabel: "Start Speaking Interview",
    category: "exam"
  },
  reading: {
    icon: "📑",
    title: "Master 1 Academic Reading Passage",
    desc: "Complete 4 reading questions using Cambridge Skimming & Scanning keyword paraphrase mapping.",
    targetTab: "reading",
    targetCount: 1,
    unit: "passage",
    buttonLabel: "Open Reading Passage",
    category: "exam"
  },
  writing: {
    icon: "✍️",
    title: "Write & Audit Task 2 PEEL Essay",
    desc: "Draft or evaluate a 250+ word essay and run the 10-Point IELTS Advantage Self-Assessment Checklist.",
    targetTab: "writing",
    targetCount: 1,
    unit: "essay",
    buttonLabel: "Open Writing Studio",
    category: "exam"
  },
  grammar: {
    icon: "✏️",
    title: "Solve 5 Grammar Fill-Up Clozes",
    desc: "Target high-yield conditionals, inversion, and impersonal passives to eliminate band penalties.",
    targetTab: "grammar",
    targetCount: 5,
    unit: "clozes",
    buttonLabel: "Practice Grammar Clozes",
    category: "core"
  },
  vocab: {
    icon: "🧠",
    title: "Review 10 SRS Vocabulary Cards",
    desc: "Master Band 8+ academic collocations and lexical upgrades with SuperMemo SM-2 spaced repetition.",
    targetTab: "vocab",
    targetCount: 10,
    unit: "cards",
    buttonLabel: "Open SRS Flashcards",
    category: "core"
  },
  diagnostic: {
    icon: "🎯",
    title: "Take 12-Question Diagnostic Test",
    desc: "Assess baseline grammar, vocabulary, reading, listening, and IELTS Advantage methodology in under 5 minutes.",
    targetTab: "diagnostic",
    targetCount: 1,
    unit: "test",
    buttonLabel: "Start Diagnostic Test",
    category: "core"
  },
  listening: {
    icon: "🎧",
    title: "Complete Section 3/4 Audio Listening Practice",
    desc: "Listen to the Cambridge dialogue script and answer 4 questions with zero replay cheats.",
    targetTab: "listening",
    targetCount: 1,
    unit: "section",
    buttonLabel: "Start Listening Audio",
    category: "exam"
  }
};

window.navigateToTab = function(tabId) {
  const cleanId = tabId.replace("tab-", "");
  const navItem = document.querySelector(`.nav-item[data-tab="${cleanId}"]`);
  if (navItem) {
    navItem.click();
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else {
    document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
    document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
    const pane = document.getElementById("tab-" + cleanId);
    if (pane) pane.classList.add("active");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};

function getDailyGoal() {
  const today = new Date().toDateString();
  const raw = localStorage.getItem("gama_daily_goal");
  if (raw) {
    try {
      const parsed = JSON.parse(raw);
      if (parsed.date === today) return parsed;
    } catch (e) {}
  }
  return {
    key: "speaking",
    date: today,
    progress: 0,
    target: 1,
    achieved: false
  };
}

function saveDailyGoal(goal) {
  localStorage.setItem("gama_daily_goal", JSON.stringify(goal));
}

window.setDailyGoal = function(goalKey, btn) {
  if (!GOAL_DEFINITIONS[goalKey]) return;
  const today = new Date().toDateString();
  const currentGoal = getDailyGoal();
  const updated = {
    key: goalKey,
    date: today,
    progress: (currentGoal.key === goalKey && currentGoal.date === today) ? currentGoal.progress : 0,
    target: GOAL_DEFINITIONS[goalKey].targetCount,
    achieved: false
  };
  saveDailyGoal(updated);

  const chipContainer = document.getElementById("dashboardGoalChips");
  if (chipContainer) {
    chipContainer.querySelectorAll(".goal-chip").forEach(c => c.classList.remove("active"));
  }
  const activeChip = btn || document.getElementById("chip_goal_" + goalKey);
  if (activeChip) activeChip.classList.add("active");

  renderDailyGoal();
};

function renderDailyGoal() {
  const goal = getDailyGoal();
  const config = GOAL_DEFINITIONS[goal.key] || GOAL_DEFINITIONS["speaking"];

  const iconEl = document.getElementById("activeGoalIcon");
  const titleEl = document.getElementById("activeGoalTitle");
  const descEl = document.getElementById("activeGoalDescription");
  const badgeEl = document.getElementById("goalStatusBadge");
  const fillEl = document.getElementById("goalProgressFill");
  const achieveBtn = document.getElementById("achieveGoalBtn");
  const completeBtn = document.getElementById("completeGoalBtn");

  if (iconEl) iconEl.innerText = config.icon;
  if (titleEl) titleEl.innerText = config.title;
  if (descEl) descEl.innerText = config.desc;

  const pct = Math.min(100, Math.round(((goal.progress || 0) / config.targetCount) * 100));
  if (fillEl) fillEl.style.width = (goal.achieved ? 100 : Math.max(10, pct)) + "%";

  if (badgeEl) {
    if (goal.achieved) {
      badgeEl.innerText = "ACHIEVED 🎉";
      badgeEl.style.background = "#10b981";
      badgeEl.style.color = "#ffffff";
    } else {
      badgeEl.innerText = `${goal.progress || 0}/${config.targetCount} ${config.unit.toUpperCase()} (${pct}%)`;
      badgeEl.style.background = "rgba(99, 102, 241, 0.2)";
      badgeEl.style.color = "#818cf8";
    }
  }

  if (achieveBtn) {
    achieveBtn.innerHTML = `<span>🚀</span> ${config.buttonLabel}`;
  }

  if (completeBtn) {
    completeBtn.innerText = goal.achieved ? "✓ Completed Today" : "✓ Mark Achieved";
    completeBtn.disabled = !!goal.achieved;
  }

  const chip = document.getElementById("chip_goal_" + goal.key);
  if (chip) {
    const chipContainer = document.getElementById("dashboardGoalChips");
    if (chipContainer) chipContainer.querySelectorAll(".goal-chip").forEach(c => c.classList.remove("active"));
    chip.classList.add("active");
  }
}

window.helpAchieveGoal = function() {
  const goal = getDailyGoal();
  const config = GOAL_DEFINITIONS[goal.key] || GOAL_DEFINITIONS["speaking"];
  showBandToast("🎯 Daily Mission Navigation", `Opening ${config.title}... Let's hit your goal!`);
  navigateToTab(config.targetTab);
};

window.markGoalAchieved = function() {
  const goal = getDailyGoal();
  const config = GOAL_DEFINITIONS[goal.key] || GOAL_DEFINITIONS["speaking"];
  goal.achieved = true;
  goal.progress = config.targetCount;
  saveDailyGoal(goal);

  const prof = OfflineLocalEngine.getProfile();
  prof.current_band = Math.min(9.0, Math.round((prof.current_band + 0.25) * 2) / 2);
  OfflineLocalEngine.saveProfile(prof);

  const currEl = document.getElementById("currentBandMetric");
  if (currEl) currEl.innerText = prof.current_band.toFixed(1);

  showBandToast("🏆 Daily Goal Achieved!", `Outstanding work! You earned a +0.25 Band Boost. New Band: ${prof.current_band.toFixed(1)}`);
  renderDailyGoal();
  renderCategoryProgress();
};

function initDailyGoalModal() {
  const modal = document.getElementById("goalWelcomeModal");
  if (!modal) return;

  const closeBtn = document.getElementById("closeGoalModalBtn");
  const skipBtn = document.getElementById("btnSkipGoalModal");

  function closeModal() {
    modal.classList.remove("open");
    sessionStorage.setItem("gama_goal_prompted", "true");
  }

  if (closeBtn) closeBtn.onclick = closeModal;
  if (skipBtn) skipBtn.onclick = closeModal;

  modal.querySelectorAll(".modal-goal-opt").forEach(btn => {
    btn.onclick = () => {
      const goalKey = btn.getAttribute("data-goal");
      if (goalKey) {
        setDailyGoal(goalKey);
        closeModal();
      }
    };
  });

  if (!sessionStorage.getItem("gama_goal_prompted")) {
    setTimeout(() => {
      modal.classList.add("open");
    }, 600);
  }
}

function getCategoryStats() {
  const raw = localStorage.getItem("gama_category_stats");
  if (raw) {
    try {
      return JSON.parse(raw);
    } catch (e) {}
  }
  return {
    core: { grammarDone: 2, vocabReviewed: 6, diagTaken: 1 },
    exam: { readingDone: 1, listeningDone: 1, writingDone: 1, speakingDone: 1 },
    advantage: { analysisDone: 1, peelDone: 1, coffeeDone: 1, checklistDone: 4 },
    system: { mistakesResolved: 1, srsReviewed: 6, backupsDone: 1 }
  };
}

function saveCategoryStats(stats) {
  localStorage.setItem("gama_category_stats", JSON.stringify(stats));
}

function renderCategoryProgress() {
  const stats = getCategoryStats();
  const prof = OfflineLocalEngine.getProfile();

  // 1. Core
  const corePct = Math.min(100, Math.round(((stats.core.grammarDone / 12) * 45) + ((stats.core.vocabReviewed / 20) * 35) + (stats.core.diagTaken ? 20 : 10)));
  const corePctEl = document.getElementById("catProgressPct_core");
  const coreBarEl = document.getElementById("catProgressBar_core");
  if (corePctEl) corePctEl.innerText = corePct + "%";
  if (coreBarEl) coreBarEl.style.width = corePct + "%";
  const diagMetric = document.getElementById("catMetricDiag");
  if (diagMetric) diagMetric.innerText = stats.core.diagTaken ? `Completed (Band ${prof.current_band.toFixed(1)})` : "Pending";
  const cefrMetric = document.getElementById("catMetricCefr");
  if (cefrMetric) cefrMetric.innerText = `${prof.cefr_level} Independent`;
  const tutorMetric = document.getElementById("catMetricTutor");
  if (tutorMetric) tutorMetric.innerText = `${stats.core.grammarDone + stats.core.vocabReviewed} Items Practiced`;

  // 2. Exam
  const examItems = stats.exam.speakingDone + stats.exam.writingDone + stats.exam.readingDone + stats.exam.listeningDone;
  const examPct = Math.min(100, Math.max(25, Math.round((examItems / 8) * 100)));
  const examPctEl = document.getElementById("catProgressPct_exam");
  const examBarEl = document.getElementById("catProgressBar_exam");
  if (examPctEl) examPctEl.innerText = examPct + "%";
  if (examBarEl) examBarEl.style.width = examPct + "%";
  const spkMetric = document.getElementById("catMetricSpeaking");
  if (spkMetric) spkMetric.innerText = stats.exam.speakingDone > 0 ? `${stats.exam.speakingDone} Mock(s) Completed` : "Set 1 Ready (Band 6.5)";
  const wrtMetric = document.getElementById("catMetricWriting");
  if (wrtMetric) wrtMetric.innerText = stats.exam.writingDone > 0 ? `${stats.exam.writingDone} Essay(s) Evaluated` : "Task 2 PEEL Ready";
  const rdMetric = document.getElementById("catMetricReading");
  if (rdMetric) rdMetric.innerText = stats.exam.readingDone > 0 ? `${stats.exam.readingDone} Passage(s) Done` : "Passage 1 Ready";
  const lsMetric = document.getElementById("catMetricListening");
  if (lsMetric) lsMetric.innerText = stats.exam.listeningDone > 0 ? `${stats.exam.listeningDone} Section(s) Done` : "Sec 1 Ready";

  // 3. Advantage
  const advPct = Math.min(100, Math.max(30, Math.round(((stats.advantage.analysisDone + stats.advantage.peelDone + stats.advantage.coffeeDone) / 6) * 100)));
  const advPctEl = document.getElementById("catProgressPct_advantage");
  const advBarEl = document.getElementById("catProgressBar_advantage");
  if (advPctEl) advPctEl.innerText = advPct + "%";
  if (advBarEl) advBarEl.style.width = advPct + "%";
  const advMetric = document.getElementById("catMetricAdvantage");
  if (advMetric) advMetric.innerText = `${stats.advantage.analysisDone} Prompts Analyzed`;
  const chkMetric = document.getElementById("catMetricChecklist");
  if (chkMetric) chkMetric.innerText = `${stats.advantage.checklistDone} Verified / 10`;
  const grmMetric = document.getElementById("catMetricGrammar");
  if (grmMetric) grmMetric.innerText = `${stats.core.grammarDone} Drills Solved (Streak: ${appState.fillupStreak})`;
  const vcbMetric = document.getElementById("catMetricVocab");
  if (vcbMetric) vcbMetric.innerText = `${stats.core.vocabReviewed} Cards Retained`;

  // 4. System
  const mistakes = OfflineLocalEngine.getMistakes();
  const activeMistakes = mistakes.filter(m => m.status !== "mastered");
  const sysPct = Math.min(100, Math.max(40, Math.round(((stats.system.srsReviewed / 12) * 50) + (activeMistakes.length === 0 ? 50 : 30))));
  const sysPctEl = document.getElementById("catProgressPct_system");
  const sysBarEl = document.getElementById("catProgressBar_system");
  if (sysPctEl) sysPctEl.innerText = sysPct + "%";
  if (sysBarEl) sysBarEl.style.width = sysPct + "%";
  const mstMetric = document.getElementById("catMetricMistakes");
  if (mstMetric) mstMetric.innerText = `${activeMistakes.length} Active / ${mistakes.length - activeMistakes.length} Mastered`;
  const accMetric = document.getElementById("catMetricAccuracy");
  const accRate = mistakes.length ? Math.round(((mistakes.length - activeMistakes.length) / mistakes.length) * 100) : 100;
  if (accMetric) accMetric.innerText = `${accRate}% Clean`;
  const timeMetric = document.getElementById("catMetricStudyTime");
  if (timeMetric) timeMetric.innerText = `${prof.daily_minutes} Min Target Active`;
  const storMetric = document.getElementById("catMetricStorage");
  if (storMetric) storMetric.innerText = "Local RAG Synced";
}

let toastTimeout = null;
function showBandToast(title, subtitle) {
  const toast = document.getElementById("bandUpdateToast");
  const tTitle = document.getElementById("toastTitle");
  const tSub = document.getElementById("toastSubtitle");
  if (!toast) return;

  if (tTitle) tTitle.innerText = title;
  if (tSub) tSub.innerText = subtitle;

  toast.classList.add("show");

  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 4500);
}

function recordPracticeActivity(skill, scoreOrBand, details) {
  const stats = getCategoryStats();
  const goal = getDailyGoal();

  if (skill === "reading") stats.exam.readingDone++;
  else if (skill === "listening") stats.exam.listeningDone++;
  else if (skill === "writing") stats.exam.writingDone++;
  else if (skill === "speaking") stats.exam.speakingDone++;
  else if (skill === "grammar") stats.core.grammarDone++;
  else if (skill === "vocab") stats.core.vocabReviewed++;
  else if (skill === "srs") stats.system.srsReviewed++;
  else if (skill === "advantage") {
    stats.advantage.analysisDone++;
    stats.advantage.peelDone++;
  }
  saveCategoryStats(stats);

  if (!goal.achieved) {
    if (
      (goal.key === "reading" && skill === "reading") ||
      (goal.key === "listening" && skill === "listening") ||
      (goal.key === "writing" && skill === "writing") ||
      (goal.key === "speaking" && skill === "speaking") ||
      (goal.key === "grammar" && skill === "grammar") ||
      (goal.key === "vocab" && (skill === "vocab" || skill === "srs"))
    ) {
      goal.progress = (goal.progress || 0) + 1;
      if (goal.progress >= (goal.target || 1)) {
        goal.achieved = true;
      }
      saveDailyGoal(goal);
    }
  }

  const prof = OfflineLocalEngine.getProfile();
  prof.skills_bands = prof.skills_bands || {
    reading: 6.5,
    listening: 7.0,
    writing: 6.0,
    speaking: 6.5,
    grammar: 7.0,
    vocab: 7.0
  };

  const parsedScore = parseFloat(scoreOrBand);
  if (!isNaN(parsedScore) && parsedScore > 0) {
    if (skill === "reading") prof.skills_bands.reading = Math.max(prof.skills_bands.reading, parsedScore);
    if (skill === "listening") prof.skills_bands.listening = Math.max(prof.skills_bands.listening, parsedScore);
    if (skill === "writing") prof.skills_bands.writing = Math.max(prof.skills_bands.writing, parsedScore);
    if (skill === "speaking") prof.skills_bands.speaking = Math.max(prof.skills_bands.speaking, parsedScore);
    if (skill === "grammar") prof.skills_bands.grammar = Math.min(9.0, prof.skills_bands.grammar + 0.1);
    if (skill === "vocab" || skill === "srs") prof.skills_bands.vocab = Math.min(9.0, prof.skills_bands.vocab + 0.1);
  }

  const baseAvg = (prof.skills_bands.reading + prof.skills_bands.listening + prof.skills_bands.writing + prof.skills_bands.speaking) / 4.0;
  const masteryBonus = Math.min(0.25, (stats.core.grammarDone * 0.02) + (stats.system.srsReviewed * 0.01));
  const newOverallBand = Math.min(9.0, Math.round((baseAvg + masteryBonus) * 2) / 2);

  prof.current_band = newOverallBand;
  let newCefr = "B2";
  if (newOverallBand >= 8.5) newCefr = "C2";
  else if (newOverallBand >= 7.0) newCefr = "C1";
  else if (newOverallBand >= 5.5) newCefr = "B2";
  else if (newOverallBand >= 4.0) newCefr = "B1";
  else newCefr = "A2";
  prof.cefr_level = newCefr;
  OfflineLocalEngine.saveProfile(prof);

  const currEl = document.getElementById("currentBandMetric");
  if (currEl) currEl.innerText = newOverallBand.toFixed(1);
  const cefrEl = document.getElementById("cefrMetric");
  if (cefrEl) cefrEl.innerText = `CEFR Level: ${newCefr}`;

  const skillLabel = skill.charAt(0).toUpperCase() + skill.slice(1);
  showBandToast(
    `🎯 ${skillLabel} Practiced! Band Score Updated`,
    `Current Overall Band: ${newOverallBand.toFixed(1)} (${newCefr}) • ${details || '+0.25 practice progress'}`
  );

  renderCategoryProgress();
  renderDailyGoal();
}

// -------------------------------------------------------------
// 1. Dashboard Module
// -------------------------------------------------------------
async function loadDashboard() {
  const data = await callApi("/api/dashboard");
  if (!data) return;

  const dash = data.dashboard;
  document.getElementById("currentBandMetric").innerText = dash.overall_band_estimate;
  document.getElementById("cefrMetric").innerText = `CEFR Level: ${dash.cefr_level}`;
  document.getElementById("targetBandMetric").innerText = dash.target_band;
  document.getElementById("srsDueMetric").innerText = dash.srs_metrics.items_due_today;
  document.getElementById("activeMistakesMetric").innerText = dash.mistake_book_metrics.active_mistakes_count;
  document.getElementById("accuracyRateMetric").innerText = `Accuracy: ${dash.mistake_book_metrics.accuracy_rate_percent}%`;

  if (data.daily_plan) {
    document.getElementById("dailyGreetingText").innerText = data.daily_plan.daily_greeting;
    const taskContainer = document.getElementById("dailyPlanTasksList");
    taskContainer.innerHTML = "";
    data.daily_plan.tasks.forEach(t => {
      const div = document.createElement("div");
      div.className = "task-item";
      div.innerHTML = `<strong>${t.title} (${t.duration_minutes} min)</strong><p>${t.description}</p>`;
      taskContainer.appendChild(div);
    });
  }

  // Skills Radar Bars
  const radarBox = document.getElementById("skillsRadarBox");
  radarBox.innerHTML = "";
  for (const [skill, score] of Object.entries(dash.skills_radar)) {
    const row = document.createElement("div");
    row.className = "radar-bar-row";
    const pct = Math.round((score / 9.0) * 100);
    row.innerHTML = `
      <span style="width: 90px;">${skill}</span>
      <div class="bar-track"><div class="bar-fill" style="width: ${pct}%;"></div></div>
      <span style="width: 45px; text-align: right; font-weight: 600;">Band ${score}</span>
    `;
    radarBox.appendChild(row);
  }

  // Render Daily Goal & Category Progress
  renderDailyGoal();
  renderCategoryProgress();
}

// -------------------------------------------------------------
// 2. AI Tutor Chat Module
// -------------------------------------------------------------
function initChat() {
  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendMessageBtn");
  const msgBox = document.getElementById("chatMessages");

  async function send() {
    const txt = chatInput.value.trim();
    if (!txt) return;

    // Append user turn
    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.innerHTML = `<div class="msg-bubble">${txt}</div>`;
    msgBox.appendChild(userDiv);
    chatInput.value = "";
    msgBox.scrollTop = msgBox.scrollHeight;

    const res = await callApi("/api/chat", "POST", { message: txt });
    const replyTxt = res ? res.reply : "I am experiencing difficulty connecting to the language model.";

    const tutorDiv = document.createElement("div");
    tutorDiv.className = "message tutor";
    tutorDiv.innerHTML = `<div class="msg-bubble">${replyTxt.replace(/\n/g, "<br>")}</div>`;
    msgBox.appendChild(tutorDiv);
    msgBox.scrollTop = msgBox.scrollHeight;
  }

  sendBtn.addEventListener("click", send);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") send();
  });
}

// -------------------------------------------------------------
// 3. 12-Question Diagnostic Test
// -------------------------------------------------------------
async function initDiagnostic() {
  const container = document.getElementById("diagnosticQuestionsContainer");
  const data = await callApi("/api/diagnostic/questions");
  if (!data || !data.questions) return;

  container.innerHTML = "";
  data.questions.forEach((q, idx) => {
    const qDiv = document.createElement("div");
    qDiv.className = "diagnostic-q-item mb-3 p-3";
    qDiv.style.background = "rgba(255,255,255,0.02)";
    qDiv.style.borderRadius = "8px";
    qDiv.style.border = "1px solid var(--border-color)";

    let optionsHtml = "";
    q.options.forEach(opt => {
      optionsHtml += `
        <label style="display:block; margin-top: 6px; cursor: pointer;">
          <input type="radio" name="diag_${q.id}" value="${opt}"> ${opt}
        </label>
      `;
    });

    qDiv.innerHTML = `
      <div style="font-size: 0.8rem; font-weight: 700; color: #38bdf8; text-transform: uppercase;">Question ${idx + 1} of 12 • ${q.category}</div>
      <p style="margin-top: 6px; font-weight: 600; font-size: 0.95rem;">${q.prompt}</p>
      <div class="options-group mt-2">${optionsHtml}</div>
    `;
    container.appendChild(qDiv);
  });

  document.getElementById("submitDiagnosticBtn").addEventListener("click", async () => {
    const answers = {};
    data.questions.forEach(q => {
      const selected = document.querySelector(`input[name="diag_${q.id}"]:checked`);
      if (selected) answers[q.id] = selected.value;
    });

    const report = await callApi("/api/diagnostic/submit", "POST", { answers: answers });
    if (report) {
      const repBox = document.getElementById("diagnosticReport");
      repBox.style.display = "block";
      repBox.innerHTML = `
        <h3>Diagnostic Assessment Results</h3>
        <p><strong>Accuracy:</strong> ${report.accuracy_percent}% (${report.correct_count} / ${report.total_questions})</p>
        <p><strong>Baseline CEFR:</strong> <span class="badge-role">${report.estimated_cefr}</span> • <strong>Estimated IELTS Band:</strong> Band ${report.estimated_band}</p>
        <p class="mt-2"><strong>Demonstrated Strengths:</strong> ${report.strengths.join(", ")}</p>
        <p><strong>Target Priority Skills:</strong> ${report.priority_skills.join(", ")}</p>
        <div class="callout-card mt-3">
          <strong>Recommended Learning Strategy:</strong>
          <p>${report.recommended_study_plan}</p>
        </div>
      `;
      const stats = getCategoryStats();
      stats.core.diagTaken = 1;
      saveCategoryStats(stats);
      recordPracticeActivity("diagnostic", report.estimated_band, `${report.correct_count}/12 diagnostic accuracy`);
      loadDashboard();
    }
  });
}

// -------------------------------------------------------------
// 4. IELTS Advantage Question Analysis Studio
// -------------------------------------------------------------
const ADVANTAGE_PROMPTS = {
  "stem": {
    title: "STEM vs Creative Arts in High School Curricula",
    prompt: "Some educationalists argue that high school curricula should prioritize STEM subjects over creative arts to ensure economic competitiveness. Others believe that artistic subjects are equally vital for developing well-rounded citizens. Discuss both views and give your own opinion. (250+ words).",
    general_topic: "Education & Curriculum Design",
    micro_topic: "Whether secondary schools should prioritize STEM over Arts or maintain balanced curricula",
    task_words: "Discuss BOTH views AND give your OWN opinion",
    trap_warning: "Do not spend 80% of your essay defending only one perspective! Because the prompt specifies 'Discuss both views', you must thoroughly explain both sides before justifying your personal verdict.",
    peel: {
      point: "STEM disciplines directly power technological modernization and industrial competitiveness.",
      explain: "Modern knowledge economies require qualified software engineers, data analysts, and researchers to drive productivity.",
      example: "For instance, nations that subsidized technology education in secondary schools witnessed marked growth in high-tech exports.",
      link: "Consequently, allocating robust curriculum hours to STEM subjects is economically justified."
    }
  },
  "ubi": {
    title: "Universal Basic Income & AI Automation",
    prompt: "As artificial intelligence and robotics automate routine workplace tasks, some economists propose that governments should introduce a guaranteed Universal Basic Income (UBI) for all adult citizens to eradicate poverty. To what extent do you agree or disagree? (250+ words).",
    general_topic: "Technology, Economics & Social Welfare",
    micro_topic: "Whether automated job displacement warrants a state-funded Universal Basic Income",
    task_words: "To what extent do you AGREE or DISAGREE (Clear position throughout required)",
    trap_warning: "Avoid sitting on the fence without a clear stance! State whether you agree, disagree, or agree to a specific extent in your introduction and maintain that position across all paragraphs.",
    peel: {
      point: "Automation is displacing routine white-collar and manual jobs at an unprecedented velocity.",
      explain: "Displaced workers cannot retrain overnight into advanced engineering roles without basic subsistence support.",
      example: "Autonomous transport and warehouse robotics could displace millions of logistics workers within a decade.",
      link: "Therefore, UBI provides an indispensable financial safety net during technological transitions."
    }
  },
  "tourism": {
    title: "Mass Tourism & Cultural Preservation",
    prompt: "In many regions across the globe, international mass tourism has become the primary source of economic revenue, yet it frequently leads to environmental degradation and the commercialization of local cultures. Do the advantages of international tourism outweigh the disadvantages? (250+ words).",
    general_topic: "Tourism & Cultural Heritage",
    micro_topic: "Whether economic dividends of mass tourism exceed its environmental and cultural costs",
    task_words: "Do advantages OUTWEIGH disadvantages (Must compare weight and give explicit judgment)",
    trap_warning: "You cannot simply list advantages in Body 1 and disadvantages in Body 2 without weighing them! You must explicitly show why one side is heavier or more significant.",
    peel: {
      point: "Tourism injects vital foreign revenue into remote regional economies.",
      explain: "These funds finance heritage preservation projects and public transport links that local tax bases could never afford.",
      example: "For instance, conservation trusts in historic Mediterranean cities are financed almost entirely by visitor levies.",
      link: "This proves that when strictly regulated, the economic dividends outweigh localized drawbacks."
    }
  },
  "traffic": {
    title: "Urban Traffic Congestion & Environmental Mitigation",
    prompt: "Traffic congestion in major metropolitan centers has reached critical levels, leading to severe air pollution, reduced economic productivity, and chronic public health issues. What are the primary causes, and what effective measures can municipal authorities adopt? (250+ words).",
    general_topic: "Urban Planning & Environmental Health",
    micro_topic: "Causes of urban vehicle gridlock and practical municipal solutions",
    task_words: "What are CAUSES and what are EFFECTIVE MEASURES (Both must be thoroughly answered)",
    trap_warning: "Ensure your proposed solutions directly address the causes you described in Body 1. Don't describe causes as 'lack of trains' and then propose 'carpooling app campaigns' as the only solution.",
    peel: {
      point: "The primary driver of traffic gridlock is inadequate, fragmented public transit networks.",
      explain: "Suburban commuters default to private automobiles when trains and buses are unreliable or prohibitively expensive.",
      example: "In commuter suburbs where municipal bus routes were pruned, private vehicle ownership surged by 35%.",
      link: "Hence, solving congestion necessitates substantial public investment in synchronized light rail."
    }
  },
  "fashion": {
    title: "Fast Fashion & Global Sustainability",
    prompt: "Consumers worldwide are purchasing substantially more inexpensive, short-lived clothing than previous generations, a trend widely known as 'fast fashion'. Why has this phenomenon emerged, and is this a positive or negative development for society? (250+ words).",
    general_topic: "Consumerism, Industry & Environment",
    micro_topic: "Reasons for the rise of fast fashion and evaluation of whether it is beneficial or detrimental",
    task_words: "WHY has this emerged? AND IS IT POSITIVE OR NEGATIVE? (Two distinct questions)",
    trap_warning: "Do not forget to answer the second question! Some students write 200 words explaining why it emerged and only 50 words on whether it is positive or negative.",
    peel: {
      point: "Fast fashion is unequivocally a detrimental development due to severe environmental and human exploitation.",
      explain: "Discarded synthetic garments shed microplastics into aquatic systems and overflow landfills in developing nations.",
      example: "The garment sector produces approximately 10% of global greenhouse emissions and exploits low-wage sweatshops.",
      link: "Thus, the fleeting benefit of cheap clothing is eclipsed by long-term ecological devastation."
    }
  }
};

function switchAdvantageSubTab(subTab) {
  ["analyzer", "coffee", "peel", "checklist"].forEach(t => {
    const btn = document.getElementById("btnAdvTab_" + t);
    const pane = document.getElementById("advSubPane_" + t);
    if (btn) btn.className = t === subTab ? "btn btn-sub-tool active" : "btn btn-sub-tool";
    if (pane) pane.style.display = t === subTab ? "block" : "none";
  });
}

function loadAdvantagePrompt(key) {
  const p = ADVANTAGE_PROMPTS[key] || ADVANTAGE_PROMPTS["stem"];
  document.getElementById("advPromptTitle").innerText = p.title;
  document.getElementById("advPromptText").innerText = p.prompt;
  document.getElementById("advGeneralTopic").innerText = p.general_topic;
  document.getElementById("advMicroTopic").innerText = p.micro_topic;
  document.getElementById("advTaskWords").innerText = p.task_words;
  document.getElementById("advTrapWarning").innerText = p.trap_warning;

  document.getElementById("advPeelPoint").innerText = p.peel.point;
  document.getElementById("advPeelExplain").innerText = p.peel.explain;
  document.getElementById("advPeelExample").innerText = p.peel.example;
  document.getElementById("advPeelLink").innerText = p.peel.link;
}

function updateChecklistProgress() {
  const container = document.getElementById("advChecklistContainer");
  const checks = container.querySelectorAll("input[type='checkbox']");
  let passed = 0;
  checks.forEach(c => { if (c.checked) passed++; });

  const pct = Math.round((passed / checks.length) * 100);
  document.getElementById("checklistProgressBar").style.width = pct + "%";
  document.getElementById("checklistScoreText").innerText = `${passed} of ${checks.length} checks verified (${pct}%)`;

  const stats = getCategoryStats();
  stats.advantage.checklistDone = Math.max(stats.advantage.checklistDone, passed);
  saveCategoryStats(stats);
  renderCategoryProgress();
  if (passed >= 5) {
    showBandToast("✅ IELTS Advantage Audit", `${passed}/10 pre-submission criteria verified! Band 7+ coherence.`);
  }
}

// -------------------------------------------------------------
// 5. Adaptive Grammar & Grammar Fill-Up (Cloze Drills)
// -------------------------------------------------------------
let activeFillupDrills = [];

function switchGrammarMode(mode) {
  appState.grammarMode = mode;
  const btnFill = document.getElementById("btnGrammar_fillup");
  const btnAdapt = document.getElementById("btnGrammar_adaptive");
  if (btnFill) btnFill.className = mode === "fillup" ? "btn btn-sub-tool active" : "btn btn-sub-tool";
  if (btnAdapt) btnAdapt.className = mode === "adaptive" ? "btn btn-sub-tool active" : "btn btn-sub-tool";

  document.getElementById("grammarFillupView").style.display = mode === "fillup" ? "block" : "none";
  document.getElementById("grammarAdaptiveView").style.display = mode === "adaptive" ? "block" : "none";

  if (mode === "adaptive") loadAdaptiveGrammar();
}

async function initGrammar() {
  await filterFillupDrills("all");
}

async function filterFillupDrills(category) {
  const data = await callApi(`/api/grammar/fillups${category && category !== "all" ? "?category=" + encodeURIComponent(category) : ""}`);
  if (!data || !data.drills) return;

  activeFillupDrills = data.drills;
  document.getElementById("fillupTotal").innerText = activeFillupDrills.length;
  renderFillupDrills(activeFillupDrills);
}

function renderFillupDrills(drills) {
  const list = document.getElementById("fillupDrillsList");
  list.innerHTML = "";

  drills.forEach((d, idx) => {
    const card = document.createElement("div");
    card.className = "cloze-card";
    card.id = "cloze_card_" + d.id;

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem;">
        <span class="badge-step">${d.category}</span>
        <span style="color: var(--text-secondary);">Drill ${idx + 1} of ${drills.length}</span>
      </div>
      <p class="cloze-prompt mt-2">${d.prompt}</p>
      <div class="cloze-input-row">
        <input type="text" class="cloze-input" id="input_${d.id}" placeholder="Type exact answer here..." onkeydown="if(event.key==='Enter') submitClozeAnswer('${d.id}')" />
        <button class="btn btn-primary btn-sm" onclick="submitClozeAnswer('${d.id}')">Check Answer</button>
      </div>
      <div class="cloze-feedback" id="feedback_${d.id}" style="display: none;"></div>
    `;
    list.appendChild(card);
  });
}

async function submitClozeAnswer(drillId) {
  const inputEl = document.getElementById("input_" + drillId);
  const card = document.getElementById("cloze_card_" + drillId);
  const feedback = document.getElementById("feedback_" + drillId);
  const val = inputEl ? inputEl.value.trim() : "";

  if (!val) return;

  const res = await callApi("/api/grammar/fillups/submit", "POST", { drill_id: drillId, user_answer: val });
  if (!res) return;

  feedback.style.display = "block";
  if (res.is_correct) {
    card.className = "cloze-card correct";
    feedback.className = "cloze-feedback success";
    feedback.innerHTML = `✅ <strong>Correct!</strong> ${res.explanation} <br><em>${res.band_note}</em>`;
    appState.fillupScore++;
    appState.fillupStreak++;
  } else {
    card.className = "cloze-card incorrect";
    feedback.className = "cloze-feedback error";
    feedback.innerHTML = `❌ <strong>Acceptable:</strong> "${res.acceptable_answers.join('" or "')}"<br>${res.explanation}<br><span style="font-size:0.75rem;">(Added to your Mistake Book)</span>`;
    appState.fillupStreak = 0;
  }

  document.getElementById("fillupScore").innerText = appState.fillupScore;
  document.getElementById("fillupStreak").innerText = appState.fillupStreak;

  recordPracticeActivity("grammar", res.is_correct ? 7.5 : 6.0, res.is_correct ? "Cloze answered correctly" : "Cloze logged to Mistake Book");
}

async function loadAdaptiveGrammar() {
  const data = await callApi("/api/grammar/adaptive");
  const content = document.getElementById("grammarSessionContent");
  if (!data) return;

  let rulesHtml = "";
  (data.lesson.rules || []).forEach(r => {
    rulesHtml += `<li>${r}</li>`;
  });

  content.innerHTML = `
    <h3>${data.lesson.title}</h3>
    <p class="subtitle">${data.message}</p>
    <ul class="mt-2" style="padding-left: 20px; line-height: 1.6;">${rulesHtml}</ul>
    <div class="callout-card mt-3">
      <strong>Examiner Academic Tip:</strong>
      <p>${data.lesson.academic_tip}</p>
    </div>
  `;
}

// -------------------------------------------------------------
// 6. Vocabulary Vault & Collocation Training
// -------------------------------------------------------------
const VOCAB_VAULT_TOPICS = {
  "environment": {
    title: "Environment & Climate Change",
    terms: [
      { term: "curb emissions", pos: "verb + noun", def: "To restrict or reduce the volume of greenhouse gases released.", ex: "Strict carbon pricing was legislated to curb industrial emissions." },
      { term: "ecological degradation", pos: "noun phrase", def: "Deterioration of natural habitats and ecosystems.", ex: "Deforestation precipitates acute ecological degradation." },
      { term: "renewable alternatives", pos: "noun phrase", def: "Clean energy sources like wind and solar.", ex: "Subsidies expedite the transition to renewable alternatives." }
    ]
  },
  "education": {
    title: "Education & Academic Curricula",
    terms: [
      { term: "foster critical thinking", pos: "verb + noun", def: "To nurture analytical problem-solving and questioning.", ex: "Seminar discussions foster critical thinking in undergraduates." },
      { term: "socioeconomic divide", pos: "noun phrase", def: "Inequality gap between wealthy and impoverished cohorts.", ex: "Free tertiary education aims to bridge the socioeconomic divide." },
      { term: "rote memorization", pos: "noun phrase", def: "Memorizing facts by repetition without deep understanding.", ex: "Modern pedagogy discourages passive rote memorization." }
    ]
  },
  "technology": {
    title: "Technology & Automation",
    terms: [
      { term: "streamline workflows", pos: "verb + noun", def: "To make processes more direct and efficient.", ex: "Artificial intelligence helps developers streamline coding workflows." },
      { term: "render obsolete", pos: "verb + adj", def: "To make something no longer useful due to new technology.", ex: "Autonomous logistics may render manual warehouse sorting obsolete." },
      { term: "algorithmic surveillance", pos: "noun phrase", def: "Automated tracking and monitoring via data algorithms.", ex: "Pervasive algorithmic surveillance raises pressing privacy dilemmas." }
    ]
  },
  "health": {
    title: "Health & Modern Lifestyles",
    terms: [
      { term: "sedentary lifestyle", pos: "noun phrase", def: "A life devoid of sufficient physical activity.", ex: "Office screen work fosters a sedentary lifestyle." },
      { term: "physiological resilience", pos: "noun phrase", def: "The body's capacity to withstand physical stress and illness.", ex: "Nutrient-dense diets bolster physiological resilience." },
      { term: "alleviate strain", pos: "verb + noun", def: "To reduce pressure or physical/mental tension.", ex: "Preventative medicine alleviates severe strain on hospital beds." }
    ]
  },
  "crime": {
    title: "Crime & Rehabilitation",
    terms: [
      { term: "serve as a deterrent", pos: "idiomatic verb phrase", def: "To discourage potential offenders from committing illegal acts.", ex: "Rigorous custodial sentences serve as a potent deterrent." },
      { term: "curb recidivism", pos: "verb + noun", def: "To prevent ex-convicts from relapsing into criminal behavior.", ex: "Vocational prison workshops help curb recidivism rates." },
      { term: "reintegrate into society", pos: "verb phrase", def: "To restore individuals back into civic life.", ex: "Community supervision facilitates efforts to reintegrate offenders." }
    ]
  },
  "globalization": {
    title: "Globalization & Cultural Identity",
    terms: [
      { term: "cultural homogenization", pos: "noun phrase", def: "The process of local customs becoming identical under global influences.", ex: "Mass media accelerates cultural homogenization." },
      { term: "foster cross-cultural empathy", pos: "verb phrase", def: "To build mutual international understanding.", ex: "Student exchange initiatives foster cross-cultural empathy." },
      { term: "indigenous heritage", pos: "noun phrase", def: "Traditional ancestral languages and practices.", ex: "Legislation protects indigenous heritage from exploitation." }
    ]
  },
  "work": {
    title: "Work & Employment",
    terms: [
      { term: "telecommuting", pos: "noun", def: "Working remotely using digital telecommunications.", ex: "Telecommuting saves employees hundreds of commuting hours annually." },
      { term: "workplace burnout", pos: "noun phrase", def: "Chronic physical and emotional exhaustion from work.", ex: "Unchecked overtime leads to widespread workplace burnout." },
      { term: "lucrative remuneration", pos: "noun phrase", def: "High financial compensation or salary.", ex: "Specialized engineers command highly lucrative remuneration." }
    ]
  },
  "urbanization": {
    title: "Urbanization & Housing",
    terms: [
      { term: "urban sprawl", pos: "noun phrase", def: "Uncontrolled expansion of city boundaries into rural land.", ex: "Green belts prevent unregulated urban sprawl." },
      { term: "affordable housing shortage", pos: "noun phrase", def: "Lack of reasonably priced residential homes.", ex: "Mega-cities grapple with an acute affordable housing shortage." },
      { term: "high-density development", pos: "noun phrase", def: "Constructing multi-story apartment complexes.", ex: "High-density development maximizes municipal transit efficiency." }
    ]
  },
  "media": {
    title: "Media & Advertising",
    terms: [
      { term: "manipulate consumer behavior", pos: "verb phrase", def: "To influence purchasing choices through subtle marketing.", ex: "Targeted digital advertisements manipulate consumer behavior." },
      { term: "disinformation campaigns", pos: "noun phrase", def: "Deliberate spread of false propaganda.", ex: "Social platforms struggle to dismantle disinformation campaigns." },
      { term: "media literacy", pos: "noun phrase", def: "The ability to critically analyze information sources.", ex: "Schools must instill media literacy to combat fake news." }
    ]
  },
  "society": {
    title: "Society, Youth & Aging",
    terms: [
      { term: "aging demographic", pos: "noun phrase", def: "A population with an increasing proportion of elderly citizens.", ex: "An aging demographic shrinks the active national workforce." },
      { term: "intergenerational solidarity", pos: "noun phrase", def: "Mutual support and respect between youth and elderly cohorts.", ex: "Mentorship programs strengthen intergenerational solidarity." },
      { term: "social cohesion", pos: "noun phrase", def: "The bonds that hold communities together peacefully.", ex: "Inclusive civic centers nurture grassroots social cohesion." }
    ]
  }
};

const COLLOCATION_PAIRS = [
  { verb: "curb", noun: "carbon emissions", ex: "Governments must curb carbon emissions immediately." },
  { verb: "foster", noun: "critical thinking", ex: "Interactive seminars foster critical thinking." },
  { verb: "streamline", noun: "operational workflows", ex: "Software tools streamline operational workflows." },
  { verb: "alleviate", noun: "traffic congestion", ex: "Light rail helps alleviate traffic congestion." },
  { verb: "reach", noun: "a consensus", ex: "Delegates struggled to reach a consensus." },
  { verb: "exert", noun: "a profound influence", ex: "Mentors exert a profound influence on youth." },
  { verb: "pose", noun: "a serious threat", ex: "Overtourism poses a serious threat to ecology." },
  { verb: "instill", noun: "civic values", ex: "Schools must instill civic values in children." },
  { verb: "bolster", noun: "economic resilience", ex: "Diversifying exports bolsters economic resilience." },
  { verb: "spark", noun: "intense controversy", ex: "The new tax sparked intense controversy." }
];

const LEXICAL_UPGRADES_TABLE = [
  { band6: "a lot of", band8: "a substantial proportion / an abundance of", context: "Use with quantifiable data or nouns" },
  { band6: "very important", band8: "of paramount importance / pivotal / indispensable", context: "Highlighting critical significance" },
  { band6: "bad effect", band8: "detrimental impact / adverse repercussions", context: "Discussing negative consequences" },
  { band6: "big problem", band8: "formidable dilemma / pressing challenge", context: "Framing essay problems in Task 2" },
  { band6: "help", band8: "facilitate / bolster / expedite", context: "Action verbs for solutions" },
  { band6: "make better", band8: "ameliorate / enhance", context: "Improving conditions or standards" },
  { band6: "I think", band8: "From my perspective / I am inclined to argue that", context: "Thesis statements and conclusions" },
  { band6: "hard to do", band8: "arduous / demanding / multifaceted", context: "Describing complex tasks" }
];

function switchVocabMode(mode) {
  appState.vocabMode = mode;
  ["vault", "collocations", "upgrades", "srs"].forEach(m => {
    const btn = document.getElementById("btnVocab_" + m);
    const view = document.getElementById("vocab" + m.charAt(0).toUpperCase() + m.slice(1) + "View");
    if (btn) btn.className = m === mode ? "btn btn-sub-tool active" : "btn btn-sub-tool";
    if (view) view.style.display = m === mode ? "block" : "none";
  });

  if (mode === "vault") renderVocabTopic(document.getElementById("vocabTopicSelect").value);
  if (mode === "collocations") renderCollocationGame();
  if (mode === "upgrades") renderUpgradesTable();
  if (mode === "srs") loadSRS();
}

function initVocabulary() {
  renderVocabTopic("environment");
}

function renderVocabTopic(topicKey) {
  const topic = VOCAB_VAULT_TOPICS[topicKey] || VOCAB_VAULT_TOPICS["environment"];
  const container = document.getElementById("vocabTopicContent");
  container.innerHTML = "";

  topic.terms.forEach(t => {
    const card = document.createElement("div");
    card.className = "card mb-2";
    card.style.background = "rgba(255,255,255,0.02)";
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <strong style="font-size: 1.05rem; color: #38bdf8;">${t.term}</strong>
        <span class="badge-role">${t.pos}</span>
      </div>
      <p class="mt-1" style="font-size: 0.9rem;"><strong>Definition:</strong> ${t.def}</p>
      <p class="mt-1" style="font-size: 0.85rem; font-style: italic; color: #a5f3fc;">"${t.ex}"</p>
    `;
    container.appendChild(card);
  });
}

function renderCollocationGame() {
  const container = document.getElementById("collocationGameGrid");
  container.innerHTML = "";

  COLLOCATION_PAIRS.forEach(p => {
    const card = document.createElement("div");
    card.className = "collocation-card";
    card.innerHTML = `
      <div class="collocation-verb">${p.verb.toUpperCase()}</div>
      <div class="collocation-noun-slot">+ <strong>${p.noun}</strong></div>
      <div class="collocation-example">"${p.ex}"</div>
    `;
    container.appendChild(card);
  });
}

function renderUpgradesTable() {
  const container = document.getElementById("upgradesTableContainer");
  let rows = "";
  LEXICAL_UPGRADES_TABLE.forEach(u => {
    rows += `
      <tr>
        <td style="color: #f87171; font-weight: 600;">"${u.band6}"</td>
        <td style="color: #34d399; font-weight: 700;">${u.band8}</td>
        <td style="color: var(--text-secondary);">${u.context}</td>
      </tr>
    `;
  });

  container.innerHTML = `
    <table class="upgrades-table">
      <thead>
        <tr>
          <th>Band 5-6 (Informal / Boring)</th>
          <th>Band 8+ Academic Upgrade</th>
          <th>Usage Context</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

// -------------------------------------------------------------
// SM-2 Spaced Repetition (SRS)
// -------------------------------------------------------------
async function loadSRS() {
  const data = await callApi("/api/srs/due");
  if (!data || !data.items || data.items.length === 0) {
    document.getElementById("cardPrompt").innerText = "🎉 All due cards reviewed! Great job.";
    document.getElementById("cardAnswerBox").style.display = "none";
    document.getElementById("revealCardBtn").style.display = "none";
    return;
  }

  appState.srsDeck = data.items;
  appState.currentCardIdx = 0;
  displayCard(appState.srsDeck[0]);
}

function displayCard(card) {
  if (!card) return;
  document.getElementById("cardPrompt").innerText = card.prompt;
  document.getElementById("cardCategoryBadge").innerText = card.category || "ACADEMIC LEXIS";
  document.getElementById("cardAnswer").innerText = card.answer;
  document.getElementById("cardAnswerBox").style.display = "none";
  document.getElementById("revealCardBtn").style.display = "inline-block";
}

document.getElementById("revealCardBtn").addEventListener("click", () => {
  document.getElementById("cardAnswerBox").style.display = "block";
  document.getElementById("revealCardBtn").style.display = "none";
});

async function gradeCard(grade) {
  const curr = appState.srsDeck[appState.currentCardIdx];
  if (!curr) return;

  await callApi("/api/srs/review", "POST", { item_id: curr.id, grade: grade });

  recordPracticeActivity("vocab", grade >= 3 ? 7.5 : 6.0, `SRS Card graded: ${grade}/5`);

  appState.currentCardIdx++;
  if (appState.currentCardIdx < appState.srsDeck.length) {
    displayCard(appState.srsDeck[appState.currentCardIdx]);
  } else {
    document.getElementById("cardPrompt").innerText = "🎉 All due cards reviewed for today!";
    document.getElementById("cardAnswerBox").style.display = "none";
    document.getElementById("revealCardBtn").style.display = "none";
    loadDashboard();
  }
}

// -------------------------------------------------------------
// 7. Reading Practice Module (Passages 1, 2, 3)
// -------------------------------------------------------------
async function loadReading() {
  await switchReadingPassage(appState.currentReadingPassage);
}

async function switchReadingPassage(passageId) {
  appState.currentReadingPassage = passageId;
  const p = await callApi(`/api/reading?passage_id=${passageId}`);
  if (!p) return;

  document.getElementById("readingTitle").innerText = p.title;
  document.getElementById("readingText").innerText = p.text;
  document.getElementById("readingScoreReport").style.display = "none";

  // Render Synonym Table
  const synBox = document.getElementById("synonymTableBox");
  if (p.synonym_table && p.synonym_table.length > 0) {
    let rows = "";
    p.synonym_table.forEach(s => {
      rows += `<tr><td><strong>${s.question_keyword}</strong></td><td><em>${s.passage_synonym}</em></td></tr>`;
    });
    synBox.innerHTML = `
      <table class="synonym-table">
        <thead><tr><th>Question Keyword</th><th>Passage Synonym Paraphrase</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    `;
  }

  // Render Questions
  const qList = document.getElementById("readingQuestionsList");
  qList.innerHTML = "";
  p.questions.forEach(q => {
    const qDiv = document.createElement("div");
    qDiv.className = "mb-3";
    if (q.type === "TFNG") {
      qDiv.innerHTML = `
        <p><strong>Q${q.num}:</strong> ${q.prompt}</p>
        <div style="margin-top: 4px;">
          <label style="margin-right: 12px;"><input type="radio" name="rq_${q.num}" value="True"> True</label>
          <label style="margin-right: 12px;"><input type="radio" name="rq_${q.num}" value="False"> False</label>
          <label><input type="radio" name="rq_${q.num}" value="Not Given"> Not Given</label>
        </div>
      `;
    } else {
      qDiv.innerHTML = `
        <p><strong>Q${q.num}:</strong> ${q.prompt}</p>
        <input type="text" id="rq_input_${q.num}" class="cloze-input mt-1" placeholder="Type answer here..." />
      `;
    }
    qList.appendChild(qDiv);
  });
}

function toggleSynonymTable() {
  const box = document.getElementById("synonymTableBox");
  const btn = document.getElementById("toggleSynonymTableBtn");
  if (box.style.display === "none") {
    box.style.display = "block";
    btn.innerText = "Hide Keyword & Synonym Table";
  } else {
    box.style.display = "none";
    btn.innerText = "🔍 Show Keyword & Synonym Mapping Table";
  }
}

document.getElementById("submitReadingBtn").addEventListener("click", async () => {
  const answers = {};
  [1, 2, 3, 4].forEach(num => {
    const radio = document.querySelector(`input[name="rq_${num}"]:checked`);
    const input = document.getElementById(`rq_input_${num}`);
    if (radio) answers[num] = radio.value;
    else if (input) answers[num] = input.value;
  });

  const rep = await callApi("/api/reading/submit", "POST", { passage_id: appState.currentReadingPassage, answers: answers });
  if (rep) {
    const box = document.getElementById("readingScoreReport");
    box.style.display = "block";
    box.innerHTML = `
      <h3>Estimated Reading Band: Band ${rep.estimated_band}</h3>
      <p>Score: <strong>${rep.correct_answers}</strong> of <strong>${rep.total_questions}</strong> correct.</p>
      <div class="callout-card mt-2">
        <strong>IELTS Advantage Reading Strategy:</strong>
        <p>Success in IELTS Reading depends on mapping keywords in questions to precise synonyms in text. Notice how 'solar radiation' mapped to 'solar photosynthesis', and 'ephemeral' meant 'shut down within decades'.</p>
      </div>
      <p class="mt-2"><em>${rep.disclaimer}</em></p>
    `;
    recordPracticeActivity("reading", rep.estimated_band, `${rep.correct_answers}/${rep.total_questions} correct`);
  }
});

// -------------------------------------------------------------
// 8. Listening Module
// -------------------------------------------------------------
async function loadListening() {
  await switchListeningSection(appState.currentListeningSection);
}

async function switchListeningSection(secId) {
  appState.currentListeningSection = secId;
  ["sec_1", "sec_2", "sec_3", "sec_4"].forEach(id => {
    const b = document.getElementById("secBtn_" + id);
    if (b) b.className = id === secId ? "chip-btn active" : "chip-btn";
  });

  const sec = await callApi(`/api/listening?sec_id=${secId}`);
  if (!sec) return;

  document.getElementById("listeningTitle").innerText = sec.title;
  document.getElementById("listeningTranscriptBox").innerText = sec.audio_script;
  document.getElementById("listeningScoreReport").style.display = "none";

  const qList = document.getElementById("listeningQuestionsList");
  qList.innerHTML = "";
  sec.questions.forEach(q => {
    const qDiv = document.createElement("div");
    qDiv.className = "mb-3";
    qDiv.innerHTML = `
      <p><strong>Q${q.num}:</strong> ${q.prompt}</p>
      <input type="text" id="lq_input_${q.num}" class="cloze-input mt-1" placeholder="Type answer..." />
    `;
    qList.appendChild(qDiv);
  });

  const playBtn = document.getElementById("playAudioScriptBtn");
  playBtn.onclick = () => speakText(sec.audio_script, playBtn);
}

document.getElementById("toggleTranscriptBtn").addEventListener("click", () => {
  const box = document.getElementById("listeningTranscriptBox");
  box.style.display = box.style.display === "none" ? "block" : "none";
});

document.getElementById("submitListeningBtn").addEventListener("click", async () => {
  const answers = {};
  [1, 2, 3, 4].forEach(num => {
    const input = document.getElementById(`lq_input_${num}`);
    if (input) answers[num] = input.value;
  });

  const rep = await callApi("/api/listening/submit", "POST", { section_id: appState.currentListeningSection, answers: answers });
  if (rep) {
    const box = document.getElementById("listeningScoreReport");
    box.style.display = "block";
    box.innerHTML = `
      <h3>Estimated Listening Band: Band ${rep.estimated_band}</h3>
      <p>Score: <strong>${rep.correct_answers}</strong> of <strong>${rep.total_questions}</strong> correct.</p>
      <p class="mt-2"><em>${rep.disclaimer}</em></p>
    `;
    recordPracticeActivity("listening", rep.estimated_band, `${rep.correct_answers}/${rep.total_questions} correct`);
  }
});

// -------------------------------------------------------------
// 9. Writing Studio (5 Task 2 Prompts & IELTS Advantage Checklist)
// -------------------------------------------------------------
const WRITING_PROMPTS_DATA = {
  "acad_t2_stem": {
    title: "Task 2: STEM vs Creative Arts (Discuss Both Views)",
    prompt: "Some educationalists argue that high school curricula should prioritize STEM subjects over creative arts to ensure economic competitiveness. Others believe artistic subjects are equally vital. Discuss both views and give your opinion. (250+ words).",
    model: `In contemporary pedagogical discourse, the prioritization of secondary school curricula remains a subject of considerable deliberation. While proponents of STEM disciplines maintain that technical expertise is the cornerstone of national economic prosperity, others advocate that creative arts are indispensable for cultivating holistic cognitive abilities. In my estimation, while STEM fields provide requisite technical competency, creative disciplines foster the lateral problem-solving necessary to catalyze innovation, thereby justifying a balanced curriculum.

On the one hand, championing Science, Technology, Engineering, and Mathematics is directly aligned with the demands of the modern knowledge economy. As automated algorithms and digital infrastructure expand, global industries face an acute shortage of software engineers, biotechnologists, and data analysts. Developing nations that systematically invested in STEM education over the preceding decade experienced marked increases in technological exports and high-skilled employment. Therefore, robust curriculum allocation to these quantitative fields is economically justifiable.

On the other hand, discarding artistic and humanistic disciplines compromises cognitive flexibility and emotional intelligence. Technical proficiency without artistic insight often yields derivative solutions. Pioneer software architects and industrial designers frequently attribute their breakthrough concepts to lateral thinking nurtured through visual arts, literature, and music. Furthermore, the arts instill cultural empathy and ethical discernment—qualities that automated artificial intelligence cannot replicate.

In conclusion, although the economic imperatives of STEM specialization are indisputable, artistic education remains equally paramount for sustained societal creativity. Educational authorities should resist the temptation of false dichotomies and instead adopt an integrated curriculum that synthesizes technical rigor with creative exploration.`
  },
  "acad_t2_ubi": {
    title: "Task 2: Universal Basic Income & AI (Agree or Disagree)",
    prompt: "As artificial intelligence and robotics automate routine workplace tasks, some economists propose that governments should introduce a guaranteed Universal Basic Income (UBI) for all adult citizens to eradicate poverty. To what extent do you agree or disagree? (250+ words).",
    model: `The exponential acceleration of robotic automation and generative artificial intelligence has precipitated intense scrutiny regarding the future of employment. Consequently, a growing cohort of economists asserts that sovereign governments must institute a guaranteed Universal Basic Income (UBI) to shield citizens from severe destitution. I firmly subscribe to this proposal, as UBI establishes an indispensable safety net during structural workplace disruption while emancipating individuals to pursue higher-order entrepreneurial and educational endeavors.

Chief among the arguments in favor of UBI is the sheer velocity of modern technological displacement. Unlike historical industrial transformations which occurred over generations, algorithmic automation threatens to render millions of white-collar analytical and blue-collar logistics roles obsolete within a single decade. Displaced workers cannot retrain instantaneously into specialized quantum or cybernetic fields. Without a guaranteed baseline income, widespread purchasing power would evaporate, precipitating devastating economic contraction and social unrest.

Furthermore, empirical pilot studies refute the orthodox critique that unconditional payments erode work ethic. In regional trials conducted across Canada and Northern Europe, recipients of basic stipends exhibited no measurable diminution in economic motivation. Instead, the guaranteed security empowered participants to complete vocational qualifications, launch micro-enterprises, or provide care for vulnerable relatives without anxiety. Thus, UBI functions not as an inducement to idleness, but as a trampoline facilitating civic productivity.

To conclude, given the unprecedented disruption driven by artificial intelligence, introducing a Universal Basic Income is both an ethical necessity and an economic imperative to safeguard social stability.`
  },
  "acad_t2_tourism": {
    title: "Task 2: Mass Tourism & Cultural Preservation (Outweigh)",
    prompt: "In many regions, international mass tourism has become the primary source of economic revenue, yet it frequently leads to environmental degradation and cultural commercialization. Do the advantages outweigh the disadvantages? (250+ words).",
    model: `The globalization of budget commercial aviation has transformed international travel from an elite privilege into a ubiquitous phenomenon. While mass tourism supplies invaluable foreign capital and employment to developing regions, it frequently precipitates ecological strain and cultural dilution. On balance, I am inclined to argue that the advantages outweigh the disadvantages, provided municipal authorities institute stringent conservation levies and carrying-capacity caps.

The paramount advantage of international tourism is its extraordinary capacity to stimulate localized economic modernization. For remote island economies and historic enclaves lacking natural mineral wealth, visitor spending constitutes the bedrock of public finances. Revenue accrued from accommodation taxes and park entrance fees directly finances the restoration of ancient monuments, healthcare centers, and sanitation networks that would otherwise languish in disrepair. Moreover, authentic eco-tourism raises global awareness regarding vulnerable natural habitats.

Nevertheless, unconstrained overtourism carries acute negative repercussions. Historic districts in European capitals frequently succumb to rapid commercialization, driving indigenous residents out as residential apartments are converted into transient holiday rentals. Furthermore, foot traffic and vehicular emissions accelerate the physical weathering of ancient stone facades. However, these drawbacks represent failures of municipal regulation rather than intrinsic defects of tourism itself. Cities that enforce daily visitor quotas demonstrate that cultural integrity can coexist with visitor influx.

In conclusion, although overtourism presents formidable environmental and cultural challenges, its profound economic and infrastructural benefits are indispensable, ensuring the advantages predominate under responsible governance.`
  },
  "acad_t2_traffic": {
    title: "Task 2: Urban Traffic Congestion (Causes & Solutions)",
    prompt: "Traffic congestion in major metropolitan centers has reached critical levels, leading to severe air pollution and lost economic productivity. What are the primary causes, and what effective measures can municipal authorities adopt? (250+ words).",
    model: `Chronic traffic congestion represents one of the most formidable urban planning dilemmas confronting twenty-first-century metropolitan centers. This phenomenon severely compromises urban air quality, amplifies greenhouse emissions, and siphons billions in economic output through lost productivity. This essay will examine the primary causes—namely defective transit infrastructure and unregulated vehicle ownership—and delineate practical municipal remedies.

The root cause of urban gridlock is the persistent deficiency of subsidized, interconnected public transportation. In suburban commuter zones, light rail and bus routes are frequently overcrowded, intermittent, or completely absent. Faced with unreliable transit schedules, citizens rationally default to private automobiles for their daily journeys. Furthermore, historical urban planning prioritized sprawling highway corridors over high-density pedestrian infrastructure, locking suburbs into automobile dependency.

To eradicate this crisis, municipal authorities must deploy a two-pronged strategy integrating economic disincentives with transit subsidies. Foremost among these interventions is the expansion of dynamic congestion charging zones, similar to the framework established in London. Levying substantial fees on vehicles entering inner-city limits during peak hours disincentivizes non-essential trips and generates revenue. Concurrently, these funds must be earmarked to expand electric metro lines, establish bus-only lanes, and implement subsidized monthly commuter passes.

In conclusion, urban gridlock is precipitated by inadequate transit alternatives and car-centric design. By combining stringent congestion pricing with rapid investments in clean mass transit, municipal governments can sustainably restore urban mobility.`
  },
  "acad_t2_fast_fashion": {
    title: "Task 2: Fast Fashion & Global Sustainability (Two Questions)",
    prompt: "Consumers worldwide are purchasing substantially more inexpensive, short-lived clothing than previous generations, a trend widely known as 'fast fashion'. Why has this phenomenon emerged, and is this a positive or negative development for society? (250+ words).",
    model: `The contemporary apparel industry has undergone a radical transformation, characterized by the meteoric rise of 'fast fashion'—the accelerated production of ultra-cheap garments designed for transient use. This essay will explain how targeted digital marketing and overseas supply chains fueled this trend, before demonstrating why it represents an unequivocally negative development for human society and planetary ecology.

The proliferation of fast fashion has been catalyzed by algorithmic social media advertising combined with globalized low-cost manufacturing. E-commerce platforms leverage real-time consumer telemetry to identify micro-trends and manufacture thousands of new clothing iterations weekly in developing nations with negligible labor overheads. Simultaneously, influencer culture normalizes wearing an outfit only once before discarding it, manufacturing artificial psychological desires for continuous novelty among youth.

This phenomenon is profoundly detrimental, primarily due to its catastrophic environmental fallout and labor exploitation. Textile dyeing and synthetic fabric processing generate roughly 10% of global greenhouse emissions and discharge massive volumes of toxic chemicals into vulnerable river basins. Moreover, polyester garments shed millions of non-biodegradable microplastics into the food chain, while discarded textiles choke landfills in the Global South. From a humanitarian perspective, sustaining such low consumer prices often relies on exploitative sweatshop conditions that violate basic labor rights.

To conclude, fast fashion has emerged through technological marketing efficiency and cheap overseas production. However, it is an overwhelmingly negative development whose fleeting aesthetic pleasure is dwarfed by immense ecological and ethical destruction.`
  }
};

function switchWritingPrompt(promptId) {
  appState.currentWritingPrompt = promptId;
  const data = WRITING_PROMPTS_DATA[promptId] || WRITING_PROMPTS_DATA["acad_t2_stem"];
  document.getElementById("currentWritingTitle").innerText = data.title;
  document.getElementById("currentWritingPrompt").innerText = data.prompt;
  document.getElementById("modelEssayTitle").innerText = `Band 9 Model: ${data.title}`;
  document.getElementById("modelEssayText").innerText = data.model;
  document.getElementById("modelEssayBox").style.display = "none";
  document.getElementById("toggleModelEssayBtn").innerText = "📖 View Band 9 Model Essay";
  document.getElementById("writingEvalReport").style.display = "none";
}

function toggleModelEssay() {
  const box = document.getElementById("modelEssayBox");
  const btn = document.getElementById("toggleModelEssayBtn");
  if (box.style.display === "none") {
    box.style.display = "block";
    btn.innerText = "Hide Model Essay";
  } else {
    box.style.display = "none";
    btn.innerText = "📖 View Band 9 Model Essay";
  }
}

function initWriting() {
  const essayInput = document.getElementById("essayInput");
  const wordCountLabel = document.getElementById("wordCountLabel");

  essayInput.addEventListener("input", () => {
    const words = essayInput.value.trim().split(/\s+/).filter(w => w.length > 0);
    wordCountLabel.innerText = words.length;
    if (words.length >= 260 && words.length <= 290) {
      wordCountLabel.style.color = "#34d399";
    } else if (words.length < 250) {
      wordCountLabel.style.color = "#f87171";
    } else {
      wordCountLabel.style.color = "#fbbf24";
    }
  });

  document.getElementById("evaluateWritingBtn").addEventListener("click", async () => {
    const text = essayInput.value.trim();
    if (!text) return;

    const rep = await callApi("/api/writing/evaluate", "POST", { prompt_id: appState.currentWritingPrompt, essay_text: text });
    if (rep) {
      const repBox = document.getElementById("writingEvalReport");
      repBox.style.display = "block";

      let criteriaHtml = "";
      for (const [cName, cScore] of Object.entries(rep.criteria)) {
        criteriaHtml += `<li><strong>${cName}:</strong> Band ${cScore}</li>`;
      }

      let checklistHtml = "";
      if (rep.advantage_checklist) {
        checklistHtml = "<h4 class='mt-3'>IELTS Advantage Pre-Submission Checklist:</h4><ul style='padding-left: 20px;'>";
        rep.advantage_checklist.forEach(c => {
          checklistHtml += `<li>${c.passed ? "✅" : "⚠️"} ${c.item}</li>`;
        });
        checklistHtml += "</ul>";
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
        <h3>Estimated Overall Writing Band: Band ${rep.estimated_band}</h3>
        <p>Word Count: <strong>${rep.word_count} words</strong> (Underlength Penalty: ${rep.underlength_penalty})</p>
        <ul class="mt-2">${criteriaHtml}</ul>
        ${checklistHtml}
        ${formativeHtml}
        <p class='mt-2'><em>${rep.disclaimer}</em></p>
      `;
      recordPracticeActivity("writing", rep.estimated_band, `${rep.word_count} words evaluated`);
    }
  });
}

// -------------------------------------------------------------
// 10. AI Speaking Examiner (6 Cambridge Sets & 3-Step Strategy)
// -------------------------------------------------------------
function initSpeaking() {
  const examSetSelect = document.getElementById("speakingExamSetSelect");
  const startBtn = document.getElementById("startInterviewBtn");
  const resetBtn = document.getElementById("resetInterviewBtn");
  const recordBtn = document.getElementById("startSpeechRecordBtn");
  const stopBtn = document.getElementById("stopSpeechRecordBtn");
  const replayBtn = document.getElementById("replayQuestionBtn");
  const skipPrepBtn = document.getElementById("skipPrepBtn");
  const transcriptEl = document.getElementById("speakingTranscriptInput");
  const timerEl = document.getElementById("speakingTimer");
  const examinerBubble = document.getElementById("examinerSpeechBubble");
  const examinerStatus = document.getElementById("examinerStatusLabel");
  const dialogueHistoryEl = document.getElementById("interviewDialogueHistory");
  const part2PrepCard = document.getElementById("part2PrepCard");
  const prepCountdownEl = document.getElementById("prepCountdownText");
  const part2CueTextEl = document.getElementById("part2CueCardText");
  const reportContainer = document.getElementById("speakingReportContainer");
  const evalReportEl = document.getElementById("speakingEvalReport");

  // Android Native Speech Recognizer Callbacks
  window.onAndroidSpeechPartial = (text) => {
    if (transcriptEl) transcriptEl.value = text;
  };
  window.onAndroidSpeechResult = (text) => {
    if (transcriptEl) transcriptEl.value = text;
  };
  window.onSpeechBegin = () => {
    if (recordBtn) recordBtn.innerText = "🎙️ Listening Live...";
  };
  window.onSpeechEnd = () => {
    if (recordBtn) recordBtn.innerText = "🎙️ Answer Examiner (Speak)";
  };

  // Web Speech API fallback for browsers
  let recognizer = null;
  const isAndroidApp = window.AndroidSTT && typeof window.AndroidSTT.startListening === "function";

  if (!isAndroidApp && ("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognizer = new SpeechRecognition();
    recognizer.continuous = true;
    recognizer.interimResults = true;
    recognizer.lang = "en-GB";

    recognizer.onresult = (e) => {
      let finalStr = "";
      for (let i = 0; i < e.results.length; ++i) {
        finalStr += e.results[i][0].transcript + " ";
      }
      transcriptEl.value = finalStr;
    };
  }

  function updateStageBadges(activeBadgeId) {
    ["badgePart1", "badgePart2", "badgePart3", "badgeResult"].forEach(id => {
      const b = document.getElementById(id);
      if (b) b.classList.remove("active");
    });
    const curr = document.getElementById(activeBadgeId);
    if (curr) curr.classList.add("active");
  }

  function appendDialogueTurn(speaker, text) {
    if (!dialogueHistoryEl) return;
    const div = document.createElement("div");
    div.className = speaker === "examiner" ? "dialogue-turn examiner" : "dialogue-turn candidate";
    div.innerHTML = `<strong>${speaker === "examiner" ? "Dr. Harrison (Examiner)" : "You (Candidate)"}:</strong> ${text}`;
    dialogueHistoryEl.appendChild(div);
    dialogueHistoryEl.scrollTop = dialogueHistoryEl.scrollHeight;
  }

  async function askExaminerQuestion(questionText, stageLabel) {
    appState.speakingInterview.currentQuestionText = questionText;
    examinerBubble.innerText = `"${questionText}"`;
    examinerStatus.innerText = stageLabel;
    appendDialogueTurn("examiner", questionText);
    speakText(questionText, null);
    transcriptEl.value = "";
    recordBtn.disabled = false;
    stopBtn.disabled = false;
  }

  window.onSpeakingSetChanged = async (setIdx) => {
    appState.currentSpeakingSetIdx = parseInt(setIdx) || 0;
    const data = await callApi(`/api/speaking/prompts?card_idx=${appState.currentSpeakingSetIdx}`);
    if (data && data.part_2_cue_card) {
      document.getElementById("speakingBand9CueModel").innerText = data.part_2_cue_card.band_9_model || "Sample Band 9 answer loading...";
    }
  };

  window.toggleBand9SpeakingModel = () => {
    const box = document.getElementById("speakingBand9ModelBox");
    const btn = document.getElementById("viewBand9SpeakingBtn");
    if (box.style.display === "none") {
      box.style.display = "block";
      btn.innerText = "Hide Model";
    } else {
      box.style.display = "none";
      btn.innerText = "💡 View Band 9 Model";
    }
  };

  // Start interview
  startBtn.addEventListener("click", async () => {
    const setIdx = parseInt(examSetSelect.value) || 0;
    appState.speakingInterview.examSetIdx = setIdx;
    const data = await callApi(`/api/speaking/prompts?card_idx=${setIdx}`);
    if (!data) return;

    appState.speakingInterview.active = true;
    appState.speakingInterview.examData = data;
    appState.speakingInterview.part1QuestionIdx = 0;
    appState.speakingInterview.part3QuestionIdx = 0;
    appState.speakingInterview.dialogueHistory = [];
    appState.speakingInterview.candidateFullTranscript = "";
    dialogueHistoryEl.innerHTML = "";
    reportContainer.style.display = "none";

    startBtn.disabled = true;
    examSetSelect.disabled = true;

    // Part 1 Begin
    appState.speakingInterview.stage = "part1";
    updateStageBadges("badgePart1");
    await askExaminerQuestion(data.part_1[0], "Part 1: Introduction (Question 1/4)");
  });

  // Candidate speak button
  recordBtn.addEventListener("click", () => {
    if (isAndroidApp) {
      window.AndroidSTT.startListening();
    } else if (recognizer) {
      try { recognizer.start(); } catch (e) {}
    }
    recordBtn.innerText = "🎙️ Listening Live...";
  });

  // Candidate stop / send answer
  stopBtn.addEventListener("click", async () => {
    if (isAndroidApp) {
      window.AndroidSTT.stopListening();
    } else if (recognizer) {
      try { recognizer.stop(); } catch (e) {}
    }
    recordBtn.innerText = "🎙️ Answer Examiner (Speak)";

    const candAns = transcriptEl.value.trim() || "(Candidate answered via audio)";
    appendDialogueTurn("candidate", candAns);
    appState.speakingInterview.candidateFullTranscript += " " + candAns;

    const data = appState.speakingInterview.examData;
    const stage = appState.speakingInterview.stage;

    // Stage State Machine
    if (stage === "part1") {
      appState.speakingInterview.part1QuestionIdx++;
      if (appState.speakingInterview.part1QuestionIdx < data.part_1.length) {
        const nextQ = data.part_1[appState.speakingInterview.part1QuestionIdx];
        await askExaminerQuestion(nextQ, `Part 1: Introduction (Question ${appState.speakingInterview.part1QuestionIdx + 1}/4)`);
      } else {
        // Transition to Part 2
        appState.speakingInterview.stage = "part2_prep";
        updateStageBadges("badgePart2");
        examinerStatus.innerText = "Part 2: 1-Minute Cue Card Preparation";
        examinerBubble.innerText = `"Thank you. Now I will give you a topic card. You have one minute to prepare your notes, and then you should speak for two minutes."`;
        speakText(examinerBubble.innerText, null);

        part2PrepCard.style.display = "block";
        part2CueTextEl.innerHTML = `<strong>Topic: ${data.part_2_cue_card.topic}</strong><ul style="padding-left: 20px; margin-top: 6px;">` +
          data.part_2_cue_card.prompts.map(p => `<li>${p}</li>`).join("") + "</ul>";

        startPart2PrepTimer();
      }
    } else if (stage === "part2_speak") {
      // Transition to Part 3
      appState.speakingInterview.stage = "part3";
      updateStageBadges("badgePart3");
      appState.speakingInterview.part3QuestionIdx = 0;
      const q = data.part_3_discussion[0];
      await askExaminerQuestion(q, "Part 3: In-Depth Discussion (Question 1/4)");
    } else if (stage === "part3") {
      appState.speakingInterview.part3QuestionIdx++;
      if (appState.speakingInterview.part3QuestionIdx < data.part_3_discussion.length) {
        const nextQ = data.part_3_discussion[appState.speakingInterview.part3QuestionIdx];
        await askExaminerQuestion(nextQ, `Part 3: In-Depth Discussion (Question ${appState.speakingInterview.part3QuestionIdx + 1}/4)`);
      } else {
        // Test Concluded
        appState.speakingInterview.stage = "done";
        updateStageBadges("badgeResult");
        examinerStatus.innerText = "Interview Concluded";
        examinerBubble.innerText = `"That is the end of the speaking test. Thank you very much. I will now compute your diagnostic evaluation."`;
        speakText(examinerBubble.innerText, null);

        recordBtn.disabled = true;
        stopBtn.disabled = true;
        startBtn.disabled = false;
        examSetSelect.disabled = false;

        // Compute diagnostic report
        const rep = await callApi("/api/speaking/evaluate", "POST", { transcript: appState.speakingInterview.candidateFullTranscript });
        if (rep) {
          reportContainer.style.display = "block";
          let upHtml = "";
          (rep.band_upgrades || []).forEach(u => {
            upHtml += `<div class="upgrade-item">Original: <em>"${u.original}"</em> ➔ <strong>${u.band_9_upgrade}</strong><br><small>${u.tip}</small></div>`;
          });

          evalReportEl.innerHTML = `
            <h3>Dr. Harrison's Official Speaking Assessment</h3>
            <p><strong>Overall Estimated Band: Band ${rep.estimated_band}</strong></p>
            <div class="split-view mt-2">
              <div>
                <p>Fluency & Coherence: <strong>Band ${rep.criteria["Fluency and Coherence"]}</strong></p>
                <p>Lexical Resource: <strong>Band ${rep.criteria["Lexical Resource"]}</strong></p>
              </div>
              <div>
                <p>Grammatical Range: <strong>Band ${rep.criteria["Grammatical Range and Accuracy"]}</strong></p>
                <p>Pronunciation: <strong>Band ${rep.criteria["Pronunciation"]}</strong></p>
              </div>
            </div>
            <div class="band-upgrade-box mt-3">
              <h4>Band 9 Lexical & Fluency Upgrades:</h4>
              ${upHtml}
            </div>
          `;
          recordPracticeActivity("speaking", rep.estimated_band, "Full speaking mock completed");
          evalReportEl.scrollIntoView({ behavior: "smooth" });
        }
      }
    }
  });

  function startPart2PrepTimer() {
    let sec = 60;
    prepCountdownEl.innerText = "01:00";
    clearInterval(appState.speakingInterview.prepTimerInterval);
    appState.speakingInterview.prepTimerInterval = setInterval(() => {
      sec--;
      const m = String(Math.floor(sec / 60)).padStart(2, "0");
      const s = String(sec % 60).padStart(2, "0");
      prepCountdownEl.innerText = `${m}:${s}`;
      if (sec <= 0) {
        clearInterval(appState.speakingInterview.prepTimerInterval);
        startPart2Speaking();
      }
    }, 1000);
  }

  function startPart2Speaking() {
    clearInterval(appState.speakingInterview.prepTimerInterval);
    part2PrepCard.style.display = "none";
    appState.speakingInterview.stage = "part2_speak";
    examinerStatus.innerText = "Part 2: Long Turn (Speak for 2 minutes)";
    examinerBubble.innerText = `"Your preparation time is over. Please begin speaking on your topic card now."`;
    speakText(examinerBubble.innerText, null);
    transcriptEl.value = "";
    recordBtn.disabled = false;
    stopBtn.disabled = false;
  }

  skipPrepBtn.addEventListener("click", () => {
    startPart2Speaking();
  });

  replayBtn.addEventListener("click", () => {
    if (appState.speakingInterview.currentQuestionText) {
      speakText(appState.speakingInterview.currentQuestionText, null);
    }
  });

  resetBtn.addEventListener("click", () => {
    clearInterval(appState.speakingInterview.prepTimerInterval);
    appState.speakingInterview.active = false;
    appState.speakingInterview.stage = "idle";
    startBtn.disabled = false;
    examSetSelect.disabled = false;
    recordBtn.disabled = true;
    stopBtn.disabled = true;
    part2PrepCard.style.display = "none";
    reportContainer.style.display = "none";
    examinerStatus.innerText = "Ready to begin interview";
    examinerBubble.innerText = `"Good day. Welcome to the IELTS Speaking test. Please select a topic above and press 'Begin Official Interview' to start."`;
  });
}

// -------------------------------------------------------------
// 11. Mistake Book
// -------------------------------------------------------------
async function loadMistakes() {
  const data = await callApi("/api/mistakes");
  if (!data) return;

  const summaryEl = document.getElementById("mistakeBookSummary");
  const listEl = document.getElementById("mistakeBookList");

  const total = data.active_mistakes.length;
  summaryEl.innerText = `You have ${total} active grammatical / lexical item(s) logged in your Mistake Book.`;

  listEl.innerHTML = "";
  data.active_mistakes.forEach(m => {
    const item = document.createElement("div");
    item.className = "card mb-2";
    item.style.background = "rgba(255,255,255,0.02)";
    item.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span class="badge-step">${m.category}</span>
        <button class="btn btn-success btn-sm" onclick="resolveMistake('${m.id}')">✓ Mark as Mastered</button>
      </div>
      <p class="mt-2" style="color: #f87171;"><strong>Error:</strong> "${m.original_text}"</p>
      <p style="color: #34d399;"><strong>Correction:</strong> "${m.corrected_text}"</p>
      <p style="font-size: 0.85rem; color: var(--text-secondary);">${m.explanation}</p>
    `;
    listEl.appendChild(item);
  });
}

async function resolveMistake(id) {
  await callApi("/api/mistakes/review", "POST", { mistake_id: id, success: true });
  loadMistakes();
  loadDashboard();
}

// -------------------------------------------------------------
// Screen Setting Analysis & Proactive Permission Calibration (v1.5.3)
// -------------------------------------------------------------
function analyzeScreenAndPermissions() {
  const innerW = window.innerWidth;
  const innerH = window.innerHeight;
  const dpr = window.devicePixelRatio || 1;
  const deviceType = innerW >= 1024 ? "Desktop/Tablet" : (innerW >= 600 ? "Large Phone/Foldable" : "Compact Mobile");

  console.log(`[Screen Analysis] Viewport: ${innerW}x${innerH}, DPR: ${dpr.toFixed(2)}, Type: ${deviceType}`);

  // Proactively check Microphone Permission for Cambridge Speaking Test
  const hasAndroidSTT = !!(window.AndroidSTT && typeof window.AndroidSTT.hasPermission === 'function');
  const hasGrantedMic = hasAndroidSTT ? window.AndroidSTT.hasPermission() : true;

  if (hasAndroidSTT && !hasGrantedMic) {
    showScreenSetupModal(innerW, innerH, dpr, deviceType);
  } else {
    // Show brief toast on first cold start per session
    if (!sessionStorage.getItem("ielts_screen_calibrated")) {
      sessionStorage.setItem("ielts_screen_calibrated", "true");
      showBandUpdateToast(`🎯 Screen Calibrated: ${innerW}x${innerH} (${dpr.toFixed(1)}x) Auto-Fit Active`);
    }
  }

  // Hook Android permission callback
  window.onMicPermissionResult = function(granted) {
    const modal = document.getElementById("screenSetupModal");
    if (modal) modal.remove();
    if (granted) {
      showBandUpdateToast("🎤 Microphone access enabled for Examiner Speaking practice!");
    } else {
      showBandUpdateToast("ℹ️ Audio practice available via Text-to-Speech.");
    }
  };
}

function showScreenSetupModal(w, h, dpr, deviceType) {
  if (document.getElementById("screenSetupModal")) return;

  const overlay = document.createElement("div");
  overlay.id = "screenSetupModal";
  overlay.className = "goal-modal-overlay open";
  overlay.style.zIndex = "99999";
  overlay.innerHTML = `
    <div class="goal-modal-card" style="max-width: 440px; text-align: center; border-radius: 18px; padding: 24px;">
      <div style="font-size: 2.2rem; margin-bottom: 8px;">🎯</div>
      <h2 style="font-size: 1.25rem; font-weight: 800; margin-bottom: 6px;">System & Screen Calibrated</h2>
      <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 14px;">
        Layout automatically fitted for <strong>${w}x${h}</strong> (${dpr.toFixed(1)}x density • ${deviceType}).
      </p>
      <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px; padding: 12px; text-align: left; margin-bottom: 16px;">
        <div style="font-size: 0.85rem; font-weight: 700; color: var(--primary-accent); margin-bottom: 4px;">
          🎙️ IELTS Speaking Examiner Setup
        </div>
        <p style="font-size: 0.78rem; color: var(--text-secondary); margin: 0; line-height: 1.4;">
          Enable microphone permission to practice Cambridge Part 1, 2 & 3 speaking simulations with Dr. Harrison using offline voice recognition.
        </p>
      </div>
      <div style="display: flex; flex-direction: column; gap: 8px;">
        <button id="btnGrantMicSetup" class="btn btn-primary" style="width: 100%; padding: 12px; font-weight: 700; border-radius: 10px;">
          Allow Microphone & Continue
        </button>
        <button id="btnSkipMicSetup" class="btn btn-secondary" style="width: 100%; padding: 10px; font-size: 0.82rem; border-radius: 10px;">
          Continue without Microphone
        </button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  document.getElementById("btnGrantMicSetup").addEventListener("click", () => {
    if (window.AndroidSTT && typeof window.AndroidSTT.requestPermission === 'function') {
      window.AndroidSTT.requestPermission();
    } else {
      overlay.remove();
    }
  });

  document.getElementById("btnSkipMicSetup").addEventListener("click", () => {
    overlay.remove();
  });
}

// -------------------------------------------------------------
// Initialization on DOM Ready
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  updateScreenDimensions();
  analyzeScreenAndPermissions();
  initIOSAudioUnlock();
  initWindowsShortcuts();
  initNavigation();
  initChat();
  initDiagnostic();
  initWriting();
  initSpeaking();
  updateConnectivityStatus();
  loadDashboard();
  initDailyGoalModal();
  onSpeakingSetChanged(0);

  const verBadge = document.getElementById("appVersionBadge");
  if (verBadge) verBadge.textContent = "v" + APP_VERSION;
  const hdrBadge = document.getElementById("headerVersionBadge");
  if (hdrBadge) hdrBadge.textContent = "v" + APP_VERSION;
  const setVal = document.getElementById("settingsVersionValue");
  if (setVal) setVal.textContent = "v" + APP_VERSION + " Production";
});
