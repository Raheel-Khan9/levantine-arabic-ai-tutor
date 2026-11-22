"""
Database persistence layer using SQLite for Ahlan AI Levantine Arabic Tutor.
Stores user profile, conversation history, and Word Vault / Spaced Repetition flashcards.
"""
import sqlite3
import json
import os
from datetime import datetime, date
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tutor.db")

# Initial starter Levantine Flashcards
INITIAL_FLASHCARDS = [
    {
        "arabic": "يعطيك العافية",
        "transliteration": "Ya3tik el 3afye",
        "english": "May God give you health / Hello / Thank you (to workers)",
        "dialect_category": "Greetings",
        "example_ar": "يعطيك العافية يا عمي، قديش الحساب؟",
        "example_translit": "Ya3tik el 3afye ya 3ammo, addeish el hseib?",
        "example_en": "God give you health sir, how much is the bill?",
        "notes": "Essential Lebanese greeting used daily with anyone working, taxi drivers, shopkeepers."
    },
    {
        "arabic": "يسلمو إيديك",
        "transliteration": "Yislamo ideik (m) / Yislamo ideiki (f)",
        "english": "Thank you (lit: May your hands be blessed)",
        "dialect_category": "Etiquette",
        "example_ar": "يسلمو إيديك ع القهوة الطيبة!",
        "example_translit": "Yislamo ideik 3al ahwe el tayybeh!",
        "example_en": "Bless your hands for the delicious coffee!",
        "notes": "Said when someone serves you food, drinks, or hands you something."
    },
    {
        "arabic": "تكرم عينك",
        "transliteration": "Tekram 3aynak (m) / Tekram 3aynik (f) / Tekram",
        "english": "You're welcome / With pleasure (lit: honored eye)",
        "dialect_category": "Etiquette",
        "example_ar": "بدي كبّاية ماي؟ - تكرم عينك هلق بجيبلك.",
        "example_translit": "Baddi kebbeyet may? - Tekram 3aynak halla2 bjiblak.",
        "example_en": "Can I have a glass of water? - With pleasure, I'll bring it right now.",
        "notes": "The most polite and gracious Lebanese way of saying 'You're welcome'."
    },
    {
        "arabic": "شو في ما في؟",
        "transliteration": "Shou fi ma fi?",
        "english": "What's up? What's going on?",
        "dialect_category": "Greetings",
        "example_ar": "أهلين يا خيي! شو في ما في اليوم؟",
        "example_translit": "Ahlein ya khayye! Shou fi ma fi el yom?",
        "example_en": "Welcome bro! What's going on today?",
        "notes": "Everyday casual Lebanese expression among friends."
    },
    {
        "arabic": "على راسي",
        "transliteration": "3ala rasi",
        "english": "At your service / Anything for you (lit: On my head)",
        "dialect_category": "Expressions",
        "example_ar": "فيك تساعدني؟ - ع راسي ومن عيوني!",
        "example_translit": "Fik tsa3edni? - 3ala rasi w min 3youni!",
        "example_en": "Can you help me? - At your service and gladly!",
        "notes": "Expresses total willingness to do a favor with deep respect."
    },
    {
        "arabic": "ولا يهمك",
        "transliteration": "Wala yhemak (m) / Wala yhemik (f)",
        "english": "Don't worry about it / No problem at all",
        "dialect_category": "Expressions",
        "example_ar": "آسف تأخرت شوي. - ولا يهمك، ما صار شي.",
        "example_translit": "Asef t2akhart chway. - Wala yhemak, ma sar shi.",
        "example_en": "Sorry I'm a bit late. - Don't worry at all, everything is fine.",
        "notes": "Instant Lebanese phrase for calming an apology or mishap."
    },
    {
        "arabic": "صحتين وهنا",
        "transliteration": "Sa7teyn w hana",
        "english": "Bon appétit / Double health",
        "dialect_category": "Food & Drink",
        "example_ar": "تفضل دوق التبولة، صحتين وهنا!",
        "example_translit": "Tfaddal dou2 el tabbouleh, sa7teyn w hana!",
        "example_en": "Please taste the tabbouleh, bon appétit!",
        "notes": "Said to anyone who is eating or drinking."
    },
    {
        "arabic": "منقوشة زعتر",
        "transliteration": "Manousheh zaatar",
        "english": "Lebanese thyme and olive oil flatbread",
        "dialect_category": "Food & Drink",
        "example_ar": "بدي منقوشة زعتر إكسترا مع كاسة شاي.",
        "example_translit": "Baddi manousheh zaatar extra ma3 keset shay.",
        "example_en": "I want an extra zaatar manousheh with a cup of tea.",
        "notes": "The quintessential Lebanese breakfast item!"
    },
    {
        "arabic": "قديش الحساب؟",
        "transliteration": "Addeish el hseib?",
        "english": "How much is the bill?",
        "dialect_category": "Daily Life",
        "example_ar": "لو سمحت يا ويتر، قديش الحساب كله؟",
        "example_translit": "Law sama7et ya waiter, addeish el hseib kello?",
        "example_en": "Excuse me waiter, how much is the total bill?",
        "notes": "Notice 'Addeish' replaces the formal 'Kam'."
    },
    {
        "arabic": "طوّل بالك",
        "transliteration": "Tawwel balak (m) / Tawwli balik (f)",
        "english": "Be patient / Take it easy / Relax",
        "dialect_category": "Expressions",
        "example_ar": "طوّل بالك يا خيي، كل شي رح ينحل.",
        "example_translit": "Tawwel balak ya khayye, kel shi rah yen7al.",
        "example_en": "Be patient my brother, everything will be solved.",
        "notes": "Common phrase used to de-escalate tension or advise patience."
    }
]

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # User Profile table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile (
        id TEXT PRIMARY KEY,
        name TEXT,
        level TEXT,
        dialect TEXT,
        streak_days INTEGER,
        last_active_date TEXT,
        total_messages INTEGER,
        words_learned INTEGER,
        average_fluency INTEGER,
        daily_goal_minutes INTEGER,
        minutes_practiced_today INTEGER,
        api_key_configured INTEGER DEFAULT 0
    )
    """)

    # Messages / Conversation History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        conversation_id TEXT,
        sender TEXT,
        text TEXT,
        transliteration TEXT,
        translation TEXT,
        correction_json TEXT,
        timestamp TEXT
    )
    """)

    # Flashcards / Word Vault
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (
        id TEXT PRIMARY KEY,
        arabic TEXT UNIQUE,
        transliteration TEXT,
        english TEXT,
        dialect_category TEXT,
        example_ar TEXT,
        example_translit TEXT,
        example_en TEXT,
        notes TEXT,
        mastery_level INTEGER DEFAULT 0,
        times_reviewed INTEGER DEFAULT 0,
        last_reviewed TEXT
    )
    """)

    # Insert default profile if not exists
    cursor.execute("SELECT COUNT(*) FROM profile WHERE id = 'user_default'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO profile (id, name, level, dialect, streak_days, last_active_date, total_messages, words_learned, average_fluency, daily_goal_minutes, minutes_practiced_today)
        VALUES ('user_default', 'Habibi Learner', 'A1', 'Lebanese / Levantine', 1, ?, 0, 10, 88, 15, 5)
        """, (str(date.today()),))

    # Insert initial flashcards if empty
    cursor.execute("SELECT COUNT(*) FROM flashcards")
    if cursor.fetchone()[0] == 0:
        for idx, card in enumerate(INITIAL_FLASHCARDS):
            card_id = f"card_{idx+1}"
            cursor.execute("""
            INSERT OR IGNORE INTO flashcards (id, arabic, transliteration, english, dialect_category, example_ar, example_translit, example_en, notes, mastery_level, times_reviewed, last_reviewed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, ?)
            """, (card_id, card["arabic"], card["transliteration"], card["english"], card["dialect_category"], card["example_ar"], card["example_translit"], card["example_en"], card["notes"], datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

def get_profile() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile WHERE id = 'user_default'")
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {
        "id": "user_default",
        "name": "Habibi Learner",
        "level": "A1",
        "dialect": "Lebanese / Levantine",
        "streak_days": 1,
        "total_messages": 0,
        "words_learned": 10,
        "average_fluency": 85,
        "daily_goal_minutes": 15,
        "minutes_practiced_today": 5
    }

def update_profile(updates: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for k, v in updates.items():
        fields.append(f"{k} = ?")
        values.append(v)
    values.append("user_default")
    query = f"UPDATE profile SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()

def record_user_message(conv_id: str, text: str, translit: str = "", translation: str = "", correction_data: Optional[Dict[str, Any]] = None):
    conn = get_connection()
    cursor = conn.cursor()
    msg_id = f"msg_{datetime.utcnow().timestamp()}"
    corr_json = json.dumps(correction_data) if correction_data else None
    cursor.execute("""
    INSERT INTO messages (id, conversation_id, sender, text, transliteration, translation, correction_json, timestamp)
    VALUES (?, ?, 'user', ?, ?, ?, ?, ?)
    """, (msg_id, conv_id, text, translit, translation, corr_json, datetime.utcnow().isoformat()))
    
    # Increment total messages in profile
    cursor.execute("UPDATE profile SET total_messages = total_messages + 1 WHERE id = 'user_default'")
    conn.commit()
    conn.close()

def record_tutor_message(conv_id: str, text: str, translit: str = "", translation: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    msg_id = f"msg_{datetime.utcnow().timestamp()}"
    cursor.execute("""
    INSERT INTO messages (id, conversation_id, sender, text, transliteration, translation, timestamp)
    VALUES (?, ?, 'tutor', ?, ?, ?, ?)
    """, (msg_id, conv_id, text, translit, translation, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_conversation_history(conv_id: str, limit: int = 30) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC LIMIT ?
    """, (conv_id, limit))
    rows = cursor.fetchall()
    conn.close()
    result = []
    for r in rows:
        item = dict(r)
        if item.get("correction_json"):
            try:
                item["correction"] = json.loads(item["correction_json"])
            except Exception:
                item["correction"] = None
        result.append(item)
    return result

def get_all_flashcards() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flashcards ORDER BY mastery_level ASC, id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_flashcard(arabic: str, transliteration: str, english: str, category: str = "General", notes: str = "", example_ar: str = "", example_translit: str = "", example_en: str = "") -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    card_id = f"card_{datetime.utcnow().timestamp()}"
    cursor.execute("""
    INSERT OR REPLACE INTO flashcards (id, arabic, transliteration, english, dialect_category, example_ar, example_translit, example_en, notes, mastery_level, times_reviewed, last_reviewed)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?)
    """, (card_id, arabic, transliteration, english, category, example_ar, example_translit, example_en, notes, datetime.utcnow().isoformat()))
    
    cursor.execute("UPDATE profile SET words_learned = (SELECT COUNT(*) FROM flashcards) WHERE id = 'user_default'")
    conn.commit()
    conn.close()
    return {"id": card_id, "arabic": arabic, "transliteration": transliteration, "english": english}

def update_flashcard_review(card_id: str, rating: str) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flashcards WHERE id = ?", (card_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"success": False, "error": "Card not found"}
    
    current_mastery = row["mastery_level"]
    times_reviewed = row["times_reviewed"] + 1

    if rating == "easy":
        new_mastery = min(5, current_mastery + 2)
    elif rating == "good":
        new_mastery = min(5, current_mastery + 1)
    elif rating == "hard":
        new_mastery = max(0, current_mastery - 1)
    else: # "again"
        new_mastery = 0

    cursor.execute("""
    UPDATE flashcards SET mastery_level = ?, times_reviewed = ?, last_reviewed = ?
    WHERE id = ?
    """, (new_mastery, times_reviewed, datetime.utcnow().isoformat(), card_id))
    
    conn.commit()
    conn.close()
    return {"success": True, "new_mastery": new_mastery, "times_reviewed": times_reviewed}

# Initialize on module load
init_db()
