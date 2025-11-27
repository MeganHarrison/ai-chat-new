Project: Nutrition Solutions AI Sales Coach Widget

General Rules
- Follow exact file/directory names and paths listed. Do not rename or add alternatives.
- Use ChatKit for UI and OpenAI Agents SDK for reasoning and orchestration.
- Use Supabase for RAG and long-term memory (table: memory_entries).
- Static scripts live under /conversation/.
- Frontend: Vanilla JS only. Backend: Node.js 18+ and Express only.
- Enforce brand voice: bold, direct, identity-focused, transformation-oriented, empathetic yet challenging.

[Project Manager]
Deliverables (root):
- REQUIREMENTS.md
- AGENT_TASKS.md
- TEST.md
Critical Notes:
- Deterministically translate TASK_LIST.md without inventing files or renaming.
- Enforce gating and path correctness across all roles.

[Designer]
Deliverables (/design):
- /design/design_spec.md
- /design/wireframe.md
Critical Notes:
- Must include: Chat window layout; Bubble pacing rules; Widget specs; State machine diagrams; Tone rules; Message sequencing; Active Client Support logic.
- Ensure mobile-responsive patterns and UI affordances for quick replies, carousel, and off-route return UX.

[Frontend Developer]
Deliverables:
- /widget/widget.js (single embed script)
- /widget/widget.css
- /widget/chat-window.html
- /frontend/chatkit.js
- /frontend/ui-state-machine.js
- /frontend/carousel-widget.js
- /frontend/utils.js
Critical Notes:
- Inject floating bubble, open/close animation, ChatKit chat window, message rendering, quick replies, widgets UI, error states, mobile support.
- Implement deterministic state machine driven by /conversation/flow.json.
- Implement off-route handling using /conversation/offroute.json via Agents SDK responses.
- Implement testimonials carousel widget with horizontal scroll and filtering by user inputs; must visually match provided screenshots.
- Use Shadow DOM or strict CSS scoping to avoid host CSS conflicts.
- Performance: initial load under 200ms; no frameworks; no build steps unless strictly required.

[Backend Developer]
Deliverables:
- /backend/server.js
- /backend/routes/message.js
- /backend/routes/rag.js
- /backend/routes/recommend.js
- /backend/routes/support.js
- /backend/routes/memory.js
- /backend/routes/carousel.js
- /backend/package.json
Critical Notes:
- Node.js 18+ with Express only.
- Integrate OpenAI Agents SDK to orchestrate guided flow, off-route logic, recommendation, Active Client Support.
- Supabase for RAG (products, pricing, policies, meal plans, FAQ, testimonials) and for long-term memory storage (memory_entries); expose POST /api/memory/store and /api/memory/fetch.
- Implement endpoints: GET /api/health; POST /api/message; POST /api/rag; POST /api/recommend; POST /api/memory/store; POST /api/memory/fetch; GET /api/carousel; POST /api/support.
- Log state transitions, message metadata, RAG hits/misses, recommendation path, support path usage to /backend/logs/.

[Tester]
Deliverables (/tests):
- /tests/TEST_PLAN.md
- /tests/test.sh
Critical Notes:
- Validate guided flow, off-route handling, RAG correctness, widget rendering, recommendation logic, Active Client Support path, and API contract consistency across all endpoints.
