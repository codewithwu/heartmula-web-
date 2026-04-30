from functools import lru_cache

from langchain.agents.middleware import (
    ModelRequest,
    ModelResponse,
    wrap_model_call,
)

from src.agents.prompts import (
    LYRICS_FORMATTING_PROMPT,
    LYRICS_FORMAT_CHECK_PROMPT,
    DEFAULT_SYSTEM_PROMPT,
    LYRICS_TAG_RECOMMEND_PROMPT,
)

from src.utils.logger import console_logger as logger


# =============================================================================
# 动态提示词中间件
# =============================================================================


@wrap_model_call
def dynamic_system_prompt(request: ModelRequest, handler) -> ModelResponse:
    """根据 api_role 动态切换系统提示词.

    - transcribe: 使用歌词格式化提示词
    - generate: 使用歌词格式校验提示词
    - default: 使用默认提示词
    """

    api_role = request.runtime.context.get("api_role", "default")
    if api_role == "transcribe":
        logger.info(f"使用歌词格式化提示词，api_role: {api_role}")
        return handler(request.override(system_prompt=LYRICS_FORMATTING_PROMPT))
    elif api_role == "generate":
        logger.info(f"使用歌词格式校验提示词，api_role: {api_role}")
        return handler(
            request.override(
                system_prompt=LYRICS_FORMAT_CHECK_PROMPT,
            )
        )
    elif api_role == "tag_recommend":
        logger.info(f"使用默认提示词，api_role: {api_role}")
        return handler(request.override(system_prompt=LYRICS_TAG_RECOMMEND_PROMPT))
    elif api_role == "default":
        logger.info(f"使用默认提示词，api_role: {api_role}")
        return handler(request.override(system_prompt=DEFAULT_SYSTEM_PROMPT))

    return handler(request)


# =============================================================================
# 模型 fallback 中间件
# =============================================================================


@wrap_model_call
def model_fallback_middleware(request: ModelRequest, handler) -> ModelResponse:
    """主模型报错时切换到备用模型.

    当主模型调用发生任何错误时，自动切换到备用模型（ling）重试。
    """
    from src.agents.llm_factory import get_llm

    try:
        return handler(request)
    except Exception as e:
        logger.warning(f"主模型调用失败，切换到备用模型: {e}")
        fallback_llm = get_llm("ling")
        return handler(request.override(model=fallback_llm))


# =============================================================================
# 中间件列表（懒加载）
# =============================================================================


@lru_cache
def get_all_middleware() -> list:
    """获取所有中间件列表（懒加载）."""
    return [
        dynamic_system_prompt,  # 动态切换提示词
        model_fallback_middleware,  # 模型失败时切换备用模型
    ]
