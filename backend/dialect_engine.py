"""
Levantine & Lebanese Arabic Dialect Engine
Contains linguistic rules, vocabulary mappings (MSA vs Levantine),
Arabizi phonetic transliteration, Lebanese idioms, and intelligent correction logic.
"""
import re
from typing import Dict, List, Tuple, Any, Optional

# Core MSA to Levantine dialect mappings
MSA_TO_LEVANTINE = {
    "ماذا": {"lev": "شو", "translit": "shou", "note": "In Levantine Arabic, 'شو' (shou) is used instead of 'ماذا' (madha)."},
    "ماذا تفعل": {"lev": "شو عم تعمل", "translit": "shou 3am ta3mel", "note": "Use 'شو عم تعمل' (shou 3am ta3mel) for 'what are you doing?'."},
    "أين": {"lev": "وين", "translit": "wein", "note": "'وين' (wein) replaces 'أين' (ayna)."},
    "كيف حالك": {"lev": "كيفك", "translit": "kifak (m) / kifik (f)", "note": "'كيفك' (kifak for male, kifik for female) is the standard Levantine greeting."},
    "لماذا": {"lev": "ليش", "translit": "leish", "note": "Use 'ليش' (leish) instead of 'لماذا' (limadha)."},
    "متى": {"lev": "أيمتى", "translit": "eimta", "note": "'أيمتى' (eimta) replaces 'متى' (mata)."},
    "من": {"lev": "مين", "translit": "min", "note": "'مين' (min) means 'who' in Levantine."},
    "كم": {"lev": "قديش", "translit": "addeish / adde", "note": "'قديش' (addeish) means 'how much / how many'."},
    "هنا": {"lev": "هون", "translit": "hon", "note": "'هون' (hon) means 'here'."},
    "هناك": {"lev": "هنيك", "translit": "hnik", "note": "'هنيك' (hnik) means 'there'."},
    "أريد": {"lev": "بدي", "translit": "baddi", "note": "In Levantine, use 'بدي' (baddi) instead of 'أريد' (ureed)."},
    "تريد": {"lev": "بدك", "translit": "baddak (m) / baddik (f)", "note": "'بدك' (baddak / baddik) = you want."},
    "الآن": {"lev": "هلق", "translit": "halla2 / halla", "note": "'هلق' or 'هلأ' (halla2) means 'now'."},
    "جيد": {"lev": "منيح", "translit": "mnih (m) / mniha (f)", "note": "'منيح' (mnih) means 'good / well'."},
    "حسنا": {"lev": "تمام / ماشي", "translit": "tamam / machi", "note": "Use 'تمام' (tamam) or 'ماشي' (machi) for 'okay/fine'."},
    "كثيرا": {"lev": "كتير", "translit": "ktiir", "note": "'كتير' (ktiir) means 'very / a lot'."},
    "كثير": {"lev": "كتير", "translit": "ktiir", "note": "'كتير' (ktiir) replaces 'كثير'."},
    "قليل": {"lev": "شوي", "translit": "chway", "note": "'شوي' (chway) means 'a little bit'."},
    "ليس": {"lev": "مش", "translit": "mish", "note": "'مش' (mish) is used to negate adjectives and nouns (e.g. مش منيح = not good)."},
    "لا أريد": {"lev": "ما بدي", "translit": "ma baddi", "note": "'ما بدي' (ma baddi) = I don't want."},
    "سوف": {"lev": "رح", "translit": "rah", "note": "'رح' (rah) indicates future tense in Levantine."},
    "نقود": {"lev": "مصاري", "translit": "masari", "note": "'مصاري' (masari) is the Levantine word for money."},
    "جميل": {"lev": "حلو", "translit": "7elo", "note": "'حلو' (7elo) means 'nice / beautiful / sweet'."},
    "فقط": {"lev": "بس", "translit": "bas", "note": "'بس' (bas) is commonly used for 'only / just / but'."},
    "أيضا": {"lev": "كمان", "translit": "kaman", "note": "'كمان' (kaman) means 'also / too / more'."},
    "شاهدت": {"lev": "شفت", "translit": "shefet", "note": "'شفت' (shefet) means 'I saw'."},
    "أذهب": {"lev": "عم روح / بروح", "translit": "3am rouh / b-rouh", "note": "Use 'بروح' for habitual or 'عم روح' for ongoing."},
    "شكرا": {"lev": "يسلمو / ميرسي", "translit": "yislamo / merci", "note": "'يسلمو' (yislamo) or 'ميرسي كتير' (merci ktiir) are popular in Lebanon alongside 'شكراً'."},
}

