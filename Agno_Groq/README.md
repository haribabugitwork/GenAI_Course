# 📰 AI News Agent using Agno, Groq, and uv

This project demonstrates how to build a real-time, search-enabled storytelling agent using [Agno](https://pypi.org/project/agno/), Groq’s blazing-fast LLMs, and [`uv`](https://github.com/astral-sh/uv) for dependency and virtual environment management.

🔗 **GitHub Repository**: [GenAI_Course > Agno_Groq](https://github.com/haribabugitwork/GenAI_Course/tree/main/Agno_Groq)

---

## 🚀 Quick Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/haribabugitwork/GenAI_Course.git
cd GenAI_Course/Agno_Groq
```

### 2. Create and Activate Virtual Environment Using uv

```bash
uv venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate
```

### 3. Add Dependencies with uv

```bash
uv add agno
uv add groq
uv add duckduckgo-search
uv add python-dotenv
```

### 4. Create a `.env` File for API Keys

Create a `.env` file in the root directory (`Agno_Groq`) with the following content:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

👉 **Need a Groq API Key?** [Sign up and generate one here](https://console.groq.com/keys)

---

## 📁 Project Structure

```
Agno_Groq/
├── .env                    # Contains GROQ_API_KEY
├── pyproject.toml          # Dependency management via uv
├── README.md               # Setup instructions and project overview
└── src/
    └── agent_runner.py     # Main entrypoint for the agent
```

---

## ▶️ Run the Agent

```bash
uv run src/agent_runner.py
```

---

## 🧠 Agent Overview

The agent is configured to act as a **sports news reporter** with web-search capabilities and markdown-formatted responses.

It uses:

- 🧠 `llama-3-70b-versatile` via Groq
- 🔎 DuckDuckGo search tool for real-time data
- 🧰 Agno for orchestrating agent logic

---

## 💬 Sample Prompt

> Tell me about a breaking news story from the latest Rajasthan vs Gujarat IPL match.

The agent responds with live-sourced summaries in an engaging tone.

---
