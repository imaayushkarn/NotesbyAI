# AGENTS.md

This file defines the AI agent that powers NotesbyAI, following the
`AGENTS.md` convention for documenting agent behavior and rules.

## Agent: Study Notes Agent

- **Defined in:** [`agents/study_notes_agent.md`](agents/study_notes_agent.md)
- **Role:** Educational Assistant
- **Underlying model:** Google Gemini (dynamic model selection — see
  `docs/architecture.md` § AI Layer)
- **Invoked from:** `app.py`, route `POST /generate`

## Agent I/O Contract

**Input:** plain text extracted from a student's pasted content or an
uploaded PDF/DOCX/TXT file (max ~15,000 characters).

**Output:** a strict JSON object with four fields:
```json
{
  "summary": "string",
  "key_points": ["string", "..."],
  "mcqs": [{"question": "string", "options": ["A","B","C","D"], "answer": "A"}],
  "viva_questions": [{"question": "string", "answer": "string"}]
}
```

## Global Agent Rules

These rules are enforced via the prompt template in `app.py`
(`PROMPT_TEMPLATE`) and apply to every generation:

1. **Grounding** — the agent must only use facts present in the
   provided study material. It must not invent information not found
   in the source text.
2. **Structured output only** — the agent must respond with valid JSON
   matching the schema above, with no markdown fences or commentary
   outside the JSON. This is enforced by `clean_json_response()` in
   `app.py`, which strips any accidental code fences before parsing.
3. **Fixed quantities** — 6–10 key points, exactly 5 MCQs, and 6 viva
   questions per generation, so the frontend layout is predictable.
4. **No persistent memory** — each request is stateless; the agent has
   no memory of previous requests or other students' material.
5. **Fail safely** — if the agent's output cannot be parsed as JSON,
   the backend returns a clear error to the user rather than displaying
   corrupted content.

## Skills used by this agent

See [`AGENTS_AND_SKILLS.md`](AGENTS_AND_SKILLS.md) for how the agent and
its skill(s) relate, and [`skills/study_notes_skill.md`](skills/study_notes_skill.md)
for the skill definition itself.
