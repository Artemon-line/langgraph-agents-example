from Agents.Multi_nodes_graph import welcome_node, age_node, skills_node, AgentState


def test_welcome_node():
    state = {"name": "Alice", "age": 30, "skills": ["Python"], "result": ""}
    result = welcome_node(state.copy())
    assert "Alice, welcome to the system!" in result["result"]


def test_age_node():
    state = {"name": "Alice", "age": 30, "skills": ["Python"], "result": "Hi!"}
    result = age_node(state.copy())
    assert "You are 30 years old!" in result["result"]


def test_skills_node():
    state = {"name": "Alice", "age": 30, "skills": ["Python", "ML"], "result": "Hi!"}
    result = skills_node(state.copy())
    assert "You have skills in: Python and ML" in result["result"]
