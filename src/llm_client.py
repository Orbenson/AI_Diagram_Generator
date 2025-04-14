# src/llm_client.py
import os, logging
from typing import Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
from .config import settings

logger = logging.getLogger(__name__)

# Ensure the API key is set in the environment for the Gemini SDK.
if settings.google_api_key:
    os.environ["GOOGLE_API_KEY"] = settings.google_api_key

def build_gemini_llm() -> "ChatGoogleGenerativeAI":
    """Return a Gemini LLM instance using langchain-google-genai."""
    logger.info("Initializing Gemini LLM")
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=settings.temperature,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

def build_hf_fallback() -> "HuggingFacePipeline":
    """Return a fallback HuggingFace LLM instance."""
    logger.info("Initializing HuggingFace fallback LLM")
    generator = pipeline("text-generation", model=settings.hf_fallback_model, max_new_tokens=256)
    # Minimal wrapper to add a no-op bind_tools
    class HFWrapper:
        def __init__(self, pipeline_instance):
            self.pipeline = pipeline_instance
        def invoke(self, prompt: str) -> str:
            return self.pipeline(prompt)[0]["generated_text"]
        def __call__(self, prompt: str) -> str:
            return self.invoke(prompt)
        def bind_tools(self, tools):
            return self
    hf_llm = HuggingFacePipeline(pipeline=generator)
    return HFWrapper(hf_llm)

def get_llm() -> Union["ChatGoogleGenerativeAI", "HuggingFacePipeline"]:
    """Try to get Gemini; fall back to HuggingFace if needed."""
    try:
        return build_gemini_llm()
    except Exception as e:
        logger.error("Gemini LLM initialization failed: %s", e)
        return build_hf_fallback()
