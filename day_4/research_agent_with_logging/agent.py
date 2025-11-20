from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search, AgentTool
from google.adk.runners import InMemoryRunner
from google.adk.plugins import (
    LoggingPlugin,
)
from google.genai import types
from dotenv import load_dotenv
import asyncio

load_dotenv()

from typing import List


retry_config = types.HttpRetryOptions(
    attempts=5, initial_delay=1, exp_base=7, http_status_codes=[429, 500, 503, 504]
)


def count_papers(papers: List[str]):
    """
    This function counts the number of papers in a list of strings.
    Args:
      papers: A list of strings, where each string is a research paper.
    Returns:
      The number of papers in the list.
    """
    return len(papers)


google_search_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="root_agent",
    description="Searches for information using Google search",
    instruction="""Use the google_search tool to search for information on the given topic. 
    Return the raw result. If the user asks for a list of papers, then give them a list of research papers you found and not the summary.
    """,
    tools=[google_search],
)


root_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="research_paper_finder",
    description="A helpful assistant for user questions.",
    instruction="""Your task is to find research papers and count them. 

    You MUST ALWAYS follow these steps:
    1) Find research papers on the user provided topic using the 'google_search_agent'. 
    2) Then, pass the papers to 'count_papers' tool to count the number of papers returned.
    3) Return both the list of research papers and the total number of papers.
    """,
    tools=[AgentTool(agent=google_search_agent), count_papers],
)
print("✅ Agent created")

runner = InMemoryRunner(agent=root_agent, plugins=[LoggingPlugin()])
print("✅ Runner configured")


print("🚀 Running agent with LoggingPlugin...")
print("📊 Watch the comprehensive logging output below:\n")


async def main():
    await runner.run_debug("Find recent papers on quantum computing")


if __name__ == "__main__":
    asyncio.run(main())


# Note
# run the agent with {adk run agent} in one termind and in the other do next
# tail -F /var/folders/1d/w2f9jsk90r9bbgjvnscrnjmc0000gn/T/agents_log/agent.latest.log
