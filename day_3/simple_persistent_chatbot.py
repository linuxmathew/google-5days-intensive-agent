from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
import asyncio
import os
import sys

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helper.run_session import run_session


# step1: define agent
retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 501, 503]
)

simple_chatbot = Agent(
    name="text_chat_bot",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="A simple chat bot with memory",
)

# step 2: Make a session
db_url = "sqlite:///my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# step 3: declare my runner
APP_NAME = os.getenv("APP_NAME")

runner = Runner(
    session_service=session_service, app_name=APP_NAME, agent=simple_chatbot
)


# step 4: run main


async def main1():
    await run_session(
        runner,
        session_service,
        simple_chatbot,
        [
            "Hello, I am Liyah! What is the capital of United Kingdom",
            "What is my name?",
        ],
        "test-db-session-01",
    )


async def main2():
    await run_session(
        runner,
        session_service,
        simple_chatbot,
        ["What is the capital of India?", "Hello! What is my name?"],
        "test-db-session-02",
    )


if __name__ == "__main__":
    print("\n Upgraded to persisten sessions")
    print(f"    - Database: my_agent_data.db")
    print(f"    - session will survive restart")
    # asyncio.run(main1())
    asyncio.run(main2())
