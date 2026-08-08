"""
Automated tests for NotesbyAI.

These tests mock the Gemini API entirely, so the suite runs in CI
without needing a real GEMINI_API_KEY or making network calls.

Run with:
    pytest
"""

import json
from unittest.mock import MagicMock

import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Frontend route
# ---------------------------------------------------------------------------

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Study" in response.data


# ---------------------------------------------------------------------------
# Input validation on /generate
# ---------------------------------------------------------------------------

def test_generate_rejects_empty_input(client, monkeypatch):
    monkeypatch.setattr(app_module, "GEMINI_API_KEY", "fake-key-for-testing")
    response = client.post("/generate", data={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_generate_rejects_short_text(client, monkeypatch):
    monkeypatch.setattr(app_module, "GEMINI_API_KEY", "fake-key-for-testing")
    response = client.post("/generate", data={"text": "too short"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_missing_api_key_returns_clear_error(client, monkeypatch):
    monkeypatch.setattr(app_module, "GEMINI_API_KEY", "")
    response = client.post(
        "/generate", data={"text": "a" * 50}
    )
    assert response.status_code == 400
    assert "API key" in response.get_json()["error"]


# ---------------------------------------------------------------------------
# Successful generation (Gemini call mocked)
# ---------------------------------------------------------------------------

FAKE_AI_JSON = {
    "summary": "This is a fake test summary of the material.",
    "key_points": ["Point one", "Point two", "Point three"],
    "mcqs": [
        {
            "question": "What is being tested?",
            "options": ["A. Nothing", "B. The API", "C. The moon", "D. Coffee"],
            "answer": "B",
        }
    ],
    "viva_questions": [
        {"question": "Why do we mock the AI in tests?", "answer": "To avoid real network calls."}
    ],
}


def test_generate_success_with_mocked_ai(client, monkeypatch):
    monkeypatch.setattr(app_module, "GEMINI_API_KEY", "fake-key-for-testing")

    fake_response = MagicMock()
    fake_response.text = json.dumps(FAKE_AI_JSON)

    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    monkeypatch.setattr(app_module, "client", fake_client)

    response = client.post(
        "/generate",
        data={"text": "Mitochondria are the powerhouse of the cell. " * 5},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert set(["summary", "key_points", "mcqs", "viva_questions"]).issubset(data.keys())
    assert data["summary"] == FAKE_AI_JSON["summary"]
    assert len(data["mcqs"]) == 1


# ---------------------------------------------------------------------------
# JSON cleaning helper
# ---------------------------------------------------------------------------

def test_clean_json_response_strips_markdown_fences():
    raw = "```json\n" + json.dumps({"summary": "ok"}) + "\n```"
    result = app_module.clean_json_response(raw)
    assert result == {"summary": "ok"}


def test_clean_json_response_handles_plain_json():
    raw = json.dumps({"summary": "no fences here"})
    result = app_module.clean_json_response(raw)
    assert result == {"summary": "no fences here"}
