from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from google.genai import types


# retry configuration for the model
retry_config = types.HttpRetryOptions(
    attempts=5, exp_base=7, http_status_codes=[429, 500, 503, 504], initial_delay=1
)


# This is the function that the RefinerAgent will call to exit the loop.
def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}


# This agent runs ONCE at the beginning to create the first draft.
initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""Write a short story based on the input of the user (around 100-200 words).
    Output only the story text with no introduction or explanation.
    """,
    output_key="initial_story",
)

# This agent's only job is to provide feedback or the approval signal. It has no tools.
critic_agent = Agent(
    name="CriticAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a constructive story critic. Review the story below.
    story:{initial_story}

    Evaluate the story's plot, character, and pacing.
    - If the story is well-written, you must respond with the phrase "APPROVED".
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.
    """,
    output_key="critique",
)

# This agent refines the story based on critique OR calls the exit_loop function.
refiner_agent = Agent(
    name="RefinerAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=""" You are a story refiner. Your job is to check the values:
    story:{initial_story}
    critique: {critique}

    - If the value of critique is exactly 'APPROVED', call the exit_loop function and nothing more,
    - Otherwise, rewrite the story to fully incorporate the feedback in critique.""",
    output_key="initial_story",
    tools=[FunctionTool(exit_loop)],
)


refinement_loop_agent = LoopAgent(
    name="refinement_loop_agent",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2,
)


root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[initial_writer_agent, refinement_loop_agent],
)
