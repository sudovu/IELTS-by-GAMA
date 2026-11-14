/**
 * IELTS by GAMA - Frontend Client Application
 * Hybrid Online + Offline AI English Tutor
 * Features dual-mode networking: REST API with zero-network standalone offline fallback.
 * Incorporates Chris Pell's IELTS Advantage Methodology & Question Analysis Framework.
 */

const API_BASE = "";
const APP_VERSION = "1.6.0";

// Global State
let appState = {
  version: APP_VERSION,
  currentTab: "dashboard",
  connectivity: "OFFLINE",
  forcedOffline: false,
  sessionToken: localStorage.getItem("gama_session_token") || null,
  currentUser: JSON.parse(localStorage.getItem("gama_current_user") || "null") || { user_id: "learner_alice", role: "learner" },
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
  getLearners() {
    const raw = localStorage.getItem("gama_learners");
    if (raw) {
      try { return JSON.parse(raw); } catch (e) {}
    }
    const def = this.getProfile();
    return [def];
  },
  getActiveLearnerId() {
    return localStorage.getItem("gama_active_learner_id") || "default_learner";
  },
  getProfile() {
    const activeId = this.getActiveLearnerId();
    const rawList = localStorage.getItem("gama_learners");
    if (rawList) {
      try {
        const list = JSON.parse(rawList);
        const found = list.find(l => l.id === activeId);
        if (found) return found;
      } catch (e) {}
    }
    const raw = localStorage.getItem("gama_profile");
    if (raw) {
      try {
        const p = JSON.parse(raw);
        p.id = p.id || activeId;
        return p;
      } catch (e) {}
    }
    return {
      id: "default_learner",
      name: "Learner",
      current_band: 6.0,
      target_band: 7.5,
      cefr_level: "B2",
      daily_minutes: 30,
      track: "Academic",
      native_language: "English",
      target_exam_date: null,
      notes: ""
    };
  },
  saveProfile(p) {
    p.id = p.id || this.getActiveLearnerId();
    localStorage.setItem("gama_profile", JSON.stringify(p));
    let list = [];
    try {
      list = JSON.parse(localStorage.getItem("gama_learners") || "[]");
    } catch (e) { list = []; }
    const idx = list.findIndex(l => l.id === p.id);
    if (idx >= 0) {
      list[idx] = { ...list[idx], ...p };
    } else {
      list.push(p);
    }
    localStorage.setItem("gama_learners", JSON.stringify(list));
  },
  computeDynamicRadar(prof) {
    const cefrMap = { A1: 3.0, A2: 4.0, B1: 5.0, B2: 6.0, C1: 7.5, C2: 8.5 };
    const baseBand = Number(prof.current_band) || cefrMap[prof.cefr_level] || 6.0;
    
    let activities = [];
    try {
      activities = JSON.parse(localStorage.getItem("gama_practice_activity") || "[]");
    } catch (e) {}
    
    const getBand = (type) => {
      const filtered = activities.filter(a => a.type === type && a.score);
      if (!filtered.length) return baseBand;
      const sum = filtered.reduce((acc, a) => acc + Number(a.score), 0);
      return Math.round((sum / filtered.length) * 10) / 10;
    };

    const reading = getBand("reading");
    const listening = getBand("listening");
    const writing = getBand("writing");
    const speaking = getBand("speaking");

    const mistakes = this.getMistakes();
    const activeGrammar = mistakes.filter(m => m.skill === "grammar" && m.status !== "mastered").length;
    const grammarPenalty = Math.min(1.5, activeGrammar * 0.1);
    const grammar = Math.max(3.0, Math.round((baseBand - grammarPenalty) * 10) / 10);

    const srs = this.getSRS();
    const masteredSRS = srs.filter(s => s.repetition >= 2).length;
    const vocabBonus = Math.min(1.0, masteredSRS * 0.05);
    const vocabulary = Math.min(9.0, Math.round((baseBand + vocabBonus) * 10) / 10);

    const fluency = Math.round(baseBand * 10) / 10;
    const pronunciation = Math.round(baseBand * 10) / 10;

    return {
      "Reading": reading,
      "Listening": listening,
      "Writing": writing,
      "Speaking": speaking,
      "Grammar": grammar,
      "Vocabulary": vocabulary,
      "Fluency": fluency,
      "Pronunciation": pronunciation
    };
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

  getCurriculumProgress() {
    const raw = localStorage.getItem("gama_curriculum_progress");
    return raw ? JSON.parse(raw) : {};
  },
  saveCurriculumProgress(prog) {
    localStorage.setItem("gama_curriculum_progress", JSON.stringify(prog));
  },
  getStarterLessons() {
    return [
      {
        id: "curric_a1_gram_present_simple", cefr_level: "A1", module_type: "grammar", title: "Present Simple & Subject-Verb Concord", order_index: 1,
        objectives: ["Understand when to use the Present Simple for habits and routines", "Master third-person singular inflection ('-s'/'-es')", "Formulate accurate negative sentences using 'does not'"],
        explanation_markdown: "The Present Simple expresses habits, daily routines, and universal truths. Third person singular (he/she/it) adds -s/-es. Negatives use do/does not + base verb.",
        examples: [{ text: "She studies English for forty minutes every evening.", notes: "Third-person singular 'she' requires 'studies'." }],
        guided_exercises: [{ id: "a1_ge_1", prompt: "My brother _____ (work) in a hospital in Manchester.", answer: "works", explanation: "'My brother' is third-person singular (he), requiring '-s'." }],
        interactive_practice: [{ id: "a1_ip_1", question: "Which sentence demonstrates correct third-person concord?", options: ["He watch documentary films.", "He watches documentary films.", "He is watches films."], correct_index: 1, explanation: "Verbs ending in '-ch' take '-es': 'watches'." }],
        assessment: [{ id: "a1_as_1", question: "Choose the correct negative form: 'Sarah _____ coffee after dinner.'", options: ["doesn't drinks", "don't drink", "doesn't drink", "not drinks"], correct_index: 2, explanation: "'Sarah' (she) takes 'doesn't' + base verb 'drink'." }]
      },
      {
        id: "curric_a1_vocab_everyday_essentials", cefr_level: "A1", module_type: "vocabulary", title: "Everyday Essentials: Numbers, Family & Time", order_index: 2,
        objectives: ["Learn essential vocabulary for time, dates, and family relationships", "Use prepositions of time ('at', 'in', 'on') accurately"],
        explanation_markdown: "Prepositions of time: AT for specific hours (at 7:00), ON for days and dates (on Friday), IN for months, years, and seasons (in July, in 2026).",
        examples: [{ text: "The lecture begins at nine o'clock on Monday.", notes: "'At' for specific time, 'on' for day." }],
        guided_exercises: [{ id: "a1_v_ge_1", prompt: "The examination takes place _____ Tuesday afternoon.", answer: "on", explanation: "Days of the week take 'on'." }],
        interactive_practice: [{ id: "a1_v_ip_1", question: "Select the correct preposition: 'The flight departs _____ midnight.'", options: ["in", "on", "at"], correct_index: 2, explanation: "Points of time like 'midnight' require 'at'." }],
        assessment: [{ id: "a1_v_as_1", question: "Which phrase correctly states a morning schedule?", options: ["The class begins at 8:00 AM on Friday.", "The class begins in 8:00 AM at Friday."], correct_index: 0, explanation: "'At' for hour, 'on' for day." }]
      },
      {
        id: "curric_a1_speak_introductions", cefr_level: "A1", module_type: "speaking", title: "Self-Introductions & Personal Information", order_index: 3,
        objectives: ["Introduce oneself clearly in formal interviews", "State nationality, origin, and occupation accurately"],
        explanation_markdown: "Formula: 'Good morning, my name is [Name]. I come from [City], and I work as a / am an undergraduate student majoring in [Field].'",
        examples: [{ text: "Good morning. My name is Bhuwan Gautam, and I come from Kathmandu, Nepal.", notes: "Clear and professional." }],
        guided_exercises: [{ id: "a1_sp_ge_1", prompt: "Complete: 'I am _____ from Pokhara, Nepal.'", answer: "originally", explanation: "'Originally' indicates hometown origin." }],
        interactive_practice: [{ id: "a1_sp_ip_1", question: "Natural answer to 'Where are you from?'", options: ["I am coming from Spain.", "I am from Valencia, which is on the eastern coast of Spain."], correct_index: 1, explanation: "Gives origin and brief context." }],
        assessment: [{ id: "a1_sp_as_1", question: "Introduce occupation properly:", options: ["I work like an accountant.", "I am working as an accountant at an international firm."], correct_index: 1, explanation: "'Work as a/an [profession]' is the idiomatic standard." }]
      },
      {
        id: "curric_a2_gram_past_simple", cefr_level: "A2", module_type: "grammar", title: "Past Simple & Completed Actions", order_index: 1,
        objectives: ["Use Past Simple to narrate finished past events", "Master negative and question forms with auxiliary 'did'"],
        explanation_markdown: "Past Simple denotes completed actions at definite times. Negatives use didn't + base verb ('didn't go', NOT 'didn't went').",
        examples: [{ text: "The committee published their findings yesterday.", notes: "Regular past with time marker 'yesterday'." }],
        guided_exercises: [{ id: "a2_ge_1", prompt: "Yesterday, they _____ (see) an informative documentary.", answer: "saw", explanation: "Irregular past of 'see' is 'saw'." }],
        interactive_practice: [{ id: "a2_ip_1", question: "Identify the correct past negative:", options: ["He didn't went yesterday.", "He didn't go yesterday."], correct_index: 1, explanation: "Auxiliary didn't requires base verb 'go'." }],
        assessment: [{ id: "a2_as_1", question: "Choose the correct past question:", options: ["Did she finished the report?", "Did she finish the report?"], correct_index: 1, explanation: "'Did' + subject + base form 'finish'." }]
      },
      {
        id: "curric_a2_vocab_travel_transport", cefr_level: "A2", module_type: "vocabulary", title: "Travel, Commuting & Urban Geography", order_index: 2,
        objectives: ["Expand transit vocabulary: commute, congestion, fare, network"],
        explanation_markdown: "Commute: daily travel to work. Congestion: heavy traffic blocking roads. Fare: price paid for travel ticket.",
        examples: [{ text: "Urban professionals commute by underground train to avoid congestion.", notes: "High-frequency transport vocabulary." }],
        guided_exercises: [{ id: "a2_v_ge_1", prompt: "Traffic _____ causes significant delays.", answer: "congestion", explanation: "'Congestion' specifically describes traffic jams." }],
        interactive_practice: [{ id: "a2_v_ip_1", question: "Daily journey people make to their workplace?", options: ["Voyage", "Commute", "Expedition"], correct_index: 1, explanation: "'Commute' specifically refers to travel to and from work." }],
        assessment: [{ id: "a2_v_as_1", question: "Public transport ticket prices are called:", options: ["fares", "debts", "penalties"], correct_index: 0, explanation: "Transport tickets are 'fares'." }]
      },
      {
        id: "curric_a2_read_scanning_notices", cefr_level: "A2", module_type: "reading", title: "Scanning Notices & Informational Announcements", order_index: 3,
        objectives: ["Distinguish skimming for gist from scanning for facts", "Locate dates, eligibility, and fees rapidly"],
        explanation_markdown: "Scanning is moving your eyes across text to locate specific keywords, dates, or numbers without reading every word.",
        examples: [{ text: "Notice: 'Submissions accepted until 5:00 PM on Friday.' Scanning for deadline -> Friday.", notes: "Direct keyword location." }],
        guided_exercises: [{ id: "a2_r_ge_1", prompt: "Members enter free; others pay £12. Member fee? (Answer: free)", answer: "free", explanation: "Targeted scanning directly yields 'free'." }],
        interactive_practice: [{ id: "a2_r_ip_1", question: "Difference between skimming and scanning?", options: ["Skimming captures gist; scanning finds specific data.", "They are identical."], correct_index: 0, explanation: "Skimming gives overview; scanning extracts target points." }],
        assessment: [{ id: "a2_r_as_1", question: "Facility closed alternate Mondays. Is it open every Monday?", options: ["Yes", "No"], correct_index: 1, explanation: "'Alternate' means every other, so not every Monday." }]
      },
      {
        id: "curric_b1_gram_present_perfect", cefr_level: "B1", module_type: "grammar", title: "Present Perfect vs. Past Simple Distinction", order_index: 1,
        objectives: ["Distinguish unfinished time (Present Perfect) from finished time (Past Simple)", "Use 'for' (duration) and 'since' (starting point) accurately"],
        explanation_markdown: "Present Perfect (have/has + participle) connects past to present. Never combine it with finished past time expressions like 'yesterday' or 'in 2020'.",
        examples: [{ text: "Researchers have investigated solar cells for over a decade.", notes: "Ongoing inquiry spanning past into present." }],
        guided_exercises: [{ id: "b1_ge_1", prompt: "She has lived here _____ three years. (for / since)", answer: "for", explanation: "'Three years' is duration, requiring 'for'." }],
        interactive_practice: [{ id: "b1_ip_1", question: "Which sentence contains an error?", options: ["I visited London two months ago.", "I have visited London two months ago."], correct_index: 1, explanation: "'Two months ago' is finished time and cannot use Present Perfect." }],
        assessment: [{ id: "b1_as_1", question: "Select correct sentence:", options: ["The company released three patches last month.", "The company has released three patches last month."], correct_index: 0, explanation: "'Last month' requires Past Simple 'released'." }]
      },
      {
        id: "curric_b1_vocab_workplace_education", cefr_level: "B1", module_type: "vocabulary", title: "Workplace Dynamics, Careers & Higher Education", order_index: 2,
        objectives: ["Learn tertiary education and vocational terminology", "Form academic word families"],
        explanation_markdown: "Tertiary education refers to university studies. Vocational education refers to practical job training. Curriculum is the academic courses offered.",
        examples: [{ text: "Tertiary education equips graduates with specialized technical competencies.", notes: "Band 7+ lexis." }],
        guided_exercises: [{ id: "b1_v_ge_1", prompt: "Practical job training is known as _____ education. (vocational / theoretical)", answer: "vocational", explanation: "'Vocational' refers to trade and technical training." }],
        interactive_practice: [{ id: "b1_v_ip_1", question: "University-level education is termed:", options: ["Primary education", "Tertiary education"], correct_index: 1, explanation: "'Tertiary' is the standard academic term." }],
        assessment: [{ id: "b1_v_as_1", question: "Collocation: 'Update their academic _____ to reflect changes.'", options: ["curriculum", "commute", "fare"], correct_index: 0, explanation: "'Academic curriculum' is the standard pairing." }]
      },
      {
        id: "curric_b1_write_cohesion_linkers", cefr_level: "B1", module_type: "writing", title: "Paragraph Architecture & Cohesive Discourse Linkers", order_index: 3,
        objectives: ["Construct clear topic sentences", "Deploy contrast (However), addition (Furthermore), and consequence (Therefore) correctly"],
        explanation_markdown: "Cohesive linkers signpost logic: However (contrast), Consequently/Therefore (result), Furthermore/Moreover (addition). Precede with a semicolon or start sentence with a comma.",
        examples: [{ text: "Renewable energy requires capital investment. Consequently, subsidies are vital.", notes: "Cause and effect signposting." }],
        guided_exercises: [{ id: "b1_w_ge_1", prompt: "Electric cars produce zero emissions. _____, their batteries require rare minerals. (However / Furthermore)", answer: "However", explanation: "Contrasts advantage with drawback." }],
        interactive_practice: [{ id: "b1_w_ip_1", question: "Which connector introduces a logical consequence?", options: ["In addition", "Therefore", "Whereas"], correct_index: 1, explanation: "'Therefore' signals logical outcome." }],
        assessment: [{ id: "b1_w_as_1", question: "Punctuate correctly:", options: ["Furthermore strict penalties deter polluters.", "Furthermore, strict penalties deter polluters."], correct_index: 1, explanation: "Sentence-initial conjunctive adverbs require a comma." }]
      },
      {
        id: "curric_b2_gram_conditionals", cefr_level: "B2", module_type: "grammar", title: "Hypothetical Conditionals & Mixed Forms in Academic Arguments", order_index: 1,
        objectives: ["Master Second, Third, and Mixed Conditionals", "Apply hypothetical subjunctive ('If governments were to...')"],
        explanation_markdown: "Second conditional (unreal present/future): If + past, would + verb. Third conditional (unreal past): If + had + participle, would have + participle. Mixed: If + had + participle, would + base verb.",
        examples: [{ text: "If municipal councils were to invest in light rail, inner-city pollution would decline substantially.", notes: "Subjunctive hypothetical proposal." }],
        guided_exercises: [{ id: "b2_ge_1", prompt: "If scientists _____ (not / develop) mRNA vaccines, recovery would have been delayed.", answer: "had not developed", explanation: "Third conditional unreal past requires 'had not developed'." }],
        interactive_practice: [{ id: "b2_ip_1", question: "Correct mixed conditional:", options: ["If she had studied medicine, she would be a doctor today.", "If she studied medicine, she would be a doctor today."], correct_index: 0, explanation: "Past condition producing present ongoing state." }],
        assessment: [{ id: "b2_as_1", question: "Identify the flawed sentence:", options: ["If taxes were increased, spending would fall.", "If taxes would be increased, spending would fall."], correct_index: 1, explanation: "Never place 'would' inside the if-clause." }]
      },
      {
        id: "curric_b2_vocab_academic_word_list", cefr_level: "B2", module_type: "vocabulary", title: "Academic Word List (AWL) Sublist 1 Mastery", order_index: 2,
        objectives: ["Deploy high-frequency AWL terms: analyze, derive, establish, constituent", "Replace informal verbs with academic equivalents"],
        explanation_markdown: "Analyze (examine methodically), Derive (obtain from source), Establish (demonstrate conclusively), Constituent (essential component).",
        examples: [{ text: "Statistical analysis establishes a definitive correlation between diet and wellness.", notes: "Band 8 academic usage." }],
        guided_exercises: [{ id: "b2_v_ge_1", prompt: "Scholars continue to _____ (analyze / look at) the socioeconomic implications.", answer: "analyze", explanation: "'Analyze' replaces informal 'look at'." }],
        interactive_practice: [{ id: "b2_v_ip_1", question: "Academic synonym for 'got' in: 'Researchers _____ conclusions from empirical data.'", options: ["got", "derived", "grabbed"], correct_index: 1, explanation: "'Derived' signifies extracting evidence-based findings." }],
        assessment: [{ id: "b2_v_as_1", question: "Collocation: 'Surveys have _____ a clear link between screen time and sleep.'", options: ["established", "built", "fixed"], correct_index: 0, explanation: "'Establish a link' is an essential collocation." }]
      },
      {
        id: "curric_b2_write_peel_paragraph_technique", cefr_level: "B2", module_type: "writing", title: "PEEL Paragraph Architecture for IELTS Writing Task 2", order_index: 3,
        objectives: ["Structure body paragraphs with Point, Explanation, Evidence, and Link (PEEL)", "Develop ideas deeply rather than listing superficial points"],
        explanation_markdown: "PEEL: Point (assertive topic sentence) -> Explanation (mechanics and reasons) -> Evidence (concrete example or case study) -> Link (synthesize back to thesis).",
        examples: [{ text: "P: Renewable investment accelerates diversification. E: It reduces reliance on volatile imports. E: Uruguay reached 98% clean grid power in 10 years. L: Hence, it safeguards fiscal stability.", notes: "Complete PEEL progression." }],
        guided_exercises: [{ id: "b2_w_ge_1", prompt: "In PEEL, the second 'E' stands for Evidence or _____? (Answer: Example)", answer: "Example", explanation: "'Example' or 'Evidence' grounds the explanation." }],
        interactive_practice: [{ id: "b2_w_ip_1", question: "Function of the Link sentence?", options: ["Introduce a new topic", "Tie the paragraph back to the overall essay thesis"], correct_index: 1, explanation: "Unites specific reasoning back to main thesis." }],
        assessment: [{ id: "b2_w_as_1", question: "Best Topic Sentence (Point):", options: ["There are good and bad things about phones.", "Ubiquitous smartphone use has compromised productivity by fragmenting concentration."], correct_index: 1, explanation: "Assertive, focused topic sentence." }]
      },
      {
        id: "curric_c1_gram_inversion", cefr_level: "C1", module_type: "grammar", title: "Negative & Restrictive Adverbial Inversion", order_index: 1,
        objectives: ["Deploy negative adverbials ('Seldom', 'Rarely', 'Not only') at sentence onset", "Invert subject and auxiliary verb accurately for dramatic emphasis"],
        explanation_markdown: "Formula: Negative Adverbial + Auxiliary Verb + Subject + Main Verb. Example: 'Seldom have economists witnessed such rapid reallocation.' 'Not only does automation lower cost, but it also improves safety.'",
        examples: [{ text: "Rarely do modern educational systems cultivate autonomous critical thinking alongside rote learning.", notes: "Inverted rhetorical opening." }],
        guided_exercises: [{ id: "c1_ge_1", prompt: "Seldom _____ (have / do / are) climatologists recorded such rapid retreat.", answer: "have", explanation: "Perfect aspect inversion requires 'have'." }],
        interactive_practice: [{ id: "c1_ip_1", question: "Correct inversion structure:", options: ["Not only automation lowers cost, but it creates jobs.", "Not only does automation lower cost, but it also creates jobs."], correct_index: 1, explanation: "Requires auxiliary 'does' immediately following 'Not only'." }],
        assessment: [{ id: "c1_as_1", question: "Rewrite with inversion: 'We rarely see such scholarship.'", options: ["Rarely we see such scholarship.", "Rarely do we see such scholarship."], correct_index: 1, explanation: "'Rarely' + auxiliary 'do' + subject 'we'." }]
      },
      {
        id: "curric_c1_vocab_academic_collocations", cefr_level: "C1", module_type: "vocabulary", title: "Nuanced Academic Collocations & Collocational Chains", order_index: 2,
        objectives: ["Master collocational pairings: mitigate risk, exert influence, exacerbate disparities", "Avoid unidiomatic literal translations"],
        explanation_markdown: "Collocations are words that naturally co-occur in formal registers: exacerbate disparities (worsen inequalities), mitigate deleterious effects (reduce harm), exert influence.",
        examples: [{ text: "Failure to regulate algorithms risks exacerbating existing socioeconomic disparities.", notes: "Band 8.5 lexical precision." }],
        guided_exercises: [{ id: "c1_v_ge_1", prompt: "Subsidies are designed to _____ (mitigate / heal) economic shocks.", answer: "mitigate", explanation: "'Mitigate' collocates with shock, impact, and risk." }],
        interactive_practice: [{ id: "c1_v_ip_1", question: "Collocation: 'Algorithms _____ a profound influence over behavior.'", options: ["make", "exert", "do"], correct_index: 1, explanation: "'Exert influence' is the standard collocation." }],
        assessment: [{ id: "c1_v_as_1", question: "Collocation for worsening a condition: 'Inadequate drainage will _____ the flooding.'", options: ["exacerbate", "enlarge", "multiply"], correct_index: 0, explanation: "'Exacerbate severity' is the academic standard." }]
      },
      {
        id: "curric_c1_speak_discourse_markers", cefr_level: "C1", module_type: "speaking", title: "Spoken Fluency Discourse Markers & Epistemic Stance", order_index: 3,
        objectives: ["Deploy framing markers: 'From an economic standpoint', 'Broadly speaking'", "Qualify generalizations with academic hedging"],
        explanation_markdown: "Perspective signposts frame thoughts: 'From a sociological vantage point...', 'While that position holds merit, one cannot overlook...'. Hedging avoids sweeping absolutes.",
        examples: [{ text: "Well, from a sociological vantage point, urbanization is something of a double-edged sword.", notes: "Sophisticated framing." }],
        guided_exercises: [{ id: "c1_sp_ge_1", prompt: "Complete: 'From a technological _____ (point / standpoint), AI accelerates diagnosis.'", answer: "standpoint", explanation: "'From a [domain] standpoint' frames perspectives." }],
        interactive_practice: [{ id: "c1_sp_ip_1", question: "Natural concession before counter-critique?", options: ["I hate this opinion, so I think...", "While that argument undoubtedly holds merit, it fails to account for..."], correct_index: 1, explanation: "Respectful academic concession demonstrates C1 spoken mastery." }],
        assessment: [{ id: "c1_sp_as_1", question: "Best way to hedge a generalization in speaking:", options: ["Everyone in the world always does this.", "The empirical evidence tends to indicate that this pattern is predominant."], correct_index: 1, explanation: "'Tends to indicate' avoids unsubstantiated absolutes." }]
      },
      {
        id: "curric_c2_gram_cleft_sentences", cefr_level: "C2", module_type: "grammar", title: "Cleft Sentences & Discourse Topicalization", order_index: 1,
        objectives: ["Formulate it-clefts ('It was the lack of...') and wh-clefts ('What we require is...')", "Foreground critical arguments stylistically"],
        explanation_markdown: "Cleft sentences divide a proposition into two clauses to emphasize focus. It-cleft: It was [focus] that [clause]. Wh-cleft: What [clause] is [focus].",
        examples: [{ text: "What is particularly striking is the sheer velocity of oceanic temperature elevation.", notes: "Wh-cleft structural focus." }],
        guided_exercises: [{ id: "c2_ge_1", prompt: "It was human negligence _____ caused the disaster. (that / which)", answer: "that", explanation: "'It was [focus] that...' is the it-cleft formula." }],
        interactive_practice: [{ id: "c2_ip_1", question: "Authentic wh-cleft structure:", options: ["What policy makers must recognize is that growth cannot occur in isolation.", "Policy makers must recognize what growth is."], correct_index: 0, explanation: "'What [clause] is [proposition]' forms a wh-cleft." }],
        assessment: [{ id: "c2_as_1", question: "Targeting causation with an it-cleft:", options: ["It was precisely because transit was privatized that fares skyrocketed.", "It was precisely because transit was privatized which fares skyrocketed."], correct_index: 0, explanation: "'It was [cause] that [consequence]' is grammatically exact." }]
      },
      {
        id: "curric_c2_vocab_idiomatic_register", cefr_level: "C2", module_type: "vocabulary", title: "Stylistic Register & Idiomatic Sophistication", order_index: 2,
        objectives: ["Deploy refined idioms: watershed moment, sea change, double-edged sword, quintessential", "Harmonize elevated register across scholarly prose"],
        explanation_markdown: "Watershed moment: decisive turning point. Sea change: profound, sweeping transformation. Double-edged sword: carrying both benefits and latent perils.",
        examples: [{ text: "The advent of AI represents a watershed moment in digital pedagogy.", notes: "Eloquent conceptualization." }],
        guided_exercises: [{ id: "c2_v_ge_1", prompt: "A decisive turning point is a _____ (watershed / waterfall) moment.", answer: "watershed", explanation: "'Watershed moment' is the standard idiom." }],
        interactive_practice: [{ id: "c2_v_ip_1", question: "Idiom for a profound transformation:", options: ["A lake change", "A sea change"], correct_index: 1, explanation: "'A sea change' denotes radical transformation." }],
        assessment: [{ id: "c2_v_as_1", question: "Sentence with flawless C2 register:", options: ["The new law was super good and changed lots of stuff.", "The landmark legislation represented a watershed moment that catalyzed a sea change in consumer privacy."], correct_index: 1, explanation: "Exemplifies elevated academic and stylistic precision." }]
      },
      {
        id: "curric_c2_read_implicit_author_stance", cefr_level: "C2", module_type: "reading", title: "Deconstructing Irony, Hedging & Implicit Author Stance", order_index: 3,
        objectives: ["Detect subtle authorial skepticism through reporting verbs ('purports', 'alleges')", "Deconstruct complex True/False/Not Given questions"],
        explanation_markdown: "Authors signal skepticism through verbs like 'purports to' or 'alleges', and scare quotes around terms like 'breakthrough'. Concessive adverbials like 'plausible as this conjecture may seem' precede rebuttals.",
        examples: [{ text: "'While proponents herald the reform, corroborating telemetry remains sparse.' Stance: Skeptical.", notes: "Signals clear doubt." }],
        guided_exercises: [{ id: "c2_r_ge_1", prompt: "A theory 'purports to explain consciousness'. Does author fully endorse it? (Yes / No)", answer: "No", explanation: "'Purports to' implies doubt and unproven claims." }],
        interactive_practice: [{ id: "c2_r_ip_1", question: "Author: 'It is arguably premature to dismantle traditional frameworks.' Stance?", options: ["Cautious and advising against rapid abandonment", "Strongly in favor of immediate abolition"], correct_index: 0, explanation: "'Premature to dismantle' explicitly advises caution." }],
        assessment: [{ id: "c2_r_as_1", question: "Sentence: 'The reform proved to be little more than rhetorical window-dressing.' Tone:", options: ["Enthusiastic", "Skeptical and dismissive"], correct_index: 1, explanation: "'Rhetorical window-dressing' conveys dismissive skepticism." }]
      }
    ];
  },

  getCurriculumLessons(level = null, moduleType = null) {
    let lessons = this.getStarterLessons();
    if (level) lessons = lessons.filter(l => l.cefr_level.toUpperCase() === level.toUpperCase());
    if (moduleType) lessons = lessons.filter(l => l.module_type.toLowerCase() === moduleType.toLowerCase());

    const progressMap = this.getCurriculumProgress();
    const activeLid = this.getActiveLearnerId();
    const learnerProg = progressMap[activeLid] || {};

    return lessons.map(l => {
      const p = learnerProg[l.id] || { status: "not_started", score: 0.0, attempts: 0 };
      return {
        id: l.id,
        cefr_level: l.cefr_level,
        module_type: l.module_type,
        title: l.title,
        order_index: l.order_index,
        status: p.status,
        score: p.score,
        attempts: p.attempts
      };
    });
  },

  getCurriculumLesson(lessonId) {
    const lessons = this.getStarterLessons();
    const lesson = lessons.find(l => l.id === lessonId);
    if (!lesson) return null;

    const copy = JSON.parse(JSON.stringify(lesson));
    const progressMap = this.getCurriculumProgress();
    const activeLid = this.getActiveLearnerId();
    const learnerProg = progressMap[activeLid] || {};
    copy.learner_progress = learnerProg[lessonId] || { status: "not_started", score: 0.0, attempts: 0 };
    return copy;
  },

  evaluateCurriculumSubmission(body) {
    const lessonId = body?.lesson_id;
    const answers = body?.answers || {};
    const lesson = this.getCurriculumLesson(lessonId);
    if (!lesson) return { success: false, error: "Lesson not found" };

    const questions = (lesson.assessment && lesson.assessment.length) ? lesson.assessment : (lesson.interactive_practice || []);
    let correct = 0;
    const feedback = [];

    questions.forEach(q => {
      const userAns = answers[q.id];
      const isCorrect = (userAns !== undefined && parseInt(userAns, 10) === q.correct_index);
      if (isCorrect) correct++;

      feedback.push({
        question_id: q.id,
        is_correct: isCorrect,
        user_answer: userAns,
        correct_answer: q.correct_index,
        explanation: q.explanation || (isCorrect ? "Correct!" : "Incorrect.")
      });

      if (!isCorrect) {
        const userText = (q.options && userAns !== undefined && q.options[parseInt(userAns, 10)]) ? q.options[parseInt(userAns, 10)] : "Unanswered";
        const correctText = (q.options && q.options[q.correct_index]) ? q.options[q.correct_index] : "Correct Option";
        this.addMistake(lesson.module_type || "grammar", lesson.title, userText, correctText, q.explanation || "");
      }
    });

    const scorePct = questions.length ? Math.round((correct / questions.length) * 100) : 100;
    const status = scorePct >= 80 ? "mastered" : (scorePct >= 60 ? "completed" : "needs_review");

    // Save progress
    const activeLid = this.getActiveLearnerId();
    const progressMap = this.getCurriculumProgress();
    if (!progressMap[activeLid]) progressMap[activeLid] = {};
    const existing = progressMap[activeLid][lessonId] || { attempts: 0, score: 0 };
    progressMap[activeLid][lessonId] = {
      status: status,
      score: Math.max(existing.score, scorePct),
      attempts: existing.attempts + 1,
      completed_at: new Date().toISOString()
    };
    this.saveCurriculumProgress(progressMap);

    return {
      success: true,
      lesson_id: lessonId,
      cefr_level: lesson.cefr_level,
      score: scorePct,
      status: status,
      total_questions: questions.length,
      correct_count: correct,
      feedback: feedback
    };
  },

  handleRequest(url, method = "GET", body = null) {
    const p = url.replace(API_BASE, "");

    if (p === "/api/learners" && method === "GET") {
      return {
        learners: this.getLearners(),
        active_learner_id: this.getActiveLearnerId()
      };
    }

    if (p === "/api/learners/current" && method === "GET") {
      return {
        learner: this.getProfile()
      };
    }

    if (p === "/api/learners/switch" && method === "POST") {
      const newId = body?.learner_id || "default_learner";
      localStorage.setItem("gama_active_learner_id", newId);
      return { success: true, active_learner_id: newId };
    }

    if (p === "/api/learners/save" && method === "POST") {
      const learnerData = body || {};
      if (!learnerData.id) {
        learnerData.id = "learner_" + Date.now().toString(36);
      }
      this.saveProfile(learnerData);
      localStorage.setItem("gama_active_learner_id", learnerData.id);
      return { success: true, learner: learnerData };
    }

    if (p === "/api/learners/delete" && method === "POST") {
      const targetId = body?.learner_id;
      if (targetId && targetId !== "default_learner") {
        let list = this.getLearners().filter(l => l.id !== targetId);
        localStorage.setItem("gama_learners", JSON.stringify(list));
        if (this.getActiveLearnerId() === targetId) {
          localStorage.setItem("gama_active_learner_id", "default_learner");
        }
      }
      return { success: true };
    }

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
      const dynamicRadar = this.computeDynamicRadar(prof);
      return {
        dashboard: {
          learner_profile: prof,
          overall_band_estimate: prof.current_band,
          target_band: prof.target_band,
          cefr_level: prof.cefr_level,
          track: prof.track,
          skills_radar: dynamicRadar,
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

    if (p.startsWith("/api/curriculum/lessons")) {
      const qIndex = p.indexOf("?");
      let level = null;
      let mod = null;
      if (qIndex >= 0) {
        const queryStr = p.slice(qIndex + 1);
        queryStr.split("&").forEach(pair => {
          const [k, v] = pair.split("=");
          if (k === "level" || k === "cefr_level") level = v;
          if (k === "module" || k === "module_type") mod = v;
        });
      }
      return {
        lessons: this.getCurriculumLessons(level, mod),
        active_learner_id: this.getActiveLearnerId()
      };
    }

    if (p.startsWith("/api/curriculum/lesson/")) {
      const lid = p.replace("/api/curriculum/lesson/", "").split("?")[0].trim();
      const lesson = this.getCurriculumLesson(lid);
      return lesson ? { lesson: lesson } : { error: "Lesson not found" };
    }

    if (p === "/api/curriculum/submit" && method === "POST") {
      return this.evaluateCurriculumSubmission(body);
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
    if (appState.sessionToken) {
      opts.headers["X-Session-Token"] = appState.sessionToken;
    }
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
      const tabId = item.getAttribute("data-tab");
      if (tabId) {
        navigateToTab(tabId);
      }
    });
  });

  // Mobile Category Filter Strip
  initMobileCategoryFilter();

  // Connectivity toggle
  const toggleBtn = document.getElementById("toggleOfflineBtn");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      appState.forcedOffline = !appState.forcedOffline;
      toggleBtn.innerText = `Force Offline: ${appState.forcedOffline ? "ON" : "OFF"}`;
      updateConnectivityStatus();
      loadDashboard();
    });
  }

  // Theme toggle button click
  const themeBtn = document.getElementById("themeToggleBtn");
  if (themeBtn) {
    themeBtn.addEventListener("click", toggleTheme);
  }
}

