# Nutrition Solutions AI Sales Coach — Requirements

## 1. Product Goal and Scope
- Build a high-converting, Intercom-style chatbot that acts like an elite transformation mentor (bold, direct, empathetic), not a rigid FAQ bot.
- Primary outcomes: qualify prospects, recommend the right Nutrition Solutions (NS) plan, and drive action via CTAs (purchase/consult/support). Secondary outcome: support existing clients.
- Must implement guided transformation flow with conditional branching, intelligent off-route handling, RAG-backed answers wrapped in brand voice, and short/long-term memory.

## 2. Target Users
- Prospects evaluating NS transformation programs.
- Returning visitors who should be recognized and resumed smoothly.
- Active clients needing rapid support for orders, meals, or accounts.

## 3. Conversation Architecture (State Machine)
- **States:** `intro_hook`, `demographics`, `goal`, `habits`, `emotional_root`, `ns_role`, `carousel_recos`, `synthesis_plan`, `cta`, `support_active_client`, `off_route`, `resume`.
- **Transitions:** Default flow goes from hook to CTA; off-route may trigger from any state; active-client keywords jump directly to `support_active_client`.

## 4. Off-Route Handling
- Detect unrelated info requests, price doubts, emotional disclosures, skipped steps.
- Pause guided flow, answer with reasoning/RAG, keep tone bold/empathetic, then offer [Resume] or a relevant CTA.

## 5. Retrieval-Augmented Generation (RAG)
- Use Supabase vector collections for FAQs/policies, testimonials, and plan/meal docs.
- Retrieve top-k (diversified) and pass to Answer Composer that wraps facts in brand voice and suggests next steps.

## 6. Memory Model
- **Short-term:** session map storing current state, slots, and last_off_route.
- **Long-term:** Supabase `memory_long_term` keyed by visitorId (cookie/localStorage) with first/last seen, salient facts, last state, last plan, intent score. Provide “forget me.”

## 7. Active Client Support Path
- Trigger via keywords ("current client", "order issue", etc.).
- Flow: acknowledge → attempt RAG answer → if unresolved, offer text/call/form concierge options → confirm handoff + ETA.

## 8. Transformation Carousel & CTAs
- Show 3–6 testimonial cards filtered by goal/gender/age/timeline/constraints.
- Card anatomy: image, headline, metric, quote, tags, CTA (“See plan like this”).
- Chained CTAs include plan start, consult, text coach, or support.

## 9. Backend API Surface (Baseline)
- `POST /api/chat/next`, `POST /api/rag/search`, `GET /api/recommendations`, `GET /api/carousel`, `GET|POST /api/memory`, `POST /api/support/route`, `POST /api/logs/state`.
- Responses include messages, next state, slots, `ui.indicators` (memory, RAG), CTA/carousel payloads.

## 10. Frontend Implementation Notes
- Intercom-style chat with vanilla JS. Chatkit module renders bubbles, quick replies, CTAs, Transformation Carousel, and indicators.
- Persist visitorId in localStorage and include on every call; ensure ARIA roles and keyboard navigation.

## 11. Brand Voice
- Bold, identity-focused, empathetic, outcome-driven; avoid clinical jargon.
- Keep replies to 1–3 short sentences; never hallucinate; escalate when unsure.

## 12. Constraints & Non-Goals
- Stack: Node.js + Express backend, Supabase storage, vanilla JS frontend.
- Artifacts stay in designated folders.
- Non-goals: payments, deep CRM, multi-language, mobile SDKs.

## 13. Supabase Data Model
- Tables: `rag_docs`, `testimonials`, `plans`, `memory_long_term`, `conv_logs` with embeddings/metadata per requirements.

## 14. Security & Privacy
- Collect minimal PII; anonymize visitorId; support “forget me.”
- Sanitize input; do not expose secrets; secure env vars.
