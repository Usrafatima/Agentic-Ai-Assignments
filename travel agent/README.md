# AI Travel Mentor Agent

## 🧠 Overview

The **AI Travel Mentor Agent** is a multi-agent system that helps users plan trips end-to-end. It combines destination discovery, booking simulation, and local exploration through specialist agents:

- **DestinationAgent** – recommends destinations based on user preferences.  
- **BookingAgent** – gathers trip details and simulates flight/hotel bookings.  
- **ExploreAgent** – suggests attractions, food, and insider tips for a chosen destination.  
- **Travel Mentor Agent (Orchestrator)** – guides the conversation, routes between specialists, and explains handoffs.

The system is built on top of the OpenAI Agents SDK (or a compatible backend like Gemini via the OpenAI-compatible bridge) with simple function tools providing structured data.

---

## ✨ Features

- Preference-driven destination suggestions  
- Simulated flight and hotel options with mock data  
- Local exploration recommendations (attractions, cuisine, tips)  
- Multi-agent handoff logic for smooth conversation flow  
- Easily extensible to real APIs (flights, hotels, reviews, maps)

---

## 🚀 Setup

### Requirements
- Python 3.9+  
- `openai-agents` (or the necessary OpenAI/Gemini client)  
- `python-dotenv` for loading secrets  

### Install dependencies
```bash
python -m venv .venv
# Activate:
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install openai-agents python-dotenv openai