function applyCategoryFilter(filterKey) {
  const filterBtns = document.querySelectorAll(".cat-filter-btn");
  const navGroups = document.querySelectorAll(".nav-category-group");

  filterBtns.forEach(btn => {
    const bFilter = btn.getAttribute("data-filter");
    if (bFilter === filterKey) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  navGroups.forEach(group => {
    const groupCat = group.getAttribute("data-group");
    if (filterKey === "all") {
      group.style.display = "";
    } else {
      group.style.display = groupCat === filterKey ? "" : "none";
    }
  });
}

function initMobileCategoryFilter() {
  const filterBtns = document.querySelectorAll(".cat-filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const filter = btn.getAttribute("data-filter");
      applyCategoryFilter(filter);

      // If current tab is not in the clicked category, switch directly to that category's primary tab
      const currentTab = appState.currentTab || "dashboard";
      const currentNavItem = document.querySelector(`.nav-item[data-tab="${currentTab}"]`);
      const currentCat = currentNavItem ? (currentNavItem.getAttribute("data-cat") || "core") : "core";

      if (currentCat !== filter) {
        if (filter === "exam") {
          navigateToTab("speaking");
        } else if (filter === "advantage") {
          navigateToTab("advantage");
        } else if (filter === "core") {
          navigateToTab("dashboard");
        } else if (filter === "system") {
          navigateToTab("mistakes");
        }
      }
    });
  });

  // Apply initial filter showing all modules by default
  applyCategoryFilter("all");
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
  const container = document.getElementById("advPromptChips") || document.getElementById("advantagePromptChips");
  if (container) {
    container.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
  }
  if (btn) btn.classList.add("active");
  const sel = document.getElementById("advPromptSelect") || document.getElementById("advantagePromptSelect");
  if (sel) sel.value = promptKey;
  loadAdvantagePrompt(promptKey);
};

window.selectGrammarFilter = function(category, btn) {
  const container = document.getElementById("grammarCategoryChips") || document.getElementById("grammarClozeFilterChips");
  if (container) {
    container.querySelectorAll(".chip-btn").forEach(b => b.classList.remove("active"));
  }
  if (btn) btn.classList.add("active");
  const sel = document.getElementById("grammarCategorySelect") || document.getElementById("clozeCategorySelect");
  if (sel) sel.value = category;
  filterFillupDrills(category);
};

