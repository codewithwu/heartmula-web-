"""音乐生成路由模块"""

import tempfile
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.agents.music_agent import AgentManager
from src.api.schemas import GenerationRequest, LyricsCheckRequest, LyricsCheckResponse
from src.api.services.generator import GeneratorService
from src.utils import console_logger

from src.agents.context import AgentContext
from src.agents.middleware import get_all_middleware

from src.agents.prompts import LyricsCheckResponse as LyricsCheckResponseRes


router = APIRouter(prefix="/api/v1", tags=["生成"])


@router.post("/generate")
async def generate(request: GenerationRequest) -> FileResponse:
    """接收歌词和标签，生成音乐并返回音频文件"""
    service = GeneratorService()
    audio_path = service.generate(
        lyrics=request.lyrics,
        tags=request.tags,
        save_dir=tempfile.gettempdir(),
    )
    return FileResponse(
        path=audio_path,
        media_type="audio/mpeg",
        filename=Path(audio_path).name,
    )


@router.post("/lyrics/check", response_model=LyricsCheckResponse)
async def check_lyrics(request: LyricsCheckRequest) -> LyricsCheckResponse:
    """校验歌词格式是否符合标准"""
    agent_manager = AgentManager()
    agent = agent_manager.get_agent(
        middleware=get_all_middleware(),
        context_schema=AgentContext,
        response_format=LyricsCheckResponseRes,
        role=request.role,
        llm_provider=request.llm_provider,
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": request.lyrics}]},
        context={"api_role": "generate"},
    )

    structured_response = result.get("structured_response")
    if structured_response:
        is_valid = structured_response.is_valid
    else:
        is_valid = False

    console_logger.info(f"歌词格式校验完成，is_valid: {is_valid}")
    return LyricsCheckResponse(is_valid=is_valid)
