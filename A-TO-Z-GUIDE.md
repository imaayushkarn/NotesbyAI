# AI Study Notes Generator — A to Z Guide

This is the complete map of your project: every file, every piece of logic,
and how they all connect — from the moment a student opens the page to the
moment they download their notes.

---

## A — The Big Picture

Your app has **3 layers** that talk to each other:

```
FRONTEND (what the student sees)
   index.html + style.css + script.js
        ↕  (fetch request)
BACKEND (the brain)
   app.py (Flask)
        ↕  (API call)
AI (the intelligence)
   Google Gemini
```

The student never talks to Gemini directly — your Flask backend sits in the
middle, sends Gemini a well-crafted instruction (a "prompt"), and hands the
answer back to the webpage.

---

## B — Folder structure, and why each thing exists

```
ai-study-notes/
├── app.py                → backend brain: routes, AI calls, file reading
├── requirements.txt      → list of Python packages to install
├── .env.example           → template for your secret API key
├── vercel.json            → tells Vercel how to run a Python app
├── api/index.py           → entry point Vercel looks for
├── templates/index.html  → the single webpage
├── static/css/style.css  → all visual styling
└── static/js/script.js   → all interactivity (tabs, upload, API calls)
```

Flask has a rule: it automatically looks for HTML in a folder called
`templates/` and CSS/JS in a folder called `static/`. That's why they're
named exactly that — it's not optional naming, Flask expects it.

---

## C — Backend, piece by piece (`app.py`)

### C1. Setup section
```python
load_dotenv()
app = Flask(__name__)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)
```
- `load_dotenv()` reads your `.env` file and makes `GEMINI_API_KEY` available.
- We **never** hardcode the key in the code — that's a security rule. Keys
  belong in `.env`, which is excluded from GitHub (see `.gitignore`).

### C2. Extracting text from files
Three small functions do one job each:
- `extract_text_from_pdf()` — uses **PyPDF2** to read each page of a PDF and
  glue the text together.
- `extract_text_from_docx()` — uses **python-docx** to read every paragraph
  of a Word file.
- Plain `.txt` files are just opened and read directly.

`get_study_text()` is the traffic controller: it checks *"did the student
paste text, or upload a file?"* and returns plain text either way, so the
rest of the app doesn't need to care which one happened.

### C3. The AI prompt
```python
PROMPT_TEMPLATE = """You are an expert teacher... 
Return ONLY valid JSON in exactly this shape: {...}
"""
```
This is the most important part of the whole project. We're not just asking
Gemini "summarize this" — we're telling it:
1. What role to play (an expert teacher)
2. What to produce (summary, key points, MCQs, viva questions)
3. The **exact JSON shape** to reply in, so our frontend can reliably read it

Asking for strict JSON (instead of free-flowing text) is what lets us turn
the AI's answer into neat cards on the webpage instead of a wall of text.

### C4. Routes — the two doors into your backend
- `@app.route("/")` → serves the webpage itself (`index.html`)
- `@app.route("/generate", methods=["POST"])` → the real work:
  1. Check an API key exists
  2. Get the study text (via `get_study_text`)
  3. Reject if it's too short (protects against empty/junk submissions)
  4. Build the prompt and call Gemini
  5. Clean and parse Gemini's JSON reply
  6. Send it back to the browser as JSON

### C5. Error handling
Every likely failure point has a friendly message instead of a crash:
missing API key, empty input, unreadable AI response, or any unexpected
exception. This matters a lot in a live demo — a crash looks bad, a clear
error message looks professional.

---

## D — Frontend structure (`templates/index.html`)

The page is split into two panels using CSS Grid:
- **Left panel** — input: a tab switcher between "Paste text" and
  "Upload file", plus the Generate button.
- **Right panel** — output: starts as an empty state, then fills with
  4 result cards (Summary, Key Points, MCQs, Viva Questions) plus a
  Download button.

Notice `{{ url_for('static', filename='css/style.css') }}` — that's Flask's
templating syntax (Jinja2). It builds the correct URL to your CSS/JS files
automatically, so you never hardcode paths.

---

## E — Styling (`static/css/style.css`)

Design choices, explained:
- **Colour palette**: violet/indigo + white + off-white paper background —
  calm, modern, "study app" feeling rather than a generic dashboard.
- **Two fonts**: Fraunces (serif, for headings/labels — gives it character)
  + Inter (sans-serif, for body text — stays readable at small sizes).
- **Cards with a labelled header** (`01 — Summary`, `02 — Key points`...) —
  makes the output feel structured, like an index, not a wall of AI text.
- **Responsive grid** — collapses to a single column under 860px so it
  still works on a phone if you demo from one.

---

## F — Interactivity (`static/js/script.js`)