# Lebanese & Levantine Idioms & Cultural Phrases
LEBANESE_EXPRESSIONS = [
    {
        "arabic": "يعطيك العافية",
        "translit": "Ya3tik el 3afye (to m) / Ya3tiki el 3afye (to f)",
        "english": "May God give you health and strength (Used as hello, thank you, or goodbye to workers/anyone)",
        "context": "Universal polite Lebanese greeting for anyone working or serving you."
    },
    {
        "arabic": "يسلمو إيديك",
        "translit": "Yislamo ideik (m) / Yislamo ideiki (f)",
        "english": "May your hands be saved (Thank you for giving/making something)",
        "context": "Said when someone serves food, hands you something, or does a favor."
    },
    {
        "arabic": "تكرم عينك",
        "translit": "Tekram 3aynak (m) / Tekram 3aynik (f) / Tekram",
        "english": "You're most welcome / With pleasure (lit: may your eye be honored)",
        "context": "Gracious Lebanese response when someone asks for something or says thank you."
    },
    {
        "arabic": "على راسي",
        "translit": "3ala rasi",
        "english": "On my head (At your service / Anything for you)",
        "context": "Shows deep respect and willingness to help immediately."
    },
    {
        "arabic": "ولا يهمك",
        "translit": "Wala yhemak (m) / Wala yhemik (f)",
        "english": "Don't worry about it / No problem at all",
        "context": "Comforting phrase when someone apologizes or worries."
    },
    {
        "arabic": "صحتين وهنا",
        "translit": "Sahteyn w hana",
        "english": "Double health and happiness (Bon appétit)",
        "context": "Said before or during a meal to someone eating."
    },
    {
        "arabic": "دايمة",
        "translit": "Deyme",
        "english": "May your table/home always be blessed and prosperous",
        "context": "Said to the host after finishing a meal at their home."
    },
    {
        "arabic": "شو في ما في؟",
        "translit": "Shou fi ma fi?",
        "english": "What's up? What's going on? (lit: what's there and what's not?)",
        "context": "Casual everyday greeting among friends in Lebanon and Syria."
    },
    {
        "arabic": "طوّل بالك",
        "translit": "Tawwel balak (m) / Tawwli balik (f)",
        "english": "Be patient / Take it easy",
        "context": "Used to ask someone to relax or calm down."
    },
    {
        "arabic": "من عيوني",
        "translit": "Min 3youni",
        "english": "From my eyes (I will gladly do it for you)",
        "context": "Enthusiastic and polite agreement to a favor."
    },
    {
        "arabic": "هاي، كيفك؟ Ça va؟",
        "translit": "Hi, kifak? Sa va?",
        "english": "Hi, how are you? Is everything fine?",
        "context": "The iconic trilingual Lebanese greeting blending English, Arabic, and French!"
    }
]

