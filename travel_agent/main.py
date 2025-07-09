import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")  # Or use gemini-1.5-pro

# --- Tool: Mock Flight Data ---
def get_flights(destination):
    flights = {
        "Paris": ["Flight A - $500", "Flight B - $520"],
        "Tokyo": ["Flight C - $700", "Flight D - $720"],
        "New York": ["Flight E - $450", "Flight F - $480"],
    }
    return flights.get(destination, ["No flights found"])

# --- Tool: Mock Hotel Data ---
def suggest_hotels(destination):
    hotels = {
        "Paris": ["Hotel Parisian - $150/night", "Eiffel Stay - $200/night"],
        "Tokyo": ["Sakura Inn - $120/night", "Tokyo Suites - $180/night"],
        "New York": ["Central Hotel - $130/night", "Broadway Inn - $170/night"],
    }
    return hotels.get(destination, ["No hotels found"])

# --- Agent 1: Destination Agent ---
def destination_agent(user_mood):
    prompt = f"""
You are DestinationAgent. Suggest 2-3 travel destinations based on the user's mood or interests: "{user_mood}".
Reply with numbered destinations only.
"""
    response = model.generate_content(content=prompt)
    return response.text.strip()

# --- Agent 2: Booking Agent ---
def booking_agent(destination):
    flights = get_flights(destination)
    hotels = suggest_hotels(destination)
    result = f"Available flights to {destination}:\n"
    for f in flights:
        result += f"- {f}\n"
    result += f"Suggested hotels in {destination}:\n"
    for h in hotels:
        result += f"- {h}\n"
    return result

# --- Agent 3: Explore Agent ---
def explore_agent(destination):
    prompt = f"""
You are ExploreAgent. Suggest top 3 attractions and 3 local foods to try in {destination}.
Format as:

Attractions:
1.
2.
3.

Foods:
1.
2.
3.
"""
    response = model.generate_content(content=prompt)
    return response.text.strip()

# --- Main runner ---
def run_travel_designer_agent():
    print("👋 Welcome to AI Travel Designer Agent powered by Gemini!")
    mood = input("🧳 Tell me your mood or interests for travel: ")

    print("\n🌍 DestinationAgent is finding best places...")
    destinations_text = destination_agent(mood)
    print(destinations_text)

    choice = input("\n✈️ Choose one destination from above: ")

    print("\n📅 BookingAgent is finding flights and hotels...")
    booking_info = booking_agent(choice)
    print(booking_info)

    print("\n🍽️ ExploreAgent suggests attractions and foods...")
    explore_info = explore_agent(choice)
    print(explore_info)

# --- Run the app ---
if __name__ == "__main__":
    run_travel_designer_agent()
