"""
Automated Test Suite for Ahlan AI Levantine Arabic Tutor backend
"""
import sys
import os
import json

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure project root is in sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_endpoints():
    print("Running Backend Verification Tests...\n")

    # 1. Test Scenarios Endpoint
    res = client.get("/api/scenarios")
    assert res.status_code == 200, f"Scenarios failed: {res.status_code}"
    scenarios = res.json().get("scenarios", [])
    assert len(scenarios) >= 5, "Expected at least 5 scenarios"
    print(f"[PASS] Scenarios Endpoint: {len(scenarios)} cultural scenarios loaded successfully.")

    # 2. Test Flashcards Endpoint
    res = client.get("/api/flashcards")
    assert res.status_code == 200, f"Flashcards failed: {res.status_code}"
    flashcards = res.json().get("flashcards", [])
    assert len(flashcards) >= 10, "Expected at least 10 starter flashcards"
    print(f"[PASS] Flashcards & Word Vault: {len(flashcards)} flashcards loaded.")

    # 3. Test Profile Endpoint
    res = client.get("/api/profile")
    assert res.status_code == 200, f"Profile failed: {res.status_code}"
    profile = res.json().get("profile", {})
    assert profile.get("dialect") == "Lebanese / Levantine", "Profile dialect mismatch"
    print(f"[PASS] User Profile Endpoint: Profile loaded (Level: {profile.get('level')}).")

    # 4. Test Diagnostic Assessment Questions
    res = client.get("/api/assessment/questions")
    assert res.status_code == 200, f"Assessment questions failed: {res.status_code}"
    questions = res.json().get("questions", [])
    assert len(questions) == 8, f"Expected 8 questions, got {len(questions)}"
    print(f"[PASS] Diagnostic Placement Test: {len(questions)} evaluation questions loaded.")

    # 5. Test Chat with MSA Correction (User says 'ماذا تريد' instead of 'شو بدك')
    payload = {
        "message": "ماذا تريد أن تشرب؟ أريد قهوة",
        "conversation_id": "test_conv",
        "level": "A1",
        "mode": "free_chat"
    }
    res = client.post("/api/chat", json=payload)
    assert res.status_code == 200, f"Chat failed: {res.status_code}"
    chat_data = res.json()
    assert chat_data.get("reply_arabic"), "Expected Arabic reply"
    assert chat_data.get("reply_transliteration"), "Expected Arabizi transliteration"
    assert chat_data.get("reply_english"), "Expected English translation"
    assert chat_data.get("correction"), "Expected correction data"
    assert chat_data["correction"]["has_correction"] is True, "Expected MSA correction trigger"
    print(f"[PASS] Chat & Dialect Correction Engine:")
    print(f"   Input:      {payload['message']}")
    print(f"   Tutor:      {chat_data['reply_arabic']}")
    print(f"   Arabizi:    {chat_data['reply_transliteration']}")
    print(f"   Correction: {chat_data['correction']['explanation']}")

    # 6. Test Pronunciation Evaluator
    pron_payload = {
        "target_phrase": "بدي فنجان قهوة وسط لو سمحت",
        "user_spoken": "بدي فنجان قهوة وسط"
    }
    res = client.post("/api/pronunciation/evaluate", json=pron_payload)
    assert res.status_code == 200, f"Pronunciation failed: {res.status_code}"
    pron_data = res.json()
    assert pron_data.get("target_translit"), "Expected translit"
    assert len(pron_data.get("phonetic_tips", [])) > 0, "Expected phonetic tips"
    print(f"[PASS] Pronunciation & Lahjeh Coach Evaluator: {pron_data['phonetic_tips'][0]}")

    # 7. Test Diagnostic Submit
    submit_payload = {
        "answers": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    }
    res = client.post("/api/assessment/submit", json=submit_payload)
    assert res.status_code == 200, f"Submit failed: {res.status_code}"
    submit_res = res.json()
    assert submit_res.get("score_percentage") == 100.0, "Expected 100% score"
    print(f"[PASS] Assessment Submission Evaluated: Level {submit_res.get('assessed_level')} ({submit_res.get('score_percentage')}%)")

    # 8. Test Expressions
    res = client.get("/api/expressions")
    assert res.status_code == 200
    exprs = res.json().get("expressions", [])
    assert len(exprs) > 5
    print(f"[PASS] Lebanese Idioms & Expressions: {len(exprs)} cultural idioms loaded.")

    print("\n ALL 8 VERIFICATION TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_endpoints()
