from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from simple_persistent_chatbot import simple_chatbot
import sys
import os
import asyncio

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper.run_session import run_session

USER_ID = os.getenv("USER_ID")
APP_NAME = os.getenv("APP_NAME")

# declare my app

research_compaction = App(
    name="research_compacter",
    root_agent=simple_chatbot,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=3, overlap_size=1
    ),
)


# create session
db_url = "sqlite:///my_agent_data2.db"
session_service = DatabaseSessionService(db_url=db_url)

# runner
research_runner = Runner(app=research_compaction, session_service=session_service)

print("Research app upgraded with Event compaction")


async def main1():
    # Turn 1
    await run_session(
        research_runner,
        session_service,
        research_compaction,
        "What is the latest news about AI in healthcare?",
        "compaction_demo",
    )

    # Turn 2
    await run_session(
        research_runner,
        session_service,
        research_compaction,
        "Are there any new developments in drug discovery?",
        "compaction_demo",
    )

    # # Turn 3
    await run_session(
        research_runner,
        session_service,
        research_compaction,
        "Tell me more about the second development you found.",
        "compaction_demo",
    )

    # # Turn 4
    await run_session(
        research_runner,
        session_service,
        research_compaction,
        "Who are the main companies involved in that?",
        "compaction_demo",
    )


async def main2():
    # Get the final session state
    final_session = await session_service.get_session(
        app_name=research_runner.app_name,
        user_id=USER_ID,
        session_id="compaction_demo",
    )

    print("--- Searching for Compaction Summary Event ---")
    found_summary = False
    for event in final_session.events:
        # Compaction events have a 'compaction' attribute
        if event.actions and event.actions.compaction:
            print("\n SUCCESS! Found the Compaction Event:")
            print(f"  Author: {event.author}")
            print(f"\n Compacted information: {event}")
            found_summary = True
            break

    if not found_summary:
        print(
            "\n No compaction event found. Try increasing the number of turns in the demo."
        )


if __name__ == "__main__":
    # asyncio.run(main1())
    asyncio.run(main2())
