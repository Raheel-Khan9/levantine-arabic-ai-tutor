/**
 * Chat module managing tutor conversations, interactive word inspector,
 * correction badges, and voice input.
 */

class ChatManager {
  constructor() {
    this.conversationId = 'conv_' + Date.now();
    this.currentLevel = 'A1';
    this.showTranslit = true;
    this.showEnglish = true;
    this.isProcessing = false;
    this.messagesContainer = document.getElementById('chat-messages');
    this.inputField = document.getElementById('chat-input');
    this.sendBtn = document.getElementById('send-btn');
    this.micBtn = document.getElementById('mic-btn');
    this.suggestedContainer = document.getElementById('suggested-replies');

    this.init();
  }

  init() {
    if (this.sendBtn) {
      this.sendBtn.addEventListener('click', () => this.sendMessage());
    }

    if (this.inputField) {
      this.inputField.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
    }

    if (this.micBtn) {
      this.micBtn.addEventListener('click', () => this.toggleVoiceRecording());
    }

    // Load initial welcome message
    this.addTutorMessage({
      reply_arabic: "أهلاً وسهلاً فيك! أنا رفيقك الذكي لتعلّم اللهجة اللبنانية والشامية. كيفك اليوم؟ شو بتحب نتعلّم سوا؟",
      reply_transliteration: "Ahlan w sahlan fik! Ana rfi2ak el zaki la te3allom el lahjeh el lebnaniyeh w el shamiyeh. Kifak el yom? Shou bte7eb net3allam sawa?",
      reply_english: "Welcome! I'm your AI tutor for learning Lebanese and Levantine Arabic. How are you today? What would you like us to learn together?",
      suggested_replies: [
        { arabic: "أنا منيح، الحمدلله! وإنت كيفك؟", translit: "Ana mnih, el-hamdillah! W inta kifak?", english: "I'm good, praise God! And how are you?" },
        { arabic: "بدي نتدرّب على كيف بطلب أكل وقهوة باللبناني.", translit: "Baddi netdarrab 3ala kif botlob akel w ahwe bel-lebnani.", english: "I want to practice ordering food and coffee in Lebanese." },
        { arabic: "شو الفرق بين العربي الفصحى واللهجة اللبنانية؟", translit: "Shou el fare2 bein el 3arabi el fos7a w el lahjeh el lebnaniyeh?", english: "What is the difference between MSA (Fusha) and Lebanese?" }
      ],
      cultural_note: "Tip: In Lebanon, greetings are super warm! You can also greet people casually with 'Marhaba', 'Sabaho' (in morning), or the famous trilingual 'Hi, kifak, ça va?'"
    });
  }

  setLevel(level) {
    this.currentLevel = level;
  }

  toggleTranslit(show) {
    this.showTranslit = show;
    document.querySelectorAll('.translit-text').forEach(el => {
      el.style.display = show ? 'block' : 'none';
    });
  }

  toggleEnglish(show) {
    this.showEnglish = show;
    document.querySelectorAll('.english-text').forEach(el => {
      el.style.display = show ? 'block' : 'none';
    });
  }

  toggleVoiceRecording() {
    if (window.audioController.isRecording) {
      window.audioController.stopListening();
    } else {
      this.micBtn.classList.add('bg-rose-500', 'text-white', 'animate-pulse');
      window.audioController.startListening(
        (transcript, isFinal) => {
          if (this.inputField) {
            this.inputField.value = transcript;
            if (isFinal) {
              this.micBtn.classList.remove('bg-rose-500', 'text-white', 'animate-pulse');
              setTimeout(() => this.sendMessage(), 600);
            }
          }
        },
        (isRecording) => {
          if (!isRecording) {
            this.micBtn.classList.remove('bg-rose-500', 'text-white', 'animate-pulse');
          }
        }
      );
    }
  }

