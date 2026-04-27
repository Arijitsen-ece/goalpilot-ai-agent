"""
Reasoning layer – Gemini-powered decision engine + multi-tool execution.
"""

from config.gemini_config import get_gemini_client, GEMINI_MODEL, SYSTEM_PROMPT
from utils.parser import extract_json
from google.genai import types

# Import tools
from agent.tools import (
    create_calendar_event,
    get_route,
    save_note
)


def get_tasks_from_goal(goal: str) -> dict:
    """
    Main agent reasoning function.

    Returns:
        {
            "type": "plan",
            "data": {...}
        }
        OR
        {
            "type": "tool",
            "message": "..."
        }
        OR
        {
            "type": "multi",
            "data": {...},
            "tool_result": "..."
        }
    """

    client = get_gemini_client()

    try:
        # 🧠 Gemini reasoning call
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=goal,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
                response_mime_type="application/json"
            )
        )

        raw_text = response.text

    except Exception as exc:
        raise RuntimeError(f"Gemini API call failed: {exc}") from exc

    # 🔍 Parse JSON safely
    try:
        data = extract_json(raw_text)
    except Exception:
        raise ValueError("Could not parse Gemini response")

    # 🧠 Self-audit log
    print("       > Internal Audit: Checking agent decision...")

    # ─────────────────────────────────────────────
    # 🧠 DECISION LOGIC (AGENT CORE)
    # ─────────────────────────────────────────────

    action = data.get("action", "plan")

    # ─────────────────────────────
    # 🔥 CASE 1: CALENDAR TOOL
    # ─────────────────────────────
    if action == "calendar":
        tool_input = data.get("tool_input", {})

        title = tool_input.get("title", "Scheduled Event")
        date = tool_input.get("date", "")
        time = tool_input.get("time", "")

        print("       > Agent selected TOOL: calendar")

        try:
            result = create_calendar_event(title, date, time)
        except Exception as e:
            result = f"❌ Calendar tool failed: {e}"

        return {
            "type": "tool",
            "message": result
        }

    # ─────────────────────────────
    # 🔥 CASE 2: ROUTE TOOL
    # ─────────────────────────────
    elif action == "route":
        tool_input = data.get("tool_input", {})

        source = tool_input.get("from", "")
        destination = tool_input.get("to", "")

        print("       > Agent selected TOOL: route")

        try:
            result = get_route(source, destination)
        except Exception as e:
            result = f"❌ Route tool failed: {e}"

        return {
            "type": "tool",
            "message": result
        }

    # ─────────────────────────────
    # 🔥 CASE 3: NOTE TOOL
    # ─────────────────────────────
    elif action == "note":
        tool_input = data.get("tool_input", {})

        content = tool_input.get("content", "")

        print("       > Agent selected TOOL: note")

        try:
            result = save_note(content)
        except Exception as e:
            result = f"❌ Note tool failed: {e}"

        return {
            "type": "tool",
            "message": result
        }

    # ─────────────────────────────
    # 🔥 CASE 4: MULTI-ACTION (PLAN + CALENDAR)
    # ─────────────────────────────
    elif action == "plan_and_schedule":

        print("       > Agent selected MULTI-ACTION: plan + calendar")

        # 🛡️ Fallback if tasks missing
        if "tasks" not in data or not isinstance(data["tasks"], list) or not data["tasks"]:
            print("       [WARN] Invalid tasks — using fallback")

            data["tasks"] = [
                "Understand the goal",
                "Break into steps",
                "Prioritize tasks",
                "Execute plan",
                "Review progress"
            ]

        # Limit tasks
        data["tasks"] = data["tasks"][:7]

        # Extract calendar info
        tool_input = data.get("tool_input", {})

        title = tool_input.get("title", "Study Session")
        date = tool_input.get("date", "")
        time = tool_input.get("time", "")

        try:
            calendar_result = create_calendar_event(title, date, time)
        except Exception as e:
            calendar_result = f"❌ Calendar failed: {e}"

        print("       ✓ Multi-action executed.\n")

        return {
            "type": "multi",
            "data": data,
            "tool_result": calendar_result
        }

    # ─────────────────────────────
    # 🔥 DEFAULT: PLANNING
    # ─────────────────────────────
    else:
        print("       > Agent selected ACTION: planning")

        # 🛡️ Fallback if Gemini fails
        if "tasks" not in data or not isinstance(data["tasks"], list) or not data["tasks"]:
            print("       [WARN] Invalid or missing tasks — generating fallback plan")

            data = {
                "goal": goal,
                "analysis": "Fallback planning due to model inconsistency.",
                "tasks": [
                    "Understand the goal clearly",
                    "Break it into smaller steps",
                    "Prioritize tasks",
                    "Execute step-by-step",
                    "Review and improve results"
                ]
            }

        # Limit tasks
        data["tasks"] = data["tasks"][:7]

        print("       ✓ Plan validated and optimized.\n")

        return {
            "type": "plan",
            "data": data
        }