# Career Mentor Agent

## 🧠 Overview

The **Career Mentor Agent** is a multi-agent AI system that helps learners explore career paths, discover the skills they need, and identify real-world job roles. It orchestrates three specialist agents to create a smooth, contextual career exploration experience:

- **CareerAgent** – suggests relevant career fields based on user interests.
- **SkillsAgent** – generates a step-by-step skill roadmap for a chosen career.
- **JobAgent** – lists real-world job titles, requirements, and tips for standing out.
- **Career Mentor (Orchestrator)** – guides the flow, asks clarifying questions, and hands off between specialists.

This is built using the OpenAI Agents SDK (or a compatible backend like Gemini via the OpenAI-compatible bridge) and simple function tools for structured decision support.

---

## ✨ Features

- Interest-driven career recommendations  
- Skill roadmap generation (beginner → intermediate → project)  
- Real-world job role suggestions with requirements and tips  
- Multi-agent handoff logic for clean orchestration  
- Easily extendable tools (e.g., connect to real databases or APIs later)

---

## 🚀 Setup

### Requirements
- Python 3.9+  
- `openai-agents` (or the equivalent SDK if using Gemini)  
- `python-dotenv` for environment variable loading  

### Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate        # Unix/macOS
# .\.venv\Scripts\activate       # Windows PowerShell

pip install openai-agents python-dotenv
If you’re using Gemini instead of OpenAI:

pip install openai python-dotenv