  async sendMessage(customText = null) {
    const text = (customText || (this.inputField ? this.inputField.value : '')).trim();
    if (!text || this.isProcessing) return;

    if (this.inputField) this.inputField.value = '';
    this.isProcessing = true;

    // Render User message
    const userBubble = this.addUserMessage(text);
    this.renderSuggestedReplies([]); // Clear suggested while waiting

    // Render Typing Indicator
    const typingIndicator = this.showTypingIndicator();

    try {
      const apiKey = localStorage.getItem('ahlan_gemini_key') || '';
      const response = await API.sendChatMessage({
        message: text,
        conversation_id: this.conversationId,
        level: this.currentLevel,
        mode: 'free_chat',
        api_key: apiKey
      });

      this.removeTypingIndicator(typingIndicator);

      // Attach feedback badge to user message bubble if available
      if (response.correction) {
        this.attachCorrectionToUserBubble(userBubble, response.correction);
      }

      // Render Tutor response
      this.addTutorMessage(response);

      // Auto play audio if enabled
      if (localStorage.getItem('ahlan_auto_audio') === 'true') {
        window.audioController.speak(response.reply_arabic);
      }

    } catch (err) {
      this.removeTypingIndicator(typingIndicator);
      console.error(err);
      this.addTutorMessage({
        reply_arabic: "صار في مشكلة صغيرة بالاتصال. فينا نجرّب مرة تانية؟",
        reply_transliteration: "Sar fi meshkle zghire bel ettesal. Fina njarreb marra tenyeh?",
        reply_english: "A small connection issue occurred. Can we try again?",
        suggested_replies: [{ arabic: "يلا نجرّب", translit: "Yalla njarreb", english: "Let's try again" }]
      });
    } finally {
      this.isProcessing = false;
    }
  }

  makeInteractiveArabicText(arabicText) {
    const words = arabicText.split(/(\s+)/);
    return words.map(w => {
      const trimmed = w.trim();
      if (!trimmed || /^[0-9\.,!؟?:\-()]+$/.test(trimmed)) {
        return w;
      }
      return `<span class="clickable-word text-emerald-900 font-arabic font-semibold" onclick="window.chatManager.inspectWord('${trimmed.replace(/'/g, "\\'")}')">${w}</span>`;
    }).join('');
  }

  addUserMessage(text) {
    const bubble = document.createElement('div');
    bubble.className = 'flex flex-col items-end mb-5 animate-fade-slide';
    bubble.innerHTML = `
      <div class="flex items-start gap-2 max-w-[85%] flex-row-reverse">
        <div class="w-8 h-8 rounded-full bg-amber-500 text-white flex items-center justify-center font-bold text-sm shadow-md flex-shrink-0">
          👤
        </div>
        <div class="bg-gradient-to-r from-amber-500 to-amber-600 text-white px-4 py-3 rounded-2xl rounded-tr-none shadow-md font-arabic text-lg leading-relaxed text-right">
          ${text}
        </div>
      </div>
      <div class="correction-container w-full max-w-[85%] mt-2"></div>
    `;
    this.messagesContainer.appendChild(bubble);
    this.scrollToBottom();
    return bubble;
  }

