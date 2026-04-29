import os
import tempfile
from pathlib import Path

import torch

from heartlib.pipelines.lyrics_transcription import HeartTranscriptorPipeline


class TranscriberService:
    """转录服务单例类"""

    _instance: "TranscriberService | None" = None
    _pipeline: HeartTranscriptorPipeline | None = None
    _pretrained_path: str | None = None

    def __new__(cls, pretrained_path: str | None = None) -> "TranscriberService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._pretrained_path = pretrained_path or os.getenv(
                "TRANSCRIBER_MODEL_PATH", "./ckpt"
            )
        return cls._instance

    @classmethod
    def from_pretrained(cls, pretrained_path: str) -> "TranscriberService":
        """加载预训练模型"""
        if cls._instance is None:
            cls._instance = cls(pretrained_path)
        return cls._instance

    def _ensure_pipeline(self) -> HeartTranscriptorPipeline:
        """确保模型已加载（懒加载）"""
        if self._pipeline is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            dtype = torch.float16 if device.type == "cuda" else torch.float32
            self._pipeline = HeartTranscriptorPipeline.from_pretrained(
                self._pretrained_path or "./ckpt",
                device=device,
                dtype=dtype,
            )
        return self._pipeline

    def transcribe(self, audio_path: str) -> str:
        """执行转录"""
        pipeline = self._ensure_pipeline()
        result = pipeline(audio_path)
        return result.get("text", "")

    def transcribe_from_file(self, file_content: bytes, filename: str) -> str:
        """从上传文件内容转录"""
        suffix = Path(filename).suffix
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        try:
            return self.transcribe(tmp_path)
        finally:
            os.unlink(tmp_path)
