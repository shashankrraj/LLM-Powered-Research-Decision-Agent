# LLM‑Powered Research & Decision Agent

> **Goal:** Turn vague business questions into analyst‑grade decision memos using local + cloud LLMs.

---

## 1. What this agent does

Input: a fuzzy question such as:

> *"Is this company worth entering in India?"*

Output: a **structured decision memo** that includes:

- Clarified sub‑questions (market, competition, regulation, economics, execution risks)
- Evidence from **web search** and **local knowledge base** (PDFs, notes)
- Reasoned judgments from an LLM
- A clear **recommendation** with supporting arguments and caveats

This is essentially an always‑on **business analyst / research associate** that you can point at any topic.

---

## 2. High‑level architecture

### 2.1 Components

- **LLM layer (local, via Ollama)**
  - `ollama/deepseek-r1:1.5b` → default reasoning / analysis model
  - `ollama/qwen2.5:3b` → coding / tool‑oriented tasks

- **Premium LLM layer (cloud, optional)**
  - `anthropic/claude-3.5-sonnet` → used only for
    - high‑stakes checks,
    - polishing important memos,
    - complex reasoning where we want extra assurance.

- **OpenClaw agent + tools**
  - **Tools** (planned):
    - `web_search` – Brave Search for web content
    - `web_fetch` – fetching & cleaning pages
    - `kb_search` – vector DB lookups over local PDFs/notes
  - **Agent** orchestrates:
    - breaking the question into sub‑questions
    - calling tools
    - synthesising a memo

- **Backend API (FastAPI)**
  - Simple HTTP API:
    - `POST /analyze` → takes a question + context, returns a memo JSON
  - Calls the OpenClaw agent and handles request/response shaping.

- **Frontend (React)**
  - Minimal web UI that lets a user:
    - enter a question,
    - see progress/steps,
    - view a formatted decision memo.

- **Vector DB (Chroma/FAISS)**
  - Stores embeddings of:
    - PDFs (annual reports, industry notes)
    - internal strategy docs
  - Exposed as a tool the agent can call ("kb_search").

---

## 3. Execution flow (MVP)

1. **User asks a question** via the UI or directly via API.
2. **Backend** forwards to OpenClaw agent.
3. **Agent (local DeepSeek) does:**
   - Clarify the question / restate scope.
   - Generate sub‑questions.
   - For each sub‑question:
     - call `web_search` + `web_fetch` as needed
     - call `kb_search` for local knowledge
   - Synthesize findings into a memo JSON:
     - `sections`: list of sections with title + content
     - `risks`: bullet list
     - `recommendation`: short summary (yes/no/depends) with rationale
4. **Backend** returns JSON.
5. **Frontend** renders memo sections in a readable layout.

Later, for high‑stakes runs, we can:

- Have Sonnet **review** the memo for coherence and missing angles.
- Add **confidence scores** and suggested next steps.

---

## 4. Roadmap

### Phase 1 – Skeleton

- [ ] **TASK‑005** – Finalise architecture + README (this document)
- [ ] **TASK‑006** – FastAPI backend with `/analyze` calling the OpenClaw agent
- [ ] **TASK‑007** – Vector DB wiring (Chroma/FAISS) + ingestion script
- [ ] **TASK‑008** – Basic React UI: input box + memo rendering
- [ ] **TASK‑009** – Testing + bug‑logging framework (unit + smoke tests)

### Phase 2 – Quality & depth

- [ ] Better prompt design for breaking down questions
- [ ] Richer memo structure (sections, exhibits, assumptions)
- [ ] Basic caching of previous analyses

### Phase 3 – Upgrade path

- [ ] Multi‑agent debate (pro/con agents)
- [ ] Confidence scoring and calibrated language
- [ ] PDF / PPT export of memos

---

## 5. Dev notes

- **Default models** are **local** to keep cost near zero.
- Cloud models (Anthropic, OpenAI) are used **only** when explicitly requested.
- All significant work items are tracked in the Notion board: *"Logan – Engineering Kanban"*.
