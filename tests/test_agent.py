# tests/test_agent.py
from src.agent import agent_chain

def test_agent_response():
    # Simple test input – your agent should return some string.
    test_message = "Explain why we use load balancers in web architectures."
    response = agent_chain.run(test_message)
    assert isinstance(response, str)
    assert len(response.strip()) > 0
