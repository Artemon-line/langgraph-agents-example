from typing import Dict, TypedDict
from langgraph.graph import StateGraph
from functools import reduce


class AgentState(TypedDict):  # Agent Schema
    message: str
    values: list
    operation: str
    name: str


def operation_node(state: AgentState) -> AgentState:
    """Simple operation on input parameters"""

    if state["operation"] == "*":
        res = reduce(lambda out, x: out * x, state["values"])
    elif state["operation"] == "+":
        res = reduce(lambda out, x: out + x, state["values"])
    else:
        raise TypeError("Only + or * are allowed")

    state["message"] = f"Hi {state['name']}, your answer is: {res}"
    return state


graph = StateGraph(AgentState)
graph.add_node("operator", operation_node)
graph.set_entry_point("operator")
graph.set_finish_point("operator")

app = graph.compile()

res = app.invoke({"name": "Jack Sparrow", "values": [1, 2, 3, 4], "operation": "*"})

print(res["message"])
