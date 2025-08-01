import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("API key not found")

#Client Setup
client = AsyncOpenAI(
      base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
      api_key=gemini_api_key,
)

#tool
@function_tool
def get_flights(origin:str, date:str, destination:str)-> str:
   return (
    f"Available flights from {origin} to {destination} on {date}:\n"
    "1. Flight JP32 at 5:00 PM - $200\n"
    "2. Flight JL41 at 11:00 AM - $150\n"
    "3. Flight EK29 at 8:00 PM - $180\n"
)

@function_tool
def suggest_hotels(destination: str, date: str, city: str) -> str:
    return (
        f"Available hotels in {city} on {date} near {destination}:\n"
        "1. Hotel Paris, 3 Bedrooms, $200 per night\n"
        "2. Nightangle, 2 Bedrooms, $150 per night\n"
        "3. King Hotel, 1 Bedroom, $80 per night\n"
    )

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

#agents 
destination_agent=Agent(
    name="Destination Agent",
    instructions="You are the Destination Agent. Given a user’s travel interests or origin, suggest 2–3 suitable destinations. For each, give one sentence why it fits. If the user’s input is vague, ask a clarifying question like “Do you prefer mountains, beaches, or cities?”",
    model=model
)

booking_agent=Agent(
    name="Booking Agent",
    instructions="You are the Booking Agent. Simulate making travel arrangements: gather required details (destination, dates, number of travelers, budget), confirm availability (mock or using data if available), and summarize the booking with a cost estimate. Always ask follow-up if information is missing. If something can’t be booked, offer an alternative.",
    model=model
)

explore_agent=Agent(
    name="Explore Agent",
    instructions="You are the Explore Agent. For a given destination, recommend top attractions, local foods to try, and one insider tip. Organize suggestions into categories such as “Must-see,” “Eat,” and “Local tip.” Tailor recommendations to user preferences if provided."
)

#main Agent
ai_travel_agent=Agent(
    name="AI Travel Agent",
    instructions="""
You are a travel mentor agent. First, ask the user about their travel goals, preferences, dates, and budget. Then:

Use the DestinationAgent to suggest appropriate destinations.

When the user picks a destination, hand off to the BookingAgent to collect details and simulate the trip booking.

After booking is settled or when the user wants to explore, hand off to the ExploreAgent for attractions, food, and insider tips.
Always explain why you are transferring (e.g., “I’m sending you to the BookingAgent to lock in your dates”). If the user is unclear at any step, ask a clarifying question before proceeding. Keep responses organized and helpful.

""",
model=model,
handoffs=[
    destination_agent,
    booking_agent,
    explore_agent,
]
)

#Run the main agent
result = Runner.run_sync(
    ai_travel_agent,
    "Can you show me available flights and hotels for a trip from New York to Paris on September 15th?",
)
print(result.final_output)