window.selectVocabTopicChip = function(topicKey, btn) {
  const container = document.getElementById("vocabTopicChips") || document.getElementById("vocabTopicFilterChips");
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
  if (!tabId) return;
  const cleanId = tabId.replace("tab-", "");

  // 1. Switch active content pane
  document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
  const targetPane = document.getElementById("tab-" + cleanId);
  if (targetPane) {
    targetPane.classList.add("active");
  }
  appState.currentTab = cleanId;

  // 2. Switch active nav item in sidebar & sync category filter
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
  const navItem = document.querySelector(`.nav-item[data-tab="${cleanId}"]`);
  if (navItem) {
    navItem.classList.add("active");

    // Ensure target group is visible without hiding other module categories
    const group = navItem.closest(".nav-category-group");
    if (group && group.style.display === "none") {
      group.style.display = "";
    }

    try {
      navItem.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
    } catch (e) {}
  }

  // 3. Tab-specific data initializers
  try {
    if (cleanId === "dashboard") loadDashboard();
    if (cleanId === "curriculum") initCurriculum();
    if (cleanId === "diagnostic") initDiagnostic();
    if (cleanId === "grammar") initGrammar();
    if (cleanId === "vocab") initVocabulary();
    if (cleanId === "reading") loadReading();
    if (cleanId === "listening") loadListening();
    if (cleanId === "writing") initWriting();
    if (cleanId === "exam") initExamSuite();
    if (cleanId === "speaking") {
      if (typeof onSpeakingSetChanged === "function") {
        onSpeakingSetChanged(appState.currentSpeakingSetIdx || 0);
      }
    }
    if (cleanId === "mistakes") loadMistakes();
    if (cleanId === "advantage") loadAdvantagePrompt("stem");
    if (cleanId === "teacher") loadTeacherDashboard();
    if (cleanId === "doublemark") loadDoubleMarkingView();
    if (cleanId === "beta") loadBetaManagement();
  } catch (err) {
    console.warn(`[Tab Nav Data Init Warning]:`, err);
  }

  window.scrollTo({ top: 0, behavior: "smooth" });
};

window.openGoalSelectorModal = function() {
  const modal = document.getElementById("goalWelcomeModal");
  if (modal) modal.classList.add("open");
};

window.toggleBand9SpeakingModel = function() {
  const box = document.getElementById("speakingBand9ModelBox");
  const btn = document.getElementById("viewBand9SpeakingBtn");
  if (!box) return;
  if (box.style.display === "none" || !box.style.display) {
    box.style.display = "block";
    if (btn) btn.innerText = "Hide Model";
  } else {
    box.style.display = "none";
    if (btn) btn.innerText = "💡 Band 9 Model";
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

  if (tTitle) tTitle.innerText = title || "Band Score Updated!";
  if (tSub) tSub.innerText = subtitle || "";

  toast.classList.add("show");

  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 4500);
}
window.showBandToast = showBandToast;
window.showBandUpdateToast = function(title, subtitle) {
  showBandToast(title, subtitle || "");
};

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
  const prof = dash.learner_profile || {};

  // Update learner badge in header
  const learnerNameEl = document.getElementById("dashboardLearnerName");
  if (learnerNameEl) learnerNameEl.innerText = prof.name || "Learner";
  
  const learnerAvatarEl = document.getElementById("learnerAvatarLetter");
  if (learnerAvatarEl) learnerAvatarEl.innerText = (prof.name || "L").charAt(0).toUpperCase();

  const learnerTrackEl = document.getElementById("dashboardLearnerTrack");
  if (learnerTrackEl) learnerTrackEl.innerText = `${dash.track || "Academic"} • Target ${dash.target_band || 7.5}`;

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

  // First-launch onboarding check
  if (!localStorage.getItem("gama_onboarded")) {
    setTimeout(() => {
      openLearnerProfileModal(true);
    }, 400);
  }
}

// -------------------------------------------------------------
// Learner Profile & Multi-Learner Onboarding Manager
// -------------------------------------------------------------
async function openLearnerProfileModal(isOnboarding = false) {
  const modal = document.getElementById("learnerProfileModal");
  if (!modal) return;
  modal.style.display = "flex";

  const titleEl = document.getElementById("learnerModalTitle");
  if (titleEl) {
    titleEl.innerText = isOnboarding ? "Welcome! Set Up Your Learning Profile" : "Learner Profile & Preferences";
  }

  await loadLearnerProfile();
}

function closeLearnerProfileModal() {
  const modal = document.getElementById("learnerProfileModal");
  if (modal) modal.style.display = "none";
}

function switchProfileModalTab(tab) {
  const tabActive = document.getElementById("tabBtnActiveProfile");
  const tabSwitch = document.getElementById("tabBtnSwitchLearner");
  const contentForm = document.getElementById("profileFormTabContent");
  const contentSwitch = document.getElementById("profileSwitchTabContent");

  if (tab === "active") {
    if (tabActive) tabActive.classList.add("active");
    if (tabSwitch) tabSwitch.classList.remove("active");
    if (contentForm) contentForm.style.display = "block";
    if (contentSwitch) contentSwitch.style.display = "none";
  } else {
    if (tabActive) tabActive.classList.remove("active");
    if (tabSwitch) tabSwitch.classList.add("active");
    if (contentForm) contentForm.style.display = "none";
    if (contentSwitch) contentSwitch.style.display = "block";
    renderLearnersList();
  }
}

async function loadLearnerProfile() {
  const res = await callApi("/api/learners/current");
  const p = res?.learner || {};

  const idEl = document.getElementById("inputLearnerId");
  if (idEl) idEl.value = p.id || "default_learner";

  const nameEl = document.getElementById("inputLearnerName");
  if (nameEl) nameEl.value = p.name || "";

  const langEl = document.getElementById("inputLearnerNativeLang");
  if (langEl) langEl.value = p.native_language || "English";

  const trackEl = document.getElementById("selectLearnerTrack");
  if (trackEl && p.track) trackEl.value = p.track;

  const cefrEl = document.getElementById("selectLearnerCEFR");
  if (cefrEl && p.cefr_level) cefrEl.value = p.cefr_level;

  const targetEl = document.getElementById("selectLearnerTargetBand");
  if (targetEl && p.target_band) targetEl.value = Number(p.target_band).toFixed(1);

  const currentEl = document.getElementById("selectLearnerCurrentBand");
  if (currentEl && p.current_band) currentEl.value = Number(p.current_band).toFixed(1);

  const minsEl = document.getElementById("selectLearnerDailyMinutes");
  if (minsEl && p.daily_minutes) minsEl.value = String(p.daily_minutes);

  const examEl = document.getElementById("inputLearnerExamDate");
  if (examEl) examEl.value = p.target_exam_date || "";

  const notesEl = document.getElementById("inputLearnerNotes");
  if (notesEl) notesEl.value = p.notes || "";
}

async function saveLearnerProfile(e) {
  if (e && e.preventDefault) e.preventDefault();

  const learnerId = document.getElementById("inputLearnerId")?.value || "default_learner";
  const name = document.getElementById("inputLearnerName")?.value.trim() || "Learner";
  const nativeLang = document.getElementById("inputLearnerNativeLang")?.value.trim() || "English";
  const track = document.getElementById("selectLearnerTrack")?.value || "Academic";
  const cefr = document.getElementById("selectLearnerCEFR")?.value || "B2";
  const targetBand = parseFloat(document.getElementById("selectLearnerTargetBand")?.value || "7.5");
  const currentBand = parseFloat(document.getElementById("selectLearnerCurrentBand")?.value || "6.0");
  const dailyMins = parseInt(document.getElementById("selectLearnerDailyMinutes")?.value || "30", 10);
  const examDate = document.getElementById("inputLearnerExamDate")?.value || null;
  const notes = document.getElementById("inputLearnerNotes")?.value.trim() || "";

  const payload = {
    id: learnerId,
    name: name,
    native_language: nativeLang,
    track: track,
    cefr_level: cefr,
    target_band: targetBand,
    current_band: currentBand,
    daily_minutes: dailyMins,
    target_exam_date: examDate,
    notes: notes
  };

  const res = await callApi("/api/learners/save", "POST", payload);
  if (res && (res.success || res.learner)) {
    localStorage.setItem("gama_onboarded", "true");
    closeLearnerProfileModal();
    await loadDashboard();
    showBandToast("✅ Profile Updated", `Active learner set to ${name} (${track} Track)`);
  } else {
    alert("Failed to save learner profile. Please try again.");
  }
}

function prepareNewLearnerProfile() {
  switchProfileModalTab("active");
  const idEl = document.getElementById("inputLearnerId");
  if (idEl) idEl.value = "learner_" + Date.now().toString(36);

  const nameEl = document.getElementById("inputLearnerName");
  if (nameEl) {
    nameEl.value = "";
    nameEl.focus();
  }
  const notesEl = document.getElementById("inputLearnerNotes");
  if (notesEl) notesEl.value = "";

  const examEl = document.getElementById("inputLearnerExamDate");
  if (examEl) examEl.value = "";
}

async function renderLearnersList() {
  const container = document.getElementById("learnerProfilesList");
  if (!container) return;
  container.innerHTML = `<p style="color:var(--text-secondary); font-size:0.85rem;">Loading profiles...</p>`;

  const data = await callApi("/api/learners");
  if (!data || !data.learners) {
    container.innerHTML = `<p style="color:var(--text-secondary);">No profiles available.</p>`;
    return;
  }

  const activeId = data.active_learner_id;
  container.innerHTML = "";

  data.learners.forEach(l => {
    const isCurrent = l.id === activeId;
    const item = document.createElement("div");
    item.style.cssText = `display:flex; justify-content:space-between; align-items:center; padding:10px 14px; border-radius:10px; border:1px solid ${isCurrent ? "var(--accent-primary)" : "var(--border-color)"}; background:${isCurrent ? "rgba(79, 70, 229, 0.08)" : "var(--bg-secondary)"};`;

    item.innerHTML = `
      <div>
        <div style="font-weight:700; font-size:0.95rem;">${l.name || "Learner"} ${isCurrent ? '<span style="font-size:0.75rem; background:var(--accent-primary); color:#fff; padding:2px 6px; border-radius:6px; margin-left:6px;">ACTIVE</span>' : ''}</div>
        <div style="font-size:0.78rem; color:var(--text-secondary); margin-top:2px;">
          ${l.track || "Academic"} • Current: ${l.current_band || 6.0} • Target: ${l.target_band || 7.5} • CEFR: ${l.cefr_level || "B2"}
        </div>
      </div>
      <div style="display:flex; gap:8px;">
        ${!isCurrent ? `<button class="btn btn-primary btn-sm" onclick="switchActiveLearner('${l.id}')">Switch</button>` : `<button class="btn btn-secondary btn-sm" onclick="switchProfileModalTab('active')">Edit</button>`}
        ${!isCurrent && l.id !== "default_learner" ? `<button class="btn btn-outline btn-sm" onclick="deleteLearnerProfile('${l.id}')" style="color:var(--danger, #ef4444);" title="Delete profile">🗑️</button>` : ''}
      </div>
    `;
    container.appendChild(item);
  });
}

async function switchActiveLearner(learnerId) {
  const res = await callApi("/api/learners/switch", "POST", { learner_id: learnerId });
  if (res && res.success) {
    await loadLearnerProfile();
    switchProfileModalTab("active");
    closeLearnerProfileModal();
    await loadDashboard();
    showBandToast("🔄 Learner Switched", "Dashboard and records updated for active profile.");
  }
}

async function deleteLearnerProfile(learnerId) {
  if (!confirm("Are you sure you want to delete this learner profile?")) return;
  const res = await callApi("/api/learners/delete", "POST", { learner_id: learnerId });
  if (res && res.success) {
    await renderLearnersList();
    showBandToast("🗑️ Profile Deleted", "Learner profile has been removed.");
  }
}

window.openLearnerProfileModal = openLearnerProfileModal;
window.closeLearnerProfileModal = closeLearnerProfileModal;
window.switchProfileModalTab = switchProfileModalTab;
window.loadLearnerProfile = loadLearnerProfile;
window.saveLearnerProfile = saveLearnerProfile;
window.prepareNewLearnerProfile = prepareNewLearnerProfile;
window.switchActiveLearner = switchActiveLearner;
window.deleteLearnerProfile = deleteLearnerProfile;

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

  if (sendBtn) sendBtn.addEventListener("click", send);
  if (chatInput) {
    chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") send();
    });
  }

  const voiceBtn = document.getElementById("voiceInputBtn");
  if (voiceBtn) {
    voiceBtn.addEventListener("click", () => {
      if (window.AndroidSTT && typeof window.AndroidSTT.startListening === "function") {
        showBandToast("🎙️ Speech Recognition", "Listening to your voice input...");
        window.onAndroidSpeechResult = (text) => {
          if (chatInput) chatInput.value = text;
        };
        window.AndroidSTT.startListening();
      } else if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        const rec = new SpeechRec();
        rec.lang = "en-GB";
        rec.onresult = (e) => {
          if (chatInput) chatInput.value = e.results[0][0].transcript;
        };
        rec.start();
        showBandToast("🎙️ Speech Recognition", "Speak now...");
      } else {
        showBandToast("🎙️ Voice Assistant", "Please type your question into the input box.");
      }
    });
  }
}

// -------------------------------------------------------------
// English Learning Academy (CEFR A1 - C2 Curriculum) Module
// -------------------------------------------------------------
let activeCurriculumLessonId = null;

async function initCurriculum() {
  await loadCurriculumLessons();
}

async function onCurriculumFilterChange() {
  const level = document.getElementById("curriculumLevelSelect")?.value || "";
  const mod = document.getElementById("curriculumModuleSelect")?.value || "";
  await loadCurriculumLessons(level, mod);
}

