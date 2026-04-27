"""
Gemini configuration for GoalPilot AI Agent
(Hackathon-safe version with direct API key)
"""

from google import genai


# ─────────────────────────────────────────────
# MODEL CONFIG
# ─────────────────────────────────────────────
GEMINI_MODEL = "models/gemini-2.5-flash"


# ─────────────────────────────────────────────
# SYSTEM PROMPT (AGENT MODE)
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an autonomous AI agent.

You must decide the correct action.

Available actions:
- plan
- calendar
- plan_and_schedule

Rules:
1. NEVER give generic tasks.
2. Tasks must be SPECIFIC and measurable.
3. If academic → include:
   - problem solving
   - past papers
   - formulas
4. If trip → include:
   - transport
   - cost estimation
   - itinerary
5. If scheduling → extract exact date/time properly.

---

FORMAT:

PLAN:
{
  "action": "plan",
  "goal": "...",
  "analysis": "...",
  "tasks": [
    "Solve 5 problems on Fourier Transform duality",
    "Revise Laplace Transform pairs (30 min)",
    "Practice convolution numericals"
  ]
}

CALENDAR:
{
  "action": "calendar",
  "tool_input": {
    "title": "...",
    "date": "YYYY-MM-DD",
    "time": "HH:MM"
  }
}

MULTI:
{
  "action": "plan_and_schedule",
  "goal": "...",
  "analysis": "...",
  "tasks": ["...", "..."],
  "tool_input": {
    "title": "...",
    "date": "YYYY-MM-DD",
    "time": "HH:MM"
  }
}
"""

# ─────────────────────────────────────────────
# CLIENT SETUP (DIRECT API KEY)
# ─────────────────────────────────────────────
def get_gemini_client():
    """
    Returns Gemini client using direct API key (hackathon-safe).
    """

    api_key = "GEMINI_API_KEY"  # ← your key here

    if not api_key:
        raise ValueError("❌ API key missing")

    return genai.Client(api_key=api_key)