  attachCorrectionToUserBubble(userBubble, correction) {
    const container = userBubble.querySelector('.correction-container');
    if (!container || !correction) return;

    const hasErrors = correction.has_correction;
    const score = correction.fluency_score || 95;
    const scoreColor = score >= 85 ? 'text-emerald-700 bg-emerald-50 border-emerald-200' : 'text-amber-700 bg-amber-50 border-amber-200';

    container.innerHTML = `
      <div class="glass-panel p-3.5 rounded-xl border text-xs text-slate-700 shadow-sm animate-fade-slide">
        <div class="flex items-center justify-between border-b pb-2 mb-2">
          <span class="font-bold flex items-center gap-1.5 ${scoreColor} px-2 py-0.5 rounded-full border">
            ⭐ Fluency: ${score}%
          </span>
          <span class="text-slate-500 font-medium">${hasErrors ? '📝 Dialect Feedback' : '✨ Native Levantine Phrasing'}</span>
        </div>

        ${hasErrors ? `
          <div class="mb-2">
            <div class="text-slate-500">Corrected Lebanese Phrasing:</div>
            <div class="font-arabic font-bold text-emerald-800 text-sm mt-0.5">${correction.corrected_text}</div>
          </div>
        ` : ''}

        <p class="text-slate-600 mb-1.5 leading-relaxed">${correction.explanation || ''}</p>

        ${correction.dialect_tip ? `
          <div class="bg-amber-50/80 border border-amber-200/60 p-2 rounded-lg text-amber-900 flex items-start gap-1.5 mt-1.5">
            <span class="text-sm">💡</span>
            <span>${correction.dialect_tip}</span>
          </div>
        ` : ''}

        ${correction.natural_alternative ? `
          <div class="mt-2 text-slate-700">
            <span class="font-semibold text-slate-900">🇱🇧 Beirut Native Style:</span>
            <span class="font-arabic text-sm text-emerald-950 font-bold ml-1">${correction.natural_alternative}</span>
          </div>
        ` : ''}
      </div>
    `;
    this.scrollToBottom();
  }

  addTutorMessage(data) {
    const bubble = document.createElement('div');
    bubble.className = 'flex flex-col items-start mb-6 animate-fade-slide';
    
    const formattedArabic = this.makeInteractiveArabicText(data.reply_arabic);

    bubble.innerHTML = `
      <div class="flex items-start gap-2.5 max-w-[90%]">
        <div class="w-9 h-9 rounded-full bg-emerald-800 text-white flex items-center justify-center font-bold text-base shadow-lg flex-shrink-0 ring-2 ring-emerald-600/30">
          🌲
        </div>
        <div class="glass-panel border border-emerald-100/90 rounded-2xl rounded-tl-none p-4 shadow-md w-full">
          
          <!-- Top Row: Arabic Text & Speak Button -->
          <div class="flex items-start justify-between gap-3 mb-2">
            <div class="font-arabic text-xl font-bold text-slate-900 leading-relaxed text-right flex-grow" dir="rtl">
              ${formattedArabic}
            </div>
            <button class="audio-btn p-2 rounded-full hover:bg-emerald-50 text-emerald-800 transition flex-shrink-0" title="Listen in Arabic">
              🔊
            </button>
          </div>

          <!-- Transliteration Pill -->
          <div class="translit-text text-amber-800 font-mono text-xs bg-amber-50/70 border border-amber-200/40 rounded-lg px-2.5 py-1.5 mb-2 leading-relaxed" style="display: ${this.showTranslit ? 'block' : 'none'}">
            <span class="font-bold text-amber-900 mr-1">🔤 Arabizi:</span> ${data.reply_transliteration || ''}
          </div>

          <!-- English Translation -->
          <div class="english-text text-slate-600 text-xs leading-relaxed border-t border-slate-100 pt-2" style="display: ${this.showEnglish ? 'block' : 'none'}">
            <span class="font-semibold text-slate-800 mr-1">🇬🇧 Translation:</span> ${data.reply_english || ''}
          </div>

          <!-- Cultural Note if present -->
          ${data.cultural_note ? `
            <div class="mt-2.5 bg-emerald-50/70 border border-emerald-200/50 p-2.5 rounded-lg text-emerald-950 text-xs flex items-start gap-2">
              <span class="text-sm">🌲</span>
              <div>
                <span class="font-bold">Lebanese Culture & Dialect Note:</span>
                <p class="text-emerald-900 mt-0.5">${data.cultural_note}</p>
              </div>
            </div>
          ` : ''}

        </div>
      </div>
    `;

    // Hook audio playback
    const audioBtn = bubble.querySelector('.audio-btn');
    if (audioBtn) {
      audioBtn.addEventListener('click', () => {
        audioBtn.classList.add('animate-bounce', 'text-amber-600');
        window.audioController.speak(data.reply_arabic, () => {
          audioBtn.classList.remove('animate-bounce', 'text-amber-600');
        });
      });
    }

    this.messagesContainer.appendChild(bubble);
    this.scrollToBottom();

    // Render suggested replies
    if (data.suggested_replies && data.suggested_replies.length > 0) {
      this.renderSuggestedReplies(data.suggested_replies);
    }
  }