async function loadCurriculumLessons(level = "", moduleType = "") {
  const listEl = document.getElementById("curriculumLessonList");
  if (!listEl) return;

  listEl.innerHTML = `<p style="color:var(--text-secondary); font-size:0.85rem; padding:8px;">Loading lessons...</p>`;

  let query = "";
  const params = [];
  if (level) params.push(`level=${encodeURIComponent(level)}`);
  if (moduleType) params.push(`module=${encodeURIComponent(moduleType)}`);
  if (params.length) query = "?" + params.join("&");

  const data = await callApi(`/api/curriculum/lessons${query}`);
  if (!data || !data.lessons) {
    listEl.innerHTML = `<p style="color:var(--text-secondary); padding:8px;">No lessons found matching filters.</p>`;
    return;
  }

  const lessons = data.lessons;
  const countEl = document.getElementById("curriculumLessonCount");
  if (countEl) countEl.innerText = `${lessons.length} Lesson${lessons.length === 1 ? '' : 's'}`;

  listEl.innerHTML = "";
  lessons.forEach(l => {
    const isSelected = l.id === activeCurriculumLessonId;
    const card = document.createElement("div");
    card.className = "curriculum-card";
    card.style.cssText = `
      cursor:pointer; padding:12px 14px; border-radius:12px;
      border:1px solid ${isSelected ? "var(--accent-primary)" : "var(--border-color)"};
      background:${isSelected ? "rgba(79, 70, 229, 0.12)" : "var(--bg-secondary)"};
      transition:all 0.2s ease;
    `;

    const statusBadge = l.status === "mastered"
      ? '<span style="font-size:0.75rem; background:#10b981; color:#fff; padding:2px 6px; border-radius:6px;">⭐ Mastered</span>'
      : (l.status === "completed"
        ? '<span style="font-size:0.75rem; background:#3b82f6; color:#fff; padding:2px 6px; border-radius:6px;">✓ Done</span>'
        : '<span style="font-size:0.75rem; background:rgba(255,255,255,0.08); color:var(--text-secondary); padding:2px 6px; border-radius:6px;">Not Started</span>');

    const scoreDisplay = l.score ? `<span style="font-size:0.75rem; font-weight:700; color:var(--accent-primary); margin-left:6px;">${l.score}%</span>` : '';

    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
        <div style="display:flex; gap:6px; align-items:center;">
          <span style="font-weight:700; font-size:0.78rem; background:var(--accent-primary); color:#fff; padding:2px 6px; border-radius:4px;">${l.cefr_level}</span>
          <span style="font-size:0.75rem; text-transform:uppercase; color:var(--text-secondary); font-weight:600;">${l.module_type}</span>
        </div>
        <div style="display:flex; align-items:center;">
          ${statusBadge}
          ${scoreDisplay}
        </div>
      </div>
      <div style="font-weight:700; font-size:0.88rem; line-height:1.3; color:var(--text-primary); margin-top:4px;">
        ${l.title}
      </div>
    `;

    card.addEventListener("click", () => selectCurriculumLesson(l.id));
    listEl.appendChild(card);
  });

  // If no active lesson, select the first lesson automatically
  if (!activeCurriculumLessonId && lessons.length > 0) {
    selectCurriculumLesson(lessons[0].id);
  }
}

async function selectCurriculumLesson(lessonId) {
  activeCurriculumLessonId = lessonId;

  // Highlight selected card
  document.querySelectorAll("#curriculumLessonList .curriculum-card").forEach(c => {
    c.style.borderColor = "var(--border-color)";
    c.style.background = "var(--bg-secondary)";
  });

  const viewer = document.getElementById("curriculumLessonViewer");
  if (!viewer) return;
  viewer.innerHTML = `<div style="text-align:center; padding:60px 20px; color:var(--text-secondary);">Loading lesson content...</div>`;

  const res = await callApi(`/api/curriculum/lesson/${lessonId}`);
  if (!res || !res.lesson) {
    viewer.innerHTML = `<p style="color:var(--danger, #ef4444);">Failed to load lesson.</p>`;
    return;
  }

  renderCurriculumLesson(res.lesson);
}

function renderCurriculumLesson(lesson) {
  const viewer = document.getElementById("curriculumLessonViewer");
  if (!viewer) return;

  const prog = lesson.learner_progress || { status: "not_started", score: 0 };
  const objectivesHtml = (lesson.objectives || []).map(o => `<li style="margin-bottom:6px;">${o}</li>`).join("");

  const examplesHtml = (lesson.examples || []).map(ex => `
    <div style="background:var(--bg-secondary); border-left:3px solid var(--accent-primary); padding:10px 14px; border-radius:0 8px 8px 0; margin-bottom:8px;">
      <div style="font-style:italic; font-weight:600; color:var(--text-primary); font-size:0.92rem;">"${ex.text}"</div>
      ${ex.notes ? `<div style="font-size:0.8rem; color:var(--text-secondary); margin-top:4px;">ℹ️ ${ex.notes}</div>` : ''}
    </div>
  `).join("");

  const guidedHtml = (lesson.guided_exercises || []).map((ge, idx) => `
    <div style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:10px; padding:12px 14px; margin-bottom:10px;">
      <div style="font-weight:600; font-size:0.9rem; margin-bottom:6px;">Exercise ${idx + 1}: ${ge.prompt}</div>
      <button class="btn btn-outline btn-sm" onclick="toggleGuidedAnswer('${ge.id}')" id="btn_ge_${ge.id}" style="font-size:0.8rem; padding:4px 10px;">Reveal Answer &amp; Analysis</button>
      <div id="ans_ge_${ge.id}" style="display:none; margin-top:8px; padding-top:8px; border-top:1px dashed var(--border-color);">
        <div style="font-weight:700; color:#10b981; font-size:0.88rem;">Answer: ${ge.answer}</div>
        <div style="font-size:0.82rem; color:var(--text-secondary); margin-top:2px;">${ge.explanation}</div>
      </div>
    </div>
  `).join("");

  const quizQuestions = (lesson.assessment && lesson.assessment.length) ? lesson.assessment : (lesson.interactive_practice || []);
  const quizHtml = quizQuestions.map((q, qIdx) => `
    <div class="curriculum-quiz-card" style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:12px; padding:16px; margin-bottom:14px;">
      <div style="font-weight:700; font-size:0.92rem; margin-bottom:10px;">
        Question ${qIdx + 1}: ${q.question}
      </div>
      <div style="display:flex; flex-direction:column; gap:8px;">
        ${(q.options || []).map((opt, optIdx) => `
          <label style="display:flex; align-items:center; gap:10px; cursor:pointer; padding:8px 12px; border-radius:8px; border:1px solid var(--border-color); background:rgba(255,255,255,0.02); transition:all 0.2s;" class="quiz-option-label">
            <input type="radio" name="curr_q_${q.id}" value="${optIdx}" style="accent-color:var(--accent-primary);">
            <span style="font-size:0.88rem;">${opt}</span>
          </label>
        `).join("")}
      </div>
      <div id="quiz_feedback_${q.id}" style="display:none; margin-top:10px; padding:8px 12px; border-radius:8px; font-size:0.85rem;"></div>
    </div>
  `).join("");

  const explanationParagraphs = (lesson.explanation_markdown || "").replace(/\n\n/g, "<br><br>").replace(/### (.*)/g, "<h4 style='margin-top:14px; margin-bottom:8px;'>$1</h4>").replace(/#### (.*)/g, "<h5 style='margin-top:12px; margin-bottom:6px;'>$1</h5>");

  viewer.innerHTML = `
    <!-- Lesson Header -->
    <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:1px solid var(--border-color); padding-bottom:16px; margin-bottom:18px;">
      <div>
        <div style="display:flex; gap:8px; align-items:center; margin-bottom:6px;">
          <span style="font-weight:800; font-size:0.82rem; background:var(--accent-primary); color:#fff; padding:3px 8px; border-radius:6px;">CEFR ${lesson.cefr_level}</span>
          <span style="font-size:0.82rem; text-transform:uppercase; color:var(--text-secondary); font-weight:700;">${lesson.module_type} MODULE</span>
        </div>
        <h3 style="margin:0; font-size:1.35rem; font-weight:800;">${lesson.title}</h3>
      </div>
      <div style="text-align:right;">
        <span style="font-size:0.8rem; color:var(--text-secondary);">Status</span>
        <div style="font-weight:700; font-size:0.95rem; text-transform:capitalize; margin-top:2px;">
          ${prog.status === "mastered" ? "⭐ Mastered" : (prog.status === "completed" ? "✓ Completed" : "Not Started")}
        </div>
      </div>
    </div>

    <!-- 1. Learning Objectives -->
    <div style="margin-bottom:20px; background:rgba(79, 70, 229, 0.05); border:1px solid rgba(79, 70, 229, 0.2); border-radius:12px; padding:14px 18px;">
      <h4 style="margin:0 0 8px 0; font-size:0.95rem; color:var(--accent-primary);">🎯 Learning Objectives</h4>
      <ul style="margin:0; padding-left:20px; font-size:0.88rem; color:var(--text-primary); line-height:1.5;">
        ${objectivesHtml}
      </ul>
    </div>

    <!-- 2. Linguistic Explanation -->
    <div style="margin-bottom:24px;">
      <h4 style="font-size:1.05rem; margin-bottom:10px; border-bottom:1px solid var(--border-color); padding-bottom:6px;">📖 Rules &amp; Linguistic Mechanics</h4>
      <div style="font-size:0.92rem; line-height:1.6; color:var(--text-primary);">
        ${explanationParagraphs}
      </div>
    </div>

    <!-- 3. Authentic Examples -->
    ${lesson.examples && lesson.examples.length ? `
      <div style="margin-bottom:24px;">
        <h4 style="font-size:1.05rem; margin-bottom:10px; border-bottom:1px solid var(--border-color); padding-bottom:6px;">💡 Real-World Models &amp; Collocations</h4>
        <div>${examplesHtml}</div>
      </div>
    ` : ''}

    <!-- 4. Guided Exercises -->
    ${lesson.guided_exercises && lesson.guided_exercises.length ? `
      <div style="margin-bottom:24px;">
        <h4 style="font-size:1.05rem; margin-bottom:10px; border-bottom:1px solid var(--border-color); padding-bottom:6px;">🛠️ Guided Practice</h4>
        <div>${guidedHtml}</div>
      </div>
    ` : ''}

    <!-- 5. Interactive Assessment Quiz -->
    ${quizQuestions.length ? `
      <div style="margin-top:28px; border-top:1px solid var(--border-color); padding-top:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
          <div>
            <h4 style="margin:0; font-size:1.05rem;">📝 Interactive Assessment (${quizQuestions.length} Questions)</h4>
            <span style="font-size:0.82rem; color:var(--text-secondary);">Select the best answer for each question and submit for instant scoring and mistake tracking.</span>
          </div>
          <div id="quizScoreBadge" style="display:none; font-weight:700; font-size:1rem; padding:4px 12px; border-radius:8px;"></div>
        </div>

        <form id="curriculumQuizForm" onsubmit="submitCurriculumAssessment(event, '${lesson.id}')">
          ${quizHtml}
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:16px;">
            <button type="submit" class="btn btn-primary" id="btnSubmitCurriculumQuiz" style="padding:10px 24px; font-weight:700;">
              Submit Assessment &amp; Record Score
            </button>
            <div id="quizSummaryFeedback" style="font-size:0.88rem; font-weight:600;"></div>
          </div>
        </form>
      </div>
    ` : ''}
  `;
}

function toggleGuidedAnswer(geId) {
  const ansBox = document.getElementById(`ans_ge_${geId}`);
  const btn = document.getElementById(`btn_ge_${geId}`);
  if (!ansBox) return;

  if (ansBox.style.display === "none") {
    ansBox.style.display = "block";
    if (btn) btn.innerText = "Hide Answer";
  } else {
    ansBox.style.display = "none";
    if (btn) btn.innerText = "Reveal Answer & Analysis";
  }
}

async function submitCurriculumAssessment(e, lessonId) {
  if (e && e.preventDefault) e.preventDefault();

  const answers = {};
  const checkedInputs = document.querySelectorAll("#curriculumQuizForm input[type='radio']:checked");
  checkedInputs.forEach(inp => {
    const qid = inp.name.replace("curr_q_", "");
    answers[qid] = parseInt(inp.value, 10);
  });

  const submitBtn = document.getElementById("btnSubmitCurriculumQuiz");
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerText = "Evaluating...";
  }

  const res = await callApi("/api/curriculum/submit", "POST", {
    lesson_id: lessonId,
    answers: answers
  });

  if (submitBtn) {
    submitBtn.disabled = false;
    submitBtn.innerText = "Re-Submit Assessment";
  }

  if (!res || !res.success) {
    alert("Evaluation failed. Please try again.");
    return;
  }

  (res.feedback || []).forEach(f => {
    const fbBox = document.getElementById(`quiz_feedback_${f.question_id}`);
    if (fbBox) {
      fbBox.style.display = "block";
      if (f.is_correct) {
        fbBox.style.background = "rgba(16, 185, 129, 0.12)";
        fbBox.style.border = "1px solid rgba(16, 185, 129, 0.3)";
        fbBox.style.color = "#10b981";
        fbBox.innerHTML = `<strong>✓ Correct!</strong> ${f.explanation}`;
      } else {
        fbBox.style.background = "rgba(239, 68, 68, 0.12)";
        fbBox.style.border = "1px solid rgba(239, 68, 68, 0.3)";
        fbBox.style.color = "#ef4444";
        fbBox.innerHTML = `<strong>✗ Incorrect.</strong> ${f.explanation}`;
      }
    }
  });

  const scoreBadge = document.getElementById("quizScoreBadge");
  if (scoreBadge) {
    scoreBadge.style.display = "inline-block";
    scoreBadge.innerText = `Score: ${res.score}% (${res.correct_count}/${res.total_questions})`;
    if (res.score >= 80) {
      scoreBadge.style.background = "#10b981";
      scoreBadge.style.color = "#fff";
    } else if (res.score >= 60) {
      scoreBadge.style.background = "#3b82f6";
      scoreBadge.style.color = "#fff";
    } else {
      scoreBadge.style.background = "#ef4444";
      scoreBadge.style.color = "#fff";
    }
  }

  const summary = document.getElementById("quizSummaryFeedback");
  if (summary) {
    summary.innerHTML = res.score >= 80
      ? `<span style="color:#10b981;">🎉 Mastered! Lesson progress saved to your profile.</span>`
      : (res.score >= 60
        ? `<span style="color:#3b82f6;">✓ Completed. Review incorrect questions to reach mastery.</span>`
        : `<span style="color:#ef4444;">Needs review. Logged to your Mistake Book.</span>`);
  }

  showBandToast("📚 Lesson Evaluated", `Scored ${res.score}% • Status: ${res.status.toUpperCase()}`);

  await loadCurriculumLessons(
    document.getElementById("curriculumLevelSelect")?.value || "",
    document.getElementById("curriculumModuleSelect")?.value || ""
  );
}

window.initCurriculum = initCurriculum;
window.onCurriculumFilterChange = onCurriculumFilterChange;
window.loadCurriculumLessons = loadCurriculumLessons;
window.selectCurriculumLesson = selectCurriculumLesson;
window.toggleGuidedAnswer = toggleGuidedAnswer;
window.submitCurriculumAssessment = submitCurriculumAssessment;

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

  const subBtn = document.getElementById("submitDiagnosticBtn");
  if (subBtn) subBtn.onclick = async () => {
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
  };
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
  await filterFillupDrills("Conditionals");
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
let currentReadingTrack = "Academic";

function switchReadingTrack(track) {
  currentReadingTrack = track;
  const isAcad = track === "Academic";
  const btnAcad = document.getElementById("btnReadingTrackAcad");
  const btnGT = document.getElementById("btnReadingTrackGT");
  const chipsAcad = document.getElementById("readingPassageChips");
  const chipsGT = document.getElementById("readingPassageChipsGT");
  const subheading = document.getElementById("readingSubheading");

  if (isAcad) {
    if (btnAcad) btnAcad.classList.add("active");
    if (btnGT) btnGT.classList.remove("active");
    if (chipsAcad) chipsAcad.style.display = "flex";
    if (chipsGT) chipsGT.style.display = "none";
    if (subheading) subheading.innerText = "Academic Reading Passages";
    switchReadingPassage("acad_p1");
  } else {
    if (btnAcad) btnAcad.classList.remove("active");
    if (btnGT) btnGT.classList.add("active");
    if (chipsAcad) chipsAcad.style.display = "none";
    if (chipsGT) chipsGT.style.display = "flex";
    if (subheading) subheading.innerText = "General Training Sections";
    switchReadingPassage("gt_s1");
  }
}
window.switchReadingTrack = switchReadingTrack;

async function loadReading() {
  await switchReadingPassage(appState.currentReadingPassage || "acad_p1");
}

async function switchReadingPassage(passageId) {
  appState.currentReadingPassage = passageId;
  const p = await callApi(`/api/reading?passage_id=${passageId}`);
  if (!p) return;

  // Update active chip UI
  document.querySelectorAll("#readingPassageChips .chip-btn, #readingPassageChipsGT .chip-btn").forEach(b => {
    b.classList.remove("active");
  });
  const activeBtn = document.getElementById(`rchip_${passageId}`);
  if (activeBtn) activeBtn.classList.add("active");

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

  // Render Questions across all types
  const qList = document.getElementById("readingQuestionsList");
  qList.innerHTML = "";
  p.questions.forEach(q => {
    const qDiv = document.createElement("div");
    qDiv.className = "mb-3 reading-q-block";
    qDiv.style.cssText = "padding:10px 14px; border:1px solid var(--border-color); border-radius:10px; background:var(--bg-secondary);";

    if (q.type === "TFNG" || q.type === "True/False/Not Given") {
      qDiv.innerHTML = `
        <p style="margin-bottom:6px;"><strong>Q${q.num} (${q.type}):</strong> ${q.prompt}</p>
        <div style="display:flex; gap:16px; margin-top:6px;">
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="True" style="accent-color:var(--accent-primary);"> True</label>
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="False" style="accent-color:var(--accent-primary);"> False</label>
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="Not Given" style="accent-color:var(--accent-primary);"> Not Given</label>
        </div>
      `;
    } else if (q.type === "YNNG" || q.type === "Yes/No/Not Given") {
      qDiv.innerHTML = `
        <p style="margin-bottom:6px;"><strong>Q${q.num} (${q.type}):</strong> ${q.prompt}</p>
        <div style="display:flex; gap:16px; margin-top:6px;">
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="Yes" style="accent-color:var(--accent-primary);"> Yes</label>
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="No" style="accent-color:var(--accent-primary);"> No</label>
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="Not Given" style="accent-color:var(--accent-primary);"> Not Given</label>
        </div>
      `;
    } else if (q.type === "MCQ" || q.type === "Multiple Choice") {
      qDiv.innerHTML = `
        <p style="margin-bottom:6px;"><strong>Q${q.num} (Multiple Choice):</strong> ${q.prompt}</p>
        <div style="display:flex; gap:14px; margin-top:6px;">
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="A" style="accent-color:var(--accent-primary);"> Option A</label>
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="B" style="accent-color:var(--accent-primary);"> Option B</label>
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="C" style="accent-color:var(--accent-primary);"> Option C</label>
          <label style="cursor:pointer;"><input type="radio" name="rq_${q.num}" value="D" style="accent-color:var(--accent-primary);"> Option D</label>
        </div>
      `;
    } else {
      qDiv.innerHTML = `
        <p style="margin-bottom:6px;"><strong>Q${q.num} (Completion):</strong> ${q.prompt}</p>
        <input type="text" id="rq_input_${q.num}" class="cloze-input mt-1" style="width:100%; max-width:360px;" placeholder="Max ${q.max_words || 2} word(s)..." />
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
    btn.innerText = "🔍 Keyword & Synonym Table";
  }
}

document.getElementById("submitReadingBtn").addEventListener("click", async () => {
  const answers = {};
  
  // Collect radio answers
  document.querySelectorAll("#readingQuestionsList input[type='radio']:checked").forEach(r => {
    const num = r.name.replace("rq_", "");
    answers[num] = r.value;
  });

  // Collect text completion answers
  document.querySelectorAll("#readingQuestionsList input[type='text']").forEach(inp => {
    const num = inp.id.replace("rq_input_", "");
    if (inp.value.trim()) answers[num] = inp.value.trim();
  });

  const rep = await callApi("/api/reading/submit", "POST", { passage_id: appState.currentReadingPassage, answers: answers });
  if (rep) {
    const box = document.getElementById("readingScoreReport");
    box.style.display = "block";

    let detailedHtml = "";
    (rep.results || []).forEach(r => {
      detailedHtml += `
        <div style="padding:8px 12px; margin-top:6px; border-radius:8px; background:${r.is_correct ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)'}; font-size:0.85rem;">
          <strong>Q${r.question_num}:</strong> ${r.is_correct ? '<span style="color:#10b981;">✓ Correct</span>' : '<span style="color:#ef4444;">✗ Incorrect</span>'}
          <div style="margin-top:2px;">Your answer: <strong>${r.user_answer || '(blank)'}</strong> | Correct: <strong>${r.correct_answer}</strong></div>
          <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:2px;">${r.explanation}</div>
        </div>
      `;
    });

    box.innerHTML = `
      <h3>Estimated Reading Band: Band ${rep.estimated_band}</h3>
      <p>Score: <strong>${rep.correct_answers}</strong> of <strong>${rep.total_questions}</strong> correct (${rep.track} Track).</p>
      <div style="margin-top:12px;">${detailedHtml}</div>
      <div class="callout-card mt-3">
        <strong>IELTS Advantage Reading Strategy:</strong>
        <p>Success in IELTS Reading depends on mapping keywords in questions to precise synonyms in text. Review the detailed breakdown above to analyze distractor traps.</p>
      </div>
      <p class="mt-2" style="font-size:0.75rem;"><em>${rep.disclaimer}</em></p>
    `;
    recordPracticeActivity("reading", rep.estimated_band, `${rep.correct_answers}/${rep.total_questions} correct`);
    loadDashboard();
  }
});

// -------------------------------------------------------------
// 8. Listening Module
// -------------------------------------------------------------
async function loadListening() {
  await switchListeningSection(appState.currentListeningSection || "sec_1");
}

async function switchListeningSection(secId) {
  appState.currentListeningSection = secId;
  ["sec_1", "sec_2", "sec_3", "sec_4"].forEach(id => {
    const b = document.getElementById("secBtn_" + id);
    if (b) b.className = id === secId ? "chip-btn active" : "chip-btn";
  });

  const sec = await callApi(`/api/listening?sec_id=${secId}&show_transcript=true`);
  if (!sec) return;

  document.getElementById("listeningTitle").innerText = sec.title;
  document.getElementById("listeningTranscriptBox").innerText = sec.audio_script || "Transcript hidden during active examination.";
  document.getElementById("listeningScoreReport").style.display = "none";

  const qList = document.getElementById("listeningQuestionsList");
  qList.innerHTML = "";
  (sec.questions || []).forEach(q => {
    const qDiv = document.createElement("div");
    qDiv.className = "mb-3 listening-q-block";
    qDiv.style.cssText = "padding:10px 14px; border:1px solid var(--border-color); border-radius:10px; background:var(--bg-secondary);";
    qDiv.innerHTML = `
      <p style="margin-bottom:6px;"><strong>Q${q.num}:</strong> ${q.prompt}</p>
      <input type="text" id="lq_input_${q.num}" class="cloze-input mt-1" style="width:100%; max-width:360px;" placeholder="Max ${q.max_words || 1} word(s)..." />
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
  document.querySelectorAll("#listeningQuestionsList input[type='text']").forEach(inp => {
    const num = inp.id.replace("lq_input_", "");
    if (inp.value.trim()) answers[num] = inp.value.trim();
  });

  const rep = await callApi("/api/listening/submit", "POST", { section_id: appState.currentListeningSection, answers: answers });
  if (rep) {
    const box = document.getElementById("listeningScoreReport");
    box.style.display = "block";

    let detailedHtml = "";
    (rep.results || []).forEach(r => {
      detailedHtml += `
        <div style="padding:8px 12px; margin-top:6px; border-radius:8px; background:${r.is_correct ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)'}; font-size:0.85rem;">
          <strong>Q${r.question_num}:</strong> ${r.is_correct ? '<span style="color:#10b981;">✓ Correct</span>' : '<span style="color:#ef4444;">✗ Incorrect</span>'}
          <div style="margin-top:2px;">Your answer: <strong>${r.user_answer || '(blank)'}</strong> | Correct: <strong>${r.correct_answer}</strong></div>
          <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:2px;">Distractor Note: ${r.distractor_analysis}</div>
        </div>
      `;
    });

    box.innerHTML = `
      <h3>Estimated Listening Band: Band ${rep.estimated_band}</h3>
      <p>Score: <strong>${rep.correct_answers}</strong> of <strong>${rep.total_questions}</strong> correct.</p>
      <div style="margin-top:12px;">${detailedHtml}</div>
      <p class="mt-2" style="font-size:0.75rem;"><em>${rep.disclaimer}</em></p>
    `;
    recordPracticeActivity("listening", rep.estimated_band, `${rep.correct_answers}/${rep.total_questions} correct`);
    loadDashboard();
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
window.resolveMistake = resolveMistake;
window.toggleTheme = toggleTheme;
window.switchAdvantageSubTab = switchAdvantageSubTab;
window.loadAdvantagePrompt = loadAdvantagePrompt;
window.updateChecklistProgress = updateChecklistProgress;
window.switchGrammarMode = switchGrammarMode;
window.filterFillupDrills = filterFillupDrills;
window.submitClozeAnswer = submitClozeAnswer;
window.switchVocabMode = switchVocabMode;
window.renderVocabTopic = renderVocabTopic;
window.gradeCard = gradeCard;
window.toggleSynonymTable = toggleSynonymTable;
window.switchReadingPassage = switchReadingPassage;
window.switchListeningSection = switchListeningSection;
window.toggleModelEssay = toggleModelEssay;
window.switchWritingPrompt = switchWritingPrompt;

function initSettings() {
  const exportBtn = document.getElementById("exportDataBtn");
  const importBtn = document.getElementById("importDataBtn");
  const dataArea = document.getElementById("dataTransferArea");
  const forceOffCheck = document.getElementById("settingForcedOffline");

  if (forceOffCheck) {
    forceOffCheck.checked = !!appState.forcedOffline;
    forceOffCheck.addEventListener("change", () => {
      appState.forcedOffline = forceOffCheck.checked;
      updateConnectivityStatus();
    });
  }

  if (exportBtn && dataArea) {
    exportBtn.addEventListener("click", () => {
      const exportPayload = {
        profile: OfflineLocalEngine.getProfile(),
        daily_goal: getDailyGoal(),
        category_stats: getCategoryStats(),
        mistakes: OfflineLocalEngine.getMistakes(),
        exported_at: new Date().toISOString()
      };
      dataArea.value = JSON.stringify(exportPayload, null, 2);
      showBandToast("💾 Learning Data Exported", "Copy the JSON text to backup or transfer.");
    });
  }

  if (importBtn && dataArea) {
    importBtn.addEventListener("click", () => {
      try {
        const parsed = JSON.parse(dataArea.value.trim());
        if (parsed.profile) OfflineLocalEngine.saveProfile(parsed.profile);
        if (parsed.daily_goal) saveDailyGoal(parsed.daily_goal);
        if (parsed.category_stats) saveCategoryStats(parsed.category_stats);
        if (parsed.mistakes) localStorage.setItem("gama_mistakes", JSON.stringify(parsed.mistakes));
        loadDashboard();
        showBandToast("✅ Data Restored", "Your learning history and band stats were successfully loaded!");
      } catch (err) {
        showBandToast("⚠️ Import Failed", "Invalid JSON format. Please verify the copied text.");
      }
    });
  }
}

// -------------------------------------------------------------
// Screen Setting Analysis & Proactive Permission Calibration (v1.5.3)
// -------------------------------------------------------------
function analyzeScreenAndPermissions() {
  try {
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
        showBandToast("🎯 Screen Calibrated", `${innerW}x${innerH} (${dpr.toFixed(1)}x) Auto-Fit Active`);
      }
    }

    // Hook Android permission callback
    window.onMicPermissionResult = function(granted) {
      const modal = document.getElementById("screenSetupModal");
      if (modal) modal.remove();
      if (granted) {
        showBandToast("🎤 Microphone Enabled", "Voice recognition ready for Examiner Speaking practice!");
      } else {
        showBandToast("ℹ️ Audio Practice", "Practice available via Text-to-Speech.");
      }
    };
  } catch (err) {
    console.warn("[Screen Analysis Warning]:", err);
  }
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
// iOS & Progressive Web App (PWA) Distribution & Install Helpers
// -------------------------------------------------------------
function isIOSDevice() {
  const ua = window.navigator.userAgent || "";
  const isIOS = /iPad|iPhone|iPod/.test(ua);
  const isIPadOS = navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1;
  return isIOS || isIPadOS;
}

function isStandaloneApp() {
  return window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
}

function openIosInstallModal() {
  const modal = document.getElementById("iosInstallModal");
  if (modal) {
    modal.style.display = "flex";
  }
}
window.openIosInstallModal = openIosInstallModal;

function closeIosInstallModal() {
  const modal = document.getElementById("iosInstallModal");
  if (modal) {
    modal.style.display = "none";
  }
}
window.closeIosInstallModal = closeIosInstallModal;

function initServiceWorker() {
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("sw.js")
        .then((reg) => {
          console.log("[PWA Service Worker] Registered with scope:", reg.scope);
        })
        .catch((err) => {
          console.warn("[PWA Service Worker] Registration failed:", err);
        });
    });
  }
}

function initIOSInstallPrompt() {
  const btn = document.getElementById("iosInstallHeaderBtn");
  if (!btn) return;

  // If user is on an iOS device and not running standalone, highlight the button
  if (isIOSDevice() && !isStandaloneApp()) {
    btn.style.borderColor = "#3b82f6";
    btn.style.boxShadow = "0 0 10px rgba(59,130,246,0.5)";
  }
}

// -------------------------------------------------------------
// Initialization on DOM Ready
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const safeInit = (fnName, fn) => {
    try {
      fn();
    } catch (e) {
      console.error(`[Init Error in ${fnName}]:`, e);
    }
  };

  safeInit("initServiceWorker", initServiceWorker);
  safeInit("initIOSInstallPrompt", initIOSInstallPrompt);
  safeInit("initTheme", initTheme);
  safeInit("updateScreenDimensions", updateScreenDimensions);
  safeInit("analyzeScreenAndPermissions", analyzeScreenAndPermissions);
  safeInit("initIOSAudioUnlock", initIOSAudioUnlock);
  safeInit("initWindowsShortcuts", initWindowsShortcuts);
  safeInit("initNavigation", initNavigation);
  safeInit("initCurriculum", initCurriculum);
  safeInit("initChat", initChat);
  safeInit("initDiagnostic", initDiagnostic);
  safeInit("initWriting", initWriting);
  safeInit("initSpeaking", initSpeaking);
  safeInit("initSettings", initSettings);
  safeInit("updateConnectivityStatus", updateConnectivityStatus);
  safeInit("loadDashboard", loadDashboard);
  safeInit("initDailyGoalModal", initDailyGoalModal);
  safeInit("onSpeakingSetChanged", () => onSpeakingSetChanged(0));

  const verBadge = document.getElementById("appVersionBadge");
  if (verBadge) verBadge.textContent = "v" + APP_VERSION;
  const hdrBadge = document.getElementById("headerVersionBadge");
  if (hdrBadge) hdrBadge.textContent = "v" + APP_VERSION;
  const setVal = document.getElementById("settingsVersionValue");
  if (setVal) setVal.textContent = "v" + APP_VERSION + " Production";
});

// ============================================================================
// PHASE 14 — FULL IELTS EXAMINATION SUITE CONTROLLER
// ============================================================================

const examSuiteState = {
  currentTrack: "Academic",
  activeSessionId: null,
  activeExamId: null,
  activePackage: null,
  activeQuestions: [], // Flattened list of questions for uniform navigation
  currentIndex: 0,
  answers: {},
  flagged: new Set(),
  timerInterval: null,
  remainingSeconds: 3600,
  totalTimeSeconds: 3600,
  autosaveTimer: null,
  prepTimerInterval: null,
  isListeningPlaying: false
};

async function initExamSuite() {
  const activeLearnerId = (typeof appState !== "undefined" && appState.currentLearner && appState.currentLearner.id) || "default_learner";

  // Check for any active in-progress session
  try {
    const res = await fetch(`/api/exam/session?learner_id=${encodeURIComponent(activeLearnerId)}`);
    if (res.ok) {
      const data = await res.json();
      const sess = data.active_session;
      const banner = document.getElementById("examActiveSessionBanner");
      const details = document.getElementById("examActiveBannerDetails");

      if (sess && sess.status === "in_progress") {
        examSuiteState.activeSessionId = sess.session_id;
        examSuiteState.activeExamId = sess.exam_id;
        examSuiteState.currentTrack = sess.track || "Academic";
        examSuiteState.remainingSeconds = sess.remaining_seconds || 3600;
        examSuiteState.totalTimeSeconds = sess.time_limit_seconds || 3600;
        examSuiteState.answers = sess.answers || {};
        examSuiteState.flagged = new Set(sess.flagged || []);

        if (details) {
          const mins = Math.floor(sess.remaining_seconds / 60);
          const secs = sess.remaining_seconds % 60;
          details.textContent = `${sess.track} ${sess.module.toUpperCase()} • Remaining Time: ${mins}m ${secs < 10 ? "0" : ""}${secs}s`;
        }
        if (banner) banner.style.display = "flex";
      } else {
        if (banner) banner.style.display = "none";
      }
    }
  } catch (e) {
    console.warn("[ExamSuite] Failed to check active session:", e);
  }

  loadExamHistory();
}

function selectExamTrack(track) {
  examSuiteState.currentTrack = track;
  const btnAcad = document.getElementById("trackBtnAcademic");
  const btnGen = document.getElementById("trackBtnGeneral");
  const fullMockTitle = document.getElementById("fullMockCardTitle");

  if (track === "Academic") {
    if (btnAcad) btnAcad.classList.add("active");
    if (btnGen) btnGen.classList.remove("active");
    if (fullMockTitle) fullMockTitle.textContent = "IELTS Academic Full 4-Skill Examination";
  } else {
    if (btnGen) btnGen.classList.add("active");
    if (btnAcad) btnAcad.classList.remove("active");
    if (fullMockTitle) fullMockTitle.textContent = "IELTS General Training Full 4-Skill Examination";
  }
}

async function launchExamSession(module) {
  const activeLearnerId = (typeof appState !== "undefined" && appState.currentLearner && appState.currentLearner.id) || "default_learner";
  const track = examSuiteState.currentTrack;

  try {
    const res = await fetch("/api/exam/start", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringifySafe({
        learner_id: activeLearnerId,
        track: track,
        module: module
      })
    });

    if (!res.ok) {
      const err = await res.json();
      alert(`Could not start exam: ${err.error || "Unknown error"}`);
      return;
    }

    const data = await res.json();
    setupExamWorkspace(data);
  } catch (e) {
    console.error("[ExamSuite] Launch failed:", e);
    alert("Connection error starting examination.");
  }
}

async function resumeActiveExam() {
  const activeLearnerId = (typeof appState !== "undefined" && appState.currentLearner && appState.currentLearner.id) || "default_learner";
  try {
    const res = await fetch(`/api/exam/session?learner_id=${encodeURIComponent(activeLearnerId)}`);
    if (res.ok) {
      const data = await res.json();
      if (data.active_session) {
        setupExamWorkspace(data.active_session);
      }
    }
  } catch (e) {
    console.error("[ExamSuite] Resume failed:", e);
  }
}

async function abandonActiveExam() {
  if (!confirm("Are you sure you want to cancel and abandon this examination session? All current unsaved answers will be discarded.")) {
    return;
  }
  const banner = document.getElementById("examActiveSessionBanner");
  if (banner) banner.style.display = "none";
  examSuiteState.activeSessionId = null;
  examSuiteState.answers = {};
  examSuiteState.flagged.clear();
  clearInterval(examSuiteState.timerInterval);
}

function setupExamWorkspace(sessionData) {
  examSuiteState.activeSessionId = sessionData.session_id;
  examSuiteState.activeExamId = sessionData.exam_id;
  examSuiteState.currentTrack = sessionData.track || "Academic";
  examSuiteState.remainingSeconds = sessionData.remaining_seconds || sessionData.time_limit_seconds || 3600;
  examSuiteState.totalTimeSeconds = sessionData.time_limit_seconds || 3600;
  examSuiteState.activePackage = sessionData.exam_package;
  examSuiteState.answers = sessionData.answers || {};
  examSuiteState.flagged = new Set(sessionData.flagged || []);
  examSuiteState.currentIndex = (sessionData.current_question || 1) - 1;

  // Flatten questions into a uniform list
  flattenExamQuestions(sessionData.exam_package, sessionData.module);

  // Switch views
  const lobby = document.getElementById("examLobbyView");
  const workspace = document.getElementById("examActiveWorkspace");
  const results = document.getElementById("examResultsView");

  if (lobby) lobby.style.display = "none";
  if (results) results.style.display = "none";
  if (workspace) workspace.style.display = "flex";

  // Update headers
  const titleEl = document.getElementById("examActiveTitle");
  const badgeEl = document.getElementById("examActiveTrackBadge");
  if (titleEl) titleEl.textContent = sessionData.exam_package ? sessionData.exam_package.title : "IELTS Examination";
  if (badgeEl) badgeEl.textContent = sessionData.track;

  // Build question palette
  renderExamPalette();

  // Start countdown timer
  startExamTimer();

  // Render first question
  renderCurrentExamQuestion();
}

function flattenExamQuestions(pkg, module) {
  const list = [];
  if (!pkg) return;

  // 1. Reading
  if (pkg.passages) {
    pkg.passages.forEach((p, pIdx) => {
      (p.questions || []).forEach(q => {
        list.push({
          skill: "reading",
          sectionTitle: `Passage ${p.passage_number}: ${p.title}`,
          stimulusText: p.text,
          passageId: p.id,
          questionKey: `read_${q.num}`,
          data: q
        });
      });
    });
  } else if (pkg.sections && module === "reading") {
    pkg.sections.forEach((s, sIdx) => {
      (s.questions || []).forEach(q => {
        list.push({
          skill: "reading",
          sectionTitle: `Section ${s.section_number}: ${s.title}`,
          stimulusText: s.text,
          questionKey: `read_${q.num}`,
          data: q
        });
      });
    });
  }

  // 2. Listening
  if (pkg.sections && module === "listening") {
    pkg.sections.forEach(s => {
      (s.questions || []).forEach(q => {
        list.push({
          skill: "listening",
          sectionTitle: `Section ${s.section_number}: ${s.title}`,
          stimulusAudioScript: s.audio_script,
          questionKey: `listen_${q.num}`,
          data: q
        });
      });
    });
  }

  // 3. Writing
  if (pkg.task_1 && pkg.task_2) {
    list.push({
      skill: "writing",
      sectionTitle: `Writing Task 1: ${pkg.task_1.title}`,
      stimulusText: pkg.task_1.prompt,
      questionKey: "writing_task_1",
      minWords: pkg.task_1.min_words || 150,
      data: { num: 1, type: "Writing Task 1", prompt: pkg.task_1.prompt }
    });
    list.push({
      skill: "writing",
      sectionTitle: `Writing Task 2: ${pkg.task_2.title}`,
      stimulusText: pkg.task_2.prompt,
      questionKey: "writing_task_2",
      minWords: pkg.task_2.min_words || 250,
      data: { num: 2, type: "Writing Task 2", prompt: pkg.task_2.prompt }
    });
  }

  // 4. Speaking
  if (pkg.part_1 && pkg.part_2 && pkg.part_3) {
    list.push({
      skill: "speaking",
      sectionTitle: "Speaking Part 1: Introduction & Interview",
      stimulusText: (pkg.part_1.questions || []).map(q => q.text).join("\n"),
      questionKey: "speaking_part_1",
      data: { num: 1, type: "Speaking Part 1", prompt: "Respond to the Part 1 introductory questions." }
    });
    list.push({
      skill: "speaking",
      sectionTitle: "Speaking Part 2: Individual Long Turn",
      cueCard: pkg.part_2.cue_card,
      questionKey: "speaking_part_2",
      prepSeconds: pkg.part_2.preparation_seconds || 60,
      data: { num: 2, type: "Speaking Part 2", prompt: pkg.part_2.cue_card ? pkg.part_2.cue_card.task : "Part 2" }
    });
    list.push({
      skill: "speaking",
      sectionTitle: "Speaking Part 3: Two-way Discussion",
      stimulusText: (pkg.part_3.questions || []).map(q => q.text).join("\n"),
      questionKey: "speaking_part_3",
      data: { num: 3, type: "Speaking Part 3", prompt: "Respond in depth to Part 3 abstract discussion questions." }
    });
  }

  // 5. Full 4-Skill Mock (combining listening, reading, writing, speaking)
  if (pkg.skills) {
    if (pkg.skills.listening) flattenExamQuestions(pkg.skills.listening, "listening");
    if (pkg.skills.reading) flattenExamQuestions(pkg.skills.reading, "reading");
    if (pkg.skills.writing) flattenExamQuestions(pkg.skills.writing, "writing");
    if (pkg.skills.speaking) flattenExamQuestions(pkg.skills.speaking, "speaking");
    return;
  }

  examSuiteState.activeQuestions = list;
}

function renderExamPalette() {
  const container = document.getElementById("examPaletteContainer");
  if (!container) return;
  container.innerHTML = "";

  const total = examSuiteState.activeQuestions.length;
  for (let i = 0; i < total; i++) {
    const item = examSuiteState.activeQuestions[i];
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "exam-palette-btn";
    btn.textContent = (i + 1);

    if (i === examSuiteState.currentIndex) {
      btn.classList.add("active");
    }
    if (examSuiteState.answers[item.questionKey] && examSuiteState.answers[item.questionKey].trim().length > 0) {
      btn.classList.add("answered");
    }
    if (examSuiteState.flagged.has(i)) {
      btn.classList.add("flagged");
    }

    btn.onclick = () => jumpToExamQuestion(i);
    container.appendChild(btn);
  }

  updatePaletteSummary();
}

function updatePaletteSummary() {
  const summaryEl = document.getElementById("examPaletteSummary");
  if (!summaryEl) return;
  const total = examSuiteState.activeQuestions.length;
  let answeredCount = 0;

  for (let i = 0; i < total; i++) {
    const item = examSuiteState.activeQuestions[i];
    if (examSuiteState.answers[item.questionKey] && examSuiteState.answers[item.questionKey].trim().length > 0) {
      answeredCount++;
    }
  }

  summaryEl.textContent = `Question ${examSuiteState.currentIndex + 1} of ${total} (${answeredCount} Answered, ${total - answeredCount} Remaining)`;
}

function startExamTimer() {
  clearInterval(examSuiteState.timerInterval);
  const digits = document.getElementById("examTimerDigits");
  const container = document.getElementById("examTimerDisplay");

  examSuiteState.timerInterval = setInterval(() => {
    examSuiteState.remainingSeconds--;

    if (examSuiteState.remainingSeconds <= 0) {
      clearInterval(examSuiteState.timerInterval);
      alert("⏱️ Examination time has expired! Your work will be submitted automatically.");
      submitExamFinal();
      return;
    }

    const mins = Math.floor(examSuiteState.remainingSeconds / 60);
    const secs = examSuiteState.remainingSeconds % 60;
    if (digits) {
      digits.textContent = `${mins < 10 ? "0" : ""}${mins}:${secs < 10 ? "0" : ""}${secs}`;
    }

    if (container) {
      if (examSuiteState.remainingSeconds <= 300) {
        container.className = "exam-timer-display timer-critical";
      } else if (examSuiteState.remainingSeconds <= 600) {
        container.className = "exam-timer-display timer-warning";
      } else {
        container.className = "exam-timer-display";
      }
    }
  }, 1000);
}

function renderCurrentExamQuestion() {
  if (examSuiteState.activeQuestions.length === 0) return;
  const item = examSuiteState.activeQuestions[examSuiteState.currentIndex];
  if (!item) return;

  const stimPane = document.getElementById("examStimulusPane");
  const intPane = document.getElementById("examInteractionPane");
  const secIndicator = document.getElementById("examActiveSectionIndicator");
  const flagBtn = document.getElementById("examFlagToggleBtn");

  if (secIndicator) secIndicator.textContent = `(${item.sectionTitle})`;
  if (flagBtn) {
    flagBtn.textContent = examSuiteState.flagged.has(examSuiteState.currentIndex) ? "🚩 Flagged" : "🏳️ Flag Question";
  }

  // 1. Render Left Stimulus Pane
  if (stimPane) {
    if (item.skill === "reading") {
      stimPane.innerHTML = `
        <div style="font-size:0.85rem; font-weight:700; color:var(--primary-accent); text-transform:uppercase; margin-bottom:8px;">${escapeHtml(item.sectionTitle)}</div>
        <div style="font-size:0.95rem; line-height:1.75; color:var(--text-primary); white-space:pre-wrap;">${escapeHtml(item.stimulusText || "")}</div>
      `;
    } else if (item.skill === "listening") {
      stimPane.innerHTML = `
        <div style="font-size:0.85rem; font-weight:700; color:var(--primary-accent); text-transform:uppercase; margin-bottom:8px;">${escapeHtml(item.sectionTitle)}</div>
        <div style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:10px; padding:1.25rem; margin-bottom:1rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <strong style="color:var(--text-primary);">Audio Simulation (Web Speech Synthesizer)</strong>
            <span class="badge" style="background:rgba(56, 189, 248, 0.15); color:var(--cat-exam-accent); font-size:0.75rem;">Concealed Transcript</span>
          </div>
          <p style="font-size:0.85rem; color:var(--text-muted); margin:0 0 12px 0;">
            In official computer-delivered IELTS, audio recordings are played once. Transcripts remain concealed during test-taking.
          </p>
          <div style="display:flex; gap:10px;">
            <button type="button" class="btn btn-sm btn-primary" id="examPlayAudioBtn" onclick="toggleExamAudioPlayback()">▶️ Play Audio</button>
            <button type="button" class="btn btn-sm btn-outline" onclick="stopExamAudioPlayback()">⏹️ Stop</button>
          </div>
        </div>
        <div style="font-size:0.85rem; color:var(--text-muted);">
          <em>Tip: Preview the question prompt carefully and anticipate word classes or numbers before listening.</em>
        </div>
      `;
    } else if (item.skill === "writing") {
      stimPane.innerHTML = `
        <div style="font-size:0.85rem; font-weight:700; color:var(--primary-accent); text-transform:uppercase; margin-bottom:8px;">${escapeHtml(item.sectionTitle)}</div>
        <div style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:10px; padding:1.25rem;">
          <h4 style="margin:0 0 10px 0; color:var(--text-primary); font-size:1.05rem;">Task Requirements:</h4>
          <p style="font-size:0.95rem; line-height:1.7; color:var(--text-primary); white-space:pre-wrap; margin:0 0 1rem 0;">${escapeHtml(item.stimulusText || "")}</p>
          <div style="display:flex; gap:12px; font-size:0.85rem; color:var(--text-muted); border-top:1px solid var(--border-color); padding-top:10px;">
            <span>Minimum Target: <strong>${item.minWords} words</strong></span>
            <span>•</span>
            <span>Recommended Time: <strong>${item.minWords === 150 ? "20" : "40"} mins</strong></span>
          </div>
        </div>
      `;
    } else if (item.skill === "speaking") {
      if (item.cueCard) {
        stimPane.innerHTML = `
          <div style="font-size:0.85rem; font-weight:700; color:var(--primary-accent); text-transform:uppercase; margin-bottom:8px;">Speaking Part 2: Task Card</div>
          <div style="background:var(--bg-secondary); border:2px dashed var(--primary-accent); border-radius:12px; padding:1.5rem; margin-bottom:1rem;">
            <h4 style="margin:0 0 10px 0; color:var(--text-primary);">${escapeHtml(item.cueCard.task)}</h4>
            <p style="font-size:0.9rem; color:var(--text-secondary); margin-bottom:8px;">You should say:</p>
            <ul style="padding-left:20px; font-size:0.9rem; color:var(--text-primary); line-height:1.6;">
              ${(item.cueCard.points || []).map(pt => `<li>${escapeHtml(pt)}</li>`).join("")}
            </ul>
          </div>
          <div style="display:flex; align-items:center; gap:12px; background:var(--bg-card); padding:1rem; border-radius:10px; border:1px solid var(--border-color);">
            <button type="button" class="btn btn-sm btn-outline" id="startPrepTimerBtn" onclick="startSpeakingPrepCountdown(60)">⏱️ Start 1-Min Prep Timer</button>
            <span id="prepTimerDisplay" style="font-family:monospace; font-weight:700; font-size:1rem; color:var(--warning-color);">01:00</span>
          </div>
        `;
      } else {
        stimPane.innerHTML = `
          <div style="font-size:0.85rem; font-weight:700; color:var(--primary-accent); text-transform:uppercase; margin-bottom:8px;">${escapeHtml(item.sectionTitle)}</div>
          <div style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:10px; padding:1.25rem;">
            <h4 style="margin:0 0 8px 0;">Examiner Spoken Questions:</h4>
            <div style="font-size:0.95rem; line-height:1.8; color:var(--text-primary); white-space:pre-wrap;">${escapeHtml(item.stimulusText || "")}</div>
          </div>
        `;
      }
    }
  }

  // 2. Render Right Interaction Pane
  if (intPane) {
    const qData = item.data;
    const currentVal = examSuiteState.answers[item.questionKey] || "";

    if (item.skill === "writing") {
      const words = currentVal.trim().length > 0 ? currentVal.trim().split(/\s+/).length : 0;
      intPane.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <h4 style="margin:0; font-size:1.05rem;">Your Written Response:</h4>
          <span style="font-size:0.85rem; font-weight:600;" id="examWordCountBadge">
            Word Count: <strong id="examWordCountNumber" style="color:${words >= item.minWords ? 'var(--success-color)' : 'var(--warning-color)'};">${words}</strong> / ${item.minWords} min
          </span>
        </div>
        <textarea id="examWritingTextarea" class="form-control" style="flex:1; width:100%; min-height:280px; padding:12px; font-size:0.95rem; line-height:1.6; border-radius:8px; border:1px solid var(--border-color); background:var(--bg-input); color:var(--text-primary); resize:vertical;" placeholder="Type your response here..." oninput="recordExamAnswer('${item.questionKey}', this.value)">${escapeHtml(currentVal)}</textarea>
      `;
    } else if (item.skill === "speaking") {
      intPane.innerHTML = `
        <div>
          <h4 style="margin:0 0 8px 0; font-size:1.05rem;">Spoken Transcript / Response Entry:</h4>
          <p style="font-size:0.85rem; color:var(--text-muted); margin:0 0 12px 0;">
            Use the microphone to record your answer via Speech-to-Text or type your exact spoken response.
          </p>
          <div style="display:flex; gap:10px; margin-bottom:12px;">
            <button type="button" class="btn btn-sm btn-outline" id="examRecordVoiceBtn" onclick="toggleExamVoiceRecognition('${item.questionKey}')">🎙️ Record Speech</button>
          </div>
          <textarea id="examSpeakingTextarea" class="form-control" style="width:100%; min-height:180px; padding:12px; font-size:0.95rem; line-height:1.6; border-radius:8px; border:1px solid var(--border-color); background:var(--bg-input); color:var(--text-primary); resize:vertical;" placeholder="Spoken transcript will appear here (or type manually)..." oninput="recordExamAnswer('${item.questionKey}', this.value)">${escapeHtml(currentVal)}</textarea>
        </div>
      `;
    } else {
      // Objective Question (MCQ, TFNG, YNNG, Completion, Matching)
      let inputHtml = "";

      if (qData.options && Array.isArray(qData.options)) {
        inputHtml = `
          <div style="display:flex; flex-direction:column; gap:8px; margin-top:12px;">
            ${qData.options.map((opt, oIdx) => `
              <label style="display:flex; align-items:center; gap:10px; padding:10px 14px; border-radius:8px; border:1px solid var(--border-color); background:var(--bg-secondary); cursor:pointer; font-size:0.92rem;">
                <input type="radio" name="opt_${item.questionKey}" value="${escapeHtml(opt)}" ${currentVal === opt ? 'checked' : ''} onchange="recordExamAnswer('${item.questionKey}', this.value)">
                <span>${escapeHtml(opt)}</span>
              </label>
            `).join("")}
          </div>
        `;
      } else if (qData.type === "TFNG" || qData.type === "True/False/Not Given") {
        inputHtml = `
          <div style="display:flex; gap:10px; margin-top:12px;">
            ${["True", "False", "Not Given"].map(val => `
              <label style="flex:1; display:flex; align-items:center; justify-content:center; gap:8px; padding:10px; border-radius:8px; border:1px solid var(--border-color); background:var(--bg-secondary); cursor:pointer;">
                <input type="radio" name="opt_${item.questionKey}" value="${val}" ${currentVal.toLowerCase() === val.toLowerCase() ? 'checked' : ''} onchange="recordExamAnswer('${item.questionKey}', this.value)">
                <span>${val}</span>
              </label>
            `).join("")}
          </div>
        `;
      } else if (qData.type === "YNNG" || qData.type === "Yes/No/Not Given") {
        inputHtml = `
          <div style="display:flex; gap:10px; margin-top:12px;">
            ${["Yes", "No", "Not Given"].map(val => `
              <label style="flex:1; display:flex; align-items:center; justify-content:center; gap:8px; padding:10px; border-radius:8px; border:1px solid var(--border-color); background:var(--bg-secondary); cursor:pointer;">
                <input type="radio" name="opt_${item.questionKey}" value="${val}" ${currentVal.toLowerCase() === val.toLowerCase() ? 'checked' : ''} onchange="recordExamAnswer('${item.questionKey}', this.value)">
                <span>${val}</span>
              </label>
            `).join("")}
          </div>
        `;
      } else {
        // Text completion
        inputHtml = `
          <div style="margin-top:14px;">
            <label style="font-size:0.85rem; color:var(--text-muted); display:block; margin-bottom:6px;">
              Enter your answer (NO MORE THAN ${qData.max_words || 2} WORDS):
            </label>
            <input type="text" class="form-control" style="width:100%; padding:10px 14px; font-size:1rem; border-radius:8px; border:1px solid var(--border-color); background:var(--bg-input); color:var(--text-primary);" value="${escapeHtml(currentVal)}" placeholder="Type answer here..." oninput="recordExamAnswer('${item.questionKey}', this.value)">
          </div>
        `;
      }

      intPane.innerHTML = `
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="badge" style="background:var(--cat-exam-bg); color:var(--cat-exam-accent); font-weight:700;">Question ${examSuiteState.currentIndex + 1}</span>
            <span style="font-size:0.82rem; color:var(--text-muted);">${escapeHtml(qData.type || "Completion")}</span>
          </div>
          <div style="font-size:1.05rem; font-weight:600; color:var(--text-primary); line-height:1.5;">${escapeHtml(qData.prompt || "")}</div>
          ${inputHtml}
        </div>
      `;
    }
  }

  // Update palette visual states
  renderExamPalette();
}

function recordExamAnswer(key, value) {
  examSuiteState.answers[key] = value;

  // Update writing word count badge live if active
  const wordBadge = document.getElementById("examWordCountNumber");
  if (wordBadge && (key === "writing_task_1" || key === "writing_task_2")) {
    const words = value.trim().length > 0 ? value.trim().split(/\s+/).length : 0;
    wordBadge.textContent = words;
  }

  // Debounced autosave
  clearTimeout(examSuiteState.autosaveTimer);
  const indicator = document.getElementById("examAutosaveIndicator");
  if (indicator) {
    indicator.innerHTML = '<span>🟡</span> <span>Saving...</span>';
  }

  examSuiteState.autosaveTimer = setTimeout(() => {
    executeAutosave();
  }, 1200);

  updatePaletteSummary();
}

async function executeAutosave() {
  if (!examSuiteState.activeSessionId) return;
  const activeLearnerId = (typeof appState !== "undefined" && appState.currentLearner && appState.currentLearner.id) || "default_learner";
  const indicator = document.getElementById("examAutosaveIndicator");

  try {
    const res = await fetch("/api/exam/autosave", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringifySafe({
        session_id: examSuiteState.activeSessionId,
        learner_id: activeLearnerId,
        answers: examSuiteState.answers,
        flagged: Array.from(examSuiteState.flagged),
        current_question: examSuiteState.currentIndex + 1,
        time_spent_seconds: examSuiteState.totalTimeSeconds - examSuiteState.remainingSeconds
      })
    });

    if (res.ok && indicator) {
      indicator.innerHTML = '<span>🟢</span> <span>All answers saved</span>';
    }
  } catch (e) {
    if (indicator) indicator.innerHTML = '<span>🔴</span> <span>Autosave failed (offline)</span>';
  }
}

