from langgraph.graph import StateGraph, START, END

from app.state import ArchiveState
from app.nodes.observer import observe_person
from app.nodes.memory_generator import generate_memory


builder = StateGraph(ArchiveState)

builder.add_node(
    "observer",
    observe_person,
)

builder.add_node(
    "memory_generator",
    generate_memory,
)

builder.add_edge(
    START,
    "observer",
)

builder.add_edge(
    "observer",
    "memory_generator",
)

builder.add_edge(
    "memory_generator",
    END,
)

memory_graph = builder.compile()