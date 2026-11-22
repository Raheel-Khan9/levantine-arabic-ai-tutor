/**
 * Ahlan AI - Main Application Controller
 * Clean Voice-First Interaction with Layla (Lebanese Arabic Voice Tutor)
 */

class AhlanVoiceApp {
  constructor() {
    this.conversationId = 'conv_' + Date.now();
    this.currentLevel = localStorage.getItem('ahlan_level') || 'A1';
    this.currentScenario = 'free_chat';
    this.showArabizi = true;
    this.showEnglish = true;
    this.isProcessing = false;
    this.recordingInterval = null;

    // DOM Elements
    this.dialogueStream = document.getElementById('voice-dialogue-stream');
    this.mainVoiceBtn = document.getElementById('main-voice-btn');
    this.voiceBtnLabel = document.getElementById('voice-btn-label');
    this.recordingIndicator = document.getElementById('recording-indicator');
    this.recordingTimer = document.getElementById('recording-timer');
    this.transcriptPreviewBox = document.getElementById('transcript-preview-box');
    this.transcriptPreviewText = document.getElementById('transcript-preview-text');
    this.tutorAvatarOrb = document.getElementById('tutor-avatar-orb');
    this.statusText = document.getElementById('status-text');
    this.tutorStatusBadge = document.getElementById('tutor-status-badge');
    this.suggestedPrompts = document.getElementById('suggested-prompts');
    this.levelSelector = document.getElementById('level-selector');
    this.keyboardDrawer = document.getElementById('text-input-drawer');
    this.keyboardInput = document.getElementById('keyboard-input');
    this.keyboardSendBtn = document.getElementById('keyboard-send-btn');
    this.toggleKeyboardBtn = document.getElementById('toggle-keyboard-btn');

    this.init();
  }

