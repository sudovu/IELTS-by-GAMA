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
  currentListeningSection: "sec_1",
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

    if (p.startsWith("/api/speaking/prompts")) {
      const idx = p.includes("card_idx=") ? parseInt(p.split("card_idx=")[1]) || 0 : 0;
      const examSets = [
        {
          id: "topic_ambition",
          title: "Career, Goals & Ambition",
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
            ]
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
          title: "Sustainable Living & Urban Heritage",
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
            ]
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
          title: "Artificial Intelligence, Automation & Media",
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
            ]
          },
          part_3_discussion: [
            "Will automated artificial intelligence systems eventually diminish the demand for human analytical skills?",
            "How can governments ensure ethical standards in algorithmic decision-making and data privacy?",
            "What impact has constant digital connectivity had on face-to-face interpersonal relationships?",
            "Are older demographics being unfairly marginalized by the rapid shift toward cashless, app-only services?"
          ]
        }
      ];
      return examSets[idx % examSets.length];
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
      let fc = wpm >= 115 && wpm <= 165 ? 7.0 : 6.0;
      let lr = 6.0;
      let gra = 6.5;

      const lower = transcript.toLowerCase();
      if (lower.includes("significant") || lower.includes("perspective") || lower.includes("consequently") || lower.includes("paramount")) {
        lr += 1.0;
      }

      // Detect lexical upgrade opportunities
      const upgrades = [];
      const upgradeMap = [
        ["i think", "from my perspective / I am inclined to argue that"],
        ["a lot of", "a substantial proportion of / an abundance of"],
        ["very important", "of paramount importance / pivotal"],
        ["good", "exemplary / profoundly beneficial"],
        ["bad", "detrimental / adverse"],
        ["big problem", "pressing challenge / formidable dilemma"],
        ["help", "facilitate / bolster"],
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
          original: "conversational flow",
          band_9_upgrade: "Integrate discourse markers: 'Notwithstanding that fact', 'In the broader scheme of things', 'To put this into perspective'",
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
          "Use cohesive conversational signposts ('Looking back at that period', 'In the broader scheme of things').",
          "Elaborate thoroughly on causes and personal reflections rather than single-sentence answers."
        ],
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

// Listening Module
async function initListening() {
  await loadListeningSection(appState.currentListeningSection || "sec_1");

  const playBtn = document.getElementById("playAudioScriptBtn");
  playBtn.addEventListener("click", () => {
    speakText(appState.listeningAudioScript || "", playBtn);
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

    const rep = await callApi("/api/listening/submit", "POST", { 
      section_id: appState.currentListeningSection,
      answers 
    });
    if (rep) {
      const repBox = document.getElementById("listeningScoreReport");
      repBox.style.display = "block";
      repBox.innerHTML = `
        <h3>Listening Score: Band ${rep.estimated_band}</h3>
        <p>Correct: <strong>${rep.correct_answers} / ${rep.total_questions}</strong></p>
        <p><em>${rep.disclaimer}</em></p>
      `;
    }
  });
}

async function loadListeningSection(secId) {
  appState.currentListeningSection = secId;
  const sec = await callApi(`/api/listening?sec_id=${secId}`);
  if (sec) {
    document.getElementById("listeningTitle").innerText = `Section ${sec.section_number}: ${sec.title}`;
    appState.listeningAudioScript = sec.audio_script || "";
    document.getElementById("listeningTranscriptBox").innerText = appState.listeningAudioScript;

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

    const repBox = document.getElementById("listeningScoreReport");
    if (repBox) repBox.style.display = "none";
  }
}

window.switchListeningSection = async function(secId) {
  document.querySelectorAll(".section-selector-bar .btn").forEach(b => {
    b.classList.remove("btn-primary", "active");
    b.classList.add("btn-outline");
  });
  const activeBtn = document.getElementById(`secBtn_${secId}`);
  if (activeBtn) {
    activeBtn.classList.remove("btn-outline");
    activeBtn.classList.add("btn-primary", "active");
  }
  await loadListeningSection(secId);
};

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
    utt.lang = "en-US";
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

  alert("Audio speech output is not supported on this browser.");
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

