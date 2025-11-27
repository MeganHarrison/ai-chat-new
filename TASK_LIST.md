# TASK_LIST.md  
This document defines the complete system specification for the multi-agent workflow.  
The Project Manager agent reads ONLY this file and converts it into:

- REQUIREMENTS.md  
- AGENT_TASKS.md  
- TEST.md  

This document provides the authoritative upstream specification for the Nutrition Solutions AI Sales Coach widget.

---

# 🎯 GOAL  

Build a **full-stack AI chat widget**, similar to Intercom, that can be embedded on any WordPress website via a single `<script src="...">` embed.

The widget uses **ChatKit** for the chat interface and **OpenAI Agents SDK** for all reasoning, guided flow handling, RAG queries, plan recommendations, off-route logic, and Active Client Support routing.  
The experience must feel like a **high-conversion transformation coach**, powered by a structured assessment + intelligent assistant capable of breaking from the script naturally.

The full system includes:
- Embeddable widget  
- ChatKit UI  
- Guided flow state machine  
- Off-route intelligence  
- Testimonials carousel widget  
- Agents SDK backend  
- Supabase RAG + memory  
- Active Client Support path  
- Recommendation engine  
- Logging + analytics hooks  

---

# 📌 HIGH-LEVEL REQUIREMENTS  

## Functional Requirements

### 1. Intercom-Style Widget  
- Must load via `<script src="https://yourdomain.com/widget.js" defer></script>`.  
- Inject floating bubble into any site.  
- Opens a ChatKit-powered chat window.  
- Mobile-responsive.  
- No frameworks (pure Vanilla JS).  

### 2. Guided Transformation Script  
Implement the complete guided assessment sequence from PLANNING.md:

1. Attention Hook  
2. Demographics  
3. Primary Goal  
4. Current Eating Habits  
5. Emotional Root ("Why Now")  
6. Role of Nutrition Solutions  
7. Testimonials Carousel  
8. Synthesis + Plan Recommendation  

- Script is stored in static JSON (`/conversation/flow.json`).  
- Flow must be implemented as a **deterministic state machine**.  

### 3. Off-Route Intelligence  
If the user:
- asks unrelated questions  
- expresses doubt  
- jumps ahead  
- becomes emotional  
- asks price/ingredient/delivery questions  

…the agent must:
- pause flow  
- answer naturally using Agents SDK  
- optionally RAG (Supabase)  
- gently return to the guided sequence without sounding forced  

Off-route rules stored in `conversation/offroute.json`.

### 4. Brand Voice Requirements  
All responses must adhere to Nutrition Solutions brand voice:
- bold  
- direct  
- identity-focused  
- transformation-oriented  
- empathetic yet challenging  
- no robotic phrasing  

### 5. RAG (Supabase Vector Search)  
Backend must query Supabase for:
- products  
- pricing  
- policies  
- meal plans  
- FAQ content  
- testimonials  

RAG responses must be wrapped in motivational copy (NEVER pure factual dump).

### 6. Transformation Carousel Widget  
- A ChatKit widget that displays 1–5 transformations.  
- Supports horizontal scrolling.  
- Data served by backend (`/api/carousel`).  
- Must filter based on user inputs (age, goals, habits).  
- Widget must match screenshots provided.  

### 7. Recommendation Logic  
Based on user responses:

- **Shred Spartan**  
- **Shred Gladiator**  
- **Beast Spartan**  
- **Beast Gladiator**

Rules defined in `conversation/recommendation_rules.json`.

### 8. Active Client Support Path  
Trigger when user says:
- “I’m a current client”  
- “Question about my order”  
- “Need help with my meals”  

Support path rules:
- acknowledge  
- RAG for technical answers  
- fallback to concierge handoff:  
  - Call  
  - Text  
  - Submit short form  

### 9. Memory  
- Short-term memory: per-session  
- Long-term memory: Supabase table (`memory_entries`)  
- Recognize returning users  
- Personalize messages  

### 10. Backend APIs  
Expose the following endpoints:

