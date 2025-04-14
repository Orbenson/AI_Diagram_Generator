from src.agent import agent

if agent is None:
    print("Agent is not available.")
else:
    # Test with a sample payload; note that the expected format is a dict with a "messages" key.
    test_payload = {"messages": [["user", "Create a diagram for a basic web application with an ALB, two EC2 instances, and an RDS database."]]}
    try:
        result = agent.invoke(test_payload)
        print("Agent response:", result)
    except Exception as e:
        print("Error invoking agent:", e)
