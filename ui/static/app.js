/**
 * IELTS by GAMA - Frontend Client Application
 * Hybrid Online + Offline AI English Tutor
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

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
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

  // Status check poll
  checkStatus();
  setInterval(checkStatus, 8000);
});

// 1. Navigation
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

    // Refresh specific pane content if needed
    if (tabId === "dashboard") loadDashboard();
    if (tabId === "vocab") loadSRSDeck();
    if (tabId === "mistakes") loadMistakes();
  }
}

// 2. Status & Offline Toggle
async function checkStatus() {
  try {
    const res = await fetch(`${API_BASE}/api/status`);
    if (res.ok) {
      const data = await res.json();
      updateStatusBadge(data.connectivity, data.forced_offline);
      document.getElementById("deviceProfileLabel").innerText = data.hardware_profile;
      document.getElementById("modelNameLabel").innerText = data.model_name;
    }
  } catch (err) {
    updateStatusBadge("● OFFLINE", true);
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
    try {
      const res = await fetch(`${API_BASE}/api/settings/offline_toggle`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ forced_offline: nextState })
      });
      if (res.ok) {
        const data = await res.json();
        updateStatusBadge(data.status, data.forced_offline);
      }
    } catch (e) {
      console.error(e);
    }
  });
}

function initThemeToggle() {
  const btn = document.getElementById("themeToggleBtn");
  btn.addEventListener("click", () => {
    document.body.classList.toggle("light-theme");
  });
}

// 3. Dashboard
async function initDashboard() {
  await loadDashboard();
}

async function loadDashboard() {
  try {
    const res = await fetch(`${API_BASE}/api/dashboard`);
    if (res.ok) {
      const data = await res.json();
      const d = data.dashboard;
      const p = data.daily_plan;

      document.getElementById("dailyGreetingText").innerText = p.daily_greeting;
      document.getElementById("currentBandMetric").innerText = d.overall_band_estimate;
      document.getElementById("targetBandMetric").innerText = d.target_band;
      document.getElementById("cefrMetric").innerText = `CEFR Level: ${d.cefr_level}`;
      document.getElementById("srsDueMetric").innerText = d.srs_metrics.items_due_today;
      document.getElementById("activeMistakesMetric").innerText = d.mistake_book_metrics.active_mistakes_count;
      document.getElementById("accuracyRateMetric").innerText = `Accuracy: ${d.mistake_book_metrics.accuracy_rate_percent}%`;

      // Render tasks
      const taskList = document.getElementById("dailyPlanTasksList");
      taskList.innerHTML = "";
      p.tasks.forEach(t => {
        const div = document.createElement("div");
        div.className = "task-item";
        div.innerHTML = `<strong>${t.title} (${t.duration_minutes}m)</strong><p>${t.description}</p>`;
        taskList.appendChild(div);
      });

      // Render radar bars
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
  } catch (err) {
    console.error(err);
  }
}

// 4. AI Tutor Chat
function initChat() {
  const input = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendMessageBtn");
  const voiceBtn = document.getElementById("voiceInputBtn");

  sendBtn.addEventListener("click", sendChatMessage);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendChatMessage();
  });

  // Speech Recognition hook for voice input
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

    recognizer.onerror = () => {
      voiceBtn.innerText = "🎙️";
    };
    recognizer.onend = () => {
      voiceBtn.innerText = "🎙️";
    };
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

  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    if (res.ok) {
      const data = await res.json();
      appendChatMessage("tutor", data.reply, data.detected_mistakes);
      speakText(data.reply.slice(0, 140)); // Pronounce initial sentence via Web Speech
    }
  } catch (err) {
    appendChatMessage("tutor", "Offline engine ready. What grammar or IELTS concept would you like to explore?");
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
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.lang = "en-GB";
    window.speechSynthesis.speak(utterance);
  }
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// 5. Diagnostic
async function initDiagnostic() {
  try {
    const res = await fetch(`${API_BASE}/api/diagnostic/questions`);
    if (res.ok) {
      const data = await res.json();
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
  } catch (err) {
    console.error(err);
  }

  document.getElementById("submitDiagnosticBtn").addEventListener("click", async () => {
    const answers = {};
    document.querySelectorAll("input[name^='diag_']:checked").forEach(input => {
      const qid = input.name.replace("diag_", "");
      answers[qid] = input.value;
    });

    const res = await fetch(`${API_BASE}/api/diagnostic/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers })
    });
    if (res.ok) {
      const report = await res.json();
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

// 6. Adaptive Grammar
async function initGrammar() {
  try {
    const res = await fetch(`${API_BASE}/api/grammar/adaptive`);
    if (res.ok) {
      const data = await res.json();
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
  } catch (err) {
    console.error(err);
  }
}

// 7. Vocabulary & SRS
async function initVocabSRS() {
  document.getElementById("revealCardBtn").addEventListener("click", () => {
    document.getElementById("cardAnswerBox").style.display = "block";
    document.getElementById("revealCardBtn").style.display = "none";
  });
  await loadSRSDeck();
}

async function loadSRSDeck() {
  try {
    const res = await fetch(`${API_BASE}/api/srs/due`);
    if (res.ok) {
      const data = await res.json();
      appState.srsDeck = data.items || [];
      appState.currentCardIdx = 0;
      showCurrentCard();
    }
  } catch (err) {
    console.error(err);
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
  try {
    await fetch(`${API_BASE}/api/srs/review`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ item_id: card.id, grade })
    });
    appState.currentCardIdx++;
    showCurrentCard();
    loadDashboard();
  } catch (err) {
    console.error(err);
  }
};

// 8. Reading
async function initReading() {
  try {
    const res = await fetch(`${API_BASE}/api/reading`);
    if (res.ok) {
      const passage = await res.json();
      document.getElementById("readingTitle").innerText = `${passage.title} (${passage.track})`;
      document.getElementById("readingText").innerText = passage.text;

      const qList = document.getElementById("readingQuestionsList");
      qList.innerHTML = "";
      passage.questions.forEach(q => {
        const div = document.createElement("div");
        div.className = "mb-2";
        div.innerHTML = `
          <p><strong>Q${q.num} [${q.type}]:</strong> ${q.prompt}</p>
          <input type="text" id="read_ans_${q.num}" class="mt-1" style="width: 100%;" placeholder="Enter answer..." />
        `;
        qList.appendChild(div);
      });
    }
  } catch (err) {
    console.error(err);
  }

  document.getElementById("submitReadingBtn").addEventListener("click", async () => {
    const answers = {};
    document.querySelectorAll("input[id^='read_ans_']").forEach(input => {
      const num = input.id.replace("read_ans_", "");
      answers[num] = input.value;
    });

    const res = await fetch(`${API_BASE}/api/reading/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers })
    });
    if (res.ok) {
      const rep = await res.json();
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

// 9. Listening
async function initListening() {
  let audioScript = "";
  try {
    const res = await fetch(`${API_BASE}/api/listening`);
    if (res.ok) {
      const sec = await res.json();
      document.getElementById("listeningTitle").innerText = `Section ${sec.section_number}: ${sec.title}`;
      audioScript = sec.audio_script || "";
      document.getElementById("listeningTranscriptBox").innerText = audioScript;

      const qList = document.getElementById("listeningQuestionsList");
      qList.innerHTML = "";
      sec.questions.forEach(q => {
        const div = document.createElement("div");
        div.className = "mb-2";
        div.innerHTML = `
          <p><strong>Q${q.num}:</strong> ${q.prompt}</p>
          <input type="text" id="list_ans_${q.num}" class="mt-1" style="width: 100%;" placeholder="Enter answer..." />
        `;
        qList.appendChild(div);
      });
    }
  } catch (err) {
    console.error(err);
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

    const res = await fetch(`${API_BASE}/api/listening/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers })
    });
    if (res.ok) {
      const rep = await res.json();
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

// 10. Writing
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

    const res = await fetch(`${API_BASE}/api/writing/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt_id: "acad_t2_stem", essay_text: text })
    });
    if (res.ok) {
      const rep = await res.json();
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

// 11. Speaking
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

    const res = await fetch(`${API_BASE}/api/speaking/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript, duration_seconds: duration })
    });
    if (res.ok) {
      const rep = await res.json();
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

// 12. Mistake Book
async function initMistakeBook() {
  await loadMistakes();
}

async function loadMistakes() {
  try {
    const res = await fetch(`${API_BASE}/api/mistakes`);
    if (res.ok) {
      const data = await res.json();
      const sumBox = document.getElementById("mistakeBookSummary");
      const listEl = document.getElementById("mistakeBookList");

      sumBox.innerHTML = `
        <p>Active error categories: <strong>${data.summary.categories.length}</strong></p>
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
  } catch (err) {
    console.error(err);
  }
}

window.resolveMistake = async function(id) {
  await fetch(`${API_BASE}/api/mistakes/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mistake_id: id, success: true })
  });
  loadMistakes();
  loadDashboard();
};

// 13. Settings & Export/Import
function initSettings() {
  const forcedOff = document.getElementById("settingForcedOffline");
  forcedOff.addEventListener("change", async () => {
    await fetch(`${API_BASE}/api/settings/offline_toggle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ forced_offline: forcedOff.checked })
    });
    checkStatus();
  });

  const exportBtn = document.getElementById("exportDataBtn");
  const importBtn = document.getElementById("importDataBtn");
  const transferArea = document.getElementById("dataTransferArea");

  exportBtn.addEventListener("click", async () => {
    const res = await fetch(`${API_BASE}/api/export`, { method: "POST" });
    if (res.ok) {
      const data = await res.json();
      transferArea.value = data.data;
    }
  });

  importBtn.addEventListener("click", async () => {
    const raw = transferArea.value.trim();
    if (!raw) return;
    const res = await fetch(`${API_BASE}/api/import`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: raw })
    });
    if (res.ok) {
      const rep = await res.json();
      alert(`Imported successfully! Restored ${rep.restored_mistakes} mistakes.`);
      loadDashboard();
      loadMistakes();
    }
  });
}
