from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
import asyncio

from dotenv import load_dotenv
import os

load_dotenv()

# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )


retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)


# try:
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if(api_key):
#         print("✅ Gemini API key setup complete.")
# except Exception as e:
#     print(
#         f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' to your Kaggle secrets. Details: {e}"
#     )


runner = InMemoryRunner(agent=root_agent)

async def debug_check():
    debug_info = await runner.run_debug("What is the capital of Japan")
    # response = runner.run("What is the capital of Japan")
    return debug_info

if __name__ == "__main__":
    debug_result = asyncio.run(debug_check())
    print("Debug info result:\n", debug_result)