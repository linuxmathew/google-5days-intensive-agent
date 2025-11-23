from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import InMemoryRunner

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import asyncio

from IPython.display import display, Image as IPImage
import base64


retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 503, 504]
)


def print_image(response):
    print("image triggered")
    for event in response:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "function_response") and part.function_response:
                    for item in part.function_response.response.get("content", []):
                        if item.get("type") == "image":
                            display(IPImage(data=base64.b64decode(item["data"])))


# MCP integration with Everything Server
mcp_image_server = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything"],
            tool_filter=["getTinyImage"],
        ),
        timeout=30,
    )
)


root_agent = LlmAgent(
    name="image_gen_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="You are an image generation agent. Use the mcp_image_server tool to generate images",
    tools=[mcp_image_server],
)

runner = InMemoryRunner(agent=root_agent)


async def main():
    response = await runner.run_debug("Provide a sample tiny image", verbose=True)
    print_image(response)


if __name__ == "__main__":
    asyncio.run(main())
