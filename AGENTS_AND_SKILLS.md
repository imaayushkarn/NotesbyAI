# AGENTS_AND_SKILLS.md

This document explains how the **agent** and **skill** in this project
relate to each other, per the hackathon requirement to document both
separately and show how they connect.

## The relationship, in one sentence
The **agent** is the orchestrator (it decides *when* and *how* to act:
validating input, choosing a model, handling failures); the **skill** is
the reusable capability it invokes (it decides *what* transformation
happens: text in, structured revision kit out).

## Diagram

```
                     ┌────────────────────────────┐
                     │   Study Notes Agent          │
                     │   (agents/study_notes_agent.md)
                     │                              │
   Raw input  ───────▶  1. Validate input           │
                     │  2. Select available model   │
                     │  3. Invoke skill  ───────────┼────┐
                     │  4. Handle errors/fallback    │    │
                     │  5. Return clean JSON         │    │
                     └────────────────────────────┘    │
                                                          ▼
                                          ┌───────────────────────────────┐
                                          │  Study Notes Skill              │
                                          │  (skills/study_notes_skill.md) │
                                          │                                 │
                                          │  Prompt template + JSON schema │
                                          │  → summary, key points, MCQs,  │
                                          │    viva questions              │
                                          └───────────────────────────────┘
```

## Why they're documented separately
- The **agent** can change independently of the skill — e.g. we could
  swap Gemini for another model provider, or add retry/rate-limit
  logic, without changing what the skill produces.
- The **skill** can be reused independently of this agent — e.g. a
  future "Batch Notes Generator" agent could reuse the exact same skill
  (same prompt + schema) for a different workflow (processing many
  files overnight instead of one live request).

## File map

| Concern | File |
|---|---|
| Agent behavior, rules, I/O contract | `AGENTS.md`, `agents/study_notes_agent.md` |
| Skill definition, prompt contract | `skills/study_notes_skill.md` |
| Where the agent is invoked in code | `app.py`, route `POST /generate` |
| Where the skill's prompt lives in code | `app.py`, `PROMPT_TEMPLATE` |

## Extending this project with a new agent or skill
1. **New skill** — add a new prompt template + JSON schema doc under
   `skills/`, matching the style of `study_notes_skill.md`.
2. **New agent** — add a new orchestration doc under `agents/`
   describing what triggers it, which skill(s) it calls, and its own
   error-handling rules, matching `study_notes_agent.md`.
3. Update this file's table and diagram to include the new pieces.
