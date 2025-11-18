from google.adk.agents import Agent, LlmAgent
from google.adk.runners import Runner
from google.adk.models.google_llm import Gemini 
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.tools.tool_context import ToolContext
from google.genai import types


retry_config = types.HttpOptions(
    attempts=5,
    exp_base=7,
    initial_delay= 1,
    http_status_code=[]
    )



root_agent = Agent(
    name="session_testing_agent", 
    model= Gemini(
        model="gemini-2.5-flash-lite",
        retry_config=retry_config
        ), 
    description= "", instruction= "",
    tools= []
)