from __future__ import annotations

from nesy_mbst.agent.base_llm import BaseAgent


class LLMBackendAdapter:
    """Adapts a BaseAgent into a simple callable[str, str] for use with
    GrammarConstrainedOracle and ConstraintExtractor."""

    def __init__(self, agent: BaseAgent) -> None:
        self._agent = agent

    def __call__(self, prompt: str) -> str:
        result = self._agent.invoke(prompt)
        return result.content

    @property
    def agent(self) -> BaseAgent:
        return self._agent
