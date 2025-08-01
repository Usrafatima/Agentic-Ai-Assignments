import os
import random
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("Api key not found")

#Client setup
client = AsyncOpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
         api_key=gemini_api_key,
)

#tool
@function_tool
def roll_dice(sides: int = 6) -> int:
    """
    Simulate rolling a dice with given number of sides.
    Returns a random number between 1 and 'sides' inclusive.
    """
    return random.randint(1, sides)

@function_tool
def generate_event() -> str:
    """
    Generate a random game event.
    Returns a random event description as a string.
    """
    events = [
        "You find a hidden treasure chest!",
        "A wild monster appears!",
        "You fall into a trap!",
        "You discover a mysterious potion.",
        "You meet a friendly traveler who offers help."
    ]
    return random.choice(events)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

#agents
narrator_Agent=Agent(
    name="Narrator Agent",
    instructions="You are the Narrator. Describe the adventure story clearly and engagingly. Guide the player through choices and scenes, setting the mood and world details. Hand off to MonsterAgent when combat starts, or to ItemAgent when the player finds items.",
    model=model
)

monster_agent=Agent(
    name="Monstor Agent",
    instructions="You are the Monster. Control combat encounters during the adventure. Respond to player actions with attacks, defenses, and special moves. Keep combat tense and exciting. After combat, hand back to NarratorAgent",
    model="model"
)

item_agent=Agent(
    name="Item Agent",
    instructions="You manage the player’s inventory and rewards. Describe items found, their effects, and how they can be used. Handle giving and updating items during the game. Hand off back to NarratorAgent after updates.",
    model=model
)

game_master_agent=Agent(
    name="Game Master Agent",
    instructions="You are the Game Master. Oversee the adventure by narrating story parts, managing combat, and handling items through your specialist agents: NarratorAgent, MonsterAgent, and ItemAgent. Seamlessly hand off control based on game events to provide a smooth player experience.",
    model=model,
    handoffs=[
        narrator_Agent,
        monster_agent,
        item_agent,
    ]
)

result=Runner.run_sync(
    game_master_agent,
    "I’m ready to begin my fantasy adventure. What is my first challenge?",
)

print(result.final_output)