# 🌲 Ahlan AI (أهلاً) - Personal Levantine & Lebanese Arabic AI Tutor

<div align="center">

![License](https://img.shields.io/badge/License-MIT-emerald.svg)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)
![Dialect](https://img.shields.io/badge/Dialect-Levantine%20%2F%20Lebanese-amber.svg)
![AI-Core](https://img.shields.io/badge/AI%20Core-Gemini%20%2B%20Smart%20Engine-green.svg)

**Your personal, voice-enabled, adaptive AI language tutor for mastering conversational Levantine and Lebanese Arabic (*El-Lahjeh El-Lebnaniyeh*).**

[Features](#-key-features) • [Quick Start](#-quick-start) • [Roleplay Scenarios](#-cultural-roleplay-scenarios) • [Architecture](#-architecture) • [Dialect Guide](#-levantine-dialect-cheat-sheet)

</div>

---

## 🌟 Overview

Most Arabic language courses teach **Modern Standard Arabic (MSA / *Fusha*)**, which nobody uses in everyday casual conversations on the streets of Beirut, Damascus, Amman, or Jerusalem.

**Ahlan AI** is built specifically for **Levantine Arabic (اللهجة الشامية / اللبنانية)**. It functions just like an experienced, warm personal tutor:
- **Understands your level**: Dynamically adapts its vocabulary, speed, and scaffolding (A0 Absolute Beginner to C1 Native Fluency).
- **Voice-enabled**: Speak into your microphone and hear authentic spoken Arabic replies.
- **Smart Dialect Correction**: Analyzes your sentences in real-time, catches textbook MSA words, and shows how a native in Beirut would say it naturally.
- **Interactive Word-Click Inspector**: Click any Arabic word in the conversation to hear its pronunciation, view its Arabizi transliteration, and save it to your **Word Vault**.
- **Dual Engine Architecture**: Works **100% out of the box** with a built-in Levantine dialect knowledgebase, and connects to **Google Gemini** for limitless conversational depth.

---

## ✨ Key Features

```
  💬 Adaptive Chat               🎭 Roleplay Scenarios           🎙️ Lahjeh Voice Coach
  ├── Real-time corrections      ├── Beirut Café & Coffee        ├── Phonetic accuracy scoring
  ├── Arabizi transliteration    ├── Souk price bargaining       ├── Qaf elision rules
  └── Interactive word lookup    └── Beirut "Service" Taxi       └── Intonation guidance

  🗂️ Word Vault & SRS            📝 Level Placement Test         🇱🇧 Slang & Idioms
  ├── 3D Flip Flashcards         ├── 8-question evaluation       ├── "3ala rasi", "Yislamo"
  ├── Leitner mastery system     ├── Automatic level calibration ├── Beirut code-switching
  └── Custom phrase creator      └── Strength & focus breakdown  └── Cultural etiquette
```

### 1. 🧠 Dynamic Level Adaptation (A0 to C1)
- **A0 (Absolute Beginner)**: Full Arabizi transliteration (*3=ع, 7=ح, 2=ء/ق, 5=خ*), word-by-word breakdowns, English translations, foundational greetings.
- **A1–A2 (Elementary to Pre-Intermediate)**: Everyday polite formulas (*Yislamo, Tekram, 3ala rasi, Ya3tik el 3afye*), ordering food, numbers, asking directions.
- **B1–B2 (Intermediate)**: Storytelling, humor, conversational rhythm, handling complex social situations.
- **C1 (Advanced)**: Native slang, rapid colloquial banter, cultural nuances.

### 2. 🎙️ Voice & Audio Synthesis
- **Speech-to-Text Input**: Practice speaking Arabic with your microphone.
- **Natural Arabic Audio Playback**: High-quality audio synthesis with adjustable speed controls (0.7x slow tutor mode to 1.3x natural speed).

### 3. 📝 Live Dialect & Grammar Feedback
- **Fluency Rating**: 1–100% score for every user response.
- **Fusha vs. Levantine Filter**: Detects when you use MSA words (e.g. *Madha* instead of *Shou*, *Ureed* instead of *Baddi*) and explains the dialectal alternative.
- **Native Beirut Alternative**: Suggests authentic idiomatic phrasing.

### 4. 🎭 Cultural Roleplay Scenarios
- **☕ Ahwet Beirut (Beirut Café)**: Order Turkish coffee (*ahwe wasat / bala soukar*), fresh *manousheh zaatar*, chat with the barista, and ask for the bill.
- **🛍️ El Souq (Old Market Bargaining)**: Bargain for cedar wood souvenirs in Byblos using polite negotiation terms (*Kermeli, Ra3ina chway*).
- **🚕 Beirut Service Taxi**: Hail a shared taxi to Hamra, confirm the fare, and tell the driver where to pull over.
- **🏡 3ind el 3ayleh (Lebanese Family Feast)**: Master dinner etiquette, praise the feast (*Tabbouleh, Kebbeh*), and say *Deyme*.
- **💼 Modern Beirut Workplace**: Experience the trilingual Lebanese workplace mix of Arabic, French, and English (*"Hi, ça va? Yalla let's start"*).

### 5. 🗂️ Word Vault & Spaced-Repetition (SRS) Flashcards
- Words encountered in chat are automatically saved to your **Word Vault**.
- 3D interactive flashcards with audio playback, example sentences, and Leitner spaced-repetition mastery grading (Easy, Good, Hard, Again).

### 6. 📝 Diagnostic Level Placement Test
- Take an 8-question evaluation to benchmark your current Levantine standing and automatically configure the AI tutor's persona and difficulty.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/levantine-arabic-ai-tutor.git
   cd levantine-arabic-ai-tutor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   - **Windows (Double-click or terminal):**
     ```bash
     start.bat
     # or
     python run.py
     ```
   - **macOS / Linux:**
     ```bash
     python3 run.py
     ```

4. **Open in your browser:**
   ```
   http://localhost:8000
   ```

---

## 🔑 AI Provider Configuration

Ahlan AI is designed with **dual-engine capability**:
1. **Built-in Smart Levantine Dialect Engine**: Ready immediately without any API keys or configuration.
2. **Google Gemini API**: Click the **⚙️ Settings** icon in the top navigation bar and paste your [Gemini API Key](https://aistudio.google.com/) for limitless generative multi-turn dialogue.

---

## 🏗️ Architecture

```
Levantine_Arabic_AI_Tutor/
├── backend/
│   ├── app.py                 # FastAPI server & REST API
│   ├── dialect_engine.py      # Levantine linguistic rules, Arabizi generator, error analyzer
│   ├── tutor_service.py       # Pedagogical adaptation, diagnostic evaluation, chat orchestration
│   ├── gemini_client.py       # Gemini API client + local engine fallback
│   ├── database.py            # SQLite storage (user profile, conversations, word vault, SRS)
│   ├── scenarios.py           # Roleplay scenario configurations & checklists
│   └── models.py              # Pydantic data schemas
├── frontend/
│   ├── index.html             # Modern Glassmorphic single-page web app
│   └── static/
│       ├── css/style.css      # Mediterranean Cedar theme & animations
│       ├── js/
│       │   ├── api.js         # Backend API client
│       │   ├── audio.js       # Web Speech STT & Arabic TTS audio engine
│       │   ├── chat.js        # Real-time chat & word inspector popover
│       │   ├── roleplay.js    # Scenario roleplay controller
│       │   ├── flashcards.js  # 3D SRS flashcards & word vault manager
│       │   └── app.js         # Main UI state controller & diagnostic test
│       └── assets/icon.svg    # Brand logo
├── run.py                     # Cross-platform application launcher
├── start.bat                  # Windows double-click runner
├── start.ps1                  # PowerShell launcher
├── requirements.txt           # Python package dependencies
├── .gitignore                 # Standard clean gitignore
└── README.md                  # Project documentation
```

---

## 🇱🇧 Levantine Dialect Cheat Sheet

| English | Modern Standard Arabic (Fusha) | Levantine / Lebanese (Shami) | Arabizi Phonetics |
| :--- | :--- | :--- | :--- |
| **What?** | ماذا (Madha) | **شو** | *Shou* |
| **Where?** | أين (Ayna) | **وين** | *Wein* |
| **How are you?** | كيف حالك (Kayfa haluk) | **كيفك** | *Kifak (m) / Kifik (f)* |
| **I want** | أريد (Ureed) | **بدي** | *Baddi* |
| **Now** | الآن (Al-Aan) | **هلق / هلأ** | *Halla2 / Halla* |
| **Good / Well** | جيد (Jayyid) | **منيح / تمام** | *Mnih (m) / Mniha (f)* |
| **A lot / Very** | كثيراً (Katheeran) | **كتير** | *Ktiir* |
| **A little bit** | قليلاً (Qaleelan) | **شوي** | *Chway* |
| **Not** | ليس (Laysa) | **مش** | *Mish* |
| **Why?** | لماذا (Limadha) | **ليش** | *Leish* |
| **Money** | نقود (Nuqood) | **مصاري** | *Masari* |
| **Thank you** | شكراً جزيلاً | **يسلمو / ميرسي كتير** | *Yislamo / Merci ktiir* |

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <b>Built with ❤️ for learners of Levantine & Lebanese Arabic.</b><br>
  <i>صحتين وهنا وتعلّم ممتع!</i>
</div>
