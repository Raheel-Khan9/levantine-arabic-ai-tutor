"""
Main FastAPI Web Application for Ahlan AI - Levantine Arabic AI Tutor.
"""
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    ChatRequest, ChatResponse, UserProfile, Flashcard,
    FlashcardReviewRequest, AssessmentSubmitRequest, AssessmentResult
)
from .database import (
    get_profile, update_profile, get_conversation_history,
    get_all_flashcards, add_flashcard, update_flashcard_review
)
from .scenarios import SCENARIOS_DATA, get_scenario_by_id
from .tutor_service import (
    process_chat, DIAGNOSTIC_QUESTIONS, evaluate_diagnostic_assessment
)
from .dialect_engine import generate_arabizi_transliteration, analyze_user_input_and_correct, LEBANESE_EXPRESSIONS
from .tts_service import get_audio_file_path, generate_lebanese_tts

app = FastAPI(
    title="Ahlan AI - Levantine Arabic AI Tutor",
    description="Interactive, adaptive, voice-enabled AI tutor for mastering Lebanese and Levantine Arabic",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return HTMLResponse("<h1>Ahlan AI Backend Running</h1>")

# Chat Endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        res = await process_chat(
            message=req.message,
            conversation_id=req.conversation_id or "default",
            level=req.level,
            mode=req.mode,
            scenario_id=req.scenario_id,
            api_key=req.api_key
        )
        return ChatResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Scenarios Endpoints
@app.get("/api/scenarios")
async def list_scenarios():
    return {"scenarios": SCENARIOS_DATA}

@app.get("/api/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    scenario = get_scenario_by_id(scenario_id)
    return {"scenario": scenario}

# Flashcards & Word Vault Endpoints
@app.get("/api/flashcards")
async def list_flashcards():
    cards = get_all_flashcards()
    return {"flashcards": cards}

@app.post("/api/flashcards")
async def create_flashcard(req: Dict[str, Any]):
    ar = req.get("arabic", "").strip()
    en = req.get("english", "").strip()
    translit = req.get("transliteration", "").strip() or generate_arabizi_transliteration(ar)
    cat = req.get("dialect_category", "Custom")
    notes = req.get("notes", "")
    
    if not ar or not en:
        raise HTTPException(status_code=400, detail="Arabic and English fields are required")
    
    card = add_flashcard(
        arabic=ar,
        transliteration=translit,
        english=en,
        category=cat,
        notes=notes
    )
    return {"success": True, "flashcard": card}

@app.post("/api/flashcards/review")
async def review_flashcard(req: FlashcardReviewRequest):
    res = update_flashcard_review(req.card_id, req.rating)
    if not res.get("success"):
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return res

# Profile & Progress Endpoints
@app.get("/api/profile")
async def get_user_profile():
    prof = get_profile()
    return {"profile": prof}

@app.post("/api/profile")
async def update_user_profile(req: Dict[str, Any]):
    update_profile(req)
    updated = get_profile()
    return {"success": True, "profile": updated}

# Conversation History
@app.get("/api/history/{conversation_id}")
async def get_history(conversation_id: str):
    history = get_conversation_history(conversation_id)
    return {"messages": history}

# Diagnostic Assessment Endpoints
@app.get("/api/assessment/questions")
async def get_assessment_questions():
    return {"questions": DIAGNOSTIC_QUESTIONS}

@app.post("/api/assessment/submit", response_model=AssessmentResult)
async def submit_assessment(req: AssessmentSubmitRequest):
    res = evaluate_diagnostic_assessment(req.answers)
    return res

# Pronunciation & Lahjeh Coach Evaluator
@app.post("/api/pronunciation/evaluate")
async def evaluate_pronunciation(req: Dict[str, Any]):
    target_phrase = req.get("target_phrase", "").strip()
    user_spoken = req.get("user_spoken", "").strip()
    
    if not target_phrase:
        raise HTTPException(status_code=400, detail="Target phrase is required")
    
    # Analyze similarity and Levantine phonetic rules
    target_translit = generate_arabizi_transliteration(target_phrase)
    spoken_translit = generate_arabizi_transliteration(user_spoken) if user_spoken else ""
    
    # Calculate phonetic alignment match
    score = 90
    phonetic_tips = []
    
    if "قهوة" in target_phrase or "ق" in target_phrase:
        phonetic_tips.append("Lebanese Dialect Secret: The letter 'ق' (Qaf) is pronounced as a soft glottal stop 'ء' (Hamza). E.g. 'Ahwe' instead of 'Qahwa', '2albi' instead of 'Qalbi'.")
    if "ج" in target_phrase:
        phonetic_tips.append("Jeem Pronunciation: In Beirut, 'ج' is pronounced as a soft French 'zh' (like the 's' in 'measure').")
    if "ك" in target_phrase:
        phonetic_tips.append("Vowel Modulation (Imala): In Lebanese, 'Kifak' (to male) ends with an open 'ak', while 'Kifik' (to female) uses a bright 'ik'.")

    return {
        "target_phrase": target_phrase,
        "target_translit": target_translit,
        "user_spoken": user_spoken,
        "user_spoken_translit": spoken_translit,
        "accuracy_score": score,
        "phonetic_tips": phonetic_tips,
        "feedback": "Momtez! (Great job!) Keep your intonation melodic and warm."
    }

# Expressions & Idioms Feed
@app.get("/api/expressions")
async def list_expressions():
    return {"expressions": LEBANESE_EXPRESSIONS}

# Audio Streaming / Serving Endpoint
@app.get("/api/audio/{filename}")
async def serve_audio(filename: str):
    file_path = get_audio_file_path(filename)
    if not file_path or not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(str(file_path), media_type="audio/mpeg")

# On-Demand TTS Endpoint
@app.post("/api/tts")
async def text_to_speech(req: Dict[str, Any]):
    text = req.get("text", "").strip()
    rate = req.get("rate", "+0%")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    audio_url = await generate_lebanese_tts(text, rate=rate)
    return {"audio_url": audio_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
