# tests/test_api.py
from fastapi.testclient import TestClient
from src.main import app
import os

client = TestClient(app)

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

def test_diagram_endpoint():
    description = ("Design a microservices architecture with three services: an authentication service, "
                   "a payment service, and an order service. Include an API Gateway for routing, an SQS queue "
                   "for message passing between services, and a shared RDS database. Group the services in a cluster "
                   "called 'Microservices'. Add CloudWatch for monitoring.")
    response = client.get("/diagram", params={"description": description})
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    # Optionally check that file exists if you save it to disk.
