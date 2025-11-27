## 🌍 Multi-Agent Disaster Response & Early Warning System
### Google AI Agents Capstone Project (Kaggle Intensive 2025)

**A next-generation, fully modular, multi-agent system that detects global disasters, scores severity, generates response plans, requests human approval, stores memory, evaluates quality - all orchestrated offline or with real data connectors.**<br>
<i>Built using principles from Google’s 5-Day AI Agents Intensive Program.</i>

---

### 🚀 Project Overview
This project is a **production-style AI multi-agent system** designed to:
- Detect **real-world disaster signals** (earthquakes, floods, wildfires, heatwaves)
- Score severity using a risk model
- Generate **actionable response plans**
- Ask for **human approval** (long-running operations pattern)
- Store long-term memory of decisions
- Evaluate plan quality using LLM-like judgment (offline-safe)
- Run fully **offline** or optionally with **real-data connectors**
This system represents a **practical model of how agents work in disaster management,** public safety, and automated command centers.

---

### 🧠 Key Features (Matches Kaggle Capstone Requirements)

The project includes all **mandatory features** for scoring: <br>

✔ **1. Multi-Agent System**

- `SignalAgent`
- `RiskAgent`
- `PlannerAgent`
- `HumanApprovalAgent`
- `EvaluationAgent`
- `CoordinatorAgent` (controller/orchestrator)

✔ **2. Tools (MCP-style custom tools)**

- Tools for fetching signals
- Tools for scoring & planning
- Tools for evaluation
- Tools for human approval
- Offline-safe real data extension via `real_data_tools/*`

✔ **3. Sessions & Memory**

- JSON-based long-term memory
- Episode logging
- Context-aware plan history

✔ **4. Observability**

- Logging system in `assets/logs.json`
- Tracing via coordinator reasoning logs
- Debug prints for message bus traffic

✔ **5. Agent Evaluation**

- Auto-judge evaluation for plan quality
- Offline-safe Gemini wrapper included
- Verdict, score, explanation

✔ **Bonus Features**

- Real-data augmentation (offline-safe synthetic generators)
- Deterministic fallback patterns
- Clean tool schema registry
- Ready-to-deploy structure for FastAPI / Vertex Agent Engine

--- 

### 🏗️ Architecture

                        ┌─────────────────────┐
                        │   Signal Agent       │
                        │  (fetch signals)     │
                        └─────────┬───────────┘
                                  │ signals.raw
                                  ▼
                        ┌─────────────────────┐
                        │    Risk Agent       │
                        │ (score severity)    │
                        └─────────┬───────────┘
                                  │ signals.scored
                                  ▼
                        ┌─────────────────────┐
                        │   Planner Agent     │
                        │ (create actions)    │
                        └─────────┬───────────┘
                                  │ plans.created
                                  ▼
                    ┌────────────────────────────────┐
                    │ Human Approval Agent (LLM/HITL)│
                    └────────────────┬───────────────┘
                                     │ approval
                                     ▼
                        ┌─────────────────────┐
                        │ Evaluation Agent    │
                        │ (judge quality)     │
                        └─────────┬───────────┘
                                  │ evaluation.done
                                  ▼
                        ┌─────────────────────┐
                        │  Coordinator Agent  │
                        │  (orchestration)    │
                        └─────────────────────┘


---

### 📁 Project Structure

```
agents-capstone/
│
├── agents/
│   ├── signal_agent.py
│   ├── risk_agent.py
│   ├── planner_agent.py
│   ├── approval_agent.py
│   ├── evaluation_agent.py
│   ├── coordinator_agent.py
│
├── tools/
│   ├── tool_schemas.py
│   ├── gemini_wrapper.py
│   ├── real_data_tools/
│       ├── earthquake_tool.py
│       ├── wildfire_tool.py
│       ├── flood_tool.py
│       ├── heatwave_tool.py
│       ├── weather_tool.py
│
├── core/
│   ├── message_bus.py
│   ├── logger.py
│
├── memory/
│   ├── memory_store.py
│
├── assets/
│   ├── demo_signals.json
│   ├── logs.json
│
├── scripts/
│   ├── run_demo.py
│
├── tests/
│   ├── test_memory.py
│   ├── test_message_bus.py
│
├── README.md
├── requirements.txt
└── .gitignore
```
---

### 🔥 How It Works (Step-by-Step)

**1. SignalAgent collects events**

From:

- `demo_signals.json`
- (Optional) synthetic real-data connectors

**2. RiskAgent scores severity**

- Using magnitude, timestamp, type → produces a “severity score”.

**3. PlannerAgent generates response plans**

Turning severity into scheduled actions such as:
 
 - Evacuations
 - Warnings
 - Firefighting deployment
 - Rescue planning

**4. HumanApprovalAgent**

Simulates HITL approval:

- In real life → a human
- In demo → auto-approve

**5. Memory stored**

Every plan saved as a session in `memory/memory.json`.

**6. EvaluationAgent scores the plan**

Produces:

 - score
 - verdict
 - explanation

**7. Coordinator returns final output**

Which includes:

 - reasoning trace
 - full plan
 - scored signals
 - approval
 - evaluation score

---

### 🧪 Running the System (Local)

**1. Activate your virtual environment:**

`.\.venv\Scripts\Activate.ps1`

**2. Run tests:**

`pytest -q`

**3. Run the demo:**

`python -u scripts/run_demo.py`

**You will see complete agent orchestration & JSON output.**

---
### 📊 Sample Output

Includes:

 - reasoning_log
 - plan
 - evaluations
 - human approval
 - scored signals
 - enriched signals from real data tools

---

### 🔗 Tech Stack

- Python 3.10+
- LLM-ready architecture (Gemini placeholder)
- Message bus system
- Tool schema registry
- JSON memory store
- Offline-safe evaluation

---

### 🏷️ Tags

`ai-agents` `multi-agent-system` `disaster-response` `google-adk` ,
`gemini-api` `context-engineering` `kaggle-capstone`

---

### ⭐ Author
## LOKESH K
**Built with ❤️ using Google’s Agent Development Kit(ADK) concepts and Kaggle’s 5-Day Intensive Framework.**






