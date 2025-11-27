# Task List

This document defines the complete project specification used by the multi-agent workflow. It must include the following sections:

- **Goal**
- **High-Level Requirements**
- **Roles**
- **Constraints**
- **Deliverables**

The Project Manager agent reads ONLY this file and converts it into REQUIREMENTS.md, AGENT_TASKS.md, and TEST.md.

---

## 🎯 Goal
Describe the primary goal of the project in 2–4 sentences that frame the bot as a conversion-focused transformation coach with a natural, scripted conversation flow.


## 📌 High-Level Requirements
List the functional and non-functional requirements.  
Keep them short, directive, and unambiguous.

Example requirements should cover:
- Intercom-style chat surface that feels conversational, coach-like, and conversion-oriented with a scripted transformation assessment.
- Guided question sequence (hook, demographics, goals, habits, emotional root, role of Nutrition Solutions, testimonials carousel, synthesis + recommendation) with conditional messaging (plan/path variations).
- Seamless off-route capability: pause the script for unrelated questions, doubt, price queries, or emotional inputs, respond naturally (reasoning + RAG), and transition back to the flow or CTA without feeling forced.
- RAG integration via Supabase vector search for product details, pricing, policies, testimonials, and meal-plan data; wrap retrieved facts in motivational, brand-aligned copy.
- Support for Active Client users (support path trigger, RAG-backed technical answers, fallback to concierge handoff text/call/form) plus ability to flag and route to human support.
- Short-term and long-term memory to recognize returning visitors and keep context across sessions.
- Transformation Carousel widget filtered by user inputs and CTA options (plan recommendations, support contact, or form submission).
- Backend APIs (recommendation synthesis, RAG query endpoints, memory capture, support routing) and frontend hooks for Chatkit interface + carousel.
- Logging/analytics hooks to capture conversation state for PM gating (per multi-agent workflow requirements).

## 🧩 Roles
Define what each agent is responsible for.  
This must stay aligned with your `multi_agent_workflow.py` setup.

### Designer
- Translate the scripted flow into a multi-agent conversation design brief: the hook, question tiers, CTA logic, transformation carousel placement, and tone for both new visitors and current clients.
- Document off-route handling, Active Client support triggers, and plan recommendation conditions (Shred/Beast plan matrix).
- Supply a wireframe description or structure notes that a Frontend Developer can follow to build the Intercom-like Chatkit UI and carousel widget.

### Frontend Developer
- Implement the Chatkit-powered chat interface, prompt/CTA surfaces, and Transformation Carousel widget per the design brief while honoring brand voice and pacing.
- Wire UI state transitions for guided questions vs. off-route conversations and surface Active Client support options (including RAG failure fallback prompts).
- Hook into the backend APIs for plan recommendations, RAG responses, memory indicators, and support routing; minimize frameworks unless needed.

### Backend Developer
- Build the API layer to power guided recommendations, RAG retrievals (via Supabase vectors), client support routing, and short/long-term memory capture/lookup.
- Ensure reasoning wraps factual responses, supply support handoff message templates, and expose endpoints that the frontend can call for plan synthesis, carousel data, and support actions.
- Keep storage in-memory or Supabase; keep code readable and self-contained.

### Tester
- Verify each requirement: guided flow, off-route handling, RAG + reasoning responses, Active Client support path or handoff, transformation carousel filtering, and backend endpoints.
- Provide a test plan and lightweight verification steps (script or checklist) that ensures conversational guards, recommendation logic, and support pathways work as described.

## ⚙️ Constraints
Include technical, operational, or architectural constraints.

Example:
- Must run without external dependencies unless specified.
- No frameworks unless explicitly allowed.
- All files must be small, readable, and saved to the correct folders.
- Follow all file names exactly as listed in AGENT_TASKS.md.

## 📦 Deliverables
List everything that must be produced by the workflow.

Example:

### Project-Root Deliverables
- REQUIREMENTS.md
- TEST.md
- AGENT_TASKS.md

### Designer Deliverables
- /design/design_spec.md (conversation flow, off-route breaks, carousel placement, CTA copy, Active Client support triggers)
- /design/wireframe.md (Chatkit + carousel layout notes and flow diagram)

### Frontend Deliverables
- /frontend/index.html (Intercom-style chat window with Chatkit, transformation carousel area, Active Client support prompt)
- /frontend/styles.css (brand-compliant styling, responsive layout, carousel design)
- /frontend/main.js (chat state machine covering guided flow, off-route handling, memory flags, RAG call integration, support CTA)

### Backend Deliverables
- /backend/server.js (API routes for recommendations, RAG queries, memory capture, support routing, plan synthesis)
- /backend/package.json (startup script, dependencies for Supabase/RAG/memory handling)

### Tester Deliverables
- /tests/TEST_PLAN.md (checklist covering conversation flow, RAG behavior, off-route logic, Active Client support path, and API contracts)
- /tests/test.sh (optional script that pings backend endpoints and validates designed responses if feasible)

## 📝 Notes (Optional)
- Guided script is critical (hook → demographics → goals → habits → emotional root → role of NS → testimonials → synthesis); ensure every agent references it for tone and sequencing.
- Off-route logic must feel human: pause the flow, answer with reasoning + RAG, and nudge back to the CTA or next question without sounding rigid.
- Active Client support prompts must surface a way to text/call concierge, offer a short form handoff, and rely on RAG answers before escalating.
- Use the Intelligent Routing Matrix to decide when to call RAG: product/pricing/policy questions, comparisons, and technical explanations must be enhanced with motivational framing.
