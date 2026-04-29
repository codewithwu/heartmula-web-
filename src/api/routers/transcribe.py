import os

from fastapi import APIRouter, File, UploadFile

from src.api.schemas import TranscribeResponse
from src.api.services.transcriber import TranscriberService

router = APIRouter(prefix="/api/v1", tags=["转录"])


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(file: UploadFile = File(...)) -> TranscribeResponse:
    """接收音频文件并返回歌词"""
    service = TranscriberService.from_pretrained(
        os.getenv("TRANSCRIBER_MODEL_PATH", "./ckpt")
    )
    content = await file.read()
    lyrics = service.transcribe_from_file(content, file.filename or "audio")
    return TranscribeResponse(lyrics=lyrics)
