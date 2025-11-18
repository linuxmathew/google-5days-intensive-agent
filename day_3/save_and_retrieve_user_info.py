from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.tools import ToolContext
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from typing import Dict, Any
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper.run_session import run_session


load_dotenv()
# Define scope levels for state keys (following best practices)
USER_NAME_SCOPE_LEVELS = ("temp", "user", "app")
APP_NAME = os.getenv("APP_NAME")
USER_ID = os.getenv("USER_ID")

retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 501, 503]
)


# This demonstrates how tools can write to session state using tool_context.
# The 'user:' prefix indicates this is user-specific data.
def save_userinfo(
    tool_context: ToolContext, user_name: str, country: str
) -> Dict[str, Any]:
    """
    Tool to record and save user name and country in session state.

    Args:
        user_name: The username to store in session state
        country: The name of the user's country
    """
    # Write to session state using the 'user:' prefix for user data
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country

    return {"status": "success"}


# This demonstrates how tools can read from session state.
def retrieve_userinfo(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to retrieve user name and country from session state.
    """
    # Read from session state
    user_name = tool_context.state.get("user:name", "Username not found")
    country = tool_context.state.get("user:country", "Country not found")

    return {"status": "success", "user_name": user_name, "country": country}


print("✅ Tools created.")

root_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="text_chat_bot",
    description="""A text chatbot.
    Tools for managing user context:
    * To record username and country when provided use `save_userinfo` tool. 
    * To fetch username and country when required use `retrieve_userinfo` tool.
    """,
    tools=[save_userinfo, retrieve_userinfo],  # Provide the tools to the agent
)

# make service
session_service = InMemorySessionService()


# runner
runner = Runner(agent=root_agent, session_service=session_service, app_name=APP_NAME)


async def main():
    await run_session(
        runner,
        [
            "Hi there, how are you doing today? What is my name?",  # Agent shouldn't know the name yet
            "My name is Sam. I'm from Poland.",  # Provide name - agent should save it
            "What is my name? Which country am I from?",  # Agent should recall from session state
        ],
        "state-demo-session",
    )
