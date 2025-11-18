# step 1: declare our agent

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper.run_session import run_session

from helper.run_session import run_session
from dotenv import load_dotenv
import asyncio

load_dotenv()


retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 501, 503]
)
root_agent = Agent(
    name="mini_alexa",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="the text chat bot",
)


# Step 2: create session = will allow us to have remember past conversation
session_service = InMemorySessionService()

# step 3: runner to run the app
APP_NAME = "default"
USER_ID = "default"
SESSION = "default"
runner = Runner(session_service=session_service, agent=root_agent, app_name=APP_NAME)


async def main1():
    await run_session(
        runner,
        session_service,
        root_agent,
        [
            "Hi, My name is Temitayo! What is the capital of the United states?",
            "What is my name?",
        ],
        "Stateful-agentic-session",
    )


# Testing Agent's forgetfulness
async def main2():
    # Run this cell after restarting the kernel. All this history will be gone...
    await run_session(
        runner,
        session_service,
        root_agent,
        [
            "What did I ask you about earlier?",
            "And remind me, what's my name?",
        ],
        "Stateful-agentic-session",
    )  # Note, we are using same session name


if __name__ == "__main__":

    print("Agent chatbot initialized")
    print(f"    - Application: {APP_NAME}")
    print(f"    - User: {USER_ID}")
    print(f"    - using:{session_service.__class__.__name__} ")

    asyncio.run(main2())  # agent that remembers
    # asyncio.run(main2())  # Agent with no memory
