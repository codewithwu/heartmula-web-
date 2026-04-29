from pydantic import BaseModel


class TranscribeResponse(BaseModel):
    """转录响应模型"""

    lyrics: str