function toggleCurrentQuestionFlag() {
  const idx = examSuiteState.currentIndex;
  if (examSuiteState.flagged.has(idx)) {
    examSuiteState.flagged.delete(idx);
  } else {
    examSuiteState.flagged.add(idx);
  }
  const flagBtn = document.getElementById("examFlagToggleBtn");
  if (flagBtn) {
    flagBtn.textContent = examSuiteState.flagged.has(idx) ? "🚩 Flagged" : "🏳️ Flag Question";
  }
  renderExamPalette();
}

function navigateExamQuestion(delta) {
  const newIdx = examSuiteState.currentIndex + delta;
  if (newIdx >= 0 && newIdx < examSuiteState.activeQuestions.length) {
    examSuiteState.currentIndex = newIdx;
    renderCurrentExamQuestion();
  }
}

function jumpToExamQuestion(index) {
  if (index >= 0 && index < examSuiteState.activeQuestions.length) {
    examSuiteState.currentIndex = index;
    renderCurrentExamQuestion();
  }
}

function confirmExitExam() {
  if (confirm("Are you sure you want to exit the examination? Your progress is saved, and you can resume anytime before your timer expires.")) {
    clearInterval(examSuiteState.timerInterval);
    const lobby = document.getElementById("examLobbyView");
    const workspace = document.getElementById("examActiveWorkspace");
    if (workspace) workspace.style.display = "none";
    if (lobby) lobby.style.display = "flex";
    initExamSuite();
  }
}

