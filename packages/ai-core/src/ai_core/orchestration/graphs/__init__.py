from typing import Callable

from langgraph.graph.state import CompiledStateGraph

from ai_core.orchestration.graphs import default_v1

graph_registry: dict[str, Callable[[], CompiledStateGraph]] = {
    "default_graph_v1": default_v1.build_graph,
}
