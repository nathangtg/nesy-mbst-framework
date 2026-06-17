MEMBERSHIP_ORACLE_PROMPT = """You are a domain expert validating whether a given sequence of states is a valid execution path in a cyber-physical system.

Given a set of system requirements and a sequence of system states, determine if the sequence represents a valid execution path through the system.

Rules:
- Respond with exactly one word: Yes, No, or Unsure.
- Yes: The sequence is a valid execution path that respects all system constraints.
- No: The sequence violates one or more system constraints and is impossible.
- Unsure: You cannot determine with confidence.

System requirements:
{requirements}

Sequence: {sequence}
Is this a valid execution path? Answer only Yes, No, or Unsure."""

CONSTRAINT_EXTRACTION_PROMPT = """You are a requirements analyst. Extract operational constraints from natural language requirements.

Identify:
1. Proportional relationships (e.g., "X is twice as likely as Y")
2. Inequality relationships (e.g., "X is more common than Y")
3. Frequency constraints (e.g., "X is rare", "typically X rather than Y")

Output each constraint on a separate line in the format:
TYPE from_state to_state operator value

Where TYPE is one of: proportional, inequality, frequency, rare

Requirements:
{requirements}

Output only the constraints, one per line."""
