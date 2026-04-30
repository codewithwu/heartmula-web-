"""Music Agent 模块."""

from typing import Annotated, Any

from langchain.agents import create_agent

from src.agents.llm_factory import get_llm
from src.utils import console_logger

from src.agents.prompts import (
    LYRICS_FORMAT_CHECK_PROMPT,
)


class AgentManager:
    """Agent 多例管理器（单例）.

    相同 role 复用同一 agent 实例，避免重复创建。
    """

    _instance: "AgentManager | None" = None
    _agents: dict[str, Any] = {}  # role → agent

    def __new__(cls) -> "AgentManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._agents = {}
        return cls._instance

    def get_agent(
        self,
        middleware=None,
        context_schema=None,
        response_format=None,
        role: Annotated[str, "角色标识"] = "default",
        llm_provider: Annotated[str, "LLM 提供者: 'longcat' 或 'ling'"] = "longcat",
    ) -> Any:
        """获取或创建 agent 实例.

        Args:
            role: 角色标识，相同 role 返回同一 agent 实例
            llm_provider: LLM 提供者

        Returns:
            Agent 实例
        """
        if role not in self._agents:
            llm = get_llm(llm_provider)
            self._agents[role] = create_agent(
                model=llm,
                middleware=middleware,
                context_schema=context_schema,
                response_format=response_format,
                system_prompt=LYRICS_FORMAT_CHECK_PROMPT,
            )
            console_logger.info(
                f"创建新 Agent 实例，role: {role}, "
                f"agent_id: {id(self._agents[role])}, "
                f"当前实例总数: {len(self._agents)}"
            )
        else:
            console_logger.info(
                f"复用已有 Agent 实例，role: {role}, "
                f"agent_id: {id(self._agents[role])}, "
                f"当前实例总数: {len(self._agents)}"
            )
        return self._agents[role]

    def clear_role(self, role: str) -> None:
        """清理指定角色的 agent 实例.

        Args:
            role: 要清理的角色标识
        """
        if role in self._agents:
            del self._agents[role]
            console_logger.info(f"已清理角色 agent: {role}")

    def clear_all(self) -> None:
        """清理所有 agent 实例."""
        self._agents.clear()
        console_logger.info("已清理所有角色 agent")

    @property
    def active_roles(self) -> list[str]:
        """获取当前活跃的角色列表."""
        return list(self._agents.keys())
