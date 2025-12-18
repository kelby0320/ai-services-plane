import operator
from typing import Annotated, Dict, TypedDict
from uuid import UUID

from ai_core.models import ModelProfile


class GraphState(TypedDict):
    """
    Represents the state of the graph.

    Attributes:
        request_id: Unique identifier for the request.
        session_id: Unique identifier for the session.
        user_id: Unique identifier for the user.
        model_bindings: Dictionary mapping slot names to model profiles.
        messages: A list of messages.
    """

    request_id: UUID
    session_id: UUID
    user_id: UUID
    model_bindings: Dict[str, ModelProfile]
    messages: Annotated[list[str], operator.add]
