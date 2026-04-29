import os

from fastapi import APIRouter, File, UploadFile

from src.agents.music_agent import AgentManager
from src.api.schemas import TranscribeResponse
from src.api.services.transcriber import TranscriberService
from src.utils import console_logger

from src.agents.context import AgentContext
from src.agents.middleware import get_all_middleware


router = APIRouter(prefix="/api/v1", tags=["转录"])


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(
    file: UploadFile = File(...),
    role: str = "transcribe",
    llm_provider: str = "longcat",
) -> TranscribeResponse:
    """接收音频文件并返回格式化后的歌词"""
    # 1. 语音转文字
    service = TranscriberService.from_pretrained(
        os.getenv("TRANSCRIBER_MODEL_PATH", "./ckpt")
    )
    content = await file.read()
    raw_lyrics = service.transcribe_from_file(content, file.filename or "audio")

    # 2. 使用 Agent 格式化歌词
    agent_manager = AgentManager()
    agent = agent_manager.get_agent(
        middleware=get_all_middleware(),
        context_schema=AgentContext,
        role=role,
        llm_provider=llm_provider,
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": raw_lyrics}]},
        context={"api_role": "transcribe"},
    )

    # 3. 提取格式化后的歌词
    messages = result.get("messages", [])
    if messages:
        last_message = messages[-1]
        formatted_lyrics = (
            last_message.content
            if hasattr(last_message, "content")
            else str(last_message)
        )
    else:
        formatted_lyrics = raw_lyrics

    console_logger.info(f"歌词格式化完成，agent: {role}")
    return TranscribeResponse(lyrics=formatted_lyrics)
