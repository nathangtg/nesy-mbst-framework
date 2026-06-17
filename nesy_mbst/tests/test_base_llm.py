from __future__ import annotations

import pytest
from nesy_mbst.agent.base_llm import BaseAgent
from nesy_mbst.agent.llm_adapter import LLMBackendAdapter
from nesy_mbst.neural.llm_oracle import GrammarConstrainedOracle
from nesy_mbst.agent.system_prompts import MEMBERSHIP_ORACLE_PROMPT


class MembershipOracleAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return "You are a domain expert validating execution paths. Respond only Yes, No, or Unsure."

    @property
    def agent_name(self) -> str:
        return "MembershipOracle"


class TestBaseAgentWithRealLLM:

    def test_agent_initialisation(self):
        agent = MembershipOracleAgent(temperature=0.1)
        assert agent.agent_name == "MembershipOracle"
        assert agent.model is not None

    def test_llm_responds_to_simple_prompt(self):
        agent = MembershipOracleAgent(temperature=0.1)
        response = agent.invoke("Say exactly one word: hello")
        assert response.content is not None
        assert len(response.content.strip()) > 0

    def test_llm_backend_adapter(self):
        agent = MembershipOracleAgent(temperature=0.1)
        adapter = LLMBackendAdapter(agent)
        response = adapter("Say exactly: Yes")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_oracle_with_real_llm_valid_path(self):
        agent = MembershipOracleAgent(temperature=0.1)
        adapter = LLMBackendAdapter(agent)
        oracle = GrammarConstrainedOracle(
            llm_backend=adapter,
            requirements="The system has states: Idle, Active, Error. Valid transitions: Idle->Active, Active->Idle, Active->Error.",
        )
        result = oracle.query_membership("IdleActive")
        assert result is not None
        assert oracle.query_count == 1

    def test_oracle_with_real_llm_invalid_path(self):
        agent = MembershipOracleAgent(temperature=0.1)
        adapter = LLMBackendAdapter(agent)
        oracle = GrammarConstrainedOracle(
            llm_backend=adapter,
            requirements="The system has states: A, B, C. Only valid transitions: A->B, B->C.",
        )
        result = oracle.query_membership("CBA")
        assert result is not None
        assert oracle.query_count == 1

    def test_oracle_caches_results(self):
        agent = MembershipOracleAgent(temperature=0.1)
        adapter = LLMBackendAdapter(agent)
        oracle = GrammarConstrainedOracle(
            llm_backend=adapter,
            requirements="System states: Start, End. Transitions: Start->End.",
        )
        result1 = oracle.query_membership("StartEnd")
        assert result1 is not None
        count_after_first = oracle.query_count
        result2 = oracle.query_membership("StartEnd")
        assert result2 == result1
        assert oracle.query_count == count_after_first

    def test_prompt_template(self):
        prompt = MEMBERSHIP_ORACLE_PROMPT.format(
            requirements="A->B is valid.",
            sequence="AB",
        )
        assert "AB" in prompt
        assert "A->B" in prompt
