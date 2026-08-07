"""
AI Study Notes Generator - Backend
-----------------------------------
This Flask app takes study material (PDF, DOCX, or pasted text) and uses
Google's free Gemini API to generate a summary, key points, MCQs and
viva questions.

You do NOT need to understand every line to run this project.
Follow README.md for setup instructions.
"""

import os
import json
import re
import tempfile

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx

# ---------------------------------------------------------------------------
# 1. Setup
# ---------------------------------------------------------------------------

load_dotenv()  # reads variables from a local .env file

app = Flask(__name__)

# Use the system temp folder for uploads. This works both when running
# locally AND on Vercel, where only /tmp is writable (the rest of the
# filesystem is read-only in a serverless function).
app.config["UPLOAD_FOLDER"] = tempfile.gettempdir()
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024  # 15 MB upload limit

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


# ---------------------------------------------------------------------------
# 2. Helpers: pull raw text out of whatever the student uploaded
# ---------------------------------------------------------------------------

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_docx(file_path: str) -> str:
    document = docx.Document(file_path)
    return "\n".join(p.text for p in document.paragraphs)


def get_study_text(request) -> str:
    """Works out whether the student pasted text or uploaded a file,
    and returns plain text either way."""

    pasted_text = request.form.get("text", "").strip()
    if pasted_text:
        return pasted_text

    uploaded_file = request.files.get("file")
    if not uploaded_file or uploaded_file.filename == "":
        return ""

    filename = uploaded_file.filename.lower()
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
    uploaded_file.save(save_path)

    try:
        if filename.endswith(".pdf"):
            return extract_text_from_pdf(save_path)
        elif filename.endswith(".docx"):
            return extract_text_from_docx(save_path)
        elif filename.endswith(".txt"):
            with open(save_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            return ""
    finally:
        # clean up the uploaded file after reading it
        if os.path.exists(save_path):
            os.remove(save_path)


# ---------------------------------------------------------------------------
# 3. The AI prompt
# ---------------------------------------------------------------------------

PROMPT_TEMPLATE = """You are an expert teacher helping a student revise for exams.

Read the study material below and generate exam-ready notes from it.
Only use facts present in the material. Do not invent information.

Return ONLY valid JSON (no markdown, no code fences, no extra commentary)
in exactly this shape:

{{
  "summary": "a clear 4-6 sentence summary of the material",
  "key_points": ["point 1", "point 2", "..."],
  "mcqs": [
    {{"question": "...", "options": ["A", "B", "C", "D"], "answer": "A"}}
  ],
  "viva_questions": [
    {{"question": "...", "answer": "short answer"}}
  ]
}}

Generate 6-10 key points, 5 MCQs, and 6 viva questions.

STUDY MATERIAL:
\"\"\"
{content}
\"\"\"
"""


def clean_json_response(raw_text: str) -> dict:
    """Gemini sometimes wraps JSON in ```json fences - strip those before parsing."""
    cleaned = re.sub(r"^```(json)?|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)


# ---------------------------------------------------------------------------
# 4. Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "No Gemini API key found. Add GEMINI_API_KEY to your .env file. "
                     "See README.md for how to get a free key."
        }), 400

    study_text = get_study_text(request)

    if not study_text or len(study_text.strip()) < 30:
        return jsonify({
            "error": "Please paste more text or upload a readable PDF/DOCX/TXT file "
                     "with at least a few sentences of content."
        }), 400

    # Gemini has limits, so trim very long documents
    study_text = study_text[:15000]

    prompt = PROMPT_TEMPLATE.format(content=study_text)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        result = clean_json_response(response.text)
        return jsonify(result)
    except json.JSONDecodeError:
        return jsonify({
            "error": "The AI response could not be read. Please try again."
        }), 500
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": f"Something went wrong: {exc}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
