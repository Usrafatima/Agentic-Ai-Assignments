from agents import (
    Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, Tool
)
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)



def tool_career_roadmap(input_str: str) -> str:
    prompt = f"Provide a step-by-step learning roadmap for a career as {input_str}.\nInclude skills, tools, platforms, and certifications."
    response = model._client.chat.completions.create(
        model=model.model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def tool_job_roles(input_str: str) -> str:
    prompt = f"List 3 entry-level job roles in Pakistan for a {input_str}, including job title, salary range in PKR, and companies."
    response = model._client.chat.completions.create(
        model=model.model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def tool_resume_tips(input_str: str) -> str:
    prompt = f"Provide 3 resume and LinkedIn tips for someone applying for {input_str} jobs."
    response = model._client.chat.completions.create(
        model=model.model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

# Create Tool objects
career_roadmap_tool = Tool(
    name="get_career_roadmap",
    description="Provides skill-building roadmap for a chosen career",
    func=tool_career_roadmap
)

job_roles_tool = Tool(
    name="get_job_roles",
    description="Provides job roles, salary info, and companies hiring",
    func=tool_job_roles
)

resume_tips_tool = Tool(
    name="get_resume_tips",
    description="Gives resume and LinkedIn tips for the career",
    func=tool_resume_tips
)

tools = [career_roadmap_tool, job_roles_tool, resume_tips_tool]


agent = Agent(
    name="Career Mentor Agent",
    instructions="""
You are a multi-agent career mentor. Use the following tools to help the user:
- get_career_roadmap: To provide skill-building roadmaps.
- get_job_roles: To provide job roles and salary info.
- get_resume_tips: To provide resume and LinkedIn tips.

Follow this flow:
1. Ask user's interests.
2. Suggest 2-3 career fields.
3. Once user picks a career, call get_career_roadmap.
4. Then call get_job_roles.
5. Then call get_resume_tips.
Answer clearly and helpfully.
""",
    tools=tools
)



def run():
    user_prompt = "I am studying statistics with finance. What career options and skills do I have?"
    result = Runner.run_sync(
        agent,
        input=user_prompt,
        run_config=config
    )
    print("=== Career Mentor Agent Response ===")
    print(result.final_output)

if __name__ == "__main__":
    run()
