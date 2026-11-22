"""
Tutor Service managing conversation sessions, diagnostic placement tests,
scenario goal evaluations, and pronunciation coach helpers.
"""
from typing import Dict, Any, List, Optional
from .models import AssessmentQuestion, AssessmentResult, WordBreakdown
from .database import (
    record_user_message, record_tutor_message, get_profile,
    update_profile, add_flashcard
)
from .gemini_client import query_gemini_tutor
from .scenarios import get_scenario_by_id
from .dialect_engine import LEVANTINE_VOCAB_DB
from .tts_service import generate_lebanese_tts

# Diagnostic Level Assessment Questions (Lebanese & Levantine Arabic)
DIAGNOSTIC_QUESTIONS = [
    {
        "id": 1,
        "prompt_ar": "كيف بتقول 'How are you?' باللبناني لرفيقك؟",
        "prompt_translit": "Kif bt2oul 'How are you?' bel lebnani la rfi2ak?",
        "prompt_en": "How do you say 'How are you?' in Lebanese to a male friend?",
        "options": [
            {"arabic": "كيفك؟ / شو الأخبار؟", "translit": "Kifak? / Shou el akhbar?", "english": "Kifak? / What's the news?"},
            {"arabic": "كيف حالك يا سيدي؟", "translit": "Kayfa haluka ya sayyidi?", "english": "Formal MSA greeting"},
            {"arabic": "إيش لونك؟", "translit": "Eish lawnak?", "english": "Gulf dialect greeting"},
            {"arabic": "أزيك؟", "translit": "Izzayak?", "english": "Egyptian dialect greeting"}
        ],
        "correct_option_index": 0,
        "level_target": "A1",
        "explanation": "'Kifak' (to male) and 'Kifik' (to female) is the quintessential Lebanese way to say 'How are you?'."
    },
    {
        "id": 2,
        "prompt_ar": "شو يعني كلمة 'بدي' باللبناني؟",
        "prompt_translit": "Shou ya3ni kilmet 'Baddi' bel lebnani?",
        "prompt_en": "What does the word 'Baddi' mean in Levantine Arabic?",
        "options": [
            {"arabic": "أنا أريد (I want)", "translit": "I want", "english": "I want"},
            {"arabic": "أنا ذاهب (I am going)", "translit": "I am going", "english": "I am going"},
            {"arabic": "أنا مشغول (I am busy)", "translit": "I am busy", "english": "I am busy"},
            {"arabic": "أنا متعب (I am tired)", "translit": "I am tired", "english": "I am tired"}
        ],
        "correct_option_index": 0,
        "level_target": "A1",
        "explanation": "'Baddi' means 'I want' (e.g. Baddi ahwe = I want coffee)."
    },
    {
        "id": 3,
        "prompt_ar": "لما حدا يقدملك قهوة أو أكل، شو العبارة اللبنانية المناسبة لشكره؟",
        "prompt_translit": "Lamma 7ada y2addimlak ahwe aw akel, shou el 3ibara el lebnaniyeh el mounasbeh la shukro?",
        "prompt_en": "When someone serves you coffee or food, what is the best Lebanese phrase to thank them?",
        "options": [
            {"arabic": "يسلمو إيديك / صحتين", "translit": "Yislamo ideik / Sa7teyn", "english": "May your hands be blessed / Double health"},
            {"arabic": "شكراً جزيلاً يا أستاذ", "translit": "Shukran jazeelan", "english": "Formal standard Arabic"},
            {"arabic": "أهلاً بك", "translit": "Ahlan bik", "english": "Welcome to you"},
            {"arabic": "لا شكراً", "translit": "La shukran", "english": "No thanks"}
        ],
        "correct_option_index": 0,
        "level_target": "A2",
        "explanation": "'Yislamo ideik' (to male) or 'Yislamo ideiki' (to female) is the most polite cultural response for receiving food/drink."
    },
    {
        "id": 4,
        "prompt_ar": "كيف بتنفي الفعل المضارع باللبناني؟ (مثلاً: I don't know)",
        "prompt_translit": "Kif btenfi el fe3el el modare3 bel lebnani? (Masalan: I don't know)",
        "prompt_en": "How do you negate a verb in Levantine Arabic? (e.g., 'I don't know')",
        "options": [
            {"arabic": "ما بعرف", "translit": "Ma ba3ref", "english": "I don't know (using 'ma' + b-verb)"},
            {"arabic": "لا أعرف", "translit": "La a3rifu", "english": "Standard Arabic"},
            {"arabic": "مش أعرف", "translit": "Mish a3ref", "english": "Incorrect syntax"},
            {"arabic": "لن أعرف", "translit": "Lan a3rif", "english": "Formal future negative"}
        ],
        "correct_option_index": 0,
        "level_target": "A2",
        "explanation": "Verbs are negated using 'ما' (ma ba3ref, ma baddi), whereas adjectives and nouns use 'مش' (mish mnih, mish hon)."
    },
    {
        "id": 5,
        "prompt_ar": "شو بتعني عبارة 'على راسي' بلبنان؟",
        "prompt_translit": "Shou bte3ni 3ibaret '3ala rasi' bi Lebnen?",
        "prompt_en": "What does the cultural idiom '3ala rasi' (lit: on my head) mean?",
        "options": [
            {"arabic": "تكرم / من عيوني / بخدمتك", "translit": "At your service / Anything for you with pleasure", "english": "At your service / With pleasure"},
            {"arabic": "وجع راس", "translit": "Headache", "english": "Headache"},
            {"arabic": "أنا فوق الجميع", "translit": "I am above all", "english": "Arrogant statement"},
            {"arabic": "مع السلامة", "translit": "Goodbye", "english": "Goodbye"}
        ],
        "correct_option_index": 0,
        "level_target": "B1",
        "explanation": "'3ala rasi' signifies utter willingness to help and deep respect."
    },
    {
        "id": 6,
        "prompt_ar": "كيف بيحكوا الشباب ببيروت تحية مختلطة بثلاث لغات؟",
        "prompt_translit": "Kif bye7ko el shabab bi Beyrouth ta7iyeh mokhtalatah bi talat loughat?",
        "prompt_en": "What is the famous trilingual Lebanese greeting among young people in Beirut?",
        "options": [
            {"arabic": "Hi, kifak? Ça va?", "translit": "Hi, kifak? Sa va?", "english": "English 'Hi' + Arabic 'kifak' + French 'Ça va'"},
            {"arabic": "Good morning, كيف حالك؟", "translit": "Good morning, kayfa haluka?", "english": "Mixed formal"},
            {"arabic": "Bonjour ya habibi فقط", "translit": "Bonjour ya habibi", "english": "Only French/Arabic"},
            {"arabic": "السلام عليكم ورحمة الله", "translit": "Salam alaykum", "english": "Traditional Islamic greeting"}
        ],
        "correct_option_index": 0,
        "level_target": "B1",
        "explanation": "'Hi, kifak, ça va?' is the legendary Beirut code-switching greeting!"
    },
    {
        "id": 7,
        "prompt_ar": "شو بتعني كلمة 'هلق' أو 'هلأ' بالعامية اللبنانية؟",
        "prompt_translit": "Shou bte3ni kilmet 'Halla2' bel 3ammiyeh el lebnaniyeh?",
        "prompt_en": "What does 'Halla2' mean in Lebanese colloquial Arabic?",
        "options": [
            {"arabic": "الآن / في هذه اللحظة (Now / Right now)", "translit": "Halla2 = Now", "english": "Now / Right now"},
            {"arabic": "أمس (Yesterday)", "translit": "Mberih", "english": "Yesterday"},
            {"arabic": "غداً (Tomorrow)", "translit": "Boukra", "english": "Tomorrow"},
            {"arabic": "بعد قليل (Later)", "translit": "Ba3dein", "english": "Later"}
        ],
        "correct_option_index": 0,
        "level_target": "B2",
        "explanation": "'Halla2' (or Halla) means 'Now' in Lebanese (replaces MSA 'Al-Aan')."
    },
    {
        "id": 8,
        "prompt_ar": "شو معنى التعبير اللبناني 'طوّل بالك'؟",
        "prompt_translit": "Shou ma3na el ta3bir el lebnani 'Tawwel balak'?",
        "prompt_en": "What does the expression 'Tawwel balak' mean?",
        "options": [
            {"arabic": "رَوِّق واصبر وخلي أعصابك هادية (Be patient / Calm down)", "translit": "Be patient / Take it easy", "english": "Be patient / Calm down"},
            {"arabic": "فكّر بسرعة", "translit": "Think quickly", "english": "Think quickly"},
            {"arabic": "طوّل قامتك", "translit": "Grow taller", "english": "Grow taller"},
            {"arabic": "تكلّم بصوت عالٍ", "translit": "Speak loudly", "english": "Speak loudly"}
        ],
        "correct_option_index": 0,
        "level_target": "B2",
        "explanation": "'Tawwel balak' (to male) or 'Tawwli balik' (to female) literally means 'make your mind long' = be patient."
    }
]

