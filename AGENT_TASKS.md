# Agent Tasks — Nutrition Solutions AI Sales Coach

## Shared Constraints
- Lightweight stack: Node.js + Express backend, vanilla JS frontend, Supabase for vectors/memory/logs.
- Brand voice: bold, identity-first, direct, empathetic.
- Store artifacts in designated folders (`/design`, `/frontend`, `/backend`, `/tests`).

## Designer
### Project Name
Nutrition Solutions AI Sales Coach

### Deliverables
- `/design/design_spec.md` — must cover:
  1. State machine diagram and step-by-step script prompts (intro_hook → CTA) with sample copy.
  2. Off-route taxonomy with sample responses and resume prompts.
  3. Active Client support flow (decision tree, copy for text/call/form handoff).
  4. Wireframes for chat UI, Transformation Carousel, and CTA layouts (Intercom-style panel).
  5. Content style guide (voice/tone rules, do/don’t, message lengths) and message templates for common cases (price doubts, emotional inputs).
  6. Carousel filtering rules mapping slots → testimonial tags; card anatomy.

### Technical Notes
- Keep messages to 1–3 short sentences with optional quick replies.
- Provide JSON-like outline of slot names, validation rules, branching conditions, and CTA taxonomy `{type,label,action,payload}`.

## Frontend Developer
### Deliverables
- `/frontend/index.html` (entry point).
- Supporting files (same folder): `styles.css`, `main.js` (or equivalent modules referenced by `index.html`).

### Purpose
Implement an Intercom-style chat UI with message bubbles, typing indicators, quick replies, CTAs, and the Transformation Carousel.

### Technical Notes
- Build a lightweight Chatkit client module that manages sessionId + visitorId (localStorage), sends requests to the backend, renders UI indicators, and handles CTA transitions.
- Export events: `onMessage`, `onStateChange`, `onCTA`.
- Enforce accessibility (ARIA roles, focus management, keyboard navigation). No heavy frameworks.

## Backend Developer
### Deliverables
- `/backend/server.js` — Express server implementing the required endpoints.
- Optional helpers: `/backend/routes/*.js`, `/backend/lib/*.js`, fixtures, and `.env.example` entries.

### Purpose
Serve chat state machine, RAG search, plan recommendations, memory persistence, support routing, and logging while wrapping answers in the NS brand voice.

### Technical Notes
- Implement endpoints: `POST /api/chat/next`, `POST /api/rag/search`, `GET /api/recommendations`, `GET /api/carousel`, `GET|POST /api/memory`, `POST /api/support/route`, `POST /api/logs/state`.
- Build an Answer Composer that wraps RAG facts in motivational tone and suggests next steps.
- Memory: in-memory map for session; Supabase for long-term visitor data.
- Provide `.env.example` for Supabase credentials.
- Plan recommendation: rules-based `fitScore` using slots + rationale string.
- Support routing: return text number, call number, and mock form submission returning `ticketId`.
- Log state transitions to `conv_logs`.

## Tester
### Deliverables
- `/tests/results.md` (or similar) summarizing outcomes against `TEST.md`.

### Purpose
Validate the end-to-end experience and workflow gating using the scenarios defined in `TEST.md`.

### Technical Notes
- Use seeded Supabase data or mocks to verify RAG truthfulness.
- Confirm UI indicators (memory, RAG), CTA chaining, and multi-agent gate checks.