GET /api/health
POST /api/message → Agents SDK orchestration
POST /api/rag → Supabase vector search
POST /api/recommend → plan synthesis
POST /api/memory/store → save memory entries
POST /api/memory/fetch → load user profile
GET /api/carousel → testimonials widget
POST /api/support → client support routing


### 11. Logging & Analytics  
Log:
- state transitions  
- message metadata  
- RAG hits/misses  
- recommendation path  
- support path usage  

Files written to `/backend/logs/`.

---

## Non-Functional Requirements  
- Must feel **human**, not scripted or robotic.  
- Use **multi-bubble sequences** for long messages.  
- Must load in under 200ms on modern devices.  
- Widget must not conflict with website CSS (Shadow DOM or scoped CSS).  
- Backend must run on Node 18+.  
- Code must remain readable + small.  
- No build systems unless strictly required.  

---

# 🧩 ROLES  

## Project Manager  
- Convert TASK_LIST.md → REQUIREMENTS.md, AGENT_TASKS.md, TEST.md  
- Ensure deterministic file generation  

## Designer  
Produce:
- `/design/design_spec.md`  
- `/design/wireframe.md`  
Must include:
- Chat window layout  
- Bubble pacing rules  
- Widget specs  
- State machine diagrams  
- Tone rules  
- Message sequencing  
- Active Client Support logic  

## Frontend Developer  
Implement:

- `/widget/widget.js` → embed script  
- `/widget/widget.css` → styling  
- `/frontend/chatkit.js` → ChatKit integration  
- `/frontend/ui-state-machine.js`  
- `/frontend/carousel-widget.js`  
- `/frontend/utils.js`

Frontend responsibilities:
- inject bubble  
- open/close animation  
- chat window creation  
- message rendering  
- quick replies UI  
- widgets UI  
- error states  
- mobile support  

## Backend Developer  
Implement Node/Express backend:

- `/backend/server.js`  
- `/backend/routes/*.js`  
- Agents SDK integration  
- RAG retrieval  
- memory store/load  
- recommendation synthesis  
- support routing  
- transformation carousel filtering  

## Tester  
Produce:

- `/tests/TEST_PLAN.md`  
- `/tests/test.sh`  

Must test:
- guided flow  
- off-route handling  
- RAG correctness  
- widget rendering  
- plan recommendation logic  
- Active Client Support path  
- API contract consistency  

---

# ⚙️ CONSTRAINTS  

- **Frontend:** Vanilla JS only.  
- **Widget:** Single embed file (`widget.js`).  
- **No frameworks** (React/Vue/Svelte prohibited).  
- **Backend:** Node.js + Express only.  
- **Agents SDK** required for all reasoning.  
- **ChatKit** required for UI.  
- **Static scripts** stored in `/conversation/`.  
- **Supabase** required for RAG & memory.  
- All deliverables must match paths exactly.  
- No renaming files or folders.  

---

# 📦 DELIVERABLES  

## Project Root
- REQUIREMENTS.md  
- AGENT_TASKS.md  
- TEST.md  

## /design
- design_spec.md  
- wireframe.md  

## /conversation
- flow.json  
- offroute.json  
- recommendation_rules.json  

## /widget
- widget.js  
- widget.css  
- chat-window.html (HTML template if needed)

## /frontend
- chatkit.js  
- ui-state-machine.js  
- carousel-widget.js  
- utils.js  

## /backend
- server.js  
- /routes/message.js  
- /routes/rag.js  
- /routes/recommend.js  
- /routes/support.js  
- /routes/memory.js  
- /routes/carousel.js  
- package.json  

## /tests
- TEST_PLAN.md  
- test.sh  

---

# 📝 NOTES  

- Agents SDK must orchestrate guided flow state machine + off-route logic.  
- ChatKit messages must use multi-bubble pacing for readability.  
- Carousel widget must visually match the screenshots provided.  
- RAG factual content must be rewritten in brand voice before sending.  
- Returning users must feel recognized and supported.  
- Off-route logic must feel intelligent and human.  
- Support path must allow instant escalation.  

---

**This TASK_LIST.md is the sole source of truth for the multi-agent workflow.**  
