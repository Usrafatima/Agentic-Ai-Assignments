import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI  # Gemini ka OpenAI-compatible bridge

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise RuntimeError("GEMINI_API_KEY nahi mila .env mein dal do.")

# Gemini client setup
client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=gemini_api_key,
)

@function_tool
def get_career_roadmap(skills: str) -> str:
    skills = skills.lower()
    if "web" in skills:
        return "Suggestions: Frontend Developer, Full Stack Developer, UI/UX Designer."
    if "data" in skills:
        return "Suggestions: Data Analyst, Machine Learning Engineer."
    if "design" in skills:
        return "Suggestions: Product Designer, UI/UX Designer."
    return "Suggestions: Software Engineer, Technical Support, Product Manager."

# Model define karo
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

# Sub-agents 
career_agent = Agent(
    name="Career Agent",
    instructions=(
        "You are a career suggestion expert. Based on the user’s interests or background, "
        "recommend 2–4 specific career fields and give a short reason for each. "
        "If the answer is vague, ask a quick follow-up before suggesting."
    ),
    model=model,
    tools=[get_career_roadmap], 
)

skill_agent = Agent(
    name="Skills Agent",
    instructions=(
        "You are a skill roadmap planner. Given a career choice, list 5–7 skills or learning steps "
        "needed to get started and become job-ready, arranged from beginner to advanced. "
        "Include one practical project idea at the end to apply the skills. If the career is unclear, ask for clarification."
    ),
    model=model,
)

job_agent = Agent(
    name="Job Agent",
    instructions=(
        "You are a job role advisor. Given a career field, list 3–5 real-world job titles in that field. "
        "For each role, include typical required skills, a one-line description of the work, and one tip to stand out. "
        "If asked, give general salary or application guidance."
    ),
    model=model,
)

career_mentor_agent = Agent(
    name="Career Mentor Agent",
    instructions=(
        "You are a career mentor. Start by asking the user about their interests, background, or goals. "
        "Based on their answer, route them to:\n\n"
        "Career Agent for career field suggestions\n\n"
        "Skills Agent for skill-building roadmap\n\n"
        "Job Agent for real-world job roles\n\n"
        "Always explain why you are transferring, and ask clarifying questions if the user’s answer is unclear. "
        "Keep your tone friendly and helpful."
    ),
    model=model,
    tools=[get_career_roadmap], 
    handoffs=[career_agent, skill_agent, job_agent],
)

# Run the conversation synchronously
result = Runner.run_sync(
    career_mentor_agent,
    "I want to be a web developer.Recommendations ?"
)
print(result.final_output)

