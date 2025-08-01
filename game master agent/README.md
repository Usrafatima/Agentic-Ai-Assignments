# 🐉 Game Master Agent – Fantasy Adventure

## 🧠 Overview

The **Game Master Agent** is a multi-agent AI system for running an interactive, text-based fantasy adventure game.  
It creates a dynamic game flow with storytelling, combat, and item management by orchestrating three specialist agents:

- **NarratorAgent** – describes the world and guides the player’s story choices.  
- **MonsterAgent** – manages combat encounters and battle outcomes.  
- **ItemAgent** – handles inventory updates, rewards, and item effects.  
- **Game Master Agent (Orchestrator)** – oversees the entire game, switching between agents as needed.

The game uses AI tools like `roll_dice()` and `generate_event()` to add randomness and excitement to the adventure.

---

## ✨ Features

- Immersive story narration and player choice handling  
- Dynamic combat system powered by dice rolls  
- Inventory and rewards management  
- Randomized events for replayability  
- Multi-agent orchestration with smooth handoffs between story, combat, and item phases

---

## 🚀 Setup

### Requirements
- Python 3.9+  
- `openai-agents` or compatible backend (e.g., Gemini with OpenAI bridge)  
- `python-dotenv` for environment management

### Install dependencies
```bash
python -m venv .venv
# Activate:
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install openai-agents python-dotenv openai
