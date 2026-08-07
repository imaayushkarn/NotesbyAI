# AI Study Notes Generator

Paste your notes or upload a PDF/DOCX, and get an instant summary, key
points, a 5-question MCQ quiz, and viva questions — powered by Google's
free Gemini AI.

This guide assumes you've **never run a project like this before**. Follow
it top to bottom and you'll have it running in about 10 minutes.

---

## What's inside

```
ai-study-notes/
├── app.py                 → the backend (Python/Flask)
├── requirements.txt       → list of packages to install
├── .env.example            → template for your secret API key
├── templates/index.html   → the webpage
├── static/css/style.css   → styling
├── static/js/script.js    → frontend logic
└── uploads/                → temporary file storage (auto-cleaned)
```

---

## Step 1 — Install Python

You need Python 3.9 or newer.

1. Go to https://www.python.org/downloads/
2. Download and install it.
3. **Windows users:** during install, tick the box that says "Add Python to PATH".
4. Check it worked — open a terminal (Command Prompt / Terminal app) and type:
   ```
   python --version
   ```
   You should see something like `Python 3.11.4`.

---

## Step 2 — Open a terminal in this folder

- **Windows:** open the `ai-study-notes` folder in File Explorer, click the
  address bar, type `cmd`, press Enter.
- **Mac:** right-click the `ai-study-notes` folder → "New Terminal at Folder"
  (or open Terminal and type `cd ` then drag the folder in).

---

## Step 3 — Install the required packages

In the terminal, run:

```
pip install -r requirements.txt
```

This downloads Flask (the web server) and the Gemini AI library. It only
needs to be done once.

> If `pip` doesn't work, try `pip3` instead.

---

## Step 4 — Get your free Gemini API key

This is what lets your app talk to Google's AI. It's free.

1. Go to **https://aistudio.google.com/app/apikey**
2. Sign in with a Google account.
3. Click **"Create API key"**.
4. Copy the long string of letters/numbers it gives you.

---

## Step 5 — Add your key to the project

1. In the `ai-study-notes` folder, find the file called `.env.example`.
2. Make a copy of it and rename the copy to exactly `.env` (no ".example").
3. Open `.env` in any text editor and paste your key after the `=` sign:
   ```
   GEMINI_API_KEY=paste_your_key_here
   ```
4. Save the file.

**Never share this file publicly or upload it to GitHub** — it's your
private key. The `.gitignore` file already keeps it out of GitHub for you.

---

## Step 6 — Run the app

Back in your terminal:

```
python app.py
```

You should see something like:

```
 * Running on http://127.0.0.1:5000
```

Open that link (`http://127.0.0.1:5000`) in your browser. Your app is live!

---

## Step 7 — Try it out

1. Paste a paragraph or two of study material into the text box
   (or switch to the "Upload file" tab and pick a PDF/DOCX).
2. Click **Generate study notes**.
3. Wait a few seconds — you'll get a summary, key points, an MCQ quiz, and
   viva questions.
4. Click **Download as text file** to save your notes.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| "No Gemini API key found" | Check your `.env` file exists and has the key pasted correctly |
| Blank/garbled text from PDF | Some PDFs are scanned images — try a text-based PDF or paste text directly |
| Port already in use | Close other running apps, or change `port=5000` in `app.py` to `port=5001` |

---

## How it works (for your presentation)

```
Student pastes text or uploads file
        ↓
Flask backend extracts plain text
   (PyPDF2 for PDF, python-docx for DOCX)
        ↓
Text is sent to Gemini AI with a teaching prompt
        ↓
Gemini returns summary + key points + MCQs + viva questions as JSON
        ↓
Webpage displays them as cards, with a downloadable text file
```

## Ideas to extend it (if you have extra time)

- Add a "Flashcards" tab (flip cards showing term → definition)
- Add a one-day revision study plan
- Add dark mode
- Let users pick number of MCQs
- Deploy it online (Render for the backend, since it needs Python)

:)