// -------------------------------------------------------------
// Interactive AI Speaking Examiner & Fluency Coach
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
  window.onSpeechError = (code) => {
    console.warn("Android speech recognition error:", code);
    if (recordBtn) recordBtn.innerText = "🎙️ Answer Examiner (Speak)";
  };

  // Web Speech API fallback for desktop browsers
  let recognizer = null;
  const isAndroidApp = window.AndroidSTT && typeof window.AndroidSTT.startListening === "function";

  if (!isAndroidApp && ("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognizer = new SpeechRecognition();
    recognizer.continuous = true;
    recognizer.interimResults = true;
    recognizer.lang = "en-GB"; // Standard British examiner accent support

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
    div.className = speaker === "examiner" ? "dialogue-item examiner-turn" : "dialogue-item candidate-turn";
    div.innerHTML = `<strong>${speaker === "examiner" ? "Dr. Harrison (Examiner)" : "You (Candidate)"}:</strong> ${text}`;
    dialogueHistoryEl.appendChild(div);
    dialogueHistoryEl.scrollTop = dialogueHistoryEl.scrollHeight;
  }

  async function askExaminerQuestion(questionText, stageLabel) {
    appState.speakingInterview.currentQuestionText = questionText;
    examinerBubble.innerText = `"${questionText}"`;
    examinerStatus.innerText = stageLabel;
    appendDialogueTurn("examiner", questionText);

    // Speak with examiner prosody (British Council accent, 0.92x cadence)
    speakText(questionText, replayBtn);

    // Enable answering controls
    recordBtn.disabled = false;
    transcriptEl.value = "";
    document.getElementById("speakingStatusText").innerText = "Examiner asked question. Tap microphone to reply.";
  }

  startBtn.addEventListener("click", async () => {
    const setIdx = parseInt(examSetSelect.value) || 0;
    appState.speakingInterview.examSetIdx = setIdx;
    appState.speakingInterview.active = true;
    appState.speakingInterview.part1QuestionIdx = 0;
    appState.speakingInterview.part3QuestionIdx = 0;
    appState.speakingInterview.dialogueHistory = [];
    appState.speakingInterview.candidateFullTranscript = "";

    dialogueHistoryEl.innerHTML = "";
    reportContainer.style.display = "none";
    part2PrepCard.style.display = "none";

    const examData = await callApi(`/api/speaking/prompts?card_idx=${setIdx}`);
    appState.speakingInterview.examData = examData;

    // Start Part 1
    appState.speakingInterview.stage = "part1";
    updateStageBadges("badgePart1");
    startBtn.disabled = true;
    examSetSelect.disabled = true;

    const firstQ = examData.part_1[0];
    await askExaminerQuestion(firstQ, "Part 1: Introduction & Interview");
  });

  resetBtn.addEventListener("click", () => {
    stopAudioSpeech(replayBtn);
    if (appState.speakingInterview.prepTimerInterval) {
      clearInterval(appState.speakingInterview.prepTimerInterval);
    }
    if (appState.speakingTimerInterval) {
      clearInterval(appState.speakingTimerInterval);
    }
    appState.speakingInterview.active = false;
    appState.speakingInterview.stage = "idle";
    startBtn.disabled = false;
    examSetSelect.disabled = false;
    recordBtn.disabled = true;
    stopBtn.disabled = true;
    part2PrepCard.style.display = "none";
    reportContainer.style.display = "none";
    updateStageBadges("badgePart1");
    examinerBubble.innerText = `"Good day. Welcome to the IELTS Speaking test. Please select a topic above and press 'Begin Official Interview' to start."`;
    examinerStatus.innerText = "Ready to begin interview";
    timerEl.innerText = "00:00";
  });

  replayBtn.addEventListener("click", () => {
    if (appState.speakingInterview.currentQuestionText) {
      speakText(appState.speakingInterview.currentQuestionText, replayBtn);
    }
  });

  recordBtn.addEventListener("click", () => {
    stopAudioSpeech(replayBtn);
    appState.speakingSeconds = 0;
    timerEl.innerText = "00:00";
    recordBtn.disabled = true;
    stopBtn.disabled = false;
    document.getElementById("speakingStatusText").innerText = "Recording... Speak clearly into microphone.";

    if (window.AndroidSTT && typeof window.AndroidSTT.startListening === "function") {
      window.AndroidSTT.startListening();
    } else if (recognizer) {
      try { recognizer.start(); } catch (e) {}
    }

    appState.speakingTimerInterval = setInterval(() => {
      appState.speakingSeconds++;
      const m = String(Math.floor(appState.speakingSeconds / 60)).padStart(2, "0");
      const s = String(appState.speakingSeconds % 60).padStart(2, "0");
      timerEl.innerText = `${m}:${s}`;
    }, 1000);
  });

  stopBtn.addEventListener("click", async () => {
    clearInterval(appState.speakingTimerInterval);
    recordBtn.disabled = false;
    stopBtn.disabled = true;
    recordBtn.innerText = "🎙️ Answer Examiner (Speak)";

    if (window.AndroidSTT && typeof window.AndroidSTT.stopListening === "function") {
      window.AndroidSTT.stopListening();
    } else if (recognizer) {
      try { recognizer.stop(); } catch (e) {}
    }

    const candidateAnswer = transcriptEl.value.trim() || "(Candidate answered briefly)";
    appendDialogueTurn("candidate", candidateAnswer);
    appState.speakingInterview.candidateFullTranscript += " " + candidateAnswer;

    // Advance state machine
    await advanceSpeakingInterview();
  });

  skipPrepBtn.addEventListener("click", () => {
    if (appState.speakingInterview.prepTimerInterval) {
      clearInterval(appState.speakingInterview.prepTimerInterval);
    }
    part2PrepCard.style.display = "none";
    startPart2SpeakingTurn();
  });

  async function advanceSpeakingInterview() {
    const interview = appState.speakingInterview;
    const examData = interview.examData;

    if (interview.stage === "part1") {
      interview.part1QuestionIdx++;
      if (interview.part1QuestionIdx < examData.part_1.length) {
        const nextQ = examData.part_1[interview.part1QuestionIdx];
        await askExaminerQuestion(nextQ, `Part 1 (${interview.part1QuestionIdx + 1}/${examData.part_1.length})`);
      } else {
        // Transition to Part 2 Cue Card Prep
        interview.stage = "part2_prep";
        updateStageBadges("badgePart2");
        startPart2Preparation(examData.part_2_cue_card);
      }
    } else if (interview.stage === "part2_speak") {
      // Transition to Part 3 Abstract Discussion
      interview.stage = "part3";
      interview.part3QuestionIdx = 0;
      updateStageBadges("badgePart3");
      const firstPart3Q = examData.part_3_discussion[0];
      await askExaminerQuestion(firstPart3Q, `Part 3: Discussion (1/${examData.part_3_discussion.length})`);
    } else if (interview.stage === "part3") {
      interview.part3QuestionIdx++;
      if (interview.part3QuestionIdx < examData.part_3_discussion.length) {
        const nextQ = examData.part_3_discussion[interview.part3QuestionIdx];
        await askExaminerQuestion(nextQ, `Part 3: Discussion (${interview.part3QuestionIdx + 1}/${examData.part_3_discussion.length})`);
      } else {
        // Test complete! Evaluate entire interview
        await completeSpeakingInterview();
      }
    }
  }

  function startPart2Preparation(cueCard) {
    part2PrepCard.style.display = "block";
    recordBtn.disabled = true;
    stopBtn.disabled = true;

    part2CueTextEl.innerHTML = `
      <strong>${cueCard.topic}</strong>
      <p style="margin-top: 6px;">You should say:<br>${cueCard.prompts.map(p => `• ${p}`).join("<br>")}</p>
    `;

    const examinerNotice = "Thank you. Now in Part 2, I am going to give you a topic and I would like you to speak for one to two minutes. Before you start, you have one minute to think about what you are going to say. You can make notes if you wish. Here is your topic.";
    examinerBubble.innerText = `"${examinerNotice}"`;
    examinerStatus.innerText = "Part 2: 1-Minute Preparation Time";
    speakText(examinerNotice, replayBtn);

    let secondsRemaining = 60;
    prepCountdownEl.innerText = "01:00";

    appState.speakingInterview.prepTimerInterval = setInterval(() => {
      secondsRemaining--;
      const s = String(secondsRemaining % 60).padStart(2, "0");
      prepCountdownEl.innerText = `00:${s}`;
      if (secondsRemaining <= 0) {
        clearInterval(appState.speakingInterview.prepTimerInterval);
        part2PrepCard.style.display = "none";
        startPart2SpeakingTurn();
      }
    }, 1000);
  }

  function startPart2SpeakingTurn() {
    appState.speakingInterview.stage = "part2_speak";
    const examinerNotice = "All right, your preparation time is up. Please speak for one to two minutes on your topic.";
    examinerBubble.innerText = `"${examinerNotice}"`;
    examinerStatus.innerText = "Part 2: Candidate Long Turn (1-2 mins)";
    speakText(examinerNotice, replayBtn);

    recordBtn.disabled = false;
    transcriptEl.value = "";
    document.getElementById("speakingStatusText").innerText = "Preparation finished. Press microphone and deliver your Part 2 talk.";
  }

  async function completeSpeakingInterview() {
    appState.speakingInterview.stage = "done";
    updateStageBadges("badgeResult");
    recordBtn.disabled = true;
    stopBtn.disabled = true;
    startBtn.disabled = false;
    examSetSelect.disabled = false;

    const concludingRemark = "Thank you very much. That is the end of the IELTS Speaking test. Let us now examine your comprehensive diagnostic assessment.";
    examinerBubble.innerText = `"${concludingRemark}"`;
    examinerStatus.innerText = "Interview Complete • Results Ready";
    speakText(concludingRemark, replayBtn);

    const fullTranscript = appState.speakingInterview.candidateFullTranscript.trim();
    const duration = Math.max(90, appState.speakingInterview.dialogueHistory.length * 30);

    const rep = await callApi("/api/speaking/evaluate", "POST", {
      transcript: fullTranscript || "I think this topic is very important and we need to help people in my opinion.",
      duration_seconds: duration
    });

    if (rep) {
      reportContainer.style.display = "block";
      renderSpeakingDiagnosticReport(rep, evalReportEl);
      evalReportEl.scrollIntoView({ behavior: "smooth" });
    }
  }

  function renderSpeakingDiagnosticReport(rep, targetEl) {
    let criteriaHtml = "";
    if (rep.criteria) {
      for (const [cName, cScore] of Object.entries(rep.criteria)) {
        criteriaHtml += `<li><strong>${cName}:</strong> Band ${cScore}</li>`;
      }
    }

    let upgradesHtml = "";
    if (rep.band_upgrades && rep.band_upgrades.length > 0) {
      upgradesHtml = "<h4 class='mt-3'>🎯 Band 8.0/9.0 Lexical & Phrasal Upgrades:</h4>";
      rep.band_upgrades.forEach(u => {
        upgradesHtml += `
          <div class="upgrade-item" style="background: rgba(255,255,255,0.03); border-left: 3px solid #10b981; padding: 10px 14px; border-radius: 6px; margin-top: 8px;">
            <p style="margin: 0;"><strong>Your Phrase:</strong> <span style="color: #ef4444;">"${u.original}"</span></p>
            <p style="margin: 4px 0 0 0;"><strong>Band 9 Native Expression:</strong> <span style="color: #10b981; font-weight: 600;">"${u.band_9_upgrade}"</span></p>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: var(--text-secondary);">${u.tip}</p>
          </div>
        `;
      });
    }

    let tipsHtml = "";
    if (rep.actionable_tips && rep.actionable_tips.length > 0) {
      tipsHtml = "<h4 class='mt-3'>💡 Actionable Examiner Coaching:</h4><ul>";
      rep.actionable_tips.forEach(t => { tipsHtml += `<li>${t}</li>`; });
      tipsHtml += "</ul>";
    }

    targetEl.innerHTML = `
      <h3>Official Speaking Assessment: Band ${rep.estimated_band}</h3>
      <p><strong>Pacing & Fluency:</strong> ${rep.fluency_metrics.words_per_minute} WPM (Target: ${rep.fluency_metrics.target_wpm_range})</p>
      <p><strong>Filler Hesitations:</strong> ${rep.fluency_metrics.total_filler_words} detected (${rep.fluency_metrics.filler_percentage}%)</p>
      <p><strong>Examiner Notes:</strong> ${rep.fluency_metrics.feedback}</p>
      <hr style="opacity: 0.15; margin: 12px 0;">
      <h4>Four-Criteria Breakdown:</h4>
      <ul>${criteriaHtml}</ul>
      ${upgradesHtml}
      ${tipsHtml}
      <p class='mt-3' style="font-size: 0.85rem; opacity: 0.8;"><em>${rep.disclaimer}</em></p>
    `;
  }
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
