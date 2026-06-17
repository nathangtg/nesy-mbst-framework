from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Sequence

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI

# Load env vars once at import time
load_dotenv()


class BaseAgent(ABC):
    def __init__(
        self,
        *,
        model_name: str | None = None,
        temperature: float = 0.2,
    ) -> None:
        self._temperature = temperature
        self._model_name = model_name or os.getenv("AZURE_DEPLOYMENT", "gpt-4.1-mini")

        # Build the LLM
        self._llm = self._build_llm()

    def _build_llm(self) -> AzureChatOpenAI:
        """Construct the Azure OpenAI chat model from environment variables."""
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPEN_AI_ENDPOINT", ""),
            api_key=os.getenv("AZURE_API_KEY", ""),
            azure_deployment=self._model_name,
            api_version="2025-03-01-preview",
            temperature=self._temperature,
        )

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the full system prompt for this agent."""

    @property
    @abstractmethod
    def agent_name(self) -> str:
        """A short human-readable name (used in logs and graph node IDs)."""

    @property
    def model(self) -> AzureChatOpenAI:
        """The raw LLM instance."""
        return self._llm

    def _build_messages(
        self,
        user_input: str,
        history: Sequence[BaseMessage] | None = None,
    ) -> list[BaseMessage]:
        """Assemble the message list for the LLM call."""
        messages: list[BaseMessage] = [SystemMessage(content=self.system_prompt)]
        if history:
            messages.extend(history)
        messages.append(HumanMessage(content=user_input))
        return messages

    def invoke(
        self,
        user_input: str,
        *,
        history: Sequence[BaseMessage] | None = None,
    ) -> AIMessage:
        """Synchronous single-turn invocation."""
        messages = self._build_messages(user_input, history)
        return self._llm.invoke(messages)

    async def ainvoke(
        self,
        user_input: str,
        *,
        history: Sequence[BaseMessage] | None = None,
    ) -> AIMessage:
        """Async single-turn invocation."""
        messages = self._build_messages(user_input, history)
        return await self._llm.ainvoke(messages)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} name={self.agent_name!r} "
            f"model={self._model_name!r}>"
        )