# tests/test_diagram.py
import os
from src.diagram_tool import generate_diagram

def test_generate_diagram():
    description = ("Create a diagram showing a basic web application with an ALB and two EC2 instances in a cluster named 'Web Tier', "
                   "and an RDS database.")
    image_path = generate_diagram(description)
    assert os.path.exists(image_path), f"Expected image file at {image_path}"
    assert image_path.endswith(".png")
