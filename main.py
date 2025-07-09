import os
import random
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# ------------------ Tools ------------------
def roll_dice(sides=6):
    return random.randint(1, sides)

def generate_event():
    events = [
        "You hear a mysterious whisper from the trees.",
        "A wild beast jumps from the shadows!",
        "You discover a hidden cave with glowing crystals.",
        "A traveler offers you a magical potion.",
        "You find a rusty key buried in the dirt."
    ]
    return random.choice(events)

# ------------------ Agents ------------------
def narrator_agent(player_choice):
    prompt = f"""
You are the NarratorAgent of a fantasy adventure game.
Continue the story based on this player action: "{player_choice}".
Keep it immersive and leave the next choice open-ended.
"""
    response = model.generate_content(content=prompt)
    return response.text.strip()

def monster_agent():
    monster = random.choice(["Goblin", "Dragon", "Skeleton Warrior"])
    dice = roll_dice(20)
    result = f"A wild {monster} appears! You roll a d20 and get {dice}.\n"
    if dice >= 12:
        result += f"You defeated the {monster} bravely!"
    else:
        result += f"The {monster} strikes you! You must retreat!"
    return result

def item_agent():
    items = ["Elixir of Health", "Sword of Shadows", "Ancient Map", "Enchanted Amulet"]
    found = random.choice(items)
    return f"You found a reward: **{found}**! It's added to your inventory."

# ------------------ Game Loop ------------------
def run_game():
    print("🎮 Welcome to the Fantasy Adventure Game!")
    print("Type 'exit' to quit the game.\n")

    while True:
        player_input = input("🔮 What do you want to do? ")

        if player_input.lower() == "exit":
            print("🏁 Thanks for playing, adventurer!")
            break

        print("\n📖 NarratorAgent says:")
        story = narrator_agent(player_input)
        print(story)

        print("\n🎲 Random Event:")
        print(generate_event())

        if "fight" in player_input.lower() or "monster" in player_input.lower():
            print("\n🧟 MonsterAgent says:")
            print(monster_agent())

        if "search" in player_input.lower() or "treasure" in player_input.lower():
            print("\n🎁 ItemAgent says:")
            print(item_agent())

        print("\n--- Next Turn ---\n")

# ------------------ Start Game ------------------
if __name__ == "__main__":
    run_game()
