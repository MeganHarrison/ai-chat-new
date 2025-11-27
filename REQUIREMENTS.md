Nutrition Solutions AI Sales Coach Widget – Requirements

Overview
Build a full-stack, Intercom-style AI chat widget that embeds on any WordPress site via a single <script src="https://yourdomain.com/widget.js" defer></script>. The widget uses ChatKit for UI and OpenAI Agents SDK for reasoning, state orchestration, RAG retrieval, recommendation logic, off-route handling, and Active Client Support. The experience must feel like a high-conversion transformation coach: bold, direct, identity-focused, empathetic yet challenging.

Primary Users
- New/anonymous visitors seeking guidance on goals and nutrition plans.
- Returning users recognized via memory.
- Current clients needing support for orders/meals.

Core Capabilities (Scope)
- Intercom-style floating bubble that opens a ChatKit-powered chat window (mobile responsive, Vanilla JS only, CSS scoped/Shadow DOM safe).
- Guided Transformation Script (deterministic state machine) driven by /conversation/flow.json covering: Attention Hook; Demographics; Primary Goal; Current Eating Habits; Emotional Root (Why Now); Role of Nutrition Solutions; Testimonials Carousel; Synthesis + Plan Recommendation.
- Off-route intelligence using Agents SDK with rules in /conversation/offroute.json to pause the script, answer naturally (optionally using Supabase RAG), and gently resume the guided flow.
- Brand voice enforcement: bold, direct, transformation-oriented, empathetic yet challenging; no robotic phrasing.
- RAG via Supabase vector search for products, pricing, policies, meal plans, FAQ, testimonials. Responses are rewritten into brand voice (no raw factual dumps).
- Transformation Carousel widget (ChatKit widget) showing 1–5 transformations, horizontally scrollable, filtered by user inputs (age, goals, habits), data served by GET /api/carousel, visually matching provided screenshots.
- Recommendation engine mapping user inputs to plans: Shred Spartan, Shred Gladiator, Beast Spartan, Beast Gladiator using /conversation/recommendation_rules.json.
- Active Client Support path for “I’m a current client” / “Question about my order” / “Need help with my meals”: acknowledge, RAG as needed, fallback to concierge handoff (Call, Text, Short form via POST /api/support).
- Memory: short-term per-session + long-term Supabase table (memory_entries) to recognize returning users and personalize.
- Backend APIs (Node 18+ Express) for orchestration, RAG, recommendation, support routing, memory store/load, carousel, and health.
- Logging & analytics hooks for state transitions, message metadata, RAG hits/misses, recommendation path, and support path usage (files in /backend/logs/).

APIs (must exist)
- GET /api/health
- POST /api/message → Agents SDK orchestration
- POST /api/rag → Supabase vector search
- POST /api/recommend → plan synthesis
- POST /api/memory/store → save memory entries
- POST /api/memory/fetch → load user profile
- GET /api/carousel → testimonials widget
- POST /api/support → client support routing

Data & Configuration
- Static conversation assets in /conversation/:
  - flow.json (guided flow)
  - offroute.json (off-route rules)
  - recommendation_rules.json (plan mapping)
- Supabase used for RAG and long-term memory (memory_entries).
- ChatKit for chat UI; OpenAI Agents SDK for reasoning and flow control.

Non-Functional Requirements
- Human, non-robotic feel with multi-bubble pacing for long messages.
- Load in under 200ms on modern devices.
- CSS isolation via Shadow DOM or scoped CSS; must not conflict with host site.
- Backend: Node.js 18+; Express only; readable, small codebase; no frameworks (no React/Vue/Svelte) and no build systems unless strictly required.

Constraints
- Frontend: Vanilla JS only.
- Widget: single embed file (/widget/widget.js) with supporting /widget/widget.css and /widget/chat-window.html template.
- Agents SDK required for all reasoning.
- ChatKit required for UI.
- Static scripts in /conversation/.
- Supabase required for RAG & memory.
- File and directory names/paths must match exactly as specified.

Deliverables (by directory)
- Project root: REQUIREMENTS.md, AGENT_TASKS.md, TEST.md
- /design: design_spec.md, wireframe.md
- /conversation: flow.json, offroute.json, recommendation_rules.json
- /widget: widget.js, widget.css, chat-window.html
- /frontend: chatkit.js, ui-state-machine.js, carousel-widget.js, utils.js
- /backend: server.js, /routes/message.js, /routes/rag.js, /routes/recommend.js, /routes/support.js, /routes/memory.js, /routes/carousel.js, package.json
- /tests: TEST_PLAN.md, test.sh

End of files.