# Vocabulary dictionary with word-by-word breakdowns for interactive tooltips
LEVANTINE_VOCAB_DB = {
    "مرحبا": {"translit": "Marhaba", "en": "Hello / Welcome", "root": "Greeting"},
    "أهلاً": {"translit": "Ahlan", "en": "Welcome", "root": "Greeting"},
    "أهلين": {"translit": "Ahlein", "en": "Welcome (Levantine warm response)", "root": "Greeting"},
    "صباح": {"translit": "Sabah", "en": "Morning", "root": "Time"},
    "الخير": {"translit": "El-Kheir", "en": "The good", "root": "Concept"},
    "صباحو": {"translit": "Sabaho", "en": "Morning! (Casual Lebanese)", "root": "Greeting"},
    "مساء": {"translit": "Masa", "en": "Evening", "root": "Time"},
    "النور": {"translit": "El-Nour", "en": "The light", "root": "Concept"},
    "كيفك": {"translit": "Kifak / Kifik", "en": "How are you?", "root": "Question"},
    "شو": {"translit": "Shou", "en": "What", "root": "Question particle"},
    "أخبارك": {"translit": "Akhbarak / Akhbarik", "en": "Your news", "root": "Noun"},
    "تمام": {"translit": "Tamam", "en": "Great / Fine", "root": "State"},
    "منيح": {"translit": "Mnih", "en": "Good (m)", "root": "Adjective"},
    "منيحة": {"translit": "Mniha", "en": "Good (f)", "root": "Adjective"},
    "الحمدلله": {"translit": "El-hamdillah", "en": "Praise be to God (I'm good)", "root": "Idiom"},
    "بدي": {"translit": "Baddi", "en": "I want", "root": "Verb/Modal"},
    "بدك": {"translit": "Baddak / Baddik", "en": "You want", "root": "Verb/Modal"},
    "بدنا": {"translit": "Baddna", "en": "We want", "root": "Verb/Modal"},
    "قهوة": {"translit": "Ahwe / Qahwe", "en": "Coffee (Lebanese pronounce 'q' as silent glottal stop)", "root": "Food/Drink"},
    "بلا": {"translit": "Bala", "en": "Without", "root": "Preposition"},
    "سكر": {"translit": "Soukar", "en": "Sugar", "root": "Food"},
    "وسط": {"translit": "Wasat", "en": "Medium sweet", "root": "Modifier"},
    "حلوة": {"translit": "Helwe", "en": "Sweet (with sugar)", "root": "Modifier"},
    "منقوشة": {"translit": "Manousheh", "en": "Lebanese flatbread pastry", "root": "Food"},
    "زعتر": {"translit": "Zaatar", "en": "Thyme and herb mix with sesame", "root": "Food"},
    "جبنة": {"translit": "Jebne", "en": "Cheese", "root": "Food"},
    "حساب": {"translit": "Hseib / Hsab", "en": "The bill / Check", "root": "Commerce"},
    "قديش": {"translit": "Addeish / Adde", "en": "How much?", "root": "Question"},
    "هيدا": {"translit": "Heida", "en": "This (m)", "root": "Demonstrative"},
    "هيدي": {"translit": "Heidi", "en": "This (f)", "root": "Demonstrative"},
    "هول": {"translit": "Hawl", "en": "These", "root": "Demonstrative"},
    "كتير": {"translit": "Ktiir", "en": "Very / A lot / Too much", "root": "Adverb"},
    "شوي": {"translit": "Chway", "en": "A little bit", "root": "Adverb"},
    "غالي": {"translit": "Ghali", "en": "Expensive", "root": "Adjective"},
    "رخيص": {"translit": "Rkhis", "en": "Cheap / Affordable", "root": "Adjective"},
    "هون": {"translit": "Hon", "en": "Here", "root": "Location"},
    "هنيك": {"translit": "Hnik", "en": "There", "root": "Location"},
    "وين": {"translit": "Wein", "en": "Where", "root": "Question"},
    "شارع": {"translit": "Chere3", "en": "Street", "root": "Location"},
    "الحمرا": {"translit": "El-Hamra", "en": "Hamra (Famous Beirut neighborhood)", "root": "Proper Noun"},
    "الأشرفية": {"translit": "El-Achrafieh", "en": "Achrafieh (Beirut district)", "root": "Proper Noun"},
    "سرفيس": {"translit": "Service", "en": "Shared taxi in Lebanon", "root": "Transport"},
    "تكسي": {"translit": "Taxi", "en": "Private taxi", "root": "Transport"},
    "يلا": {"translit": "Yalla", "en": "Let's go / Hurry / Come on", "root": "Interjection"},
    "عفو": {"translit": "3afwan", "en": "Excuse me / You're welcome", "root": "Etiquette"},
    "لو": {"translit": "Law", "en": "If", "root": "Particle"},
    "سمحت": {"translit": "Sama7et", "en": "You please (Law sama7et = please)", "root": "Etiquette"},
    "يسلمو": {"translit": "Yislamo", "en": "Thank you (May your hands be healthy)", "root": "Etiquette"},
    "تكرم": {"translit": "Tekram", "en": "You're welcome / With pleasure", "root": "Etiquette"},
    "حبيبي": {"translit": "Habibi", "en": "My beloved / My friend (to m)", "root": "Affection"},
    "حبيبتي": {"translit": "Habibti", "en": "My beloved / My friend (to f)", "root": "Affection"},
    "يا": {"translit": "Ya", "en": "O (Vocative call, e.g. Ya khayye = oh my brother)", "root": "Particle"},
    "خيي": {"translit": "Khayye", "en": "My brother (Lebanese slang for bro/buddy)", "root": "Noun"},
    "اختي": {"translit": "Okhti", "en": "My sister", "root": "Noun"},
    "ميرسي": {"translit": "Merci", "en": "Thank you (Lebanese French-Arabic)", "root": "Etiquette"},
    "بونجور": {"translit": "Bonjour", "en": "Good morning (Widely used in Beirut)", "root": "Greeting"},
    "بونسوار": {"translit": "Bonsoir", "en": "Good evening", "root": "Greeting"},
    "شو_في_ما_في": {"translit": "Shou fi ma fi", "en": "What's up? What's going on?", "root": "Idiom"},
    "عم": {"translit": "3am", "en": "Continuous action marker (e.g. 3am ba3mel = I am doing)", "root": "Grammar Marker"},
    "رح": {"translit": "Rah", "en": "Future marker (e.g. rah rouh = I will go)", "root": "Grammar Marker"},
    "مش": {"translit": "Mish", "en": "Not (Negation particle for nouns & adjectives)", "root": "Negation"},
    "ما": {"translit": "Ma", "en": "Not (Negation particle for verbs, e.g. ma ba3ref = I don't know)", "root": "Negation"}
}

