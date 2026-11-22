/**
 * API client module for Ahlan AI Levantine Arabic Tutor
 */
const API = {
  baseUrl: '/api',

  async get(endpoint) {
    const res = await fetch(`${this.baseUrl}${endpoint}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Network error' }));
      throw new Error(err.detail || `Error ${res.status}`);
    }
    return res.json();
  },

  async post(endpoint, data) {
    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Network error' }));
      throw new Error(err.detail || `Error ${res.status}`);
    }
    return res.json();
  },

  // Chat
  async sendChatMessage(payload) {
    return this.post('/chat', payload);
  },

  // Scenarios
  async getScenarios() {
    return this.get('/scenarios');
  },

  async getScenario(id) {
    return this.get(`/scenarios/${id}`);
  },

  // Flashcards & Word Vault
  async getFlashcards() {
    return this.get('/flashcards');
  },

  async createFlashcard(data) {
    return this.post('/flashcards', data);
  },

  async reviewFlashcard(cardId, rating) {
    return this.post('/flashcards/review', { card_id: cardId, rating });
  },

  // Profile & Analytics
  async getProfile() {
    return this.get('/profile');
  },

  async updateProfile(updates) {
    return this.post('/profile', updates);
  },

  async getHistory(convId) {
    return this.get(`/history/${convId}`);
  },

  // Diagnostic Test
  async getAssessmentQuestions() {
    return this.get('/assessment/questions');
  },

  async submitAssessment(answers) {
    return this.post('/assessment/submit', { answers });
  },

  // Pronunciation Evaluation
  async evaluatePronunciation(targetPhrase, userSpoken) {
    return this.post('/pronunciation/evaluate', {
      target_phrase: targetPhrase,
      user_spoken: userSpoken
    });
  },

  // Expressions & Idioms
  async getExpressions() {
    return this.get('/expressions');
  }
};