Walk through it in the order things actually happen:

1. **Tab switching** — clicking "Paste text" / "Upload file" just toggles
   which `<div>` is visible; both are always in the HTML, only one shows.

2. **File selected** — when a file is chosen, the dropzone's label text
   updates to show the filename, so the student gets visual confirmation.

3. **Generate button clicked**:
   ```js
   const formData = new FormData();
   formData.append("text", ...) OR formData.append("file", ...);
   fetch("/generate", { method: "POST", body: formData });
   ```
   This is the bridge to the backend — `fetch` sends the data to your
   Flask `/generate` route and waits for a JSON response.

4. **While waiting** — the loading overlay (spinner + message) shows, and
   the button is disabled so the student can't double-click and send two
   requests at once.

5. **Response arrives** — `renderResults()` takes the JSON and builds real
   HTML elements for each summary line, key point, MCQ, and viva question,
   then inserts them into the page. The correct MCQ answer gets a green
   highlight by matching the `answer` letter against each option's text.

6. **Download button** — takes the same data already on the page and
   reformats it as a plain `.txt` file client-side, using a `Blob` — no
   extra backend request needed for this part.

---

## G — The full journey of one request (memorize this for your demo)

```
1. Student pastes text or picks a file
2. Clicks "Generate study notes"
3. JavaScript packages it into FormData and POSTs to /generate
4. Flask receives it, extracts plain text (PyPDF2 / python-docx if a file)
5. Flask builds the teaching prompt and sends it to Gemini
6. Gemini replies with structured JSON (summary, points, MCQs, viva Qs)
7. Flask cleans up the JSON and sends it back to the browser
8. JavaScript reads the JSON and builds the result cards on screen
9. Student can download everything as a .txt file
```

---

## H — Environment variables & security

- `.env` holds your **private** Gemini key. It's read by `load_dotenv()`
  and never appears in your code or on GitHub (blocked by `.gitignore`).
- On Vercel, the same key is stored as an **Environment Variable** in the
  project dashboard instead of a `.env` file — same idea, different home.
- **Rule of thumb**: any password/API key always lives in environment
  variables, never typed directly into a `.py` or `.js` file.

---

## I — Running it locally vs. deploying

| | Local | Vercel |
|---|---|---|
| Command | `python app.py` | Push to GitHub → import in Vercel |
| Key stored in | `.env` file | Vercel dashboard → Environment Variables |
| File uploads saved to | your `uploads`/temp folder | `/tmp` (auto-cleared) |
| Good for | development & testing | live demo link to share with judges |

(Full step-by-step for both is in `README.md` and in our earlier messages.)

---

## J — Common errors & fixes

| Error | Meaning | Fix |
|---|---|---|
| `ModuleNotFoundError` | A package isn't installed | `pip install -r requirements.txt` |
| "No Gemini API key found" | `.env` missing or empty | Check `.env` has `GEMINI_API_KEY=your_key` |
| Blank output / JSON error | AI reply wasn't valid JSON | Usually temporary — click Generate again |
| Garbled PDF text | It's a scanned/image PDF | Use a text-based PDF, or paste text directly |
| Port already in use | Something else is using port 5000 | Change `port=5000` to `port=5001` in `app.py` |

---

## K — Questions judges commonly ask (and how to answer)

**"Why Flask and not Django?"**
Flask is lightweight and has almost no boilerplate — perfect for a small,
focused app built quickly, while Django is built for large multi-feature
platforms.

**"Why JSON output from the AI instead of plain text?"**
Structured JSON lets the frontend reliably split the answer into separate
cards (summary vs. MCQs vs. viva questions) instead of guessing where one
section ends and another begins.

**"What happens if a student uploads a huge PDF?"**
The backend trims text to 15,000 characters before sending it to Gemini,
to stay within the AI's input limits and keep responses fast.

**"Is the student's data stored anywhere?"**
No — uploaded files are deleted immediately after their text is extracted,
and nothing is saved to a database in this version.

**"How would you extend this?"**
Flashcards, a one-day revision planner, multi-language summaries, or OCR
support for handwritten/scanned notes (all listed as future scope).

---

## L — Quick pre-demo checklist

- [ ] `.env` has a valid `GEMINI_API_KEY`
- [ ] `python app.py` runs with no errors
- [ ] Tried both "Paste text" and "Upload file" at least once
- [ ] Tried the Download button
- [ ] Have a short (2–3 paragraph) piece of sample text ready, in case wifi
      is slow and you don't want to hunt for a PDF live
- [ ] Know the 9-step request journey (Section G) well enough to explain
      it without reading

---

You now know this project end to end — not just what it does, but *why*
each piece exists. If any part still feels unclear, tell me which section
and I'll break it down further.
