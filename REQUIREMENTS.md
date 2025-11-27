# REQUIREMENTS.md

System requirements derived from TASK_LIST.md.
These requirements define WHAT must be built (not HOW).
All tasks, deliverables, and tests must be traceable back to these requirements.

---

# 1. SYSTEM OVERVIEW

The system must implement a **full-stack AI chat widget**, similar to Intercom, that can be embedded on any WordPress website through a **single universal embed script**.

The widget must provide:

1. A **ChatKit-based chat interface** embedded into any website.
2. A **guided transformation assessment** that flows through a structured script.
3. Intelligent **off-route handling** using Agents SDK + RAG.
4. A **Transformation Carousel widget** rendered inside the chat.
5. A **plan recommendation engine** driven by rules and reasoning.
6. An **Active Client Support path** that uses RAG first, then escalates to human support.
7. Short-term and long-term **memory** with Supabase storage.
8. A Node.js/Express **backend API layer** orchestrating Agents SDK, RAG, memory, routing, and recommendations.

The experience must not feel robotic. It must match Nutrition Solutions' brand voice: bold, direct, identity-focused, empathetic, and transformation-oriented.

---

# 2. FUNCTIONAL REQUIREMENTS

## 2.1 Widget Loading System

1. The widget must load through:

   ```html
   <script src="https://yourdomain.com/widget.js" defer></script>
   ```

2. The script must:

   * Inject a floating chat bubble into any website.
   * Open/close a chat window when clicked.
   * Load ChatKit and all required CSS/HTML dynamically.
   * Work on all modern browsers.
   * Not conflict with site CSS (Shadow DOM or isolated CSS required).
   * Be mobile-responsive.

3. The widget must function without requiring WordPress or other CMS integration.

---

## 2.2 Chat Interface (ChatKit)

1. The interface must use ChatKit to render:

   * User messages
   * Agent messages
   * Typing indicators
   * Quick reply buttons
   * Carousel widgets
   * Multi-bubble message sequences

2. The UI must:

   * Match the aesthetic of the provided mockups/screenshots.
   * Support custom widgets including the Transformation Carousel.
   * Support loading, error, and fallback states.
   * Render multi-bubble responses where long content is split for readability.

---

## 2.3 Guided Assessment Flow

The guided transformation script must follow the exact sequence:

1. Attention Hook
2. Demographics
3. Primary Goal
4. Current Eating Habits
5. Emotional Root / “Why Now?”
6. Role of Nutrition Solutions
7. Testimonials Showcase (with Transformation Carousel widget)
8. Synthesis + Plan Recommendation

### Requirements:

* The flow must be implemented as a **deterministic state machine**.
* Script content must be stored in static files:

  * `/conversation/flow.json`
  * `/conversation/offroute.json`
* Each question must be presented with selectable quick replies where applicable.
* The system must capture and store all user inputs for use in recommendation synthesis.

---

## 2.4 Off-Route Intelligence

When the user:

* asks unrelated questions
* expresses doubt or emotions
* jumps ahead
* asks about pricing, ingredients, delivery
* types freeform text

The system must:

1. Temporarily pause the guided flow.
2. Respond using Agents SDK reasoning + optional Supabase RAG.
3. Provide a natural, human-feeling response.
4. Gently resume the guided flow without forcing the user.

Off-route rules must be defined in `/conversation/offroute.json`.

---

## 2.5 Brand Voice Requirements

All agent responses must:

* Be bold, direct, identity-focused.
* Use motivational framing.
* Avoid robotic or generic chatbot phrasing.
* Use second-person (“you”) and coach-like tone.
* Break long replies into multi-bubble sequences.
* Wrap all factual RAG results inside brand-aligned motivational context.

---

## 2.6 RAG (Supabase Vector Search)

The system must use Supabase to retrieve:

* product details
* pricing
* policies (refunds, shipping, subscription)
* meal plans
* FAQs
* testimonials

Requirements:

1. Backend must expose a `/api/rag` endpoint.
2. RAG must be performed only when relevant; otherwise rely on reasoning.
3. Factual results must be rewritten into brand voice.
4. Testimonials used for the carousel must come from a Supabase table.

---

## 2.7 Transformation Carousel Widget

1. The widget must render inside ChatKit using a widget component.
2. It must horizontally scroll through transformation images + captions.
3. It must auto-filter based on user inputs:

   * age
   * gender
   * primary goal
   * habits
