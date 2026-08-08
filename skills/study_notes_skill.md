# Skill: Study Material → Structured Revision Kit

## What this skill does
A reusable capability that transforms any block of educational text into
four standardized revision artifacts: summary, key points, multiple-
choice quiz, and viva (oral exam) questions — all grounded strictly in
the source text.

This is implemented as a **prompt-engineered skill** on top of Gemini
(rather than a separately fine-tuned model), defined by the fixed
template in `app.py::PROMPT_TEMPLATE`.

## Skill contract

**Given:** plain text of study material (any subject, any length up to
~15,000 characters)

**Produces:** a JSON object with:
- `summary` — 4–6 sentence overview
- `key_points` — 6–10 concise facts/concepts
- `mcqs` — 5 questions, each with 4 options and one marked correct answer
- `viva_questions` — 6 short-answer oral questions with model answers

## Why this is a distinct "skill" rather than just a raw AI call
The skill encodes several deliberate design decisions that turn a
generic LLM call into a repeatable, reliable capability:

1. A **fixed output schema**, so any caller (this app, or a future one)
   gets predictable, parseable results every time.
2. A **grounding constraint** ("do not invent facts") specifically
   suited to an educational context where hallucination is unacceptable.
3. A **fixed quantity contract** (exactly 5 MCQs, 6 viva questions,
   etc.) so downstream UI can be built without defensive/variable
   layout code.
4. **Format cleanup logic** (`clean_json_response`) that makes the skill
   robust to models that wrap JSON in markdown fences — a common,
   otherwise-breaking quirk of LLM output.

## How to reuse this skill elsewhere
Because the skill is just a prompt template + a JSON contract, it can be
reused outside this app:
1. Take `PROMPT_TEMPLATE` from `app.py`.
2. Fill in `{content}` with any study text.
3. Send it to any Gemini-compatible `generateContent` endpoint.
4. Parse the response with the same `clean_json_response()` logic.

## Relationship to the agent
This skill is the **core capability** invoked by the Study Notes Agent
(see `agents/study_notes_agent.md`). The agent adds the surrounding
behavior (input validation, model fallback, error handling); the skill
is the specific prompt + schema contract that does the actual
transformation. See `AGENTS_AND_SKILLS.md` for how they fit together.

## Example

**Input (excerpt):**
> "Mitochondria are membrane-bound organelles found in most eukaryotic
> cells. They generate most of the cell's supply of ATP through
> respiration, and are therefore often called the powerhouse of the
> cell."

**Output (excerpt):**
```json
{
  "summary": "Mitochondria are organelles that produce ATP...",
  "key_points": ["Mitochondria are membrane-bound organelles", "..."],
  "mcqs": [{"question": "What is the primary function of mitochondria?", "options": ["Protein synthesis","ATP production","Waste removal","Cell division"], "answer": "B"}],
  "viva_questions": [{"question": "Why are mitochondria called the powerhouse of the cell?", "answer": "Because they generate most of the cell's ATP through respiration."}]
}
```
