import pytest
from unittest.mock import patch, mock_open
from Agents.Agent_Bot import process, save_conversation, chat_loop
from langchain_core.messages import HumanMessage, AIMessage

def test_process_function():
    """Test the process function directly"""
    initial_state = {"messages": [HumanMessage(content="hello")]}
    result = process(initial_state.copy())
    assert isinstance(result, dict)
    assert len(result["messages"]) == 2
    assert isinstance(result["messages"][-1], AIMessage)

@patch("builtins.input", side_effect=["hello", "exit"])
def test_chat_loop(mock_input):
    """Test the chat loop with mocked input"""
    conversation_history = chat_loop()
    assert len(conversation_history) >= 2
    assert isinstance(conversation_history[0], HumanMessage)
    assert conversation_history[0].content == "hello"

@patch("builtins.open", new_callable=mock_open)
def test_save_conversation(mock_file):
    """Test conversation saving"""
    conversation = [
        HumanMessage(content="hello"),
        AIMessage(content="hi there"),
    ]
    save_conversation(conversation, "test_log.txt")

    # Check if file was written correctly
    mock_file().write.assert_any_call("Conversation history:\n")
    mock_file().write.assert_any_call("User: hello\n")
    mock_file().write.assert_any_call("AI: hi there\n\n")
    mock_file().write.assert_any_call("End of Conversation")
