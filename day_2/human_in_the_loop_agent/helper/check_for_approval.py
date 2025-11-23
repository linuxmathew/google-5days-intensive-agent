# Helper Functions to Process Events
# These handle the event iteration logic for you.

# check_for_approval() - Detects if the agent paused

# Loops through all events and looks for the special adk_request_confirmation event
# Returns approval_id (identifies this specific request) and invocation_id (identifies which execution to resume)
# Returns None if no pause detected


def check_for_approval(events):
    """Check if events contain an approval request.

    Returns:
        dict with approval details or None
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_call
                    and part.function_call.name == "adk_request_confirmation"
                ):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                    }
    return None
