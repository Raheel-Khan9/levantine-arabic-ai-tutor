"""
AI Client handling Google Gemini API integration with structured Levantine Tutor prompts,
plus fallback to the local smart dialect engine.
"""
import os
import json
import httpx
from typing import Dict, Any, Optional, List
from .dialect_engine import analyze_user_input_and_correct, get_smart_tutor_response, generate_arabizi_transliteration

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

TUTOR_SYSTEM_PROMPT = """
You are "Ahlan AI" (أهلاً), an expert, warm, and highly engaging native Lebanese and Levantine Arabic tutor.
Your mission is to teach the user conversational Levantine Arabic (specifically the Lebanese dialect - اللهجة اللبنانية).

CRITICAL RULES:
1. DIALECT PRIORITY: Always speak in authentic LEVANTINE / LEBANESE ARABIC (e.g. use "شو", "وين", "كيفك", "بدي", "كتير", "منيح", "هلق/هلأ", "رح", "عم", "يسلمو", "تكرم", "يعطيك العافية") - NEVER use textbook Modern Standard Arabic (Fusha) unless you are explicitly explaining the difference.
2. ADAPT TO LEVEL:
   - Level A0 / A1: Use very simple words, warm encouragement, complete Arabizi phonetics, and clear English translations.
   - Level A2: Common conversational phrases, polite formulas, daily routine words.
   - Level B1 / B2: More idiomatic expressions, storytelling, Lebanese humor and cultural context.
   - Level C1: Advanced colloquial phrasing, fast natural flow, cultural nuances.
3. ERROR CORRECTION: If the user makes a grammar mistake, uses standard Arabic (Fusha) words instead of Levantine, or misgenders words, gently provide a correction, explain the Lebanese alternative, and give a fluency rating (1-100).
4. RETURN FORMAT: You MUST strictly return a valid JSON object with the following schema:
{
  "reply_arabic": "Arabic text in Levantine dialect",
  "reply_transliteration": "Arabizi phonetic transliteration (using 3 for ع, 7 for ح, 2 for ء/ق, 5 for خ, etc.)",
  "reply_english": "English translation of your reply",
  "correction": {
    "has_correction": true/false,
    "original_text": "user's text",
    "corrected_text": "corrected version in Lebanese Arabic",
    "explanation": "concise explanation of grammar/vocabulary improvement",
    "dialect_tip": "Lebanese dialect tip (e.g. difference from MSA)",
    "natural_alternative": "how a native in Beirut would say it",
    "fluency_score": 85
  },
  "suggested_replies": [
    {"arabic": "...", "translit": "...", "english": "..."},
    {"arabic": "...", "translit": "...", "english": "..."},
    {"arabic": "...", "translit": "...", "english": "..."}
  ],
  "cultural_note": "A fun cultural or linguistic tidbit about Lebanon/Levant"
}
"""

async def query_gemini_tutor(
    user_message: str,
    level: str = "A1",
    mode: str = "free_chat",
    scenario_context: Optional[str] = None,
    api_key: Optional[str] = None,
    history: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Sends request to Google Gemini API if key is available, or falls back to smart local dialect engine.
    """
    active_key = (api_key or GEMINI_API_KEY).strip()

    if not active_key:
        # Graceful local fallback using our rich Levantine knowledgebase
        local_corr = analyze_user_input_and_correct(user_message, current_level=level)
        local_reply = get_smart_tutor_response(user_message, level=level, mode=mode)
        return {
            "reply_arabic": local_reply["reply_arabic"],
            "reply_transliteration": local_reply["reply_transliteration"],
            "reply_english": local_reply["reply_english"],
            "correction": local_corr,
            "suggested_replies": local_reply["suggested_replies"],
            "cultural_note": local_reply.get("cultural_note", "Tip: In Lebanon, 'Yislamo' (يسلمو) is the friendliest way to thank someone!"),
            "source": "local_dialect_engine"
        }

    # Prepare Gemini Request
    # Try gemini-2.5-flash or gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={active_key}"
    
    prompt_context = f"User Level: {level}. Mode: {mode}.\n"
    if scenario_context:
        prompt_context += f"Scenario Context: {scenario_context}\n"
    
    prompt_context += f"User said: {user_message}\n"
    prompt_context += "Remember to respond strictly in JSON matching the specified schema."

    payload = {
        "system_instruction": {
            "parts": [{"text": TUTOR_SYSTEM_PROMPT}]
        },
        "contents": [
            {
                "parts": [{"text": prompt_context}]
            }
        ],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.7
        }
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text_content)
                parsed["source"] = "gemini_ai"
                return parsed
            else:
                # Fallback to local if Gemini endpoint returns error
                local_corr = analyze_user_input_and_correct(user_message, current_level=level)
                local_reply = get_smart_tutor_response(user_message, level=level, mode=mode)
                return {
                    "reply_arabic": local_reply["reply_arabic"],
                    "reply_transliteration": local_reply["reply_transliteration"],
                    "reply_english": local_reply["reply_english"],
                    "correction": local_corr,
                    "suggested_replies": local_reply["suggested_replies"],
                    "cultural_note": f"Note: Gemini API returned status {resp.status_code}. Using built-in dialect engine.",
                    "source": "local_fallback"
                }
    except Exception as e:
        local_corr = analyze_user_input_and_correct(user_message, current_level=level)
        local_reply = get_smart_tutor_response(user_message, level=level, mode=mode)
        return {
            "reply_arabic": local_reply["reply_arabic"],
            "reply_transliteration": local_reply["reply_transliteration"],
            "reply_english": local_reply["reply_english"],
            "correction": local_corr,
            "suggested_replies": local_reply["suggested_replies"],
            "cultural_note": f"Local Lebanese engine active. ({str(e)})",
            "source": "local_fallback"
        }
