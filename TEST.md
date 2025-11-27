Acceptance Criteria

[Designer]
- Produces /design/design_spec.md and /design/wireframe.md covering: Chat window layout; Bubble pacing rules; Widget specs; Deterministic state machine diagrams for the guided flow; Tone and brand voice rules; Message sequencing; Active Client Support logic; mobile-responsive behaviors.
- Designs specify Shadow DOM/scoped CSS approach and quick replies affordances, carousel widget layout with 1–5 items and horizontal scrolling, and patterns for pausing/resuming guided flow.

[Frontend Developer]
- Widget loads via <script src="https://yourdomain.com/widget.js" defer></script> on a blank WordPress page without console errors; injects a floating bubble; opens a ChatKit-powered chat window; supports mobile viewports.
- No frameworks used (pure Vanilla JS). No build system required to run in the browser.
- CSS isolation: host site styles do not alter the widget; Shadow DOM or scoped CSS is used.
- Guided flow implemented as a deterministic state machine driven solely by /conversation/flow.json and renders the sequence: Attention Hook → Demographics → Primary Goal → Current Eating Habits → Emotional Root → Role of Nutrition Solutions → Testimonials Carousel → Synthesis + Plan Recommendation.
- Off-route handling: when user asks unrelated/pricing/ingredients/delivery or shows doubt/emotion, the flow pauses; widget displays a natural answer (via Agents SDK) and resumes the guided sequence without robotic phrasing; rules originate from /conversation/offroute.json.
- Brand voice adherence in all UI-rendered assistant messages: bold, direct, identity-focused, transformation-oriented, empathetic yet challenging; multi-bubble pacing for long messages.
- Testimonials carousel widget renders 1–5 transformations, supports horizontal scrolling, and filters by user inputs (age, goals, habits); visuals match provided screenshots.
- Files present: /widget/widget.js, /widget/widget.css, /widget/chat-window.html, /frontend/chatkit.js, /frontend/ui-state-machine.js, /frontend/carousel-widget.js, /frontend/utils.js, /conversation/flow.json, /conversation/offroute.json, /conversation/recommendation_rules.json.
- Performance: first meaningful interaction in under 200ms on modern devices; no blocking of host page.

[Backend Developer]
- Environment: Node.js 18+; Express app boots without errors.
- Endpoints exist and respond:
  - GET /api/health → 200 with simple status.
  - POST /api/message → invokes Agents SDK orchestration; logs state transitions and message metadata.
  - POST /api/rag → queries Supabase; returns rewritten brand-voice responses; logs RAG hits/misses.
  - POST /api/recommend → returns one of: Shred Spartan, Shred Gladiator, Beast Spartan, Beast Gladiator, based on /conversation/recommendation_rules.json and user inputs.
  - POST /api/memory/store and /api/memory/fetch → persist/fetch from Supabase memory_entries; returning users recognized.
  - GET /api/carousel → returns 1–5 transformations filtered by age/goals/habits.
  - POST /api/support → executes Active Client Support routing (acknowledge, RAG if needed, concierge options).
- Logging files written under /backend/logs/ for state transitions, message metadata, RAG hits/misses, recommendation path, support path usage.
- CORS and JSON content-type handling allow widget to call APIs from any WordPress origin as configured.

[Tester]
- /tests/TEST_PLAN.md documents test cases for: guided flow sequencing; off-route scenarios (unrelated, price/ingredient/delivery, emotional, jump ahead, doubt); RAG correctness and brand-voice rewriting; carousel filtering and UI; recommendation mapping with sample inputs; Active Client Support triggers and routing; memory persistence/recognition; endpoint status codes and response schemas; logging verification; performance (<200ms load) and CSS isolation.
- /tests/test.sh (if created) can run smoke tests against all endpoints and basic DOM checks for the widget.
- All deliverables and file paths match exactly as listed under Deliverables.

End of files.
