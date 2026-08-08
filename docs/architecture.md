# NotesbyAI Architecture

## Overview

NotesbyAI is an AI-powered web application that converts
student study material into structured exam-preparation resources.

## Architecture

```text
Student
   |
   v
Web Interface
   |
   v
Flask Backend
   |
   +----> PDF/DOCX/TXT Extraction
   |
   v
Study Notes Agent
   |
   v
Study Notes Generation Skill
   |
   v
Gemini AI
   |
   v
Output Validation
   |
   v
Structured Study Pack
   |
   +--> Summary
   +--> Key Points
   +--> MCQs
   +--> Viva Questions
   +--> Flashcards
   +--> Revision Plan
   |
   v
Student Review
