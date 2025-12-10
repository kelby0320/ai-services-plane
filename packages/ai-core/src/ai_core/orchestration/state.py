import operator
from typing import Annotated, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of the graph.

    Attributes:
        messages: A list of messages.
    """

    messages: Annotated[list[str], operator.add]
