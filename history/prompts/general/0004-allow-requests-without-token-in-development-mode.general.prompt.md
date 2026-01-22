---
id: 0004
title: Allow requests without token in development mode
stage: general
date: 2026-01-18
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: danish
command: "Allow requests without token in development mode"
labels: ["bug-fix", "frontend", "authentication", "api", "development"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/app/api/proxy/[...path]/route.ts
tests:
---

## Prompt

Fix the persistent unauthorized error in the chatbot component by modifying the proxy route to allow requests without tokens in development mode, so the backend can handle authentication and the proxy can provide mock data for 401 responses.

## Response snapshot

Modified the proxy route authentication logic to:
1. Allow requests to proceed to the backend in development mode even without a valid token
2. Maintain strict authentication in production mode
3. Let the backend handle authentication and return 401 responses
4. Enable the proxy route to catch 401 responses and provide mock data for development

## Outcome

- ✅ Impact: Resolved persistent unauthorized error in chatbot component
- 🧪 Tests: Manual verification that chatbot can make API calls in development
- 📁 Files: Updated proxy route authentication logic
- 🔁 Next prompts: Verify complete chatbot functionality
- 🧠 Reflection: Development workflow requires more flexible authentication handling

## Evaluation notes (flywheel)

- Failure modes observed: Proxy route blocking requests before reaching backend in development
- Graders run and results (PASS/FAIL): Manual verification - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test complete end-to-end functionality