  init() {
    // Level Selector
    if (this.levelSelector) {
      this.levelSelector.value = this.currentLevel;
      this.levelSelector.addEventListener('change', (e) => {
        this.currentLevel = e.target.value;
        localStorage.setItem('ahlan_level', this.currentLevel);
        this.sendTutorGreeting();
      });
    }

    // Scenario Buttons
    document.querySelectorAll('.scenario-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.scenario-btn').forEach(b => {
          b.classList.remove('active-scenario', 'bg-emerald-700', 'text-white');
          b.classList.add('bg-slate-800', 'text-slate-300');
        });
        const target = e.currentTarget;
        target.classList.add('active-scenario', 'bg-emerald-700', 'text-white');
        target.classList.remove('bg-slate-800', 'text-slate-300');

        this.currentScenario = target.dataset.scenario;
        this.sendTutorGreeting();
      });
    });

    // Main Voice Recording Button (Start / Stop)
    if (this.mainVoiceBtn) {
      this.mainVoiceBtn.addEventListener('click', () => this.handleVoiceButtonClick());
    }

    // Keyboard Input Toggle & Submit
    if (this.toggleKeyboardBtn) {
      this.toggleKeyboardBtn.addEventListener('click', () => {
        this.keyboardDrawer.classList.toggle('hidden');
        if (!this.keyboardDrawer.classList.contains('hidden')) {
          this.keyboardInput.focus();
        }
      });
    }

    if (this.keyboardSendBtn) {
      this.keyboardSendBtn.addEventListener('click', () => this.handleKeyboardSend());
    }

    if (this.keyboardInput) {
      this.keyboardInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.handleKeyboardSend();
        }
      });
    }

    // Settings Modal
    this.initSettingsModal();

    // Quick Level Placement Test Modal
    this.initLevelTestModal();

    // Playback state hook on AudioController
    window.audioController.onPlaybackStateChange = (isPlaying) => {
      this.updateTutorSpeakingState(isPlaying);
    };

    // Send initial warm Lebanese greeting
    this.sendTutorGreeting();
  }

  updateTutorSpeakingState(isSpeaking) {
    if (isSpeaking) {
      this.tutorAvatarOrb.classList.add('ring-8', 'ring-emerald-500/40', 'scale-105');
      this.statusText.textContent = 'Layla is speaking in Lebanese...';
      this.tutorStatusBadge.className = 'mt-2 text-xs font-semibold text-emerald-300 bg-emerald-950 border border-emerald-500/60 px-3 py-1 rounded-full flex items-center gap-1.5 shadow-lg animate-pulse';
    } else {
      this.tutorAvatarOrb.classList.remove('ring-8', 'ring-emerald-500/40', 'scale-105');
      this.statusText.textContent = 'Layla is ready to listen';
      this.tutorStatusBadge.className = 'mt-2 text-xs font-semibold text-emerald-400 bg-emerald-950/80 border border-emerald-800/60 px-3 py-1 rounded-full flex items-center gap-1.5 shadow-sm';
    }
  }

  async handleVoiceButtonClick() {
    if (this.isProcessing) return;

    if (!window.audioController.isRecording) {
      // START RECORDING
      this.startRecordingUI();
      await window.audioController.startRecording(
        (liveText) => {
          if (liveText) {
            this.transcriptPreviewBox.classList.remove('hidden');
            this.transcriptPreviewText.textContent = liveText;
          }
        },
        (isRec) => {
          if (!isRec && !this.isProcessing) {
            this.stopRecordingUI();
          }
        }
      );
    } else {
      // STOP RECORDING AND SEND
      const capturedText = window.audioController.stopRecording();
      this.stopRecordingUI();

      const textToSend = capturedText || this.transcriptPreviewText.textContent;
      if (textToSend && textToSend !== '...') {
        this.processUserMessage(textToSend);
      } else {
        // If microphone didn't capture clear words, prompt to retry or type
        this.statusText.textContent = "Didn't catch that — please tap and speak again!";
      }
    }
  }

  startRecordingUI() {
    this.mainVoiceBtn.className = 'flex-grow bg-gradient-to-r from-rose-600 to-rose-700 hover:from-rose-500 hover:to-rose-600 text-white font-bold py-4 px-6 rounded-2xl text-base transition transform active:scale-95 shadow-xl flex items-center justify-center gap-3 border border-rose-400/50 animate-pulse';
    this.voiceBtnLabel.textContent = '⏹️ Done Speaking — Tap to Send';

    this.recordingIndicator.classList.remove('hidden');
    this.transcriptPreviewBox.classList.remove('hidden');
    this.transcriptPreviewText.textContent = 'Listening to your Lebanese Arabic...';

    this.statusText.textContent = 'Listening to you speak...';

    // Start timer
    let seconds = 0;
    this.recordingTimer.textContent = '00:00';
    clearInterval(this.recordingInterval);
    this.recordingInterval = setInterval(() => {
      seconds++;
      const mins = String(Math.floor(seconds / 60)).padStart(2, '0');
      const secs = String(seconds % 60).padStart(2, '0');
      this.recordingTimer.textContent = `${mins}:${secs}`;
    }, 1000);
  }

  stopRecordingUI() {
    clearInterval(this.recordingInterval);
    this.mainVoiceBtn.className = 'flex-grow bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 text-white font-bold py-4 px-6 rounded-2xl text-base transition transform active:scale-95 shadow-xl flex items-center justify-center gap-3 border border-emerald-400/30';
    this.voiceBtnLabel.textContent = '🎙️ Tap to Speak with Layla';

    this.recordingIndicator.classList.add('hidden');
    this.transcriptPreviewBox.classList.add('hidden');
  }

  handleKeyboardSend() {
    const text = this.keyboardInput.value.trim();
    if (!text || this.isProcessing) return;
    this.keyboardInput.value = '';
    this.processUserMessage(text);
  }

  async sendTutorGreeting() {
    this.dialogueStream.innerHTML = '';
    this.isProcessing = true;
    this.statusText.textContent = 'Layla is starting the conversation...';

    try {
      const apiKey = localStorage.getItem('ahlan_gemini_key') || '';
      const initialPrompt = this.currentScenario === 'beirut_cafe' 
        ? "أهلاً يا مية هلا! تفضل عود وين ما بدك بقهوتنا ببيروت. شو بتحب تشرب؟"
        : (this.currentScenario === 'service_taxi'
        ? "سرفيس! وين رايح يا شباب؟ عالحمرا ولا عالمصيطبة؟"
        : (this.currentScenario === 'souk_bargaining'
        ? "أهلاً وسهلاً بالسوق العتيق! عجبك شي من التحف وخشب الأرز؟"
        : (this.currentScenario === 'family_dinner'
        ? "أهلاً بحبيب قلبي! نورت بيتنا! في تبولة وكبة وورق عنب، تفضل."
        : "مرحبا! أنا ليلى، معلمتك للهجة اللبنانية. كيفك اليوم؟ شو الأخبار؟")));

      // Fetch response
      const res = await API.sendChatMessage({
        message: "START_SESSION: " + initialPrompt,
        conversation_id: this.conversationId,
        level: this.currentLevel,
        mode: 'roleplay',
        scenario_id: this.currentScenario,
        api_key: apiKey
      });

      this.addTutorMessage(res);

      // Play audio automatically
      if (res.audio_url) {
        window.audioController.playAudio(res.audio_url, res.reply_arabic);
      } else {
        window.audioController.playAudio(null, res.reply_arabic);
      }

    } catch (e) {
      console.error(e);
    } finally {
      this.isProcessing = false;
    }
  }

  async processUserMessage(userText) {
    this.isProcessing = true;
    this.statusText.textContent = 'Layla is listening & evaluating...';

    const userBubble = this.addUserMessage(userText);
    this.renderSuggestedPrompts([]);

    try {
      const apiKey = localStorage.getItem('ahlan_gemini_key') || '';
      const response = await API.sendChatMessage({
        message: userText,
        conversation_id: this.conversationId,
        level: this.currentLevel,
        mode: 'free_chat',
        scenario_id: this.currentScenario,
        api_key: apiKey
      });

      // Attach feedback & correction badge to user message
      if (response.correction) {
        this.attachCorrection(userBubble, response.correction);
      }

      // Add Layla's response
      this.addTutorMessage(response);

      // Play Layla's Lebanese Voice
      if (response.audio_url) {
        window.audioController.playAudio(response.audio_url, response.reply_arabic);
      } else {
        window.audioController.playAudio(null, response.reply_arabic);
      }

    } catch (err) {
      console.error(err);
      this.statusText.textContent = 'Connection error. Please try again.';
    } finally {
      this.isProcessing = false;
    }
  }

  addUserMessage(text) {
    const bubble = document.createElement('div');
    bubble.className = 'flex flex-col items-end mb-4 animate-fade-slide';
    bubble.innerHTML = `
      <div class="flex items-start gap-2 max-w-[85%] flex-row-reverse">
        <div class="w-8 h-8 rounded-full bg-amber-500 text-slate-950 flex items-center justify-center font-bold text-xs shadow flex-shrink-0">
          👤
        </div>
        <div class="bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 px-4 py-2.5 rounded-2xl rounded-tr-none shadow font-arabic text-base font-bold text-right" dir="rtl">
          ${text}
        </div>
      </div>
      <div class="correction-slot w-full max-w-[85%] mt-1.5"></div>
    `;
    this.dialogueStream.appendChild(bubble);
    this.scrollToBottom();
    return bubble;
  }

  attachCorrection(userBubble, correction) {
    const slot = userBubble.querySelector('.correction-slot');
    if (!slot || !correction) return;

    const hasDiff = correction.has_correction;
    const score = correction.fluency_score || 95;

    slot.innerHTML = `
      <div class="bg-slate-800/90 border border-slate-700/80 p-3 rounded-2xl text-xs text-slate-200 shadow-md">
        <div class="flex items-center justify-between border-b border-slate-700/80 pb-1.5 mb-1.5">
          <span class="font-bold px-2 py-0.5 rounded-full ${score >= 85 ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-amber-950 text-amber-300 border border-amber-800'}">
            ⭐ Fluency: ${score}%
          </span>
          <span class="text-slate-400 font-medium">${hasDiff ? '🇱🇧 Lebanese Dialect Feedback' : '✨ Natural Levantine Phrasing'}</span>
        </div>

        ${hasDiff ? `
          <div class="mb-1.5">
            <span class="text-slate-400">In Lebanese say:</span>
            <div class="font-arabic font-bold text-emerald-400 text-sm mt-0.5" dir="rtl">${correction.corrected_text}</div>
          </div>
        ` : ''}

        <p class="text-slate-300 leading-relaxed text-[11px]">${correction.explanation || ''}</p>

        ${correction.natural_alternative ? `
          <div class="mt-1.5 text-slate-300 border-t border-slate-700/60 pt-1">
            <span class="text-slate-400 font-medium">Beirut Native:</span>
            <span class="font-arabic text-emerald-300 font-bold ml-1">${correction.natural_alternative}</span>
          </div>
        ` : ''}
      </div>
    `;
    this.scrollToBottom();
  }

  addTutorMessage(data) {
    const bubble = document.createElement('div');
    bubble.className = 'flex flex-col items-start mb-4 animate-fade-slide';
    
    bubble.innerHTML = `
      <div class="flex items-start gap-2.5 max-w-[90%]">
        <div class="w-8 h-8 rounded-full bg-emerald-700 text-white flex items-center justify-center font-bold text-xs shadow flex-shrink-0">
          🇱🇧
        </div>
        <div class="bg-slate-800/95 border border-slate-700/90 rounded-2xl rounded-tl-none p-3.5 shadow-lg w-full">
          
          <!-- Arabic Voice Dialogue & Audio Button -->
          <div class="flex items-start justify-between gap-3 mb-1.5">
            <div class="font-arabic text-xl font-bold text-white leading-relaxed text-right flex-grow" dir="rtl">
              ${data.reply_arabic}
            </div>
            <button class="replay-audio-btn p-1.5 rounded-full bg-slate-700/80 hover:bg-emerald-700 text-emerald-300 hover:text-white transition flex-shrink-0" title="Replay Layla's voice">
              🔊
            </button>
          </div>

          <!-- Arabizi Transliteration -->
          <div class="text-amber-300/90 font-mono text-xs bg-amber-950/40 border border-amber-800/50 rounded-lg px-2.5 py-1 mb-1.5 leading-relaxed" style="display: ${this.showArabizi ? 'block' : 'none'}">
            <span class="font-bold text-amber-400 mr-1">🔤 Arabizi:</span> ${data.reply_transliteration || ''}
          </div>

          <!-- English Translation -->
          <div class="text-slate-300 text-xs leading-relaxed border-t border-slate-700/60 pt-1.5" style="display: ${this.showEnglish ? 'block' : 'none'}">
            <span class="font-semibold text-slate-400 mr-1">🇬🇧 Translation:</span> ${data.reply_english || ''}
          </div>

          <!-- Cultural Note if present -->
          ${data.cultural_note ? `
            <div class="mt-2 bg-emerald-950/60 border border-emerald-800/60 p-2 rounded-lg text-emerald-200 text-[11px]">
              💡 <span class="font-semibold">Cultural Tip:</span> ${data.cultural_note}
            </div>
          ` : ''}

        </div>
      </div>
    `;

    // Replay Button
    const replayBtn = bubble.querySelector('.replay-audio-btn');
    if (replayBtn) {
      replayBtn.addEventListener('click', () => {
        if (data.audio_url) {
          window.audioController.playAudio(data.audio_url, data.reply_arabic);
        } else {
          window.audioController.playAudio(null, data.reply_arabic);
        }
      });
    }

    this.dialogueStream.appendChild(bubble);
    this.scrollToBottom();

    // Render Suggested Quick Phrases
    if (data.suggested_replies && data.suggested_replies.length > 0) {
      this.renderSuggestedPrompts(data.suggested_replies);
    }
  }

  renderSuggestedPrompts(replies) {
    if (!this.suggestedPrompts) return;
    this.suggestedPrompts.innerHTML = '';
    if (!replies || replies.length === 0) return;

    replies.forEach(r => {
      const chip = document.createElement('button');
      chip.className = 'bg-slate-800/90 hover:bg-emerald-900/80 border border-slate-700 hover:border-emerald-500 rounded-xl px-3 py-1.5 text-xs text-slate-200 transition flex items-center gap-2 shadow-sm';
      chip.innerHTML = `
        <span class="font-arabic font-bold text-emerald-400" dir="rtl">${r.arabic}</span>
        <span class="text-slate-400 text-[10px]">(${r.english || r.translit})</span>
      `;
      chip.addEventListener('click', () => {
        this.processUserMessage(r.arabic);
      });
      this.suggestedPrompts.appendChild(chip);
    });
  }

  scrollToBottom() {
    if (this.dialogueStream) {
      this.dialogueStream.scrollTop = this.dialogueStream.scrollHeight;
    }
  }

  initSettingsModal() {
    const btn = document.getElementById('settings-btn');
    const modal = document.getElementById('settings-modal');
    const closeBtn = document.getElementById('close-settings-modal');
    const saveBtn = document.getElementById('save-settings-btn');
    const keyInput = document.getElementById('gemini-key-input');
    const arabiziToggle = document.getElementById('setting-arabizi-toggle');
    const englishToggle = document.getElementById('setting-english-toggle');

    if (btn && modal) {
      btn.addEventListener('click', () => {
        if (keyInput) keyInput.value = localStorage.getItem('ahlan_gemini_key') || '';
        modal.classList.remove('hidden');
      });
    }

    if (closeBtn && modal) {
      closeBtn.addEventListener('click', () => modal.classList.add('hidden'));
    }

    if (arabiziToggle) {
      arabiziToggle.addEventListener('change', (e) => {
        this.showArabizi = e.target.checked;
        document.querySelectorAll('.translit-text').forEach(el => el.style.display = this.showArabizi ? 'block' : 'none');
      });
    }

    if (englishToggle) {
      englishToggle.addEventListener('change', (e) => {
        this.showEnglish = e.target.checked;
        document.querySelectorAll('.english-text').forEach(el => el.style.display = this.showEnglish ? 'block' : 'none');
      });
    }

    if (saveBtn && keyInput) {
      saveBtn.addEventListener('click', () => {
        localStorage.setItem('ahlan_gemini_key', keyInput.value.trim());
        saveBtn.textContent = '✅ Saved!';
        setTimeout(() => {
          saveBtn.textContent = 'Save Settings';
          modal.classList.add('hidden');
        }, 800);
      });
    }
  }

  initLevelTestModal() {
    const btn = document.getElementById('quick-test-btn');
    const modal = document.getElementById('level-test-modal');
    const closeBtn = document.getElementById('close-test-modal');
    const submitBtn = document.getElementById('submit-quick-test-btn');
    const container = document.getElementById('quick-questions-container');

    const testQuestions = [
      {
        id: 1,
        q: "How do you say 'How are you?' in Lebanese Arabic to a friend?",
        options: ["كيفك؟ (Kifak / Kifik)", "كيف حالك يا سيدي؟ (Formal Fusha)", "إيش لونك؟ (Gulf)"],
        correct: 0
      },
      {
        id: 2,
        q: "What does 'بدي' (Baddi) mean in Levantine Arabic?",
        options: ["I want (أنا أريد)", "I am going (أنا رايح)", "I am tired (تعبان)"],
        correct: 0
      },
      {
        id: 3,
        q: "What is the polite Lebanese response when someone serves you food/coffee?",
        options: ["يسلمو إيديك (Yislamo ideik)", "شكراً جزيلاً يا أستاذ (Formal)", "لا شكراً (No thanks)"],
        correct: 0
      },
      {
        id: 4,
        q: "How do you negate verbs in Lebanese? (e.g. 'I don't know')",
        options: ["ما بعرف (Ma ba3ref)", "لا أعرف (La a3rifu)", "مش أعرف (Mish a3ref)"],
        correct: 0
      }
    ];

    const answers = {};

    if (btn && modal) {
      btn.addEventListener('click', () => {
        container.innerHTML = '';
        testQuestions.forEach((tq, idx) => {
          const card = document.createElement('div');
          card.className = 'bg-slate-800/80 p-3.5 rounded-xl border border-slate-700';
          card.innerHTML = `
            <div class="font-bold text-white mb-2">${idx + 1}. ${tq.q}</div>
            <div class="space-y-1.5">
              ${tq.options.map((opt, oIdx) => `
                <label class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-slate-700/60 cursor-pointer">
                  <input type="radio" name="tq_${tq.id}" value="${oIdx}" class="text-emerald-500 focus:ring-emerald-500">
                  <span class="text-slate-200">${opt}</span>
                </label>
              `).join('')}
            </div>
          `;
          card.querySelectorAll(`input[name="tq_${tq.id}"]`).forEach(inp => {
            inp.addEventListener('change', (e) => {
              answers[tq.id] = parseInt(e.target.value);
            });
          });
          container.appendChild(card);
        });

        modal.classList.remove('hidden');
      });
    }

    if (closeBtn && modal) {
      closeBtn.addEventListener('click', () => modal.classList.add('hidden'));
    }

    if (submitBtn) {
      submitBtn.addEventListener('click', () => {
        let correctCount = 0;
        testQuestions.forEach(tq => {
          if (answers[tq.id] === tq.correct) correctCount++;
        });

        let assessed = 'A0';
        if (correctCount === 4) assessed = 'B1';
        else if (correctCount >= 2) assessed = 'A1';
        else assessed = 'A0';

        this.currentLevel = assessed;
        localStorage.setItem('ahlan_level', assessed);
        if (this.levelSelector) this.levelSelector.value = assessed;

        alert(`Diagnostic Result: Your calibrated level is ${assessed}! Layla will now adapt to your level.`);
        modal.classList.add('hidden');
        this.sendTutorGreeting();
      });
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.app = new AhlanVoiceApp();
});