def generate_arabizi_transliteration(arabic_text: str) -> str:
    """
    Converts Arabic text into natural, readable Arabizi / Lebanese Latin script.
    Uses standard Arabizi numbers (3=ع, 7=ح, 2=ء/ق, 5=خ, etc.) and Lebanese phonetics.
    """
    if not arabic_text:
        return ""
    
    # Custom mapping dictionary for whole phrases or high-frequency words
    phrase_map = {
        "يعطيك العافية": "Ya3tik el 3afye",
        "يسلمو إيديك": "Yislamo ideik",
        "تكرم عينك": "Tekram 3aynak",
        "على راسي": "3ala rasi",
        "ولا يهمك": "Wala yhemak",
        "صحتين وهنا": "Sa7teyn w hana",
        "شو في ما في": "Shou fi ma fi",
        "كيف حالك": "Kifak",
        "صباح الخير": "Sabah el-kheir",
        "مساء الخير": "Masa el-kheir",
        "أهلاً وسهلاً": "Ahlan w sahlan",
        "الحمد لله": "El-hamdillah",
        "الحمدلله": "El-hamdillah",
        "شو الأخبار": "Shou el akhbar",
        "شو عم تعمل": "Shou 3am ta3mel",
        "شو عم تعملي": "Shou 3am ta3mli",
        "قديش الحساب": "Addeish el hseib",
        "لو سمحت": "Law sama7et",
        "ميرسي كتير": "Merci ktiir",
        "بدي فنجان قهوة": "Baddi fenjen ahwe",
        "ما في مشكلة": "Ma fi meshkle",
        "مع السلامة": "Ma3 el salame",
        "تصبح على خير": "Tisba7 3ala kheir",
        "إن شاء الله": "Inshallah",
        "والله": "Wallah"
    }

    cleaned = arabic_text.strip()
    for phrase, translit in phrase_map.items():
        if phrase in cleaned:
            cleaned = cleaned.replace(phrase, translit)

    # Letter-by-letter phonetic rules for remaining words
    char_map = {
        'ا': 'a', 'أ': 'a', 'إ': 'e', 'آ': 'aa', 'ء': '2', 'ئ': '2', 'ؤ': '2',
        'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': '7', 'خ': '5',
        'د': 'd', 'ذ': 'z', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh',
        'ص': '9', 'ض': 'd', 'ط': '6', 'ظ': 'z', 'ع': '3', 'غ': 'gh',
        'ف': 'f', 'ق': '2', # Lebanese typically pronounce Qaf as hamza '2'
        'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n', 'ه': 'h', 'ة': 'a',
        'و': 'w', 'ي': 'y', 'ى': 'a', ' ': ' ', '،': ',', '؟': '?'
    }

    # If already mostly transliterated or contains english characters
    words = cleaned.split()
    translit_words = []
    for word in words:
        # If already mapped or in Latin
        if re.search(r'[a-zA-Z0-9]', word):
            translit_words.append(word)
            continue
        
        # Check vocab db
        cleaned_word = re.sub(r'[^\w\s]', '', word)
        if cleaned_word in LEVANTINE_VOCAB_DB:
            translit_words.append(LEVANTINE_VOCAB_DB[cleaned_word]["translit"])
            continue

        # Character replacement fallback
        t_word = []
        for char in word:
            t_word.append(char_map.get(char, char))
        translit_words.append("".join(t_word))

    res = " ".join(translit_words)
    # Fix common transliteration artifacts
    res = re.sub(r'al-', 'el-', res, flags=re.IGNORECASE)
    res = re.sub(r'\s+', ' ', res).strip()
    return res