function confirmSubmitExam() {
  const total = examSuiteState.activeQuestions.length;
  let answered = 0;
  for (let i = 0; i < total; i++) {
    const item = examSuiteState.activeQuestions[i];
    if (examSuiteState.answers[item.questionKey] && examSuiteState.answers[item.questionKey].trim().length > 0) {
      answered++;
    }
  }

  const unanswered = total - answered;
  let msg = `You have completed ${answered} of ${total} questions.`;
  if (unanswered > 0) {
    msg += ` You have ${unanswered} UNANSWERED questions remaining!`;
  }
  msg += "\n\nAre you sure you want to finalize and submit your examination? Once submitted, your answers will be locked and graded.";

  if (confirm(msg)) {
    submitExamFinal();
  }
}

async function submitExamFinal() {
  clearInterval(examSuiteState.timerInterval);
  const activeLearnerId = (typeof appState !== "undefined" && appState.currentLearner && appState.currentLearner.id) || "default_learner";

  try {
    const res = await fetch("/api/exam/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringifySafe({
        session_id: examSuiteState.activeSessionId,
        learner_id: activeLearnerId,
        final_answers: examSuiteState.answers
      })
    });

    if (!res.ok) {
      const err = await res.json();
      alert(`Submission error: ${err.error || "Failed to process results."}`);
      return;
    }

    const data = await res.json();
    renderExamResults(data.results || data);
  } catch (e) {
    console.error("[ExamSuite] Submission failed:", e);
    alert("Connection error submitting examination.");
  }
}

