import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]


llm = ChatOllama(model="llama3.2:latest")


def process(state: AgentState) -> AgentState:
    """Process response from LLM"""
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    state["messages"].append(AIMessage(content=response.content))
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

user_input = input("Say something: ")

conversation_history = []

while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("User: ")

with open("log.txt", "w") as file:
    file.write("Conversation history:\n")

    for m in conversation_history:
        if isinstance(m, HumanMessage):
            file.write(f"User: {m.content}\n")
        elif isinstance(m, AIMessage):
            file.write(f"AI: {m.content}\n\n")
    file.write("End of Conversation")
