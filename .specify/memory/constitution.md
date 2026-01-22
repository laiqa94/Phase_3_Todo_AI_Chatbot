<!--
Sync Impact Report
Version change: 1.0.0 → 1.1.0
Modified principles: IV. Layered Web Architecture → IV. Layered Web Architecture with AI Integration, V. Reliability & Observability → V. Reliability, Testing, and Observability with AI Safeguards, VI. Secure Data Stewardship → VI. Secure Data Stewardship with AI Constraints
Added sections: AI Integration Principles; Authentication & Authorization for AI; Database & Data Integrity for AI Operations
Removed sections: None
Templates requiring updates:
 - ⚠️ .specify/templates/plan-template.md (needs AI integration considerations)
 - ⚠️ .specify/templates/spec-template.md (needs AI requirements alignment)
 - ⚠️ .specify/templates/tasks-template.md (needs AI-related tasks categorization)
Follow-up TODOs:
 - None
-->

# AI Todo Chatbot – Full-Stack Backend Constitution (FastAPI + Cohere + Agent SDK)

## Core Principles

### I. Spec-Driven Delivery
Every initiative MUST originate from an approved `/specs/<feature>/spec.md`, translated into plan.md and tasks.md before implementation. No code may ship without traceable specs, measurable acceptance criteria, and archived Prompt History Records tying user intent to outputs.

### II. Agent-Orchestrated Workflow
Workflows MUST leverage the prescribed agent sequence (SpecAnalyzer → ArchitecturePlanner → DatabaseSchema → AuthIntegration → BackendAPI → FrontendAPI → FrontendUI → TaskState → Testing → Documentation) with the ProjectOrchestrator coordinating handoffs. Each agent stays within its scope, and deviations require documented approval.

### III. Authenticated Multi-Tenancy
Better Auth with JWT is the single source of identity. All backend operations MUST enforce JWT verification, scope every database query by authenticated user, and prevent cross-tenant leakage. Frontend API calls include bearer tokens automatically via `/lib/api.ts`.

### IV. Layered Web Architecture with AI Integration
Frontend (Next.js 16+ App Router + Tailwind) → API (FastAPI) → AI Services (Cohere-powered) → Persistence (SQLModel + Neon PostgreSQL) is the mandated stack. Data flows strictly follow this chain; no UI element may bypass the API, no AI service may bypass the API, and no API may bypass SQLModel models or migrations. AI interactions must be mediated through dedicated backend services.

### V. Reliability, Testing, and Observability with AI Safeguards
Every feature requires red-green-refactor discipline, automated tests per user story, and structured logging on both tiers. Integration tests must cover CRUD flows, authentication, AI service calls, and error handling before release. Observability data (logs/metrics) must include user, request, and AI interaction IDs for traceability. AI responses must be logged for audit and quality assurance.

### VI. Secure Data Stewardship with AI Constraints
Secrets live only in environment variables or managed secret stores. Personal data must be encrypted in transit (HTTPS) and never logged in plaintext. AI provider keys (Cohere) must be securely stored and accessed only through backend services. Data retention and deletion policies follow spec directives; AI training data must exclude personally identifiable information; deviations require explicit governance review.

## AI Integration Principles

### VII. AI Authentication & Authorization
Every AI action MUST be executed in the context of an authenticated user. JWT token validation is MANDATORY before any AI-assisted task operation. AI must NEVER act without a valid user_id from auth context. AI cannot access or modify another user's data. AI must not bypass backend authorization rules. Secrets (.env values) are STRICTLY non-readable by AI.

### VIII. AI-Driven Task Management Constraints
AI agents can only interact with tasks through predefined backend services and endpoints. AI must NEVER write raw SQL or directly access the database. All task operations (create, read, update, delete, complete) must go through properly authenticated API endpoints. AI responses to user queries must be validated and sanitized before presentation.

### IX. AI Service Reliability & Fallback
AI service calls must have appropriate timeouts and retry mechanisms. When AI services are unavailable, the system must gracefully degrade to basic functionality. AI-generated content must be validated against security and content policies before being processed or stored.

## Platform & System Constraints

- Multi-user AI-powered todo scope with responsive UX across desktop and mobile breakpoints.
- Backend: FastAPI with SQLModel models, JWT middleware, and endpoints limited to `/api/{user_id}/tasks*` operations defined in specs.
- AI Services: Cohere integration through dedicated backend services with rate limiting and error handling.
- Frontend: Next.js server components by default, client components only where interactivity demands (forms, toggles, filters).
- Database: Neon PostgreSQL schema with `users` (Better Auth-managed) and `tasks` tables; tasks include status, due dates, metadata, and foreign key to users.
- AI Integration: All AI interactions must be logged and auditable, with clear attribution to user sessions.
- Deployment artifacts must preserve monorepo layout and support automated migrations before app start.

## Workflow & Quality Gates

1. Read & summarize all relevant specs before planning.
2. Validate Constitution Check items in plan.md; block work until satisfied.
3. Maintain Todo task state (pending → in_progress → completed) for every engagement.
4. Record Prompt History after each user exchange; surface ADR suggestions for cross-cutting decisions.
5. Tests (unit, integration, contract) must run and pass before marking tasks complete; failures automatically block promotion.
6. AI integration tests must validate security boundaries and proper error handling.
7. Documentation updates (README, quickstarts) accompany feature delivery to keep onboarding accurate.

## Governance

- This constitution supersedes other guidance when conflicts arise.
- Amendments require: (a) documented proposal, (b) review against specs/templates, (c) version bump logged in Sync Impact Report.
- Versioning uses semantic rules: MAJOR for principle changes, MINOR for new sections/principles, PATCH for clarifications.
- Compliance reviews occur at each `/sp.plan` gate; violations demand remediation plans in plan.md before implementation proceeds.

**Version**: 1.1.0 | **Ratified**: 2026-01-17 | **Last Amended**: 2026-01-17