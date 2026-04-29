"""应用配置模块."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """从环境变量加载的应用配置."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM 配置
    longcat_api_key: str = ""
    longcat_model_name: str = "LongCat-Flash-Chat"
    longcat_base_url: str = "https://api.longcat.chat/openai"

    ling_api_key: str = ""
    ling_model_name: str = "Ling-1T"
    ling_base_url: str = "https://api.tbox.cn/api/llm/v1/"

    # 默认 LLM 提供者
    default_llm_provider: Literal["longcat", "ling"] = "longcat"


settings = Settings()
