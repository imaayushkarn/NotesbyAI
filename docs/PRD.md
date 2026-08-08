# Product Requirements Document (PRD)

## Product Name
**NotesbyAI** — AI Study Notes Generator

## 1. Problem Statement
Students spend disproportionate time reading long textbooks, PDFs, and
lecture notes before exams, with no fast way to extract what actually
matters or test their own understanding.

## 2. Goal
Let a student paste or upload any study material and receive, within
seconds, an exam-ready revision kit: a summary, key points, a practice
quiz, and viva-style questions — without needing to read the whole
source material first.

## 3. Target Users
- School and college students preparing for exams
- Students preparing for viva/oral exams
- Competitive exam aspirants revising large volumes of material
- Teachers building quick quizzes from existing material

## 4. Scope (v1.0)

### In scope
| Feature | Description |
|---|---|
| Text input | Paste raw study text directly |
| File input | Upload PDF, DOCX, or TXT |
| AI Summary | 4–6 sentence plain-language summary |
| Key Points | 6–10 bullet points of core facts |
| MCQ Quiz | 5 multiple-choice questions with marked answers |
| Viva Questions | 6 short-answer oral-exam-style questions |
| Download | Export the generated notes as a `.txt` file |

### Out of scope (future work — see `docs/architecture.md` § Future Scope)
- Flashcard flip-cards
- OCR for scanned/handwritten notes
- Multi-language summaries
- User accounts / saved history
- Mind maps

## 5. User Stories

1. *As a student*, I want to paste my notes and get a summary, so I can
   revise a topic in minutes instead of re-reading pages.
2. *As a student*, I want to upload a PDF chapter, so I don't have to
   manually retype it.
3. *As a student preparing for a viva*, I want likely oral questions
   with model answers, so I can rehearse out loud.
4. *As a student*, I want a quick MCQ quiz, so I can self-test before an
   exam.
5. *As a student*, I want to download my notes, so I can revise offline
   later.

## 6. Non-Functional Requirements

| Requirement | Target |
|---|---|
| Response time | Under 10 seconds for a typical chapter (~2–5 pages) |
| Input size limit | Up to 15 MB file upload; text trimmed to ~15,000 characters sent to the AI |
| Availability | Runs both locally (Flask dev server) and on Vercel (serverless) |
| Data privacy | Uploaded files are deleted immediately after text extraction; no material is stored permanently |
| Reliability | AI model calls fall back across multiple model names if one is deprecated (see `docs/architecture.md` § AI Layer) |

## 7. Success Metrics (for hackathon demo)
- A judge can upload a real PDF and get usable notes in under 15 seconds
- Zero unhandled crashes during a live demo of the 5 core features
- All output is grounded in the source material (no invented facts)

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| AI model name gets deprecated mid-demo | Multi-model fallback chain in `app.py` (see architecture doc) |
| AI returns malformed JSON | Backend catches `JSONDecodeError` and returns a clean error instead of crashing |
| Large/scanned PDFs return no text | User-facing error message asks for a text-based file or pasted text |
| API quota exceeded | Friendly error message; no partial/broken UI state |

## 9. Acceptance Criteria (v1.0)
- [ ] User can paste text OR upload a PDF/DOCX/TXT file
- [ ] Output includes summary, key points, MCQs, and viva questions
- [ ] Output can be downloaded as a text file
- [ ] Invalid input (empty, too short, unsupported file type) shows a
      clear error instead of failing silently
- [ ] App runs both locally and on a public Vercel deployment
