import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("API key not found")

# Client Setup
client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=gemini_api_key,
)

# Tools
@function_tool
def get_flights(origin: str, date: str, destination: str) -> str:
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

@function_tool
def get_explore_info(destination: str, preference: str = "") -> str:
    """
    Recommend attractions, food, and one insider tip for the given destination.
    preference can be things like 'food', 'culture', 'adventure' to tailor suggestions.
    """
    base = (
        f"Explore recommendations for {destination}:\n"
        "Must-see: Eiffel Tower, Louvre Museum\n"
        "Eat: Croissants at a local bakery, Steak frites\n"
        "Local tip: Buy a museum pass to skip long lines.\n"
    )
    if "food" in preference.lower():
        base = (
            f"Food-focused recommendations for {destination}:\n"
            "Must-try: Macarons, Escargot\n"
            "Local tip: Visit the market in the morning for fresh pastries.\n"
        )
    return base

# Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Agents
destination_agent = Agent(
    name="Destination Agent",
    instructions=(
        "You are the Destination Agent. Given a user’s travel interests or origin, suggest 2–3 suitable destinations. "
        "For each, give one sentence why it fits. If the user’s input is vague, ask a clarifying question like "
        "\"Do you prefer mountains, beaches, or cities?\""
    ),
    model=model,
 
)

booking_agent = Agent(
    name="Booking Agent",
    instructions=(
        "You are the Booking Agent. Simulate making travel arrangements: extract origin, destination, date, number of travelers, "
        "and budget from the user input or prior context. Then use the flight and hotel tools to confirm availability. "
        "Summarize the booking with a cost estimate. Always ask follow-up if information is missing. If something can’t be booked, "
        "offer an alternative."
    ),
    model=model,
    tools=[get_flights, suggest_hotels],
)

explore_agent = Agent(
    name="Explore Agent",
    instructions=(
        "You are the Explore Agent. For a given destination, recommend top attractions, local foods to try, and one insider tip. "
        "Organize suggestions into categories such as 'Must-see,' 'Eat,' and 'Local tip.' Tailor recommendations to user preferences if provided."
    ),
    model=model,
    tools=[get_explore_info],
)

ai_travel_agent = Agent(
    name="AI Travel Agent",
    instructions=(
        "You are a travel mentor agent. First, parse the user input to identify travel goals, origin, destination, dates, and budget. "
        "Then:\n"
        "1. If destination is unclear, hand off to Destination Agent to suggest destinations.\n"
        "2. When the user has a destination and date, hand off to Booking Agent to collect any missing details and simulate booking using the flights and hotels tools.\n"
        "3. After booking is settled, or if the user wants to explore, hand off to Explore Agent for attractions, food, and insider tips.\n"
        "Always explain why you are transferring (e.g., 'I'm sending you to the Booking Agent to lock in your dates'). "
        "If the user is unclear at any step, ask a clarifying question before proceeding. Keep responses organized and helpful."
    ),
    model=model,
    tools=[get_flights, suggest_hotels, get_explore_info],  
    handoffs=[
        destination_agent,
        booking_agent,
        explore_agent,
    ],
)

# Run the main agent
result = Runner.run_sync(
    ai_travel_agent,
    "I’m planning a trip from Los Angeles to Tokyo on October 10th. Can you book my flights and hotels, and then tell me what top attractions and foods I should try there?",
)
print(result.final_output)
