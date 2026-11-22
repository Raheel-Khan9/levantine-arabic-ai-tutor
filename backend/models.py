"""
Data models for Ahlan - Levantine Arabic AI Tutor
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class WordBreakdown(BaseModel):
    arabic: str
    transliteration: str
    english: str
    root_or_note: Optional[str] = None

class CorrectionData(BaseModel):
    has_correction: bool = False
    original_text: str = ""
    corrected_text: str = ""
    explanation: str = ""
    dialect_tip: str = ""
    natural_alternative: str = ""
    fluency_score: int = 100
    vocabulary_breakdown: List[WordBreakdown] = []

class MessageItem(BaseModel):
    id: str
    sender: str # "user" or "tutor"
    text: str
    transliteration: Optional[str] = None
    translation: Optional[str] = None
    correction: Optional[CorrectionData] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = "default"
    level: str = "A1" # A0, A1, A2, B1, B2, C1
    mode: str = "free_chat" # free_chat, roleplay, pronunciation, grammar_drill
    scenario_id: Optional[str] = None
    api_key: Optional[str] = None
    api_provider: str = "gemini" # gemini, openai, local
    voice_speed: float = 0.9

class ChatResponse(BaseModel):
    reply_arabic: str
    reply_transliteration: str
    reply_english: str
    correction: Optional[CorrectionData] = None
    conversation_id: str
    current_level: str
    suggested_replies: List[Dict[str, str]] = [] # [{"arabic": "...", "translit": "...", "english": "..."}]
    vocabulary_highlight: List[WordBreakdown] = []
    cultural_note: Optional[str] = None
    audio_url: Optional[str] = None

class ScenarioObjective(BaseModel):
    id: str
    text_en: str
    text_ar: str
    completed: bool = False

class Scenario(BaseModel):
    id: str
    title_ar: str
    title_en: str
    icon: str
    category: str
    level: str
    location: str
    description: str
    initial_tutor_message: str
    initial_transliteration: str
    initial_translation: str
    objectives: List[ScenarioObjective]
    starter_hints: List[Dict[str, str]]

class Flashcard(BaseModel):
    id: str
    arabic: str
    transliteration: str
    english: str
    dialect_category: str # "Greetings", "Food & Drink", "Slang/Expressions", "Directions", "Daily Life"
    example_ar: str
    example_translit: str
    example_en: str
    notes: Optional[str] = None
    mastery_level: int = 0 # 0 to 5
    times_reviewed: int = 0
    last_reviewed: Optional[str] = None

class FlashcardReviewRequest(BaseModel):
    card_id: str
    rating: str # "easy", "good", "hard", "again"

class UserProfile(BaseModel):
    id: str = "user_default"
    name: str = "Learner"
    level: str = "A1"
    dialect: str = "Lebanese / Levantine"
    streak_days: int = 1
    total_messages: int = 0
    words_learned: int = 0
    average_fluency: int = 85
    daily_goal_minutes: int = 15
    minutes_practiced_today: int = 5
    api_key_configured: bool = False

class AssessmentQuestion(BaseModel):
    id: int
    prompt_ar: str
    prompt_translit: str
    prompt_en: str
    options: List[Dict[str, str]]
    correct_option_index: int
    level_target: str
    explanation: str

class AssessmentSubmitRequest(BaseModel):
    answers: Dict[int, int] # question_id -> selected_option_index

class AssessmentResult(BaseModel):
    assessed_level: str
    score_percentage: float
    total_correct: int
    total_questions: int
    level_description: str
    strengths: List[str]
    focus_areas: List[str]
    recommended_scenarios: List[str]
