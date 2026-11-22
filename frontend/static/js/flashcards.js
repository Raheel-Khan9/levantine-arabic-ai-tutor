/**
 * Word Vault & Spaced Repetition (SRS) Flashcard Deck Manager
 */

class FlashcardsManager {
  constructor() {
    this.cards = [];
    this.currentIndex = 0;
    this.isFlipped = false;

    this.cardElement = document.getElementById('flashcard-3d');
    this.cardFront = document.getElementById('card-front-content');
    this.cardBack = document.getElementById('card-back-content');
    this.cardCounter = document.getElementById('card-counter');
    this.categoryBadge = document.getElementById('card-category-badge');
    this.wordVaultTable = document.getElementById('vault-table-body');
    this.searchVaultInput = document.getElementById('vault-search');

    this.init();
  }

  async init() {
    // Card Flip on Click
    if (this.cardElement) {
      this.cardElement.addEventListener('click', () => this.flipCard());
    }

    // Audio Play Button on Card
    const cardAudioBtn = document.getElementById('card-audio-btn');
    if (cardAudioBtn) {
      cardAudioBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.playCurrentCardAudio();
      });
    }

    // Grading Buttons (SRS)
    document.querySelectorAll('.srs-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const rating = e.currentTarget.dataset.rating;
        this.submitReview(rating);
      });
    });

    // Vault search
    if (this.searchVaultInput) {
      this.searchVaultInput.addEventListener('input', (e) => this.filterVault(e.target.value));
    }

    // Add Word Modal
    const addWordBtn = document.getElementById('add-custom-word-btn');
    if (addWordBtn) {
      addWordBtn.addEventListener('click', () => this.showAddWordModal());
    }

    await this.loadFlashcards();
  }

  async loadFlashcards() {
    try {
      const data = await API.getFlashcards();
      this.cards = data.flashcards || [];
      this.currentIndex = 0;
      this.renderCurrentCard();
      this.renderVaultTable(this.cards);
      this.updateStats();
    } catch (e) {
      console.error('Error loading flashcards:', e);
    }
  }

  renderCurrentCard() {
    if (!this.cards || this.cards.length === 0) {
      if (this.cardFront) {
        this.cardFront.innerHTML = `<div class="text-center text-slate-500 font-arabic text-lg">لا يوجد بطاقات حالياً<br><span class="text-xs">No cards available</span></div>`;
      }
      return;
    }

    const card = this.cards[this.currentIndex];
    this.isFlipped = false;
    if (this.cardElement) {
      this.cardElement.classList.remove('rotate-y-180');
    }

    if (this.cardCounter) {
      this.cardCounter.textContent = `${this.currentIndex + 1} / ${this.cards.length}`;
    }

    if (this.categoryBadge) {
      this.categoryBadge.textContent = card.dialect_category || 'General';
    }

    // Front: Arabic Word & Mastery Stars
    if (this.cardFront) {
      const stars = '⭐'.repeat(card.mastery_level || 1);
      this.cardFront.innerHTML = `
        <div class="text-xs text-amber-800 font-semibold mb-2">Mastery: ${stars}</div>
        <div class="font-arabic text-4xl font-bold text-slate-900 mb-3" dir="rtl">${card.arabic}</div>
        <div class="text-xs text-slate-500 font-medium">Click card to flip & reveal meaning 🔄</div>
      `;
    }

    // Back: Transliteration, English, Example & Notes
    if (this.cardBack) {
      this.cardBack.innerHTML = `
        <div class="font-arabic text-2xl font-bold text-emerald-950 mb-1" dir="rtl">${card.arabic}</div>
        <div class="text-amber-800 font-mono text-sm font-semibold bg-amber-50 px-2.5 py-1 rounded-lg mb-2">
          ${card.transliteration}
        </div>
        <div class="text-slate-800 font-semibold text-sm mb-3">
          ${card.english}
        </div>
        
        ${card.example_ar ? `
          <div class="bg-slate-50 border border-slate-200/80 rounded-xl p-2.5 text-xs text-left w-full mb-2">
            <div class="font-bold text-slate-700 mb-0.5">Example in Lebanese:</div>
            <div class="font-arabic text-emerald-900 font-bold text-sm text-right" dir="rtl">${card.example_ar}</div>
            <div class="text-slate-500 font-mono text-[10px]">${card.example_translit || ''}</div>
            <div class="text-slate-600 text-[11px]">${card.example_en || ''}</div>
          </div>
        ` : ''}

        ${card.notes ? `
          <div class="text-[11px] text-emerald-800 italic bg-emerald-50/60 rounded px-2 py-1">
            💡 ${card.notes}
          </div>
        ` : ''}
      `;
    }
  }

  flipCard() {
    this.isFlipped = !this.isFlipped;
    if (this.cardElement) {
      this.cardElement.classList.toggle('rotate-y-180', this.isFlipped);
    }
  }

  playCurrentCardAudio() {
    if (this.cards.length === 0) return;
    const card = this.cards[this.currentIndex];
    window.audioController.speak(card.arabic);
  }

  async submitReview(rating) {
    if (this.cards.length === 0) return;
    const card = this.cards[this.currentIndex];

    try {
      await API.reviewFlashcard(card.id, rating);
      // Advance to next card
      this.currentIndex = (this.currentIndex + 1) % this.cards.length;
      this.renderCurrentCard();
      this.updateStats();
    } catch (e) {
      console.error('Error submitting review:', e);
    }
  }

  renderVaultTable(cardsToRender) {
    if (!this.wordVaultTable) return;
    this.wordVaultTable.innerHTML = '';

    cardsToRender.forEach(c => {
      const row = document.createElement('tr');
      row.className = 'border-b border-slate-100 hover:bg-slate-50/80 transition text-xs';
      row.innerHTML = `
        <td class="py-3 px-3.5 font-arabic font-bold text-base text-slate-900" dir="rtl">${c.arabic}</td>
        <td class="py-3 px-3.5 font-mono text-amber-800">${c.transliteration}</td>
        <td class="py-3 px-3.5 text-slate-700 font-medium">${c.english}</td>
        <td class="py-3 px-3.5"><span class="px-2 py-0.5 rounded-full bg-emerald-100/70 text-emerald-900 text-[10px] font-bold">${c.dialect_category}</span></td>
        <td class="py-3 px-3.5 text-amber-600">${'⭐'.repeat(c.mastery_level || 1)}</td>
        <td class="py-3 px-3.5 text-right">
          <button class="p-1.5 rounded-full hover:bg-emerald-100 text-emerald-800 transition" onclick="window.audioController.speak('${c.arabic.replace(/'/g, "\\'")}')">
            🔊
          </button>
        </td>
      `;
      this.wordVaultTable.appendChild(row);
    });
  }

  filterVault(query) {
    const q = query.toLowerCase().trim();
    if (!q) {
      this.renderVaultTable(this.cards);
      return;
    }
    const filtered = this.cards.filter(c => 
      c.arabic.includes(q) ||
      c.transliteration.toLowerCase().includes(q) ||
      c.english.toLowerCase().includes(q) ||
      c.dialect_category.toLowerCase().includes(q)
    );
    this.renderVaultTable(filtered);
  }

  updateStats() {
    const totalWords = this.cards.length;
    const mastered = this.cards.filter(c => c.mastery_level >= 3).length;
    const totalEl = document.getElementById('vault-total-count');
    const masterEl = document.getElementById('vault-mastered-count');
    if (totalEl) totalEl.textContent = totalWords;
    if (masterEl) masterEl.textContent = mastered;
  }

  showAddWordModal() {
    const modal = document.getElementById('add-word-modal');
    if (modal) modal.classList.remove('hidden');
  }
}

window.flashcardsManager = null;