4. Backend must expose `/api/carousel` to return filtered results.
5. The UI must match the provided aesthetic layout.

---

## 2.8 Recommendation Engine

Rules must follow:

* **Shred Spartan** — fat loss goal + user wants to cook some meals.
* **Shred Gladiator** — fat loss goal + user wants all meals provided.
* **Beast Spartan** — muscle gain goal + user wants to cook some meals.
* **Beast Gladiator** — muscle gain goal + user wants all meals provided.

Requirements:

1. Logic must be defined in `/conversation/recommendation_rules.json`.
2. Backend must expose `/api/recommend`.
3. Recommendations must synthesize:

   * user profile
   * guided flow answers
   * RAG-enhanced reasoning
4. Output must be authoritative, personalized, and psychologically aware.

---

## 2.9 Active Client Support Path

Trigger phrases include:

* “current client”
* “question about my order”
* “help with meals”

Requirements:

1. Detect with regex or semantic classification.
2. Provide supportive acknowledgment.
3. Use RAG for technical answers.
4. If unresolved, escalate to human support:

   * offer phone number
   * offer SMS option
   * provide short form submission
5. Backend must expose route: `/api/support`.

---

## 2.10 Memory System

### Short-Term Memory

* Lives per-session inside state machine.

### Long-Term Memory

* Stored in Supabase table defined by backend.
* Must store:

  * name
  * goals
  * preferences
  * past interactions
* Must fetch memory at session start and personalize conversation accordingly.

Backend must expose:

* `/api/memory/store`
* `/api/memory/fetch`

---

## 2.11 Backend API Requirements

The backend must expose:

```
GET  /api/health
POST /api/message
POST /api/rag
POST /api/recommend
POST /api/memory/store
POST /api/memory/fetch
GET  /api/carousel
POST /api/support
```

Requirements:

* All endpoints must return JSON.
* All errors must return structured error responses.
* Agents SDK must handle orchestration within `/api/message`.

---

## 2.12 Logging & Analytics

System must log:

* state transitions
* RAG hits/misses
* plan recommendations
* support escalations
* off-route triggers

Logs must be stored in `/backend/logs/`.

---

# 3. NON-FUNCTIONAL REQUIREMENTS

1. Widget must load in under 200ms.
2. Must be mobile-first and fully responsive.
3. Must not require React, Vue, or any framework.
4. Must not interfere with website CSS.
5. Code must be readable, modular, and small.
6. Backend must run on Node 18+.
7. All files must match the directory structure exactly.

---

# 4. CONVERSATION STATE MACHINE REQUIREMENTS

The state machine must:

1. Include states for each guided step.
2. Include states for:

   * off-route
   * Active Client Support
   * multi-bubble sequences
   * waiting for user input
3. Support transitions:

   * next step
   * back to flow from off-route
   * interrupt when user inputs support triggers
4. Emit metadata for analytics.
5. Pass all state data to recommendation engine.

---

# 5. FILE STRUCTURE REQUIREMENTS

The following files MUST exist:

```
/design/design_spec.md
/design/wireframe.md

/conversation/flow.json
/conversation/offroute.json
/conversation/recommendation_rules.json

/widget/widget.js
/widget/widget.css
/widget/chat-window.html

/frontend/chatkit.js
/frontend/ui-state-machine.js
/frontend/carousel-widget.js
/frontend/utils.js

/backend/server.js
/backend/routes/message.js
/backend/routes/rag.js
/backend/routes/recommend.js
/backend/routes/support.js
/backend/routes/memory.js
/backend/routes/carousel.js
/backend/package.json
/backend/logs/

/tests/TEST_PLAN.md
/tests/test.sh
```

No renaming allowed.

---

# 6. ACCEPTANCE CRITERIA

The system is complete when:

1. The widget loads on a blank HTML file with the embed script.
2. Chat opens and functions through ChatKit UI.
3. Guided flow progresses exactly as scripted.
4. Off-route responses behave naturally and resume flow.
5. Transformation Carousel loads and filters correctly.
6. Recommendations match rule logic.
7. Active Client Support triggers from user messages.
8. RAG responds for all factual queries.
9. Memory stores and retrieves correctly.
10. All backend routes return valid JSON.
11. TEST_PLAN.md passes all checklist items.
12. No framework dependencies exist on frontend.

---

This document defines WHAT must be built.
AGENT_TASKS.md will specify HOW each agent produces their required files.
TEST.md will define the validation framework.
