# src/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from .agent import agent_chain
from .diagram_tool import generate_diagram
from .config import settings
import logging, base64, os

app = FastAPI(title="AI Diagram Generator API")

logging.basicConfig(level=settings.log_level, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("app")

@app.get("/")
def root():
    return {"message": "Welcome to the AI Diagram Generator API Service."}

@app.get("/status")
def status():
    return {"message": "Agent service is running."}

@app.get("/diagram")
async def diagram_endpoint(description: str = ""):
    if not description:
        return JSONResponse({"error": "No description provided"}, status_code=400)
    try:
        image_path = generate_diagram(description)
    except Exception as e:
        logger.error("Failed to generate diagram: %s", e, exc_info=True)
        return JSONResponse({"error": "Failed to generate diagram"}, status_code=500)
    return FileResponse(image_path, media_type="image/png")

# ─────────────────────────────────────────────────────────────
#  Assistant‑style endpoint
# ─────────────────────────────────────────────────────────────
@app.post("/assistant_chat")
async def assistant_chat(request: Request):
    """
    Conversational endpoint.
    JSON body:
        {
          "message": "user prompt",
          "conversation_id": "optional‑thread‑id"
        }
    """
    payload = await request.json()
    message = payload.get("message", "")
    conversation_id = payload.get("conversation_id", "default")

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    if agent_chain is None:
        raise HTTPException(status_code=500, detail="Agent not available")

    try:
        # CompiledStateGraph → use .invoke(), passing the message list
        state = agent_chain.invoke({"messages": [("user", message)]})
        # The agent returns state dict; get the last assistant message
        last_msg = state["messages"][-1]
        assistant_text = getattr(last_msg, "content", str(last_msg))

        # Optionally pull an image path from the assistant text
        image_path = None
        if isinstance(assistant_text, str) and "saved to" in assistant_text:
            # crude pattern: "... saved to /full/path.png"
            image_path = assistant_text.split("saved to", 1)[-1].strip().split()[0]

        return JSONResponse(
            {
                "conversation_id": conversation_id,
                "response": assistant_text,
                "image_path": image_path,
            }
        )

    except Exception as exc:
        logger.exception("Assistant endpoint error")
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {exc}")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
