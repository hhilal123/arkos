from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import time
import uuid
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config_module.loader import config
from agent_module.agent import Agent
from state_module.state_handler import StateHandler
from memory_module.memory import Memory
from model_module.ArkModelNew import ArkModelLink, UserMessage, SystemMessage, AIMessage


app = FastAPI(title="ArkOS Agent API", version="1.0.0")

# Initialize the agent and dependencies once
flow = StateHandler(yaml_path=config.get("state.graph_path"))
memory = Memory(
    user_id=config.get("memory.user_id"),
    session_id=None,
    db_url=config.get("database.url"),
)
llm = ArkModelLink(base_url=config.get("llm.base_url"))
agent = Agent(agent_id=config.get("memory.user_id"), flow=flow, memory=memory, llm=llm)

# Default system prompt for the agent


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """OAI-compatible endpoint wrapping the full ArkOS agent."""
    payload = await request.json()

    messages = payload.get("messages", [])
    model = payload.get("model", "ark-agent")
    response_format = payload.get("response_format")

    context_msgs = []

    context_msgs.append(SystemMessage(content=config.get("app.system_prompt")))

    # Convert OAI messages into internal message objects
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            context_msgs.append(SystemMessage(content=content))
        elif role == "user":
            context_msgs.append(UserMessage(content=content))
        elif role == "assistant":
            context_msgs.append(AIMessage(content=content))

    # Get the last assistant message
    final_msg = agent.step(context_msgs) or AIMessage(content="(no response)")

    # Format as OpenAI chat completion response
    completion = {
        "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": final_msg.content},
                "finish_reason": "stop",
            }
        ],
    }

    return JSONResponse(content=completion)


if __name__ == "__main__":
    uvicorn.run(
        "base_module.app:app",
        host=config.get("app.host"),
        port=int(config.get("app.port")),
        reload=config.get("app.reload"),
    )
