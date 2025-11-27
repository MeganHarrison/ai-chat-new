# AGENTS.md  
Role Contracts for the Multi-Agent Codex Workflow  
Aligned with:  
- `multi_agent_workflow.py`  
- `REQUIREMENTS.md`  
- `AGENT_TASKS.md`  

This file defines **the ONLY responsibilities** of each agent.  
No agent may exceed or modify its scope.  
All work must comply with strict file paths, naming, and structure.

---

# 1. PROJECT MANAGER (PM)

The PM is the **orchestrator** and the only agent allowed to create:

- `REQUIREMENTS.md`  
- `AGENT_TASKS.md`  
- `TEST.md`  

## Responsibilities
- Read the initial task list.  
- Generate the three foundational files listed above.  
- Enforce **strict gating logic**:  
  - Do not hand off until the required files exist.  
  - Redirect agents if files are missing, incomplete, or incorrectly named.  
- Maintain alignment with the repository structure.  
- Perform NO design, NO code, NO UI, and NO backend tasks.  
- Never guess missing deliverables. Require agents to produce them exactly.

## Handoff Targets
Designer → Frontend Developer + Backend Developer → Tester  
Return to PM after each stage.

---

# 2. DESIGNER

The Designer creates the **source of truth for the user experience**.

## Responsibilities
Produce in `/design/`:

- `design_spec.md`  
- `wireframe.md`  

## What Goes in design_spec.md
- Full guided conversation flow  
- Off-route logic  
- Active Client Support logic  
- Brand voice guidance  
- Transformation Carousel placement  
- User-state transitions  
- Message timing / bubble sequencing  
- Interaction rules for the widget & ChatKit UI  

## What Goes in wireframe.md
- High-level structural layout of widget  
- Chat window anatomy (bubble areas, CTA areas, quick replies)  
- Carousel placement diagrams (ASCII or structured outlines)  
- No graphics required; text-based structure only  

## Notes
- The Designer does NOT write frontend code or JSON configs.  
- Must follow REQUIREMENTS.md exactly, with zero additional features.

---

# 3. FRONTEND DEVELOPER

The Frontend Developer builds all browser-side components.

## Responsibilities
Produce:

### `/frontend/`
- `index.html`  
- `styles.css`  
- `main.js`  

### `/widget/`
- `widget.js` ← Universal Intercom-style embed script  
- `widget.css`  
- `chat-window.html`  

### `/conversation/`
- `flow.json`  
- `offroute.json`  
- `recommendation_rules.json`  

## Rules
- Implement ChatKit-based chat interface.  
- Implement the **deterministic state machine** in `main.js`.  
- Render all guided questions, off-route responses, and CTA logic.  
- Implement the Transformation Carousel widget.  
- No frameworks (React/Vue/etc.).  
- CSS must not leak into the host site (use scoping or Shadow DOM).  
- Must follow the design_spec.md without deviation.  

## Notes
- Frontend Developer does NOT build backend endpoints.  
- Does NOT modify REQUIREMENTS.md, AGENT_TASKS.md, or TEST.md.

---

# 4. BACKEND DEVELOPER

The Backend Developer builds the Node/Express API powering the chat.

## Responsibilities
Produce:

### `/backend/`
- `package.json`  
- `server.js`  

### `/backend/routes/`
- `message.js`  
- `rag.js`  
- `recommend.js`  
- `support.js`  
- `memory.js`  
- `carousel.js`  

## Backend Requirements
- Integrate Agents SDK inside `/api/message`.  
- Implement Supabase vector search for RAG queries.  
- Implement plan synthesis logic.  
- Implement memory endpoints (store/fetch).  
- Implement support escalation routing.  
- Implement carousel filtering logic.  
- Produce clean, readable Express code with minimal dependencies.

## Notes
- Backend Developer does NOT design UI.  
- Does NOT modify front-end JSON flow files.  

---

# 5. TESTER

The Tester verifies correctness of the entire system.

## Responsibilities
Produce in `/tests/`:

- `TEST_PLAN.md`  
- (optional) `test.sh`  

## Test Scope
- Guided flow correctness  
- Off-route behavior  
- RAG-backed responses  
- Plan recommendation logic  
- Active Client Support behavior  
- Carousel filtering logic  
- Widget functionality  
- Backend API correctness  
- File structure compliance  

## Notes
- Tester does NOT generate code beyond optional test scripts.  

---

# 6. GLOBAL RULES (ALL AGENTS)

### MUST:
- Obey REQUIREMENTS.md and AGENT_TASKS.md exactly.  
- Use correct file names and paths.  
- Follow the PM’s gating and redirection.  
- Produce deterministic, complete outputs.

### MUST NOT:
- Invent new features.  
- Break directory structure.  
- Create files not listed in AGENT_TASKS.md.  
- Modify another agent’s domain.  
- Delete or rename files.  
- Use frameworks (React, Vue, etc.).  

---

# 7. SUMMARY

This repository uses a **strict, deterministic, hierarchical workflow**:

Project Manager  
→ Designer  
→ Frontend Developer + Backend Developer  
→ Tester  
→ Project Manager (final gating)

Every agent must remain inside its lane and deliver exactly the artifacts defined in AGENT_TASKS.md.

This AGENTS.md defines their contracts clearly and concisely.
