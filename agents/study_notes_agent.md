# Study Notes Agent

## Purpose
Convert raw study material into a structured, exam-ready revision kit,
acting as a knowledgeable teacher who never strays from the source
material provided.

## Persona
The agent is instructed (via `PROMPT_TEMPLATE` in `app.py`) to behave as
*"an expert teacher helping a student revise for exams."* This framing
biases the model toward pedagogically useful phrasing (clear, exam-
relevant, appropriately simplified) rather than generic summarization.

## Inputs
| Source | How it reaches the agent |
|---|---|
| Pasted text | Taken directly from the `text` form field |
| PDF upload | Extracted via `PyPDF2.PdfReader`, page by page |
| DOCX upload | Extracted via `python-docx`, paragraph by paragraph |
| TXT upload | Read directly as UTF-8 text |

All four paths converge into a single plain-text string before reaching
the agent — the agent itself has no awareness of the original file
format.

## Processing steps
1. Input is validated (rejects empty/too-short submissions before
   spending an API call).
2. Input is trimmed to ~15,000 characters to respect model context
   limits and keep latency low.
3. Input is inserted into the fixed prompt template, which specifies
   role, task, constraints, and required output schema.
4. The agent (Gemini) generates a single JSON response.
5. The response is cleaned of any markdown code fences and parsed.

## Outputs
See the I/O contract in `AGENTS.md`. Four sections are always produced:
summary, key points, MCQs (with marked correct answers), and viva
questions (with model answers).

## Constraints & Guardrails
- **Grounding rule**: "Only use facts present in the material. Do not
  invent information." This is a direct prompt instruction, chosen
  because factual invention in a study tool would actively mislead a
  student preparing for an exam.
- **Output shape is fixed** so the frontend never has to guess how to
  render the response.
- **No chain-of-thought or commentary** is requested or displayed —
  only the final structured answer.

## Failure Modes & Handling
| Failure | Handling |
|---|---|
| Model returns non-JSON text | Caught by `clean_json_response()` / `JSONDecodeError`, returns a friendly error |
| Requested model is deprecated | Backend automatically tries the next candidate model, then queries `list_models()` |
| Input too short/empty | Rejected before the agent is even called |
| API key missing/invalid | Rejected with a setup-instruction error before the agent is called |

## Where this agent is NOT used
The agent is only invoked for the `/generate` route. Serving the
frontend page (`/`) and the client-side download feature involve no AI
call at all.
