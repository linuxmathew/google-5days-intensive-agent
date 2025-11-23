from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import FunctionTool
from google.adk.models.google_llm import Gemini
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from helper.check_for_approval import check_for_approval
from helper.create_approval_response import (
    create_approval_response,
)
from helper.print_agent_response import print_agent_response
import uuid

from dotenv import load_dotenv

load_dotenv()

# Let's build a shipping coordinator agent with one tool that:

# Auto-approves small orders (≤5 containers)
# Pauses and asks for approval on large orders (>5 containers)
# Completes or cancels based on the approval decision
# This demonstrates the core long-running operation pattern: pause → wait for human input → resume.

# The ToolContext Parameter
# Notice the function signature includes tool_context: ToolContext. ADK automatically provides this object when your tool runs. It gives you two key capabilities:

# Request approval: Call tool_context.request_confirmation()
# Check approval status: Read tool_context.tool_confirmation

LARGE_ORDER_THRESHOLD = 5


retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, initial_delay=1, http_status_codes=[429, 500, 501, 503]
)


def place_shipping_order(
    num_containers: int, destination: str, tool_context: ToolContext
) -> dict:
    """Places a shipping order. Requires approval if ordering is more than 5 containers (LARGE_ORDER_THRESHOLD)

    Args:
        num_containers: Number of containers to ship
        destination: shipping destination

    Returns:
        Dictionary with order status
    """

    # SCENARIO 1: Small orders (≤5 containers) auto-approve
    if num_containers <= LARGE_ORDER_THRESHOLD:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-AUTO",
            "destination": destination,
            "message": f"Order auto-approved: {num_containers} containers to {destination}",
        }

    # SCENARIO 2: This is the first time this tool is called. Large orders need human approval - PAUSE here.
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"{num_containers} to {destination}. Do you want to approve?",
            payload={"destination": destination, "num_containers": num_containers},
        )
        return {"status": "pending", "num_containers": num_containers}

    # SCENARIO 3: The tool is called AGAIN and is now resuming. Handle approval response - RESUME here.
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "order_id": f"ORD-{num_containers}-MANUAL",
            "destination": destination,
            "message": f"Order manually-approve: {num_containers} to {destination}",
        }
    else:
        return {
            "status": "rejected",
            "message": f"order {num_containers}, rejected to {destination}address",
        }


# Create shipping agent with pausable tool
shipping_agent = LlmAgent(
    name="shipping_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a shipping coordinator assistant.
  
  When users request to ship containers:
   1. Use the place_shipping_order tool with the number of containers and destination
   2. If the order status is 'pending', inform the user that approval is required
   3. After receiving the final result, provide a clear summary including:
      - Order status (approved/rejected)
      - Order ID (if available)
      - Number of containers and destination
   4. Keep responses concise but informative
  """,
    tools=[FunctionTool(func=place_shipping_order)],
)

# The problem: A regular LlmAgent is stateless - each call is independent with no memory of previous interactions. If a tool requests approval, the agent can't remember what it was doing.

# The solution: Wrap your agent in an App with resumability enabled. The App adds a persistence layer that saves and restores state.

root_agent = App(
    name="shipping_coordinator",
    root_agent=shipping_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

session_service = InMemorySessionService()
shipping_runner = Runner(app=root_agent, session_service=session_service)


# Understand Key Technical Concepts¶
# 👉 events - ADK creates events as the agent executes. Tool calls, model responses, function results - all become events

# 👉 adk_request_confirmation event - This event is special - it signals "pause here!"

# Automatically created by ADK when your tool calls request_confirmation()
# Contains the invocation_id
# Your workflow must detect this event to know the agent paused
# 👉 invocation_id - Every call to run_async() gets a unique invocation_id (like "abc123")

# When a tool pauses, you save this ID
# When resuming, pass the same ID so ADK knows which execution to continue
# Without it, ADK would start a NEW execution instead of resuming the paused one


async def run_shipping_workflow(query: str, auto_approve: bool = True):
    """Runs a shipping workflow with approval handling.

    Args:
        query: User's shipping request
        auto_approve: Whether to auto-approve large orders (simulates human decision)
    """

    print(f"\n{'='*60}")
    print(f"User > {query}\n")

    # Generate unique session ID
    session_id = f"order_{uuid.uuid4().hex[:8]}"

    # Create session
    await session_service.create_session(
        app_name="shipping_coordinator", user_id="test_user", session_id=session_id
    )

    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    events = []

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # STEP 1: Send initial request to the Agent. If num_containers > 5, the Agent returns the special `adk_request_confirmation` event
    async for event in shipping_runner.run_async(
        user_id="test_user", session_id=session_id, new_message=query_content
    ):
        events.append(event)

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # STEP 2: Loop through all the events generated and check if `adk_request_confirmation` is present.
    approval_info = check_for_approval(events)

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # STEP 3: If the event is present, it's a large order - HANDLE APPROVAL WORKFLOW
    if approval_info:
        print(f"⏸️  Pausing for approval...")
        print(f"🤔 Human Decision: {'APPROVE ✅' if auto_approve else 'REJECT ❌'}\n")

        # PATH A: Resume the agent by calling run_async() again with the approval decision
        async for event in shipping_runner.run_async(
            user_id="test_user",
            session_id=session_id,
            new_message=create_approval_response(
                approval_info, auto_approve
            ),  # Send human decision here
            invocation_id=approval_info[
                "invocation_id"
            ],  # Critical: same invocation_id tells ADK to RESUME
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent > {part.text}")

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    else:
        # PATH B: If the `adk_request_confirmation` is not present - no approval needed - order completed immediately.
        print_agent_response(events)

    # print(f"{'='*60}\n")


async def main():
    # Demo 1: It's a small order. Agent receives auto-approved status from tool
    await run_shipping_workflow("Ship 3 containers to Singapore")

    # Demo 2: Workflow simulates human decision: APPROVE ✅
    await run_shipping_workflow("Ship 10 containers to Rotterdam", auto_approve=True)

    # Demo 3: Workflow simulates human decision: REJECT ❌
    await run_shipping_workflow("Ship 8 containers to Los Angeles", auto_approve=False)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

# RUNNING INSTRUICTION
# I had issue running this with
# adk run
# Kindly run as a
# python3 agent.py
