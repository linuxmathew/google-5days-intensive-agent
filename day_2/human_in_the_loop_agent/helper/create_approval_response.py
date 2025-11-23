from google.genai import types

# create_approval_response() - Formats the human decision

# Takes the approval info and boolean decision (True/False) from the human
# Creates a FunctionResponse that ADK understands
# Wraps it in a Content object to send back to the agent


def create_approval_response(approval_info, approved):
    """Create approval response message."""
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved},
    )
    return types.Content(
        role="user", parts=[types.Part(function_response=confirmation_response)]
    )
