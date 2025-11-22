# Google 5-Day AI Agents Intensive — Hands-On Code & Notes

This repository contains the hands-on code, notes, and experiments I completed while participating in Google’s **5-Day AI Agents Intensive Course**, taught by Google’s ML researchers and engineers.  
The course focuses on building practical, production-ready AI agents using the **Agent Development Kit (ADK)**, **Gemini**, **Model Context Protocol (MCP)**, and other modern agentic frameworks.

This repo is organized by **Day 1 → Day 5**, following the exact structure of the programme.

---

## 📚 What the 5-Day Intensive Covers

The programme blends conceptual deep dives with hands-on codelabs, whitepapers, podcasts, and live sessions.  
Over five days, participants explore:

- **Models** (foundations for agent reasoning)
- **Tools** (actions, external APIs, real-time data access)
- **Orchestration** (how agents coordinate decisions)
- **Memory** (sessions, working memory, long-term memory)
- **Evaluation** (logs, traces, metrics, LLM-as-a-judge)
- **Productionization** (deployment, scaling, A2A protocol)

By the end, learners can build reliable, observable, multi-agent systems ready for real-world use.

---

# 🗂️ Repository Structure

day_1/
day_2/
day_3/
day_4/
day_5/



Each folder contains:

- My hands-on code from the daily codelabs  
- Additional scripts I wrote to deepen understanding  
- Notes and experiments based on the whitepapers  
- Mini-agent builds and tests  

---

# 🧭 Day-by-Day Breakdown

## **Day 1 — Introduction to Agents**
**Focus:** Foundations of AI agents, taxonomy, capabilities, reliability, Agent Ops, agent interoperability, identity & security.

**Hands-on work included:**
- Building the first AI agent using **Gemini + ADK**
- Implementing Google Search as a real-time tool
- Creating the first **multi-agent system**
- Exploring basic architectural patterns

**Course materials included:**
- Intro whitepaper - available [here](https://drive.google.com/file/d/1C-HvqgxM7dj4G2kCQLnuMXi1fTpXRdpx/view).
- NotebookLM summary podcast - available [here](https://www.youtube.com/watch?v=zTxvGzpfF-g).  
 
 
- Two codelabs (first agent + multi-agent systems)

---

## **Day 2 — Agent Tools & Interoperability with MCP**
**Focus:** External tools, tool design best practices, Model Context Protocol (MCP), long-running operations, enterprise readiness.

**Hands-on work included:**
- Creating custom tools from Python functions  
- Extending agent actions using ADK  
- Implementing MCP  
- Building long-running operations (pause → resume)

**Course materials included:**
- Tools & MCP whitepaper - available [here](https://drive.google.com/file/d/1ENMUDzybOzxnycQQxNh5sE9quRd0s3Sd/view)
- NotebookLM podcast - available [here](https://www.youtube.com/watch?v=Cr4NA6rxHAM)
- Codelabs on tool design, MCP, and long-running ops

---

## **Day 3 — Context Engineering: Sessions & Memory**
**Focus:** Statefulness, context windows, assembling dynamic context, session history, working memory, long-term persistence.

**Hands-on work included:**
- Making agents stateful  
- Managing session conversation history  
- Context engineering patterns in ADK  
- Adding long-term memory across separate sessions

**Course materials included:**
- Context Engineering whitepaper  - available [here](https://drive.google.com/file/d/1JW6Q_wwvBjMz9xzOtTldFfPiF7BrdEeQ/view)
- NotebookLM podcast - available [here](https://www.youtube.com/watch?v=FMcExVE15a4) 
- Codelabs on context management and memory

---

## **Day 4 — Agent Quality**
**Focus:** Observability and evaluation: logs, traces, metrics, HITL evaluation, LLM-as-a-judge, debugging agent behavior.

**Hands-on work included:**
- Instrumenting logs, traces, and metrics  
- Evaluating agent responses  
- Understanding agent decision flows  
- Debugging failure cases using ADK’s observability tools

**Course materials included:**
- Agent Quality whitepaper  - available [here](https://drive.google.com/file/d/1EnTSGztSrjooYMLaDe8EnoATfsSoe3xv/view)
- NotebookLM podcast  - available [here](https://www.youtube.com/watch?v=LFQRy-Ci-lk)
- Codelabs on debugging and evaluation

---

## **Day 5 — Prototype to Production**
**Focus:** Deployment, scaling, productionization, Agent2Agent (A2A) Protocol, multi-agent systems on Vertex AI.

**Hands-on work included:**
- Building multi-agent systems using A2A  
- Local-to-cloud agent deployment  
- Optional deployment to **Vertex AI Agent Engine**

**Course materials included:**
- Prototype-to-Production whitepaper - available [here](https://drive.google.com/file/d/1s00Cr_C8LXtrsGrlRG4WUJx4GmAtdzrQ/view)
- NotebookLM podcast - available [here](https://www.youtube.com/watch?v=8Wyt9l7ge-g)
- Codelabs on A2A, deployment, and production patterns

---

# 🎓 Capstone Project (Course Finale)

The intensive ends with a capstone:  
> **Build and showcase a complete AI agent system using the skills learned across all five days.**

Top submissions earn:
- Kaggle Swag  
- Feature on Kaggle’s social platforms  
- Kaggle badge and certificate (available by end of December 2025)

I may include my capstone project here as soon as it is finished.

---

# 🚀 Technologies Used

- **Gemini models** (Gemini 2.5, etc.)  
- **ADK — Agent Development Kit**  
- **Google Search Tooling**  
- **Model Context Protocol (MCP)**  
- **A2A Protocol**  
- **Vertex AI Agent Engine**  
- **Python (ADK-based agents, codelabs)**  
- **NotebookLM** (summary podcasts, whitepaper discussions)  

---

# 🧩 Purpose of This Repository

This repo serves as:

- My personal learning record  
- A reference for others taking the intensive  
- A practical guide to modern agent development  
- A collection of working ADK examples  
- A base for future agent projects and production deployments  

---

# 🛠️ Setup Instructions (for Running My Code)

Requirements vary per day, but in general you will need:

- Python 3.10+  
- Google ADK (pip install adk)  
- A Gemini API key  
- A verified Kaggle account (for running official codelabs)

Create a `.env` file and add:

