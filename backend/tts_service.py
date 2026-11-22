"""
High-Definition Lebanese Female Voice Text-to-Speech (TTS) Engine
Uses Microsoft Edge TTS Neural voice: ar-LB-LaylaNeural (Lebanese Arabic Female).
"""
import os
import hashlib
import asyncio
from pathlib import Path
from typing import Optional

AUDIO_CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "audio"
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_VOICE = "ar-LB-LaylaNeural" # Authentic Lebanese Female Voice

async def generate_lebanese_tts(text: str, voice: str = DEFAULT_VOICE, rate: str = "+0%") -> str:
    """
    Generates an MP3 audio file for the given Arabic text using the authentic Lebanese female neural voice.
    Returns the relative path / filename of the cached audio.
    """
    import edge_tts

    if not text or not text.strip():
        return ""

    # Clean text from English/parentheses for cleaner Arabic pronunciation
    cleaned_text = text.strip()

    # Generate deterministic cache filename based on text and voice
    text_hash = hashlib.md5(f"{cleaned_text}_{voice}_{rate}".encode('utf-8')).hexdigest()
    filename = f"tts_{text_hash}.mp3"
    filepath = AUDIO_CACHE_DIR / filename

    if filepath.exists() and filepath.stat().st_size > 1000:
        return f"/api/audio/{filename}"

    try:
        communicate = edge_tts.Communicate(cleaned_text, voice=voice, rate=rate)
        await communicate.save(str(filepath))
        return f"/api/audio/{filename}"
    except Exception as e:
        print(f"Error generating Edge TTS: {e}")
        # Fallback to general Levantine/Arabic voice if specific voice has network glitch
        try:
            communicate = edge_tts.Communicate(cleaned_text, voice="ar-SY-AmanyNeural", rate=rate)
            await communicate.save(str(filepath))
            return f"/api/audio/{filename}"
        except Exception as e2:
            print(f"Fallback TTS failed: {e2}")
            return ""

def get_audio_file_path(filename: str) -> Optional[Path]:
    filepath = AUDIO_CACHE_DIR / filename
    if filepath.exists():
        return filepath
    return None