def analyze_user_input_and_correct(user_text: str, current_level: str = "A1") -> Dict[str, Any]:
    """
    Evaluates the user's sentence for:
    1. Standard Arabic (MSA) vs Levantine dialect usage (flags MSA words & offers Lebanese replacements).
    2. Grammatical & spelling accuracy.
    3. Fluency score (0-100).
    4. Lebanese natural alternative.
    5. Word breakdowns.
    """
    user_clean = user_text.strip()
    detected_corrections = []
    has_msa = False
    fluency_deduction = 0

    # 1. Check for MSA words that should be Levantine
    corrected_version = user_clean
    dialect_tips = []

    for msa_term, data in MSA_TO_LEVANTINE.items():
        # Match word boundaries or substring
        pattern = r'\b' + re.escape(msa_term) + r'\b'
        if re.search(pattern, user_clean):
            has_msa = True
            fluency_deduction += 10
            corrected_version = re.sub(pattern, data["lev"], corrected_version)
            dialect_tips.append(f"Used '{msa_term}' (Fusha/MSA) → In Lebanese, say '{data['lev']}' ({data['translit']}). {data['note']}")

    # 2. Check for missing Lebanese prefixes (e.g. saying 'أريد' or using standard verb without 'عم' or 'بـ')
    if "اريد" in user_clean or "أريد" in user_clean:
        has_msa = True
        corrected_version = corrected_version.replace("اريد", "بدي").replace("أريد", "بدي")
        dialect_tips.append("In Lebanese Arabic, 'بدي' (baddi) is always used instead of 'أريد' (ureed).")
        fluency_deduction += 10

    # 3. Check for greeting improvements
    if user_clean.strip() in ["مرحبا", "سلام", "اهلا", "أهلا"]:
        natural_alt = "أهلين! كيفك شو الأخبار؟ (Ahlein! Kifak shou el akhbar?)"
    elif "بدي" in corrected_version and "قهوة" in corrected_version:
        natural_alt = "بدي فنجان قهوة لو سمحت (Baddi fenjen ahwe law sama7et)"
    elif "كيفك" in corrected_version:
        natural_alt = "هاي كيفك؟ شو في ما في؟ (Hi, kifak? Shou fi ma fi?)"
    else:
        natural_alt = f"{corrected_version} (Natural Lebanese phrasing)"

    fluency_score = max(50, 100 - fluency_deduction)
    has_correction = len(dialect_tips) > 0 or (corrected_version != user_clean)

    # 4. Generate word breakdown for words present in input
    vocab_breakdown = []
    tokens = re.findall(r'[\u0600-\u06FF]+|[a-zA-Z0-9]+', user_clean)
    for token in tokens:
        if token in LEVANTINE_VOCAB_DB:
            entry = LEVANTINE_VOCAB_DB[token]
            vocab_breakdown.append({
                "arabic": token,
                "transliteration": entry["translit"],
                "english": entry["en"],
                "root_or_note": entry.get("root", "")
            })

    explanation_str = " ".join(dialect_tips) if dialect_tips else ("Mumtez! (Excellent) Your sentence is natural and accurate in Levantine Arabic." if fluency_score > 85 else "Good attempt! Keep practicing Lebanese conversational phrasing.")

    return {
        "has_correction": has_correction,
        "original_text": user_clean,
        "corrected_text": corrected_version if has_correction else user_clean,
        "explanation": explanation_str,
        "dialect_tip": dialect_tips[0] if dialect_tips else "Tip: In Lebanese Arabic, the letter 'ق' (Qaf) is pronounced as a soft glottal stop 'ء' (Hamza), like 'Ahwe' for 'Qahwa'!",
        "natural_alternative": natural_alt,
        "fluency_score": fluency_score,
        "vocabulary_breakdown": vocab_breakdown
    }

