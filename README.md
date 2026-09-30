# Streaming Live RAG

Samsung PRISM Y2026 GenAI Hackathon  
Theme 04: Streaming Live RAG

## Overview

Streaming Live RAG is a session-aware retrieval-augmented generation system designed for live, incremental user requests.

The system handles:

- Incomplete requests using WAIT
- Early retrieval when sufficient information is available
- Conversational input using SUPPRESS
- Multi-intent decomposition
- Independent retrieval for multiple queries
- Evidence fusion
- Grounded answer generation with evidence citations
- Session-aware answer refinement
- Telemetry for system decisions and latency

## Architecture

```text
User Transcript
      |
      v
Retrieval Controller
 WAIT / RETRIEVE / SUPPRESS
      |
      v
Multi-Intent Decomposer
      |
      v
Query 1 / Query 2 / Query 3
      |
      v
FAISS Retrieval
      |
      v
Evidence Fusion
      |
      v
Session Memory
      |
      v
Groq Grounded Generator
      |
      v
Answer + [E#] Citations
      |
      v
Telemetry

Videos: https://drive.google.com/drive/folders/1emwsf03tffyX-4fPdLJ8M_ODnHumsz4i?usp=sharing