  renderSuggestedReplies(replies) {
    if (!this.suggestedContainer) return;
    this.suggestedContainer.innerHTML = '';
    if (!replies || replies.length === 0) return;

    replies.forEach(r => {
      const btn = document.createElement('button');
      btn.className = 'text-left bg-white/90 hover:bg-emerald-50 border border-emerald-200/70 hover:border-emerald-500 rounded-xl px-3.5 py-2 text-xs text-slate-800 shadow-sm transition transform hover:-translate-y-0.5 flex flex-col gap-0.5';
      btn.innerHTML = `
        <span class="font-arabic font-bold text-emerald-900 text-sm" dir="rtl">${r.arabic}</span>
        <span class="text-slate-500 font-mono text-[10px]">${r.translit || ''}</span>
        <span class="text-slate-600 text-[11px]">${r.english || ''}</span>
      `;
      btn.addEventListener('click', () => {
        this.sendMessage(r.arabic);
      });
      this.suggestedContainer.appendChild(btn);
    });
  }

  showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'flex items-center gap-2 mb-4 animate-pulse';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = `
      <div class="w-8 h-8 rounded-full bg-emerald-800 text-white flex items-center justify-center font-bold text-sm shadow">
        🌲
      </div>
      <div class="glass-panel px-4 py-2.5 rounded-2xl rounded-tl-none text-slate-500 text-xs flex items-center gap-1.5 font-arabic">
        <span>أهلاً عم يفكّر...</span>
        <div class="flex gap-1 ml-1">
          <div class="w-1.5 h-1.5 bg-emerald-600 rounded-full animate-bounce"></div>
          <div class="w-1.5 h-1.5 bg-emerald-600 rounded-full animate-bounce [animation-delay:0.2s]"></div>
          <div class="w-1.5 h-1.5 bg-emerald-600 rounded-full animate-bounce [animation-delay:0.4s]"></div>
        </div>
      </div>
    `;
    this.messagesContainer.appendChild(indicator);
    this.scrollToBottom();
    return indicator;
  }

  removeTypingIndicator(indicator) {
    if (indicator && indicator.parentNode) {
      indicator.parentNode.removeChild(indicator);
    }
  }

  scrollToBottom() {
    if (this.messagesContainer) {
      this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
  }

  async inspectWord(word) {
    const modal = document.getElementById('word-inspector-modal');
    if (!modal) return;

    document.getElementById('inspect-word-ar').textContent = word;
    document.getElementById('inspect-word-translit').textContent = 'Loading...';
    document.getElementById('inspect-word-en').textContent = 'Fetching Levantine meaning...';

    modal.classList.remove('hidden');

    try {
      // Look up in dialect engine or ask backend
      const res = await API.evaluatePronunciation(word, '');
      document.getElementById('inspect-word-translit').textContent = res.target_translit || word;
      document.getElementById('inspect-word-en').textContent = 'Levantine Arabic Word';

      // Save word button listener
      const saveBtn = document.getElementById('save-word-btn');
      saveBtn.onclick = async () => {
        await API.createFlashcard({
          arabic: word,
          transliteration: res.target_translit || word,
          english: 'Vocabulary from chat',
          dialect_category: 'Chat Vocabulary',
          notes: 'Saved from conversation'
        });
        saveBtn.textContent = '✅ Added to Word Vault!';
        setTimeout(() => {
          saveBtn.textContent = '📥 Save to Word Vault';
          modal.classList.add('hidden');
        }, 1200);
      };

      // Play audio on inspect
      document.getElementById('inspect-word-audio').onclick = () => {
        window.audioController.speak(word);
      };

    } catch (e) {
      console.error(e);
    }
  }
}

window.chatManager = null;
