# Agents and Skills

## Custom Agent

### Study Notes Agent

Location:

`agents/study_notes_agent.md`

Purpose:

Transforms student study material into structured exam
preparation resources.

Responsibilities:

- Summarization
- Key-point extraction
- MCQ generation
- Viva generation
- Flashcard generation
- Revision planning

## Custom Skill

### Study Notes Generation Skill

Location:

`skills/study_notes_skill.md`

Purpose:

Defines the structured process and quality rules used to
generate study resources from source material.

## Human in the Loop

The student reviews generated resources before using them.

## Agent Workflow

User Input
↓
Text Extraction
↓
Study Notes Agent
↓
Study Notes Generation Skill
↓
Validation
↓
Student Review
↓
Final Study Pack
