"""
Utility helpers for parsing Gemini API responses.
"""

import json
import re


def extract_json(raw_text: str) -> dict:
    """
    Robustly extract a JSON object from a raw text string.

    Gemini sometimes wraps JSON in markdown code fences (```json … ```)
    even when instructed not to.  This function strips those fences before
    parsing so the rest of the code always gets a clean dict.

    Args:
        raw_text: The raw string returned by the Gemini API.

    Returns:
        Parsed dict with keys: "goal", "analysis", "tasks".

    Raises:
        ValueError: If no valid JSON object can be found.
    """
    # 1. Strip markdown code fences if present
    cleaned = re.sub(r"```(?:json)?", "", raw_text).strip()
    cleaned = cleaned.rstrip("`").strip()

    # 2. Try direct parse first (happy path)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 3. Find the first {...} block in the string (fallback)
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(
        "Could not extract valid JSON from the Gemini response.\n"
        f"Raw response was:\n{raw_text}"
    )


def validate_agent_response(data: dict) -> bool:
    """
    Validate that the parsed response has the required keys and types.

    Args:
        data: Parsed dict from the Gemini response.

    Returns:
        True if valid, raises ValueError otherwise.
    """
    required_keys = {"goal", "analysis", "tasks"}
    missing = required_keys - data.keys()

    if missing:
        raise ValueError(f"Gemini response missing required keys: {missing}")

    if not isinstance(data["tasks"], list) or len(data["tasks"]) == 0:
        raise ValueError("'tasks' must be a non-empty list.")

    if not (4 <= len(data["tasks"]) <= 7):
        # Soft warning – we don't abort, just note it
        print(f"  [WARN] Expected 4–7 tasks, got {len(data['tasks'])}. Continuing anyway.")

    return True
