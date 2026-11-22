/**
 * Roleplay & Cultural Scenarios Manager for Ahlan AI
 */

class RoleplayManager {
  constructor() {
    this.scenarios = [];
    this.activeScenario = null;
    this.scenarioListContainer = document.getElementById('scenarios-grid');
    this.roleplayActiveView = document.getElementById('roleplay-active-view');
    this.roleplaySelectionView = document.getElementById('roleplay-selection-view');
    this.rpMessagesContainer = document.getElementById('rp-messages');
    this.rpInput = document.getElementById('rp-input');
    this.rpSendBtn = document.getElementById('rp-send-btn');
    this.rpMicBtn = document.getElementById('rp-mic-btn');
    this.rpExitBtn = document.getElementById('rp-exit-btn');
    this.rpObjectivesContainer = document.getElementById('rp-objectives');
    this.rpHintsContainer = document.getElementById('rp-starter-hints');
    this.conversationId = null;

    this.init();
  }

  async init() {
    if (this.rpSendBtn) {
      this.rpSendBtn.addEventListener('click', () => this.sendRpMessage());
    }

    if (this.rpInput) {
      this.rpInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendRpMessage();
        }
      });
    }

    if (this.rpMicBtn) {
      this.rpMicBtn.addEventListener('click', () => this.toggleRpVoice());
    }

    if (this.rpExitBtn) {
      this.rpExitBtn.addEventListener('click', () => this.exitScenario());
    }

    await this.loadScenarios();
  }

  async loadScenarios() {
    try {
      const data = await API.getScenarios();
      this.scenarios = data.scenarios || [];
      this.renderScenariosGrid();
    } catch (e) {
      console.error('Error loading scenarios:', e);
    }
  }

  renderScenariosGrid() {
    if (!this.scenarioListContainer) return;
    this.scenarioListContainer.innerHTML = '';

    this.scenarios.forEach(sc => {
      const card = document.createElement('div');
      card.className = 'glass-panel hover:border-emerald-500 rounded-2xl p-5 shadow-md hover:shadow-xl transition transform hover:-translate-y-1 cursor-pointer flex flex-col justify-between border border-slate-200/80';
      card.innerHTML = `
        <div>
          <div class="flex items-center justify-between mb-3">
            <span class="text-3xl p-2.5 bg-emerald-50 rounded-2xl border border-emerald-100">${sc.icon}</span>
            <span class="text-xs font-bold px-2.5 py-1 rounded-full bg-amber-100/80 text-amber-900 border border-amber-200">${sc.level}</span>
          </div>
          <h3 class="font-bold text-slate-900 text-lg font-arabic mb-0.5" dir="rtl">${sc.title_ar}</h3>
          <h4 class="font-semibold text-emerald-800 text-sm mb-2">${sc.title_en}</h4>
          <div class="text-xs text-slate-500 mb-2.5 flex items-center gap-1 font-medium">
            <span>📍 Location:</span> <span>${sc.location}</span>
          </div>
          <p class="text-xs text-slate-600 leading-relaxed mb-4">${sc.description}</p>
        </div>
        <button class="w-full bg-emerald-800 hover:bg-emerald-700 text-white font-semibold py-2 px-4 rounded-xl text-xs transition shadow flex items-center justify-center gap-1.5">
          <span>Start Roleplay Scenario</span> <span>➔</span>
        </button>
      `;
      card.addEventListener('click', () => this.startScenario(sc));
      this.scenarioListContainer.appendChild(card);
    });
  }

  startScenario(scenario) {
    this.activeScenario = JSON.parse(JSON.stringify(scenario)); // clone
    this.conversationId = `scenario_${scenario.id}_${Date.now()}`;

    // Switch views
    if (this.roleplaySelectionView) this.roleplaySelectionView.classList.add('hidden');
    if (this.roleplayActiveView) this.roleplayActiveView.classList.remove('hidden');

    // Set Header
    document.getElementById('rp-title').textContent = `${scenario.icon} ${scenario.title_en} (${scenario.title_ar})`;
    document.getElementById('rp-location').textContent = `📍 ${scenario.location} • Level: ${scenario.level}`;

    // Render Objectives
    this.renderObjectives();

    // Render Hints
    this.renderHints();

    // Clear and Add Initial Tutor Message
    if (this.rpMessagesContainer) {
      this.rpMessagesContainer.innerHTML = '';
      this.addRpTutorMessage({
        reply_arabic: scenario.initial_tutor_message,
        reply_transliteration: scenario.initial_transliteration,
        reply_english: scenario.initial_translation
      });
    }
  }

  exitScenario() {
    this.activeScenario = null;
    if (this.roleplayActiveView) this.roleplayActiveView.classList.add('hidden');
    if (this.roleplaySelectionView) this.roleplaySelectionView.classList.remove('hidden');
  }

  renderObjectives() {
    if (!this.rpObjectivesContainer || !this.activeScenario) return;
    this.rpObjectivesContainer.innerHTML = '';

    this.activeScenario.objectives.forEach(obj => {
      const item = document.createElement('div');
      item.className = `p-2.5 rounded-xl border text-xs flex items-start gap-2 transition ${obj.completed ? 'bg-emerald-50 border-emerald-300 text-emerald-900' : 'bg-white/80 border-slate-200 text-slate-700'}`;
      item.innerHTML = `
        <span class="text-sm flex-shrink-0">${obj.completed ? '✅' : '⭕'}</span>
        <div>
          <div class="font-bold ${obj.completed ? 'line-through text-emerald-800' : 'text-slate-900'}">${obj.text_en}</div>
          <div class="font-arabic text-[11px] text-slate-500 mt-0.5" dir="rtl">${obj.text_ar}</div>
        </div>
      `;
      this.rpObjectivesContainer.appendChild(item);
    });
  }

  renderHints() {
    if (!this.rpHintsContainer || !this.activeScenario) return;
    this.rpHintsContainer.innerHTML = '';

    this.activeScenario.starter_hints.forEach(hint => {
      const btn = document.createElement('button');
      btn.className = 'text-left bg-white/90 hover:bg-amber-50 border border-amber-200/80 rounded-xl p-2 text-xs shadow-sm transition';
      btn.innerHTML = `
        <div class="font-arabic font-bold text-amber-950 text-sm" dir="rtl">${hint.arabic}</div>
        <div class="text-slate-500 font-mono text-[10px]">${hint.translit}</div>
        <div class="text-slate-600 text-[11px]">${hint.english}</div>
      `;
      btn.addEventListener('click', () => {
        this.sendRpMessage(hint.arabic);
      });
      this.rpHintsContainer.appendChild(btn);
    });
  }

  toggleRpVoice() {
    if (window.audioController.isRecording) {
      window.audioController.stopListening();
    } else {
      this.rpMicBtn.classList.add('bg-rose-500', 'text-white', 'animate-pulse');
      window.audioController.startListening(
        (transcript, isFinal) => {
          if (this.rpInput) {
            this.rpInput.value = transcript;
            if (isFinal) {
              this.rpMicBtn.classList.remove('bg-rose-500', 'text-white', 'animate-pulse');
              setTimeout(() => this.sendRpMessage(), 600);
            }
          }
        },
        (isRecording) => {
          if (!isRecording) {
            this.rpMicBtn.classList.remove('bg-rose-500', 'text-white', 'animate-pulse');
          }
        }
      );
    }
  }

  async sendRpMessage(customText = null) {
    const text = (customText || (this.rpInput ? this.rpInput.value : '')).trim();
    if (!text || !this.activeScenario) return;

    if (this.rpInput) this.rpInput.value = '';

    // Render User Message
    this.addRpUserMessage(text);

    // Evaluate Objectives Completed
    this.checkObjectivesProgress(text);

    try {
      const apiKey = localStorage.getItem('ahlan_gemini_key') || '';
      const response = await API.sendChatMessage({
        message: text,
        conversation_id: this.conversationId,
        level: this.activeScenario.level.split('-')[0] || 'A1',
        mode: 'roleplay',
        scenario_id: this.activeScenario.id,
        api_key: apiKey
      });

      this.addRpTutorMessage(response);

      if (localStorage.getItem('ahlan_auto_audio') === 'true') {
        window.audioController.speak(response.reply_arabic);
      }

    } catch (e) {
      console.error(e);
    }
  }

  checkObjectivesProgress(userText) {
    if (!this.activeScenario) return;
    const txt = userText.toLowerCase();

    this.activeScenario.objectives.forEach(obj => {
      if (!obj.completed) {
        if (obj.id.includes('greet') && (txt.includes('marhaba') || txt.includes('مرحبا') || txt.includes('يعطيك') || txt.includes('bonjour') || txt.includes('اهلين'))) {
          obj.completed = true;
        } else if (obj.id.includes('order_drink') && (txt.includes('قهوة') || txt.includes('ahwe') || txt.includes('شاي') || txt.includes('بدي') || txt.includes('وسط') || txt.includes('سكر'))) {
          obj.completed = true;
        } else if (obj.id.includes('order_food') && (txt.includes('منقوشة') || txt.includes('زعتر') || txt.includes('جبنة') || txt.includes('manousheh'))) {
          obj.completed = true;
        } else if (obj.id.includes('ask_bill') && (txt.includes('حساب') || txt.includes('قديش') || txt.includes('hseib') || txt.includes('addeish') || txt.includes('يسلمو'))) {
          obj.completed = true;
        } else if (obj.id.includes('destination') && (txt.includes('حمرا') || txt.includes('hamra') || txt.includes('شارع') || txt.includes('رايح'))) {
          obj.completed = true;
        } else if (obj.id.includes('stop') && (txt.includes('يمين') || txt.includes('هون') || txt.includes('hon') || txt.includes('نزّلني'))) {
          obj.completed = true;
        } else if (obj.id.includes('inquire') && (txt.includes('قديش') || txt.includes('سعر') || txt.includes('حقه') || txt.includes('addeish'))) {
          obj.completed = true;
        } else if (obj.id.includes('bargain') && (txt.includes('غالي') || txt.includes('كرمالي') || txt.includes('راعينا') || txt.includes('kermeli'))) {
          obj.completed = true;
        } else if (obj.id.includes('praise_food') && (txt.includes('طيبة') || txt.includes('بتعقد') || txt.includes('يسلمو') || txt.includes('صحتين'))) {
          obj.completed = true;
        } else if (obj.id.includes('end_meal') && (txt.includes('دايمة') || txt.includes('deyme') || txt.includes('شبعت'))) {
          obj.completed = true;
        }
      }
    });

    this.renderObjectives();
  }

  addRpUserMessage(text) {
    const bubble = document.createElement('div');
    bubble.className = 'flex flex-col items-end mb-4 animate-fade-slide';
    bubble.innerHTML = `
      <div class="bg-gradient-to-r from-amber-500 to-amber-600 text-white px-4 py-2.5 rounded-2xl rounded-tr-none shadow font-arabic text-base max-w-[85%] text-right">
        ${text}
      </div>
    `;
    this.rpMessagesContainer.appendChild(bubble);
    this.rpMessagesContainer.scrollTop = this.rpMessagesContainer.scrollHeight;
  }

  addRpTutorMessage(data) {
    const bubble = document.createElement('div');
    bubble.className = 'flex flex-col items-start mb-4 animate-fade-slide';
    bubble.innerHTML = `
      <div class="glass-panel border border-emerald-100 rounded-2xl rounded-tl-none p-3.5 shadow-sm max-w-[90%] w-full">
        <div class="flex items-start justify-between gap-2 mb-1.5">
          <div class="font-arabic text-lg font-bold text-slate-900 leading-relaxed text-right flex-grow" dir="rtl">
            ${data.reply_arabic}
          </div>
          <button class="audio-btn p-1.5 rounded-full hover:bg-emerald-50 text-emerald-800 transition" title="Listen">
            🔊
          </button>
        </div>
        <div class="text-amber-800 font-mono text-xs bg-amber-50/70 rounded px-2 py-1 mb-1">
          ${data.reply_transliteration || ''}
        </div>
        <div class="text-slate-600 text-xs border-t border-slate-100 pt-1">
          ${data.reply_english || ''}
        </div>
      </div>
    `;

    const audioBtn = bubble.querySelector('.audio-btn');
    if (audioBtn) {
      audioBtn.addEventListener('click', () => {
        window.audioController.speak(data.reply_arabic);
      });
    }

    this.rpMessagesContainer.appendChild(bubble);
    this.rpMessagesContainer.scrollTop = this.rpMessagesContainer.scrollHeight;
  }
}

window.roleplayManager = null;
