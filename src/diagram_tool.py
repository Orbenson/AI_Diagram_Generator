# src/diagram_tool.py
import os, re, uuid, logging
from typing import List, ClassVar

from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, APIGateway
from diagrams.aws.integration import SQS
from diagrams.aws.management import Cloudwatch
from diagrams.generic.blank import Blank

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ICON_MAP = {
    "EC2": EC2,
    "RDS": RDS,
    "ALB": ELB,
    "ELB": ELB,
    "APIGateway": APIGateway,
    "SQS": SQS,
    "CloudWatch": Cloudwatch,
}

def _draw(title: str, nodes: List[dict], edges: List[dict]) -> str:
    """Generic renderer given explicit nodes / edges."""
    fname = f"{title.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"
    fpath = os.path.join(OUTPUT_DIR, fname)
    with Diagram(title, filename=fpath, outformat="png", show=False):
        obj = {}
        for n in nodes:
            cls = ICON_MAP.get(n["type"], Blank)
            obj[n["id"]] = cls(n["label"])
        for e in edges:
            src = obj[e["from"]]
            for dst in e["to"]:
                src >> obj[dst]
    img_path = f"{fpath}.png"
    logger.info("Diagram saved: %s", img_path)
    return img_path


def generate_diagram(description: str) -> str:
    """Lightweight heuristic generator used by /diagram endpoint."""
    desc = description.lower()

    if "microservices" in desc or "service" in desc:
        title = "Microservices Architecture"
        fname = f"micro_{uuid.uuid4().hex[:6]}"
        fpath = os.path.join(OUTPUT_DIR, fname)

        with Diagram(title, filename=fpath, outformat="png", show=False):
            # External components
            gw  = APIGateway("API Gateway")
            sqs = SQS("SQS Queue")
            db  = RDS("Shared RDS")
            cw  = Cloudwatch("CloudWatch")

            # Cluster with the three services
            with Cluster("Microservices"):
                auth  = EC2("Authentication Service")
                pay   = EC2("Payment Service")
                order = EC2("Order Service")

            # Routing arrows
            gw >> auth
            gw >> pay
            gw >> order

            order >> sqs
            pay  >> sqs

            # All services → DB & CloudWatch
            for svc in (auth, pay, order):
                svc >> db
                svc >> cw

        return f"{fpath}.png"


    title = "Basic Web App"
    nodes = [
        {"id": "alb",  "type": "ALB", "label": "Load Balancer"},
        {"id": "web1", "type": "EC2", "label": "Web Server 1"},
        {"id": "web2", "type": "EC2", "label": "Web Server 2"},
        {"id": "db",   "type": "RDS", "label": "Database"},
    ]
    edges = [
        {"from": "alb",  "to": ["web1", "web2"]},
        {"from": "web1", "to": ["db"]},
        {"from": "web2", "to": ["db"]},
    ]
    return _draw(title, nodes, edges)

class Node(BaseModel):
    id: str = Field(..., description="Unique node id")
    type: str = Field(..., description="Node type, e.g. EC2, RDS, ALB")
    label: str = Field(..., description="Display label")

class Edge(BaseModel):
    from_: str = Field(..., alias="from", description="Source node id")
    to: List[str] = Field(..., description="Destination node ids")
    model_config = {"populate_by_name": True}

class DiagramInput(BaseModel):
    title: str = Field(..., description="Title of the diagram")
    nodes: List[Node] = Field(..., description="Array of Node objects")
    edges: List[Edge] = Field(..., description="Array of Edge objects")


class DiagramTool(BaseTool):
    name: str = "draw_diagram"
    description: str = "Generate a diagram PNG from a JSON specification."
    args_schema: ClassVar[type[BaseModel]] = DiagramInput  # pydantic‑safe

    def _run(self, title: str, nodes: List[Node], edges: List[Edge]) -> str:
        node_dicts = [n.model_dump() for n in nodes]
        edge_dicts = [e.model_dump(by_alias=True) for e in edges]
        return _draw(title, node_dicts, edge_dicts)

    async def _arun(self, title: str, nodes: List[Node], edges: List[Edge]) -> str:
        return self._run(title, nodes, edges)


diagram_tool = DiagramTool()

__all__ = ["generate_diagram", "diagram_tool", "DiagramTool", "DiagramInput"]
