from fastapi import Request

from ai_orchestrator.context import AppContext


def get_context(request: Request) -> AppContext:
    """Get the AppContext from the request state."""
    return request.app.state.context
