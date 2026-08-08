# Architecture Document

## 1. System Overview

NotesbyAI is a three-layer application: a static frontend, a Flask
backend, and Google's Gemini API as the AI layer. There is no database —
the system is stateless, processing each request independently.

```
┌─────────────┐      HTTP (fetch/POST)      ┌──────────────┐      HTTPS       ┌─────────────┐
│  Frontend    │ ───────────────────────────▶│  Flask API   │ ───────────────▶│  Gemini API  │
│ (HTML/CSS/JS)│ ◀───────────────────────────│  (app.py)    │ ◀───────────────│  (Google)    │
└─────────────┘        JSON response         └──────────────┘   JSON response └─────────────┘
```

## 2. Components

### 2.1 Frontend (`templates/`, `static/`)
- Plain HTML/CSS/JavaScript — no framework, no build step, so it loads
  instantly and is easy to inspect for judges.
- `script.js` owns all client-side state: which input tab is active,
  the last AI response (for the download button), and loading state.
- Communicates with the backend via a single `fetch("/generate")` call
  using `multipart/form-data` (needed to support file uploads).

### 2.2 Backend API (`app.py`)
Two routes:
- `GET /` — serves the single-page frontend.
- `POST /generate` — accepts pasted text or an uploaded file, extracts
  plain text, prompts Gemini, and returns structured JSON.

Responsibilities:
1. **Input normalization** — `get_study_text()` abstracts away whether
   the source was pasted text or a file, so downstream code only ever
   deals with plain text.
2. **Text extraction** — `PyPDF2` for PDF, `python-docx` for DOCX, plain
   file read for TXT.
3. **Prompt construction** — a single template (`PROMPT_TEMPLATE`)
   instructs Gemini to act as a teacher and return **strict JSON**, so
   the frontend can reliably render structured cards instead of parsing
   free text.
4. **AI Layer resilience** — Google frequently renames/retires model
   IDs. `app.py` tries a list of current candidate models in order, and
   if all fail, calls `genai.list_models()` to discover whatever model
   is currently available on the caller's account and uses that. This
   means a future model rename does not require a code change to
   recover.
5. **Error handling** — every failure mode (missing API key, empty
   input, malformed AI response, model unavailable) returns a clear
   JSON error instead of an unhandled exception.

### 2.3 AI Layer (Gemini API)
- Accessed via the `google-generativeai` Python SDK.
- Model selection is dynamic (see 2.2.4) rather than hardcoded to a
  single model string, which is a deliberate resilience decision given
  how often Google has renamed Gemini models during 2026.
- The prompt explicitly forbids inventing facts not present in the
  source material, to reduce hallucination risk in an educational tool.

## 3. Data Flow (single request)

```
1. Student submits text or file
2. Browser sends multipart/form-data POST to /generate
3. Flask extracts plain text (file parser or direct passthrough)
4. Text (trimmed to 15,000 chars) is inserted into PROMPT_TEMPLATE
5. Flask calls Gemini via candidate model list (or list_models() fallback)
6. Gemini returns JSON: { summary, key_points, mcqs, viva_questions }
7. Flask validates/parses the JSON and returns it to the browser
8. script.js renders it into result cards
9. Student may download the rendered notes as .txt (client-side only,
   no additional backend call)
```

## 4. Deployment Architecture

Two supported environments, using the same codebase:

| | Local | Vercel (production) |
|---|---|---|
| Entry point | `app.py` run directly | `api/index.py` imports the same Flask `app` |
| Routing | Flask's built-in dev server | `vercel.json` routes all paths to `api/index.py` |
| File storage | System temp dir | `/tmp` (the only writable path in a Vercel function) |
| Secrets | `.env` file (git-ignored) | Vercel dashboard → Environment Variables |
| Scaling | Single process | Auto-scaled serverless functions per request |

## 5. Security Considerations
- API key is never committed to source control (`.gitignore` excludes
  `.env`); on Vercel it lives only in the encrypted environment variable
  store.
- Uploaded files are deleted immediately after text extraction — no
  study material is persisted to disk beyond the request lifecycle.
- Upload size is capped (`MAX_CONTENT_LENGTH`) to prevent abuse.

## 6. Testing Strategy
See `docs/testing.md` for full details. In summary: unit tests mock the
Gemini API so CI does not require a real API key, and cover input
validation, text extraction, and JSON parsing independently of network
calls.

## 7. Future Scope
- OCR support for scanned/handwritten notes
- Flashcard mode
- Persisted history (would introduce a database layer)
- Multi-language summary output
- Streaming AI responses instead of a single blocking call
