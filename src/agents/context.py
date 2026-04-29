"""Agent Context 模块.

定义 agent 运行时的上下文结构。
"""

from typing import TypedDict


class AgentContext(TypedDict):
    """Agent 运行时上下文（每次请求传入，不持久化）.

    Attributes:
        api_role: API 角色标识，用于动态切换系统提示词
    """

    api_role: str