function renderExamResults(results) {
  const workspace = document.getElementById("examActiveWorkspace");
  const resultsView = document.getElementById("examResultsView");
  if (workspace) workspace.style.display = "none";
  if (resultsView) resultsView.style.display = "flex";

  const overallEl = document.getElementById("resultsOverallBand");
  const confEl = document.getElementById("resultsConfidenceRange");
  const timestampEl = document.getElementById("resultsExamTimestamp");
  const titleEl = document.getElementById("resultsExamTitle");
  const gridEl = document.getElementById("resultsSkillBandsGrid");
  const qContainer = document.getElementById("resultsDetailedQuestionsContainer");
  const recContainer = document.getElementById("resultsRecommendationsList");

  if (overallEl) overallEl.textContent = Number(results.overall_band || 0.0).toFixed(1);
  if (confEl && results.confidence_range) {
    confEl.textContent = `Confidence Range: [${results.confidence_range[0]} – ${results.confidence_range[1]}]`;
  }
  if (timestampEl) timestampEl.textContent = `Completed on ${new Date().toLocaleDateString()}`;
  if (titleEl) titleEl.textContent = `${results.track || 'IELTS'} Practice Examination Results`;

  // Render Skill Bands
  if (gridEl && results.band_breakdown) {
    gridEl.innerHTML = Object.entries(results.band_breakdown).map(([skill, band]) => `
      <div style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:8px; padding:10px;">
        <div style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted);">${escapeHtml(skill)}</div>
        <div style="font-size:1.6rem; font-weight:800; color:var(--text-primary); margin-top:2px;">${Number(band).toFixed(1)}</div>
      </div>
    `).join("");
  }

  // Render Detailed Question Review
  if (qContainer) {
    qContainer.innerHTML = "";
    const skills = results.skills || {};

    // Reading questions review
    if (skills.reading && skills.reading.questions) {
      skills.reading.questions.forEach(q => {
        const isCor = q.is_correct;
        const card = document.createElement("div");
        card.style.background = isCor ? "rgba(16, 185, 129, 0.06)" : "rgba(239, 68, 68, 0.06)";
        card.style.border = `1px solid ${isCor ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`;
        card.style.borderRadius = "10px";
        card.style.padding = "1rem";

        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:var(--text-primary);">Reading Q${q.question_num}: ${escapeHtml(q.type || "")}</strong>
            <span class="badge" style="background:${isCor ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)'}; color:${isCor ? '#10b981' : '#ef4444'}; font-weight:700;">
              ${isCor ? '✅ Correct' : '❌ Incorrect'}
            </span>
          </div>
          <div style="font-size:0.92rem; color:var(--text-primary); margin-bottom:8px;">${escapeHtml(q.prompt || "")}</div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:0.86rem; margin-bottom:8px;">
            <div>Your Answer: <strong style="color:${isCor ? '#10b981' : '#ef4444'};">${escapeHtml(q.user_answer || "Unanswered")}</strong></div>
            <div>Correct Answer: <strong style="color:#10b981;">${escapeHtml(q.correct_answer || "")}</strong></div>
          </div>
          ${q.explanation ? `<div style="font-size:0.84rem; color:var(--text-secondary); background:var(--bg-secondary); padding:8px 12px; border-radius:6px; border-left:3px solid var(--primary-accent);"><em>Explanation:</em> ${escapeHtml(q.explanation)}</div>` : ''}
        `;
        qContainer.appendChild(card);
      });
    }

    // Listening questions review
    if (skills.listening && skills.listening.questions) {
      skills.listening.questions.forEach(q => {
        const isCor = q.is_correct;
        const card = document.createElement("div");
        card.style.background = isCor ? "rgba(16, 185, 129, 0.06)" : "rgba(239, 68, 68, 0.06)";
        card.style.border = `1px solid ${isCor ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`;
        card.style.borderRadius = "10px";
        card.style.padding = "1rem";

        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:var(--text-primary);">Listening Q${q.question_num}</strong>
            <span class="badge" style="background:${isCor ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)'}; color:${isCor ? '#10b981' : '#ef4444'}; font-weight:700;">
              ${isCor ? '✅ Correct' : '❌ Incorrect'}
            </span>
          </div>
          <div style="font-size:0.92rem; color:var(--text-primary); margin-bottom:8px;">${escapeHtml(q.prompt || "")}</div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:0.86rem; margin-bottom:8px;">
            <div>Your Answer: <strong style="color:${isCor ? '#10b981' : '#ef4444'};">${escapeHtml(q.user_answer || "Unanswered")}</strong></div>
            <div>Correct Answer: <strong style="color:#10b981;">${escapeHtml(q.correct_answer || "")}</strong></div>
          </div>
          ${q.distractor_note ? `<div style="font-size:0.84rem; color:var(--text-secondary); background:var(--bg-secondary); padding:8px 12px; border-radius:6px; border-left:3px solid var(--primary-accent);"><em>Distractor Analysis:</em> ${escapeHtml(q.distractor_note)}</div>` : ''}
        `;
        qContainer.appendChild(card);
      });
    }

    // Writing review
    if (skills.writing) {
      const wCard = document.createElement("div");
      wCard.style.background = "var(--bg-secondary)";
      wCard.style.border = "1px solid var(--border-color)";
      wCard.style.borderRadius = "10px";
      wCard.style.padding = "1rem";
      wCard.innerHTML = `
        <h4 style="margin:0 0 10px 0;">Writing Assessment Rubric Feedback</h4>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:0.88rem;">
          <div>Task 1 (${skills.writing.task_1 ? skills.writing.task_1.word_count : 0}w): <strong>Band ${skills.writing.task_1 ? skills.writing.task_1.band : '-'}</strong></div>
          <div>Task 2 (${skills.writing.task_2 ? skills.writing.task_2.word_count : 0}w): <strong>Band ${skills.writing.task_2 ? skills.writing.task_2.band : '-'}</strong></div>
        </div>
        <p style="font-size:0.82rem; color:var(--text-muted); margin:8px 0 0 0;">Weighted formula: Task 1 (1/3) + Task 2 (2/3) strictly applied.</p>
      `;
      qContainer.appendChild(wCard);
    }
  }

  // Render Targeted Recommendations
  if (recContainer) {
    recContainer.innerHTML = `
      <ul style="padding-left:20px; margin:0;">
        <li><strong>Mistake Ledger Integration:</strong> Incorrect responses have been automatically filed into your personal Mistake Book for targeted spaced-repetition drills.</li>
        <li><strong>Recommended Curriculum:</strong> Target B2/C1 grammar modules in the English Academy to reinforce sentence structure and modal hedging.</li>
        <li><strong>Vocabulary Expansion:</strong> Review high-frequency academic collocations in the Themed Vocabulary Academy.</li>
      </ul>
    `;
  }
}

async function loadExamHistory() {
  const activeLearnerId = (typeof appState !== "undefined" && appState.currentLearner && appState.currentLearner.id) || "default_learner";
  const container = document.getElementById("examHistoryTableContainer");
  if (!container) return;

  try {
    const res = await fetch(`/api/exam/history?learner_id=${encodeURIComponent(activeLearnerId)}`);
    if (res.ok) {
      const data = await res.json();
      const history = data.history || [];

      if (history.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted); font-size:0.9rem;">No completed examination sessions yet. Choose an exam above to begin!</p>';
        return;
      }

      container.innerHTML = `
        <table class="table" style="width:100%; font-size:0.88rem; border-collapse:collapse;">
          <thead>
            <tr style="border-bottom:1px solid var(--border-color); text-align:left; color:var(--text-muted);">
              <th style="padding:8px;">Date</th>
              <th style="padding:8px;">Module</th>
              <th style="padding:8px;">Track</th>
              <th style="padding:8px;">Status</th>
              <th style="padding:8px;">Overall Band</th>
              <th style="padding:8px; text-align:right;">Action</th>
            </tr>
          </thead>
          <tbody>
            ${history.map(h => `
              <tr style="border-bottom:1px solid var(--border-color);">
                <td style="padding:8px;">${new Date(h.started_at).toLocaleDateString()}</td>
                <td style="padding:8px;"><strong>${escapeHtml(h.module ? h.module.toUpperCase() : '')}</strong></td>
                <td style="padding:8px;">${escapeHtml(h.track || '')}</td>
                <td style="padding:8px;"><span class="badge" style="background:${h.status === 'submitted' ? 'rgba(16,185,129,0.15)' : 'rgba(245,158,11,0.15)'}; color:${h.status === 'submitted' ? '#10b981' : '#f59e0b'};">${escapeHtml(h.status)}</span></td>
                <td style="padding:8px; font-weight:700; color:var(--primary-accent);">${h.band_score ? Number(h.band_score).toFixed(1) : '-'}</td>
                <td style="padding:8px; text-align:right;">
                  ${h.status === 'submitted' ? `<button class="btn btn-xs btn-outline" onclick="viewHistoricalExamResults('${h.id}')">View Report</button>` : `<button class="btn btn-xs btn-primary" onclick="resumeActiveExam()">Resume</button>`}
                </td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      `;
    }
  } catch (e) {
    console.warn("[ExamSuite] Failed to load history:", e);
  }
}

async function viewHistoricalExamResults(sessionId) {
  const activeLearnerId = (typeof appState !== "undefined" && appState.currentLearner && appState.currentLearner.id) || "default_learner";
  try {
    const res = await fetch(`/api/exam/results?session_id=${encodeURIComponent(sessionId)}&learner_id=${encodeURIComponent(activeLearnerId)}`);
    if (res.ok) {
      const data = await res.json();
      renderExamResults(data.results || data);
    }
  } catch (e) {
    alert("Could not load historical exam report.");
  }
}

function returnToExamLobby() {
  const lobby = document.getElementById("examLobbyView");
  const workspace = document.getElementById("examActiveWorkspace");
  const results = document.getElementById("examResultsView");

  if (workspace) workspace.style.display = "none";
  if (results) results.style.display = "none";
  if (lobby) lobby.style.display = "flex";

  initExamSuite();
}

function showExamInstructionsModal() {
  alert(
    "IELTS PRACTICE EXAMINATION INSTRUCTIONS\n\n" +
    "1. TIMING: Full mock is 164 mins. Individual skills: Reading (60m), Listening (32m), Writing (60m), Speaking (14m).\n" +
    "2. AUTOSAVE: All answers and flagged items are automatically saved continuously to SQLite.\n" +
    "3. RECOVERY: Accidental browser refreshes restore your session with elapsed timer preserved.\n" +
    "4. CONCEALMENT: Answer keys and transcripts remain concealed until final submission.\n" +
    "5. SCORING: Objective grading out of 40; Writing weighted 1/3 (Task 1) + 2/3 (Task 2); Speaking transcript evaluation."
  );
}

// Listening Web Speech synthesis simulation
function toggleExamAudioPlayback() {
  if (!("speechSynthesis" in window)) {
    alert("Web Speech Synthesis is not supported in this browser or device.");
    return;
  }

  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    const btn = document.getElementById("examPlayAudioBtn");
    if (btn) btn.textContent = "▶️ Play Audio";
    return;
  }

  const item = examSuiteState.activeQuestions[examSuiteState.currentIndex];
  const scriptText = (item && item.stimulusAudioScript) ? item.stimulusAudioScript : "";

  if (!scriptText || scriptText.trim().length === 0) {
    alert("Audio dialogue script is unavailable for this section.");
    return;
  }

  const utterance = new SpeechSynthesisUtterance(scriptText);
  utterance.rate = 0.95;
  utterance.pitch = 1.0;
  utterance.lang = "en-GB";

  utterance.onstart = () => {
    const btn = document.getElementById("examPlayAudioBtn");
    if (btn) btn.textContent = "⏸️ Pause Audio";
  };

  utterance.onend = () => {
    const btn = document.getElementById("examPlayAudioBtn");
    if (btn) btn.textContent = "▶️ Play Audio";
  };

  utterance.onerror = (err) => {
    console.warn("[ExamSuite] Speech synthesis error:", err);
    const btn = document.getElementById("examPlayAudioBtn");
    if (btn) btn.textContent = "▶️ Play Audio";
  };

  window.speechSynthesis.speak(utterance);
}

function stopExamAudioPlayback() {
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
    const btn = document.getElementById("examPlayAudioBtn");
    if (btn) btn.textContent = "▶️ Play Audio";
  }
}

// Speaking Part 2 countdown timer
function startSpeakingPrepCountdown(seconds) {
  clearInterval(examSuiteState.prepTimerInterval);
  let rem = seconds;
  const disp = document.getElementById("prepTimerDisplay");
  const btn = document.getElementById("startPrepTimerBtn");
  if (btn) btn.disabled = true;

  examSuiteState.prepTimerInterval = setInterval(() => {
    rem--;
    if (disp) {
      disp.textContent = `00:${rem < 10 ? '0' : ''}${rem}`;
    }
    if (rem <= 0) {
      clearInterval(examSuiteState.prepTimerInterval);
      if (disp) disp.textContent = "00:00 (Time up! Begin speaking)";
      if (btn) btn.disabled = false;
    }
  }, 1000);
}

// Speaking Speech-to-Text recording toggle
function toggleExamVoiceRecognition(targetKey) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("Speech Recognition is not supported by your browser. Please type your response directly into the textarea.");
    return;
  }

  const btn = document.getElementById("examRecordVoiceBtn");
  const textarea = document.getElementById("examSpeakingTextarea");

  if (btn && btn.classList.contains("recording")) {
    btn.classList.remove("recording");
    btn.textContent = "🎙️ Record Speech";
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-GB";
  recognition.continuous = true;
  recognition.interimResults = true;

  if (btn) {
    btn.classList.add("recording");
    btn.textContent = "⏹️ Stop Recording";
  }

  recognition.onresult = (event) => {
    let transcript = "";
    for (let i = 0; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript + " ";
    }
    if (textarea) {
      textarea.value = transcript.trim();
      recordExamAnswer(targetKey, transcript.trim());
    }
  };

  recognition.onerror = () => {
    if (btn) {
      btn.classList.remove("recording");
      btn.textContent = "🎙️ Record Speech";
    }
  };

  recognition.onend = () => {
    if (btn) {
      btn.classList.remove("recording");
      btn.textContent = "🎙️ Record Speech";
    }
  };

  recognition.start();
}

// =========================================================================
// PHASE 16: AUTHENTICATION, RBAC & SESSION MANAGEMENT
// =========================================================================
window.openAuthModal = function() {
  const m = document.getElementById("authModal");
  if (m) m.style.display = "flex";
};

window.closeAuthModal = function() {
  const m = document.getElementById("authModal");
  if (m) m.style.display = "none";
};

function updateAuthPillUI() {
  const user = appState.currentUser || { user_id: "learner_alice", role: "learner" };
  const iconEl = document.getElementById("authRoleIcon");
  const roleEl = document.getElementById("authRoleLabel");
  const userEl = document.getElementById("authUsernameLabel");

  const roleIcons = {
    learner: "👤",
    teacher: "👩‍🏫",
    examiner: "👨‍⚖️",
    admin: "👑"
  };

  if (iconEl) iconEl.textContent = roleIcons[user.role] || "👤";
  if (roleEl) roleEl.textContent = user.role.charAt(0).toUpperCase() + user.role.slice(1);
  if (userEl) userEl.textContent = user.user_id;

  const teacherNotice = document.getElementById("teacherActiveUserBadge");
  if (teacherNotice) {
    teacherNotice.textContent = `${user.user_id} (${user.role.toUpperCase()})`;
  }
}

window.loginWithCredentials = async function(username, password) {
  const errEl = document.getElementById("loginErrorAlert");
  if (errEl) {
    errEl.style.display = "none";
    errEl.textContent = "";
  }

  try {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (data.status === "authenticated") {
      appState.sessionToken = data.session_token;
      appState.currentUser = data.user;
      localStorage.setItem("gama_session_token", data.session_token);
      localStorage.setItem("gama_current_user", JSON.stringify(data.user));
      updateAuthPillUI();
      closeAuthModal();
      showToastNotification(`Signed in as ${data.user.username} (${data.user.role})`);
      if (appState.currentTab === "teacher") loadTeacherDashboard();
      if (appState.currentTab === "doublemark") loadDoubleMarkingView();
      if (appState.currentTab === "beta") loadBetaManagement();
    } else {
      const msg = data.error || data.message || "Invalid username or password.";
      if (errEl) {
        errEl.textContent = msg;
        errEl.style.display = "block";
      } else {
        alert("Authentication failed: " + msg);
      }
    }
  } catch (err) {
    if (errEl) {
      errEl.textContent = "Login request failed. Check server connectivity.";
      errEl.style.display = "block";
    } else {
      alert("Login request failed: " + err.message);
    }
  }
};

window.handleCustomLogin = async function(e) {
  e.preventDefault();
  const u = document.getElementById("loginUsername").value.trim();
  const p = document.getElementById("loginPassword").value;
  await loginWithCredentials(u, p);
};

window.logoutCurrentUser = async function() {
  if (appState.sessionToken) {
    try {
      await fetch("/api/auth/logout", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "X-Session-Token": appState.sessionToken
        },
        body: JSON.stringify({ session_token: appState.sessionToken })
      });
    } catch (e) {}
  }
  appState.sessionToken = null;
  appState.currentUser = { user_id: "anonymous", role: "guest" };
  localStorage.removeItem("gama_session_token");
  localStorage.removeItem("gama_current_user");
  updateAuthPillUI();
  closeAuthModal();
  showToastNotification("Signed out successfully");
};

async function verifyActiveSession() {
  if (!appState.sessionToken) {
    appState.currentUser = { user_id: "anonymous", role: "guest" };
    updateAuthPillUI();
    return;
  }
  try {
    const res = await fetch("/api/auth/me", {
      headers: { "X-Session-Token": appState.sessionToken }
    });
    if (res.ok) {
      const data = await res.json();
      if (data.authenticated && data.user) {
        appState.currentUser = data.user;
        updateAuthPillUI();
        return;
      }
    }
    // Session is invalid or expired
    appState.sessionToken = null;
    appState.currentUser = { user_id: "anonymous", role: "guest" };
    localStorage.removeItem("gama_session_token");
    localStorage.removeItem("gama_current_user");
    updateAuthPillUI();
  } catch (err) {
    // Network error: maintain cached session in offline mode
    updateAuthPillUI();
  }
}

// =========================================================================
// PHASE 16: TEACHER REVIEW DASHBOARD & STUDIO
// =========================================================================
let currentActiveAssignment = null;
let currentTeacherAssignments = [];

window.loadTeacherDashboard = async function() {
  const listEl = document.getElementById("teacherAssignmentList");
  const countEl = document.getElementById("teacherQueueCountBadge");
  if (!listEl) return;

  listEl.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--text-muted); font-size:0.85rem;">Loading review queue...</div>`;

  try {
    const res = await callApi("/api/teacher/dashboard");
    if (res.error) {
      listEl.innerHTML = `<div style="padding:1rem; color:var(--warning-color); font-size:0.85rem;">${res.error} (Sign in as Teacher or Examiner to access this studio)</div>`;
      return;
    }
    currentTeacherAssignments = res.assignments || [];
    if (countEl) countEl.textContent = `${currentTeacherAssignments.length} items`;
    filterTeacherQueue();
  } catch (err) {
    listEl.innerHTML = `<div style="padding:1rem; color:var(--danger-color); font-size:0.85rem;">Failed to load assignments: ${err.message}</div>`;
  }
};

window.filterTeacherQueue = function() {
  const skill = document.getElementById("teacherSkillFilter")?.value || "all";
  const status = document.getElementById("teacherStatusFilter")?.value || "all";
  const listEl = document.getElementById("teacherAssignmentList");
  if (!listEl) return;

  const filtered = currentTeacherAssignments.filter(a => {
    if (skill !== "all" && a.skill !== skill) return false;
    if (status !== "all" && a.status !== status) return false;
    return true;
  });

  renderTeacherAssignments(filtered);
};

function renderTeacherAssignments(assignments) {
  const listEl = document.getElementById("teacherAssignmentList");
  if (!listEl) return;

  if (assignments.length === 0) {
    listEl.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--text-muted); font-size:0.85rem;">No assignments match current filter.</div>`;
    return;
  }

  listEl.innerHTML = assignments.map(a => {
    const isSelected = currentActiveAssignment && currentActiveAssignment.assignment_id === a.assignment_id;
    const statusColors = {
      assigned: "rgba(59,130,246,0.15); color:#60a5fa; border:1px solid rgba(59,130,246,0.3);",
      in_review: "rgba(245,158,11,0.15); color:#fbbf24; border:1px solid rgba(245,158,11,0.3);",
      submitted: "rgba(16,185,129,0.15); color:#34d399; border:1px solid rgba(16,185,129,0.3);"
    };

    return `
      <div style="background:var(--bg-card); border:${isSelected ? '2px solid var(--cat-educator-accent)' : '1px solid var(--border-color)'}; border-radius:10px; padding:12px; cursor:pointer; transition:border-color 0.15s;" onclick="selectAssignmentForReview('${a.assignment_id}')">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <span class="nav-badge ${a.skill === 'writing' ? 'badge-exam' : 'badge-advantage'}" style="text-transform:uppercase; font-size:0.7rem;">${a.skill}</span>
          <span style="font-size:0.72rem; padding:2px 8px; border-radius:4px; ${statusColors[a.status] || ''}">${a.status}</span>
        </div>
        <div style="font-size:0.88rem; font-weight:600; color:var(--text-primary); margin-bottom:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${a.prompt_topic || 'Submission ' + a.assignment_id}</div>
        <div style="font-size:0.75rem; color:var(--text-muted); display:flex; justify-content:space-between;">
          <span>Candidate: <strong>${a.learner_id}</strong></span>
          <span>${a.submitted_at ? a.submitted_at.substring(0, 10) : ''}</span>
        </div>
      </div>
    `;
  }).join("");
}

window.selectAssignmentForReview = async function(assignmentId) {
  try {
    const res = await callApi(`/api/teacher/assignment?assignment_id=${encodeURIComponent(assignmentId)}`);
    if (res.error) {
      alert("Error: " + res.error);
      return;
    }
    currentActiveAssignment = res.assignment;
    renderTeacherAssignments(currentTeacherAssignments);
    populateReviewStudio(res.assignment, res.evaluation);
  } catch (err) {
    alert("Failed to load assignment: " + err.message);
  }
};

function populateReviewStudio(assignment, evaluation) {
  const emptyEl = document.getElementById("teacherStudioEmptyState");
  const formEl = document.getElementById("teacherStudioActiveForm");
  if (!emptyEl || !formEl) return;

  emptyEl.style.display = "none";
  formEl.style.display = "block";

  document.getElementById("studioSkillBadge").textContent = assignment.skill.toUpperCase();
  document.getElementById("studioTaskTitle").textContent = assignment.prompt_topic || "Assessment Task";
  document.getElementById("studioCandidateId").textContent = assignment.learner_id;
  document.getElementById("studioSubmissionDate").textContent = assignment.submitted_at || "Recent";
  document.getElementById("studioRevisionBadge").textContent = `v${evaluation ? (evaluation.revision_number || 1) : 1}`;
  document.getElementById("studioPromptContent").textContent = assignment.prompt_topic;
  document.getElementById("studioSubmissionContent").textContent = assignment.submission_text;

  const modalityEl = document.getElementById("studioSpeakingModalitySection");
  if (modalityEl) {
    modalityEl.style.display = assignment.skill === "speaking" ? "block" : "none";
  }

  // Populate Criteria Sliders
  const isWriting = assignment.skill === "writing";
  const criteria = isWriting 
    ? [
        { id: "tr", name: "Task Response / Achievement", desc: "Addresses prompt requirements and develops position" },
        { id: "cc", name: "Coherence & Cohesion", desc: "Logical progression, paragraphing, and cohesive linking" },
        { id: "lr", name: "Lexical Resource", desc: "Range, precision, collocation, and style appropriateness" },
        { id: "gra", name: "Grammatical Range & Accuracy", desc: "Complex structures, sentence variety, and error-free rate" }
      ]
    : [
        { id: "fc", name: "Fluency & Coherence", desc: "Speech flow, continuity, and connective markers" },
        { id: "lr", name: "Lexical Resource", desc: "Idiomatic expressions, precision, and vocabulary range" },
        { id: "gra", name: "Grammatical Range & Accuracy", desc: "Syntactic variety, tense accuracy, and clause structures" },
        { id: "p", name: "Pronunciation", desc: "Intonation, phonological clarity, rhythm, and stress" }
      ];

  const cContainer = document.getElementById("studioCriteriaContainer");
  const existingScores = evaluation ? (evaluation.criteria_scores || {}) : {};

  cContainer.innerHTML = criteria.map(c => {
    const val = existingScores[c.id] || 6.5;
    return `
      <div class="criteria-score-box">
        <div class="criteria-score-header">
          <div>
            <div style="font-weight:600; font-size:0.85rem; color:var(--text-primary);">${c.name}</div>
            <div style="font-size:0.72rem; color:var(--text-muted);">${c.desc}</div>
          </div>
          <div class="criteria-score-val" id="val_${c.id}">${val.toFixed(1)}</div>
        </div>
        <input type="range" class="form-range" id="slider_${c.id}" min="1.0" max="9.0" step="0.5" value="${val}" style="width:100%; cursor:pointer;" oninput="onCriterionSliderChange('${c.id}', this.value)">
      </div>
    `;
  }).join("");

  // Populate Qualitative Fields
  document.getElementById("studioStrengthsInput").value = evaluation?.strengths || "";
  document.getElementById("studioImprovementsInput").value = evaluation?.improvements || "";
  document.getElementById("studioFeedbackInput").value = evaluation?.feedback_text || "";

  updateStudioOverallScore();
}

window.onCriterionSliderChange = function(critId, val) {
  const disp = document.getElementById("val_" + critId);
  if (disp) disp.textContent = parseFloat(val).toFixed(1);
  updateStudioOverallScore();
};

function updateStudioOverallScore() {
  const isWriting = currentActiveAssignment && currentActiveAssignment.skill === "writing";
  const ids = isWriting ? ["tr", "cc", "lr", "gra"] : ["fc", "lr", "gra", "p"];
  
  let total = 0;
  ids.forEach(id => {
    const s = document.getElementById("slider_" + id);
    total += s ? parseFloat(s.value) : 6.5;
  });

  const avg = total / ids.length;
  // IELTS band rounding: round to nearest 0.5 (or .25 rounds up to .5, .75 rounds up to next whole)
  const remainder = avg - Math.floor(avg);
  let rounded = Math.floor(avg);
  if (remainder >= 0.75) rounded += 1.0;
  else if (remainder >= 0.25) rounded += 0.5;

  const overallEl = document.getElementById("studioOverallScoreDisplay");
  if (overallEl) overallEl.textContent = rounded.toFixed(1);
}

function gatherStudioEvaluationData(status) {
  if (!currentActiveAssignment) return null;
  const isWriting = currentActiveAssignment.skill === "writing";
  const ids = isWriting ? ["tr", "cc", "lr", "gra"] : ["fc", "lr", "gra", "p"];
  
  const criteriaScores = {};
  ids.forEach(id => {
    const s = document.getElementById("slider_" + id);
    criteriaScores[id] = s ? parseFloat(s.value) : 6.5;
  });

  const overallEl = document.getElementById("studioOverallScoreDisplay");
  const overallBand = overallEl ? parseFloat(overallEl.textContent) : 6.5;

  return {
    assignment_id: currentActiveAssignment.assignment_id,
    reviewer_id: appState.currentUser?.user_id || "teacher_sarah",
    skill: currentActiveAssignment.skill,
    overall_band: overallBand,
    criteria_scores: criteriaScores,
    strengths: document.getElementById("studioStrengthsInput").value.trim(),
    improvements: document.getElementById("studioImprovementsInput").value.trim(),
    feedback_text: document.getElementById("studioFeedbackInput").value.trim(),
    assessment_mode: document.getElementById("studioAssessmentMode")?.value || "both",
    status: status
  };
}

window.saveTeacherDraft = async function() {
  const data = gatherStudioEvaluationData("draft");
  if (!data) return;

  try {
    const res = await callApi("/api/teacher/review/save", "POST", data);
    if (res.error) {
      alert("Error: " + res.error);
    } else {
      showToastNotification(`Working draft saved (Revision v${res.evaluation.revision_number})`);
      document.getElementById("studioRevisionBadge").textContent = `v${res.evaluation.revision_number}`;
      loadTeacherDashboard();
    }
  } catch (err) {
    alert("Draft save failed: " + err.message);
  }
};

window.submitTeacherEvaluation = async function() {
  const data = gatherStudioEvaluationData("submitted");
  if (!data) return;

  if (!confirm(`Submit official examiner evaluation with Overall Band ${data.overall_band}? This will commit your marks to the candidate record.`)) {
    return;
  }

  try {
    const res = await callApi("/api/teacher/review/submit", "POST", data);
    if (res.error) {
      alert("Error: " + res.error);
    } else {
      showToastNotification(`Evaluation submitted successfully (Overall Band: ${data.overall_band})`);
      loadTeacherDashboard();
    }
  } catch (err) {
    alert("Submission failed: " + err.message);
  }
};

// New Assignment Modal functions
window.openNewAssignmentModal = function() {
  const m = document.getElementById("newAssignmentModal");
  if (m) m.style.display = "flex";
};
window.closeNewAssignmentModal = function() {
  const m = document.getElementById("newAssignmentModal");
  if (m) m.style.display = "none";
};
window.handleCreateAssignment = async function(e) {
  e.preventDefault();
  const payload = {
    skill: document.getElementById("assignSkill").value,
    reviewer_id: document.getElementById("assignReviewerId").value.trim(),
    learner_id: document.getElementById("assignLearnerId").value.trim(),
    prompt_topic: document.getElementById("assignPrompt").value.trim(),
    submission_text: document.getElementById("assignSubmissionText").value.trim()
  };

  try {
    const res = await callApi("/api/teacher/assignment/create", "POST", payload);
    if (res.error) {
      alert("Error: " + res.error);
    } else {
      closeNewAssignmentModal();
      showToastNotification("New review assignment created!");
      loadTeacherDashboard();
    }
  } catch (err) {
    alert("Failed to create assignment: " + err.message);
  }
};

// =========================================================================
// PHASE 16: BLIND DOUBLE-MARKING & RECONCILIATION
// =========================================================================
let currentDoubleMarkPairs = [];
let activeDoubleMarkPair = null;

window.loadDoubleMarkingView = async function() {
  const listEl = document.getElementById("doubleMarkPairsList");
  const countEl = document.getElementById("doubleMarkPairCountBadge");
  if (!listEl) return;

  listEl.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--text-muted); font-size:0.85rem;">Loading paired assignments...</div>`;

  try {
    const res = await callApi("/api/examiner/double_marking");
    if (res.error) {
      listEl.innerHTML = `<div style="padding:1rem; color:var(--warning-color); font-size:0.85rem;">${res.error} (Sign in as Examiner or Admin)</div>`;
      return;
    }
    currentDoubleMarkPairs = res.double_marked_assignments || [];
    if (countEl) countEl.textContent = `${currentDoubleMarkPairs.length} pairs`;
    renderDoubleMarkPairs(currentDoubleMarkPairs);
  } catch (err) {
    listEl.innerHTML = `<div style="padding:1rem; color:var(--danger-color); font-size:0.85rem;">Failed to load double-marking: ${err.message}</div>`;
  }
};

