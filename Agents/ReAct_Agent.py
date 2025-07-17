from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int):
    """This is an additional function"""
    return a + b


@tool
def subtract(a: int, b: int):
    """This is an subtraction  function"""
    return a - b


@tool
def multiply(a: int, b: int):
    """This is an multiplication function"""
    return a * b


tools = [add, subtract, multiply]

model = ChatOllama(model="llama3.2:latest").bind_tools(tools)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(
        content="You are my AI assistant, please answer my query to the best of your ability."
    )
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}


def should_continue(state: AgentState):
    messages = state["messages"]
    last = messages[-1]

    if not last.tool_calls:
        return "end"
    else:
        return "continue"


graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent", should_continue, {"continue": "tools", "end": END}
)

graph.add_edge("tools", "our_agent")  ## Back to the agent

app = graph.compile()


def print_stream(stream):
    for s in stream:
        m = s["messages"][-1]
        if isinstance(m, tuple):
            print(m)
        else:
            m.pretty_print()


inputs = {
    "messages": [
        (
            "user",
            "Add 40 + 12, then multiply the result by 2. The also tell me a joke",
        )
    ]
}
print_stream(app.stream(inputs, stream_mode="values"))
