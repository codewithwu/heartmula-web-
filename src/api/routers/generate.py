"""音乐生成路由模块"""

import tempfile
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.api.schemas import GenerationRequest
from src.api.services.generator import GeneratorService

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