async def process_chat(
    message: str,
    conversation_id: str,
    level: str,
    mode: str,
    scenario_id: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main chat pipeline: query AI, record messages, auto-extract vocab, update progress stats.
    """
    scenario_ctx = None
    if scenario_id:
        scenario = get_scenario_by_id(scenario_id)
        scenario_ctx = f"Scenario: {scenario['title_en']} ({scenario['location']}). Goal: {scenario['description']}"

    # Query LLM / Dialect Engine
    ai_response = await query_gemini_tutor(
        user_message=message,
        level=level,
        mode=mode,
        scenario_context=scenario_ctx,
        api_key=api_key
    )

    # Persist in DB
    record_user_message(
        conv_id=conversation_id,
        text=message,
        correction_data=ai_response.get("correction")
    )
    record_tutor_message(
        conv_id=conversation_id,
        text=ai_response.get("reply_arabic", ""),
        translit=ai_response.get("reply_transliteration", ""),
        translation=ai_response.get("reply_english", "")
    )

    # Auto-extract and save any unique Levantine words to Word Vault
    vocab_breakdowns: List[WordBreakdown] = []
    if ai_response.get("correction") and ai_response["correction"].get("vocabulary_breakdown"):
        for v in ai_response["correction"]["vocabulary_breakdown"]:
            vocab_breakdowns.append(WordBreakdown(
                arabic=v["arabic"],
                transliteration=v["transliteration"],
                english=v["english"],
                root_or_note=v.get("root_or_note")
            ))
            # Save into flashcards
            add_flashcard(
                arabic=v["arabic"],
                transliteration=v["transliteration"],
                english=v["english"],
                category="From Chat",
                notes=v.get("root_or_note", "")
            )

    # Generate high quality Lebanese female voice audio
    reply_ar = ai_response.get("reply_arabic", "")
    audio_url = ""
    if reply_ar:
        try:
            audio_url = await generate_lebanese_tts(reply_ar)
        except Exception as e:
            print(f"TTS generation error: {e}")

    return {
        "reply_arabic": reply_ar,
        "reply_transliteration": ai_response.get("reply_transliteration", ""),
        "reply_english": ai_response.get("reply_english", ""),
        "correction": ai_response.get("correction"),
        "conversation_id": conversation_id,
        "current_level": level,
        "suggested_replies": ai_response.get("suggested_replies", []),
        "vocabulary_highlight": [v.model_dump() for v in vocab_breakdowns],
        "cultural_note": ai_response.get("cultural_note"),
        "audio_url": audio_url
    }

def evaluate_diagnostic_assessment(answers: Dict[int, int]) -> AssessmentResult:
    """
    Evaluates the user's answers to determine their proficiency tier:
    - 0-25%: A0 (Absolute Beginner)
    - 26-50%: A1 (Elementary)
    - 51-70%: A2 (Pre-Intermediate)
    - 71-85%: B1 (Intermediate)
    - 86-95%: B2 (Upper Intermediate)
    - 96-100%: C1 (Advanced / Near-Native)
    """
    total = len(DIAGNOSTIC_QUESTIONS)
    correct_count = 0

    for q in DIAGNOSTIC_QUESTIONS:
        qid = q["id"]
        selected = answers.get(qid)
        if selected is not None and selected == q["correct_option_index"]:
            correct_count += 1

    pct = (correct_count / total) * 100.0

    if pct <= 25:
        assessed_lvl = "A0"
        desc = "A0 - Absolute Beginner: Starting your journey! We'll provide full Arabizi phonetics, word-by-word breakdowns, and easy foundational greetings."
        strengths = ["Enthusiasm to learn authentic Lebanese Arabic!"]
        focus = ["Basic greetings (Marhaba, Kifak, Yislamo)", "Essential food & drink vocabulary", "Arabizi phonetic numbers (3, 7, 2, 5)"]
        recommended_scenarios = ["beirut_cafe"]
    elif pct <= 50:
        assessed_lvl = "A1"
        desc = "A1 - Elementary Learner: You recognize basic Lebanese greetings and core vocabulary like 'Baddi' and 'Kifak'."
        strengths = ["Familiarity with common Levantine greetings", "Understanding basic daily requests"]
        focus = ["Present continuous tense (3am + verb)", "Levantine negation (mish vs ma)", "Ordering at cafes & restaurants"]
        recommended_scenarios = ["beirut_cafe", "service_taxi"]
    elif pct <= 70:
        assessed_lvl = "A2"
        desc = "A2 - Pre-Intermediate: Good command of everyday phrasing, politeness formulas, and basic directional/commerce vocabulary."
        strengths = ["Solid foundation in Lebanese social etiquette (Yislamo, Sahteyn)", "Bargaining and taxi navigation basics"]
        focus = ["Verb conjugations across all pronouns", "Expanded adjectives (Mnih, Ktiir, Helo)", "Past and future tense in Levantine"]
        recommended_scenarios = ["souk_bargaining", "service_taxi"]
    elif pct <= 85:
        assessed_lvl = "B1"
        desc = "B1 - Intermediate: Strong grasp of Levantine conversational rhythm, Beirut slang, and cultural idioms ('3ala rasi', 'Shou fi ma fi')."
        strengths = ["Natural use of Lebanese colloquial phrases", "Comfortable with code-switching and social nuances"]
        focus = ["Expressing nuanced opinions and storytelling", "Deep Lebanese idioms and proverbs", "Speed and pronunciation fluidity"]
        recommended_scenarios = ["family_dinner", "beirut_startup_office"]
    else:
        assessed_lvl = "B2"
        desc = "B2/C1 - Advanced Speaker: Fluent mastery of Levantine dialect subtleties, humorous expressions, and cultural fluidity!"
        strengths = ["High dialect accuracy and cultural instinct", "Flawless distinction between Fusha and Lebanese"]
        focus = ["Complex debate topics", "Fast colloquial banter", "Mastering regional Levantine accents (Beirut, Mount Lebanon, Tripoli)"]
        recommended_scenarios = ["family_dinner", "beirut_startup_office", "souk_bargaining"]

    # Update profile with assessed level
    update_profile({"level": assessed_lvl, "average_fluency": int(pct)})

    return AssessmentResult(
        assessed_level=assessed_lvl,
        score_percentage=pct,
        total_correct=correct_count,
        total_questions=total,
        level_description=desc,
        strengths=strengths,
        focus_areas=focus,
        recommended_scenarios=recommended_scenarios
    )