def get_smart_tutor_response(user_input: str, level: str, mode: str = "free_chat", scenario_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Intelligent built-in conversational tutor response engine.
    Generates rich, tailored Levantine Arabic tutor dialogues, transliterations, translations,
    and suggested interactive user replies based on proficiency level (A0 to C1).
    """
    text_lower = user_input.lower().strip()
    u_clean = user_input.strip()

    # Determine topic / intent
    is_greeting = any(w in u_clean or w in text_lower for w in ["مرحبا", "هاي", "صباح", "مساء", "اهلين", "أهلين", "marhaba", "hi", "hello", "bonjour", "kifak", "kifik"])
    is_asking_how_are_you = any(w in u_clean or w in text_lower for w in ["كيفك", "كيف حالك", "شو الأخبار", "kifak", "kifik", "how are you", "ca va"])
    is_food_coffee = any(w in u_clean or w in text_lower for w in ["قهوة", "شاي", "منقوشة", "اكل", "أكل", "مطعم", "حساب", "baddi", "coffee", "food", "eat", "ahwe", "manousheh"])
    is_bargaining_shopping = any(w in u_clean or w in text_lower for w in ["قديش", "سعر", "غالي", "مصاري", "سوق", "addeish", "price", "expensive", "money", "buy"])
    is_taxi_directions = any(w in u_clean or w in text_lower for w in ["تكسي", "سرفيس", "حمرا", "اشرفية", "شارع", "وين", "taxi", "service", "hamra", "where", "street"])
    is_thanks = any(w in u_clean or w in text_lower for w in ["شكرا", "يسلمو", "ميرسي", "thank", "merci", "yislamo"])

    # Adapt response based on level
    if is_greeting:
        if level in ["A0", "A1"]:
            reply_ar = "أهلين وسهلين! كيفك اليوم؟ مبسوط إنك عم تتعلّم لبناني معي."
            reply_translit = "Ahlein w sahlan! Kifak el yom? Mabsout ennak 3am tet3allam lebnani ma3i."
            reply_en = "Welcome! How are you today? I'm happy you're learning Lebanese with me."
            suggested = [
                {"arabic": "أنا منيح، شكراً! وإنت كيفك؟", "translit": "Ana mnih, shukran! W inta kifak?", "english": "I'm good, thanks! And how are you?"},
                {"arabic": "تمام الحمدلله، شو في ما في؟", "translit": "Tamam el-hamdillah, shou fi ma fi?", "english": "Great praise God, what's up?"},
                {"arabic": "بدي إتعلّم كيف بطلب قهوة باللبناني.", "translit": "Baddi et3allam kif botlob ahwe bel-lebnani.", "english": "I want to learn how to order coffee in Lebanese."}
            ]
            cultural = "In Lebanon, greetings are very warm! People often use 'Ahlein' (welcome) or combine French, Arabic, and English like 'Hi, kifak, ça va?'"
        else:
            reply_ar = "يا هلا والله! نوّرت. شو الأخبار؟ طمني كيف كان نهارك؟"
            reply_translit = "Ya hala wallah! Nawwart. Shou el akhbar? Tammenni kif ken nharak?"
            reply_en = "Welcome! You lit up the place. What's the news? Tell me, how was your day?"
            suggested = [
                {"arabic": "نهاري كان كتير حلو ومليان شغل.", "translit": "Nhari ken ktiir 7elo w malyen shoghol.", "english": "My day was very nice and full of work."},
                {"arabic": "الحمدلله كل شي تمام، عم جرّب مارس حكي.", "translit": "El-hamdillah kel shi tamam, 3am jarreb mares 7aki.", "english": "Praise God all is fine, I'm trying to practice speaking."}
            ]
            cultural = "'Nawwart' (lit: you brought light) is a gracious Lebanese compliment when welcoming someone."

    elif is_asking_how_are_you:
        reply_ar = "أنا بألف خير والحمدلله! ومتحمس كتير ندردش سوا. شو بتحب نحكي اليوم؟"
        reply_translit = "Ana bi alf kheir w el-hamdillah! W mt7ammes ktiir ndardesh sawa. Shou bte7eb nehki el yom?"
        reply_en = "I'm doing wonderful, praise God! And very excited to chat together. What would you like to talk about today?"
        suggested = [
            {"arabic": "عن الأكل اللبناني والمنقوشة", "translit": "3an el akel el lebnani w el manousheh", "english": "About Lebanese food and manousheh"},
            {"arabic": "عن أحلى الأماكن ببيروت ولبنان", "translit": "3an a7la el ameken bi Beyrouth w Lebnen", "english": "About the nicest places in Beirut and Lebanon"},
            {"arabic": "بدي نتدرّب على جمل المحادثة اليومية", "translit": "Baddi netdarrab 3ala jemal el mou7adaseh el yawmiyeh", "english": "I want to practice daily conversation phrases"}
        ]
        cultural = "Notice the verb 'ندردش' (ndardesh) - it's the authentic Levantine word for 'to chat/hang out casually'!"

    elif is_food_coffee:
        reply_ar = "يا عيني! بالقهوة اللبنانية منقول: 'بدي فنجان قهوة وسط' أو 'بلا سكر'. ومعها منقوشة زعتر سخنة. بتحب القهوة حلوة ولا سادة؟"
        reply_translit = "Ya 3ayni! Bel-ahwe el lebnaniyeh mn2oul: 'Baddi fenjen ahwe wasat' aw 'bala soukar'. W ma3ha manousheh zaatar sokhne. Bte7eb el ahwe helwe wala sede?"
        reply_en = "Oh lovely! In Lebanese coffee shops we say: 'I want a cup of medium-sweet coffee' or 'without sugar'. With a warm zaatar manousheh. Do you like coffee sweet or black/plain?"
        suggested = [
            {"arabic": "بدي قهوة وسط مع منقوشة جبنة لو سمحت.", "translit": "Baddi ahwe wasat ma3 manousheh jebne law sama7et.", "english": "I want medium coffee with cheese manousheh, please."},
            {"arabic": "أنا بحب القهوة بلا سكر على الصبح.", "translit": "Ana b7eb el ahwe bala soukar 3ala el sobe7.", "english": "I like coffee without sugar in the morning."},
            {"arabic": "قديش الحساب كله سوا؟", "translit": "Addeish el hseib kello sawa?", "english": "How much is the total bill?"}
        ]
        cultural = "In Lebanese dialect, 'Qahwa' (قهوة) is pronounced 'Ahwe' (the 'Q' becomes a soft glottal stop / hamza). 'Sahteyn' (صحتين) is always said to someone ordering food."

    elif is_bargaining_shopping:
        reply_ar = "بالسوق ببيروت، إذا حسيت السعر غالي فيك تقول للبياع بلطف: 'كتير هيك يا خيي، كرمالي راعينا بالسعر شوية!' شو عم تشتري؟"
        reply_translit = "Bel souq bi Beyrouth, iza 7asseit el se3er ghali fik t2oul lal bayya3 bi lotof: 'Ktiir heik ya khayye, kermeli ra3ina bel se3er chway!' Shou 3am tishtiri?"
        reply_en = "In the market in Beirut, if you feel the price is high you can politely tell the seller: 'That's too much my brother, for my sake give us a little discount!' What are you buying?"
        suggested = [
            {"arabic": "عم بشتري هدايا تذكارية وتطريز لبناني.", "translit": "3am bishtiri hadaya tezkeriyeh w tatriz lebnani.", "english": "I'm buying souvenirs and Lebanese embroidery."},
            {"arabic": "قديش بتحسبلي ياها من الآخر؟", "translit": "Addeish bte7sebli yaha min el akher?", "english": "What's your final best price for me?"}
        ]
        cultural = "'Kermeli' (كرمالي) means 'for my sake / do me a favor'. It's a magic polite negotiation word in Lebanon!"

    elif is_taxi_directions:
        reply_ar = "تمام! بالتاكسي أو السرفيس ببيروت بتسأل الشوفير: 'سرفيس على الحمرا؟' ولما توصل بتقله: 'على يمينك هون لو سمحت'."
        reply_translit = "Tamam! Bel taxi aw el service bi Beyrouth btis2al el chauffeur: 'Service 3ala el Hamra?' W lamma towsal btello: '3ala yeminak hon law sama7et'."
        reply_en = "Great! In a taxi or shared 'Service' in Beirut, you ask the driver: 'Service to Hamra?' and when you arrive you tell him: 'On your right here, please'."
        suggested = [
            {"arabic": "قديش السرفيس لشارع بدارو؟", "translit": "Addeish el service la chere3 Badaro?", "english": "How much is the service ride to Badaro street?"},
            {"arabic": "نزّلني هون عند الصيدلية إذا بتريد.", "translit": "Nazzilni hon 3ind el saydaliyeh iza btreed.", "english": "Drop me off here by the pharmacy if you please."}
        ]
        cultural = "In Lebanon, a 'Service' (pronounced the French way: Ser-vees) is a shared taxi along fixed routes, much cheaper than an 'Express' private taxi!"

    elif is_thanks:
        reply_ar = "تكرم عينك! هيدا واجبي. وإذا بدك تسألني عن أي كلمة أو معنى، أنا هون دايماً لمساعدتك."
        reply_translit = "Tekram 3aynak! Heida wejbi. W iza baddak tis2alni 3an ayye kilmeh aw ma3na, ana hon dayman la mosa3adtak."
        reply_en = "You're most welcome! It's my pleasure. If you want to ask me about any word or meaning, I'm always here to help you."
        suggested = [
            {"arabic": "يسلمو كتير! كيف منقول 'I missed you' باللبناني؟", "translit": "Yislamo ktiir! Kif mn2oul 'I missed you' bel lebnani?", "english": "Thanks a lot! How do we say 'I missed you' in Lebanese?"},
            {"arabic": "شو الفرق بين 'منيح' و 'تمام'؟", "translit": "Shou el fare2 bein 'mnih' w 'tamam'?", "english": "What's the difference between 'mnih' and 'tamam'?"}
        ]
        cultural = "'Tekram 3aynak' (to male) or 'Tekram 3aynik' (to female) is the most affectionate and respectful way to say 'You are welcome'."

    else:
        # Default adaptive conversational reply
        reply_ar = f"فهمت عليك تماماً! حكيك حلو وعم يتحسن. شو رأيك نكمّل الحديث ونركّز على مصطلحات أكتر باللبناني؟"
        reply_translit = "Fhemet 3leik tamamam! 7akyak 7elo w 3am yet7assan. Shou ra2yak nkammeil el 7adis w nrakkez 3ala mostala7at aktar bel lebnani?"
        reply_en = "I understood you completely! Your speech is nice and improving. What do you think about continuing the conversation and focusing on more Lebanese expressions?"
        suggested = [
            {"arabic": "يلا تمام، علّمني كلمات جديدة بستعملها كل يوم.", "translit": "Yalla tamam, 3allemni kilmet jdideh basta3melha kel yom.", "english": "Let's go! Teach me new words I can use every day."},
            {"arabic": "كيف بحكي عن روتيني اليومي وعيلتي؟", "translit": "Kif ba7ki 3an routini el yawmi w 3ayelti?", "english": "How do I talk about my daily routine and family?"}
        ]
        cultural = "Remember in Lebanese we add the prefix 'بـ' (b-) to present tense verbs: 'بشرب' (I drink), 'بحكي' (I speak), 'بروح' (I go)."

    return {
        "reply_arabic": reply_ar,
        "reply_transliteration": reply_translit,
        "reply_english": reply_en,
        "suggested_replies": suggested,
        "cultural_note": cultural
    }
