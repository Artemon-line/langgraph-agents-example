from typing import Dict, TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    age: int
    skills: list
    result: str


def welcome_node(state: AgentState) -> AgentState:
    """Welcome node"""
    state["result"] = f"{state['name']}, welcome to the system!"
    return state


def age_node(state: AgentState) -> AgentState:
    """Age node"""
    state["result"] = f"{state['result']} You are {state['age']} years old!"
    return state


def skills_node(state: AgentState) -> AgentState:
    """Skills node"""
    ar = state["skills"].copy()
    last_skill = ar.pop()
    skills = ", ".join(ar)
    state["result"] = f"{state['result']} You have skills in: {skills} and {last_skill}"
    return state


graph = StateGraph(AgentState)
graph.add_node("welcome_node", welcome_node)
graph.add_node("age_node", age_node) 
graph.add_node("skills_node", skills_node)

graph.set_entry_point("welcome_node")
graph.add_edge("welcome_node", "age_node")
graph.add_edge("age_node", "skills_node")
graph.set_finish_point("skills_node")

app = graph.compile()

res = app.invoke(
    {"name": "Linda", "age": 31, "skills": ["Python", "Machine Learning", "LangGraph"]}
)

print(res["result"])
