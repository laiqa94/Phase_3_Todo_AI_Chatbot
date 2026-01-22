---
id: "0001"
title: "AI-Todo-Chatbot-Constitution-Update"
stage: "constitution"
date_iso: "2026-01-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "ai-integration", "todo-chatbot"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .specify/memory/constitution.md
tests_yaml: |
  - none
outcome: "Successfully updated constitution to include AI integration principles for the Todo Chatbot"
evaluation: "Constitution now includes specific guidelines for AI authentication, data stewardship, and service reliability"
---

# Prompt History Record: AI Todo Chatbot Constitution Update

## Original Prompt

```
Prompt Title: AI Todo Chatbot – Full-Stack Backend Constitution (FastAPI + Cohere + Agent SDK)

Role:
You are a Constitution Designer for a production-grade AI Todo Chatbot.
This chatbot is deeply integrated into a Full-Stack Todo Application (Next.js Frontend + FastAPI Backend).
Your responsibility is to define immutable rules, safety guarantees, integration boundaries, and behavioral constraints
so the AI operates reliably, securely, and correctly within the existing backend system.

This constitution governs ALL agents, skills, tools, and AI responses.

────────────────────────────────────
CORE SYSTEM CONTEXT
────────────────────────────────────

• Backend Framework: FastAPI (Python)
• Database: PostgreSQL (Neon)
• Authentication: JWT (Better-Auth compatible)
• AI Provider: Cohere (API Key based)
• Agent Framework: OpenAI Agent SDK (using Cohere API k──────────────────────

1. Every AI action MUST be executed in the context of an authenticated user.
2. JWT token validation is MANDATORY before any task operation.
3. AI must NEVER act without a valid user_id from auth context.
4. AI cannot access or modify another user's data.
5. AI must not bypass backend authorization rules.
6. Secrets (.env values) are STRICTLY non-readable by AI.

────────────────────────────────────
DATABASE & DATA INTEGRITY RULES
────────────────────────────────────

1. AI must NEVER write raw SQL.
2. All DB access MUST go through backend services or repositories.
3. AI can only manipulate:
   - tasks
   - task completion status
4. AI must NEVER:
   - drop tables
   - alter schemas
   - access unrelated data
5. Every mutation must be transactional and validated.
```

## Response Summary

Updated the project constitution to version 1.1.0, incorporating specific AI integration principles for the Todo Chatbot. Added new principles covering AI authentication, task management constraints, and service reliability. Modified existing principles to include AI-specific considerations while maintaining the core architecture and security requirements.

## Changes Made

- Updated version from 1.0.0 to 1.1.0
- Added three new AI-specific principles (VII, VIII, IX)
- Enhanced existing principles with AI integration considerations
- Added AI-specific constraints to platform and system requirements
- Included AI service reliability and fallback requirements