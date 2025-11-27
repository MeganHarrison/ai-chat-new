# Nutrition Solutions AI Sales Coach — Test Plan

## Conventions
- Tasks include `[Owner]` tags and explicit acceptance criteria.
- Focus areas: guided flow, off-route handling, memory, RAG accuracy, transformation carousel, CTAs, and API contracts.

## 1. Conversation Flow and Branching
- **[Tester] Guided path:** hook → demographics → goal → habits → emotional_root → ns_role → carousel_recos → synthesis_plan → cta.
  - Prompts are concise; slot values are summarized correctly; plan recommendations surface with ≥2 CTAs.
- **[Tester] Consistency + branching:** conflicting inputs trigger clarifying questions; skipping two steps offers pause + helpful CTAs.

## 2. Off-Route Handling
- **Unrelated question:** Pause, answer via RAG, resume prompt restores next state.
- **Price doubt:** Value reframe with CTA options (Resume, See Plans).
- **Emotional disclosure:** Empathetic 2-sentence reply plus actionable encouragement before resuming.

## 3. RAG Correctness
- Ask 3 factual (policy/product) and 1 testimonial request.
  - Answers match seeded Supabase data, use brand tone, include next step, and show RAG indicator in UI.

## 4. Memory
- **Short-term:** Bot references slots later in-session without re-asking.
- **Long-term:** Returning visitor greeted with prior context; can resume last state/plan.
- **Forget me:** After request, long-term memory cleared on refresh.

## 5. Active Client Support
- Trigger “current client + delivery issue.”
  - Bot acknowledges, attempts RAG answer, then offers text/call/form options with expected response time.

## 6. Transformation Carousel
- Provide goal/gender/age/timeline.
  - Carousel items match filters, include accessible roles, arrow-key navigation, and CTAs leading to plan context.

## 7. Backend APIs
- **/api/chat/next:** Returns messages, state, slots, UI directives.
- **/api/rag/search:** Returns `{id,type,title,snippet,score,tags}` respecting filters.
- **/api/recommendations:** Provides plans with fitScore + rationale tied to slots.
- **/api/memory (GET/POST):** Retrieves and upserts visitor data.
- **/api/support/route:** Includes text/call/form options and ticket id when form used.
- **/api/logs/state:** Records state transitions with timestamps.

## 8. Frontend UX
- Chat renders bubbles, quick replies, CTAs, carousel, and typing indicators; accessible via ARIA roles and keyboard focus.
- Indicators for memory (“Welcome back”) and RAG badges show only when applicable.

## 9. Tone & Brand
- Sample 10 interactions; verify bold, direct, empathetic voice with no fabricated facts.

## 10. Failure Handling
- **RAG error:** UI retries gracefully; flow can continue.
- **Offline:** UI shows offline state and queues message for retry.

## 11. Workflow Gates
- Confirm PM artifacts (REQUIREMENTS.md, AGENT_TASKS.md, TEST.md), Designer deliverables (/design/design_spec.md), and dev outputs (/frontend/index.html, /backend/server.js) exist before testing proceeds.
