from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import google_search
from google.adk.runners import Runner, InMemoryRunner
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

# try:
#     api_key = os.getenv("GOOGLE_API_KEY")
#     # print("API", api_key)
#     if api_key:
#         print("✅ Gemini API key setup complete.")
# except Exception as e:
#     print(
#         f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' to your Kaggle secrets. Details: {e}"
#     )

retry_config = types.HttpRetryOptions(
    attempts=5, initial_delay=1, exp_base=7, http_status_codes=[429, 500, 503, 504]
)


root_agent = Agent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="alexa",
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)

print("✅ Root Agent defined.")


# declare runner
runner = InMemoryRunner(agent=root_agent)


async def main():
    response = await runner.run("Tell me about quantum computing")
    # print(response)


if __name__ == "__main__":
    asyncio.run(main())
