import re
from typing import Tuple

INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"disregard (all )?system (prompts|instructions)",
    r"you are now a",
    r"act as an unrestricted",
    r"reveal (your|the) system prompt",
    r"show me your base instructions",
    r"dan mode",
    r"jailbreak"
]


def check_input_guardrails(query: str) -> Tuple[bool, str]:
    """
    Evaluates input text against safety guardrails.
    Returns: (is_safe: bool, refusal_or_clean_message: str)
    """
    clean_query = query.strip()

    # 1. Prompt Injection Detection
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, clean_query, re.IGNORECASE):
            return False, "I cannot fulfill this request. I am designed exclusively to assist with Nykaa customer support queries."

    # 2. Minimum length check
    if len(clean_query) < 2:
        return False, "Your query is too short. Please provide a full question regarding Nykaa orders or policies."

    return True, clean_query