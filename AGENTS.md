# NotesbyAI Agent Rules

## Purpose

NotesbyAI uses AI agents to transform student-provided study
material into structured exam-preparation resources.

## Core Rules

1. Use only information available in the supplied study material.
2. Never intentionally invent facts.
3. Clearly indicate when information is missing.
4. Keep generated answers concise and suitable for students.
5. Preserve important technical terms and definitions.
6. Generated MCQs must have one correct answer.
7. Viva questions must be answerable from the supplied material.
8. Do not expose API keys or secrets.
9. Validate AI output before displaying it.
10. Human/student review is required before using generated material
   for examination preparation.

## Human in the Loop

The student remains responsible for reviewing generated notes,
questions and answers before relying on them.

The AI assists the student; it does not replace human judgment.

## Output Requirements

The study agent should generate:

- Summary
- Key Points
- MCQs
- Viva Questions
- Flashcards
- Revision Plan

## Failure Handling

If the uploaded material cannot be read or does not contain enough
information, the system must report the problem instead of
fabricating content.
