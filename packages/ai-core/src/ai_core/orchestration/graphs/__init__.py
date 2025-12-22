from typing import Callable

from langgraph.graph.state import CompiledStateGraph

from ai_core.orchestration.graphs import default_v1, dummy_v1
from ai_core.orchestration.services import Services

graph_registry: dict[str, Callable[[Services], CompiledStateGraph]] = {
    "default_v1": default_v1.build_graph,
    "dummy_v1": dummy_v1.build_graph,
}