function renderDoubleMarkPairs(pairs) {
  const listEl = document.getElementById("doubleMarkPairsList");
  if (!listEl) return;

  if (pairs.length === 0) {
    listEl.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--text-muted); font-size:0.85rem;">No paired assignments active.</div>`;
    return;
  }

  listEl.innerHTML = pairs.map(p => {
    const isSelected = activeDoubleMarkPair && activeDoubleMarkPair.pair_id === p.pair_id;
    return `
      <div style="background:var(--bg-card); border:${isSelected ? '2px solid var(--cat-educator-accent)' : '1px solid var(--border-color)'}; border-radius:10px; padding:12px; cursor:pointer;" onclick="selectDoubleMarkPair('${p.pair_id}')">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
          <span class="nav-badge badge-educator">Pair #${p.pair_id.substring(0,8)}</span>
          <span style="font-size:0.75rem; color:${p.disagreement_detected ? 'var(--danger-color)' : 'var(--success-color)'}; font-weight:700;">
            ${p.disagreement_detected ? '⚠️ Divergence >0.5' : (p.is_reconciled ? '✅ Reconciled' : 'In Review')}
          </span>
        </div>
        <div style="font-size:0.85rem; font-weight:600; color:var(--text-primary); margin-bottom:2px;">Submission ${p.submission_id}</div>
        <div style="font-size:0.75rem; color:var(--text-muted);">
          Examiners: ${p.reviewer_1_id} &amp; ${p.reviewer_2_id}
        </div>
      </div>
    `;
  }).join("");
}

window.selectDoubleMarkPair = function(pairId) {
  const pair = currentDoubleMarkPairs.find(p => p.pair_id === pairId);
  if (!pair) return;

  activeDoubleMarkPair = pair;
  renderDoubleMarkPairs(currentDoubleMarkPairs);

  const emptyEl = document.getElementById("doubleMarkEmptyState");
  const wsEl = document.getElementById("doubleMarkActiveWorkspace");
  emptyEl.style.display = "none";
  wsEl.style.display = "block";

  document.getElementById("dmSkillBadge").textContent = (pair.skill || "Writing").toUpperCase();
  document.getElementById("dmSubmissionTitle").textContent = `Submission #${pair.submission_id}`;
  document.getElementById("dmPairIdBadge").textContent = pair.pair_id;

  const gateBadge = document.getElementById("dmGateStatusBadge");
  const blindAlert = document.getElementById("dmBlindProtectionAlert");

  if (pair.evaluations_count < 2) {
    gateBadge.textContent = "BLIND MARKING ACTIVE";
    gateBadge.style.background = "rgba(245,158,11,0.15)";
    gateBadge.style.color = "var(--warning-color)";
    blindAlert.style.display = "block";
  } else {
    gateBadge.textContent = pair.disagreement_detected ? "RECONCILIATION REQUIRED" : "CONSENSUS ALIGNED";
    gateBadge.style.background = pair.disagreement_detected ? "rgba(239,68,68,0.15)" : "rgba(16,185,129,0.15)";
    gateBadge.style.color = pair.disagreement_detected ? "var(--danger-color)" : "var(--success-color)";
    blindAlert.style.display = "none";
  }

  // Render Disagreement Matrix
  const tbody = document.getElementById("dmMatrixTableBody");
  const matrix = pair.disagreement_matrix || {};
  const criteriaKeys = Object.keys(matrix);

  if (criteriaKeys.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:1.5rem; color:var(--text-muted);">Awaiting second examiner submission to unlock matrix.</td></tr>`;
  } else {
    tbody.innerHTML = criteriaKeys.map(key => {
      const row = matrix[key];
      const diff = row.difference || 0;
      const isAlert = diff > 0.5;
      return `
        <tr>
          <td><strong>${key.toUpperCase()}</strong></td>
          <td>${row.reviewer_1_score !== undefined ? row.reviewer_1_score.toFixed(1) : '--'}</td>
          <td>${row.reviewer_2_score !== undefined ? row.reviewer_2_score.toFixed(1) : '--'}</td>
          <td><span class="${isAlert ? 'diff-alert' : 'diff-ok'}">${diff.toFixed(1)}</span></td>
          <td>${isAlert ? '<span style="color:var(--danger-color); font-weight:700;">Exceeds ±0.5 Band</span>' : '<span style="color:var(--success-color);">Within Tolerance</span>'}</td>
        </tr>
      `;
    }).join("");
  }
};

window.submitSeniorReconciliation = async function() {
  if (!activeDoubleMarkPair) return;
  const band = parseFloat(document.getElementById("dmReconciledBandSelect").value);
  const notes = document.getElementById("dmReconciliationNotesInput").value.trim();

  if (!notes) {
    alert("Please provide reconciliation rationale & audit commentary explaining the final consensus determination.");
    return;
  }

  const payload = {
    pair_id: activeDoubleMarkPair.pair_id,
    senior_examiner_id: appState.currentUser?.user_id || "examiner_clara",
    reconciled_overall_band: band,
    reconciliation_notes: notes
  };

  try {
    const res = await callApi("/api/examiner/reconcile", "POST", payload);
    if (res.error) {
      alert("Error: " + res.error);
    } else {
      showToastNotification(`Consensus Band ${band} committed. Both examiner records preserved in audit ledger.`);
      loadDoubleMarkingView();
    }
  } catch (err) {
    alert("Reconciliation failed: " + err.message);
  }
};

// =========================================================================
// PHASE 16: SUPERVISED BETA PILOT & ASSESSMENT CALIBRATION
// =========================================================================
window.loadBetaManagement = async function() {
  loadCalibrationMetrics();
  loadBetaCohorts();
};

async function loadCalibrationMetrics() {
  try {
    const res = await callApi("/api/benchmark/calibration");
    const badge = document.getElementById("calibrationStateBadge");
    const nEl = document.getElementById("calibMetricN");
    const maeEl = document.getElementById("calibMetricMae");
    const biasEl = document.getElementById("calibMetricBias");
    const agree05El = document.getElementById("calibMetricAgreement05");
    const agree10El = document.getElementById("calibMetricAgreement10");

    if (res.status === "pending_human_calibration" || res.valid_samples === 0) {
      if (badge) badge.textContent = "PENDING HUMAN CALIBRATION";
      if (nEl) nEl.textContent = "0";
      if (maeEl) maeEl.textContent = "N=0";
      if (biasEl) biasEl.textContent = "N=0";
      if (agree05El) agree05El.textContent = "N=0";
      if (agree10El) agree10El.textContent = "N=0";
    } else {
      if (badge) {
        badge.textContent = "CALIBRATION ACTIVE";
        badge.style.background = "rgba(16,185,129,0.15)";
        badge.style.color = "var(--success-color)";
      }
      if (nEl) nEl.textContent = res.valid_samples;
      if (maeEl) maeEl.textContent = (res.mae !== undefined ? res.mae.toFixed(2) : "--");
      if (biasEl) biasEl.textContent = (res.mean_bias !== undefined ? (res.mean_bias > 0 ? "+" : "") + res.mean_bias.toFixed(2) : "--");
      if (agree05El) agree05El.textContent = (res.within_0_5_band_rate !== undefined ? (res.within_0_5_band_rate * 100).toFixed(1) + "%" : "--");
      if (agree10El) agree10El.textContent = (res.within_1_0_band_rate !== undefined ? (res.within_1_0_band_rate * 100).toFixed(1) + "%" : "--");
    }
  } catch (err) {
    console.warn("Failed to load calibration metrics:", err);
  }
}

async function loadBetaCohorts() {
  const container = document.getElementById("betaCohortsContainer");
  if (!container) return;

  try {
    const res = await callApi("/api/beta/cohorts");
    const cohorts = res.cohorts || [];

    container.innerHTML = cohorts.map(c => `
      <div class="beta-cohort-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span class="nav-badge badge-educator" style="font-size:0.72rem;">${c.cohort_type.toUpperCase()}</span>
          <span style="font-size:0.75rem; color:var(--text-muted);">${c.status}</span>
        </div>
        <h4 style="margin:0 0 4px 0; font-size:1.05rem; color:var(--text-primary);">${c.name}</h4>
        <div style="font-size:0.8rem; color:var(--text-secondary); margin-bottom:12px;">Target Band: <strong>${c.target_band_min} – ${c.target_band_max}</strong></div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.82rem; border-top:1px solid var(--border-color); padding-top:8px;">
          <span>Enrolled: <strong>${c.enrolled_count || 0} / ${c.target_capacity}</strong></span>
          <span style="font-size:0.75rem; color:var(--primary-accent);">${Math.round(((c.enrolled_count || 0) / c.target_capacity) * 100)}% Cap</span>
        </div>
      </div>
    `).join("");
  } catch (err) {
    container.innerHTML = `<div style="color:var(--danger-color); padding:1rem;">Failed to load cohorts: ${err.message}</div>`;
  }
}

// Enroll Participant Modal
window.openEnrollParticipantModal = function() {
  const m = document.getElementById("enrollParticipantModal");
  if (m) m.style.display = "flex";
};
window.closeEnrollParticipantModal = function() {
  const m = document.getElementById("enrollParticipantModal");
  if (m) m.style.display = "none";
};
window.handleEnrollParticipant = async function(e) {
  e.preventDefault();
  const consent = document.getElementById("enrollConsentCheckbox").checked;
  if (!consent) {
    alert("Mandatory informed consent must be provided to enroll in the supervised pilot.");
    return;
  }

  const payload = {
    cohort_id: document.getElementById("enrollCohortSelect").value,
    user_id: document.getElementById("enrollUserId").value.trim(),
    target_band: parseFloat(document.getElementById("enrollTargetBand").value),
    informed_consent: true
  };

  try {
    const res = await callApi("/api/beta/participants/enroll", "POST", payload);
    if (res.error) {
      alert("Error: " + res.error);
    } else {
      closeEnrollParticipantModal();
      showToastNotification(`Participant ${payload.user_id} enrolled in cohort!`);
      loadBetaCohorts();
    }
  } catch (err) {
    alert("Enrollment failed: " + err.message);
  }
};

window.handleBetaFeedbackSubmit = async function(e) {
  e.preventDefault();
  const payload = {
    participant_id: document.getElementById("feedbackParticipantId").value.trim(),
    category: document.getElementById("feedbackCategory").value,
    rating: parseInt(document.getElementById("feedbackRating").value, 10),
    comments: document.getElementById("feedbackText").value.trim()
  };

  try {
    const res = await callApi("/api/beta/feedback", "POST", payload);
    if (res.error) {
      alert("Error: " + res.error);
    } else {
      showToastNotification("Thank you! Pilot feedback recorded.");
      document.getElementById("feedbackText").value = "";
    }
  } catch (err) {
    alert("Feedback submission failed: " + err.message);
  }
};

window.handleBetaBugSubmit = async function(e) {
  e.preventDefault();
  const payload = {
    reporter_id: document.getElementById("bugReporterId").value.trim(),
    severity: document.getElementById("bugSeverity").value,
    title: document.getElementById("bugTitle").value.trim(),
    description: document.getElementById("bugDescription").value.trim()
  };

  try {
    const res = await callApi("/api/beta/bugs", "POST", payload);
    if (res.error) {
      alert("Error: " + res.error);
    } else {
      showToastNotification(`Bug report logged (${payload.severity.toUpperCase()}): #${res.bug_id}`);
      document.getElementById("bugTitle").value = "";
      document.getElementById("bugDescription").value = "";
    }
  } catch (err) {
    alert("Bug logging failed: " + err.message);
  }
};

// Initial setup on document load
document.addEventListener("DOMContentLoaded", () => {
  verifyActiveSession();
});

