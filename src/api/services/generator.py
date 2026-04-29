"""音乐生成服务模块"""

import os
import tempfile
import uuid

import torch

from heartlib.pipelines.music_generation import HeartMuLaGenPipeline


class GeneratorService:
    """音乐生成服务单例类"""

    _instance: "GeneratorService | None" = None
    _pipeline: HeartMuLaGenPipeline | None = None
    _model_path: str | None = None

    def __new__(cls) -> "GeneratorService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._model_path = os.getenv("GENERATOR_MODEL_PATH", "./ckpt")
        return cls._instance

    def _ensure_pipeline(self) -> HeartMuLaGenPipeline:
        """确保模型已加载（懒加载）"""
        if self._pipeline is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            mula_dtype = torch.bfloat16 if device.type == "cuda" else torch.float32
            codec_dtype = torch.float32

            self._pipeline = HeartMuLaGenPipeline.from_pretrained(
                self._model_path or "./ckpt",
                device=device,
                dtype={"mula": mula_dtype, "codec": codec_dtype},
                version="3B",
                lazy_load=True,
            )
        return self._pipeline

    def generate(self, lyrics: str, tags: str, save_dir: str | None = None) -> str:
        """生成音乐文件"""
        if save_dir is None:
            save_dir = tempfile.gettempdir()

        save_path = os.path.join(save_dir, f"generated_{uuid.uuid4().hex}.mp3")

        pipeline = self._ensure_pipeline()
        pipeline(
            inputs={"lyrics": lyrics, "tags": tags},
            save_path=save_path,
        )
        return save_path
