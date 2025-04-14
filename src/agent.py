# src/agent.py
import logging
from typing import List, Union
from .diagram_tool import diagram_tool
from .config import settings
from .llm_client import get_llm

logger = logging.getLogger(__name__)

llm = get_llm()


agent_executor: Union[object, None] = None
if llm:
    try:
        from langgraph.prebuilt import create_react_agent
        tools: List = [diagram_tool]
        agent_executor = create_react_agent(
            model=llm,
            tools=tools,
        )
        logger.info("LangGraph React agent created successfully.")
    except Exception as e:
        logger.error("LangGraph agent creation failed: %s. Running agent in dummy mode.", e)
        agent_executor = None
else:
    logger.warning("No valid LLM available. Agent running in dummy mode.")
    agent_executor = None

agent_chain = agent_executor
