"""
Agent tools – scheduling + real-world execution tools.
"""

from datetime import datetime


# ─────────────────────────────────────────────────────────────
# 1. TASK SCHEDULING TOOL
# ─────────────────────────────────────────────────────────────
def create_schedule(tasks: list, days: int) -> dict:
    """
    Distribute tasks evenly across the given number of days.
    """

    if not tasks:
        raise ValueError("Cannot schedule an empty task list.")
    if days < 1:
        raise ValueError("Number of days must be at least 1.")

    schedule: dict = {f"Day {d}": [] for d in range(1, days + 1)}

    # Round-robin distribution
    for idx, task in enumerate(tasks):
        day_key = f"Day {(idx % days) + 1}"
        schedule[day_key].append(task)

    # Fill empty days (important edge case)
    review_task = f"Review & Practice: {tasks[-1]}"
    for day_key, day_tasks in schedule.items():
        if not day_tasks:
            schedule[day_key].append(review_task)

    return schedule


# ─────────────────────────────────────────────────────────────
# 2. FORMAT OUTPUT TOOL
# ─────────────────────────────────────────────────────────────
def format_schedule(schedule: dict, goal: str, analysis: str) -> str:
    """
    Render schedule into a clean formatted string.
    """

    lines = []
    border = "═" * 60

    lines.append(f"\n{border}")
    lines.append("  📅  GoalPilot AI — Autonomous Execution Plan")
    lines.append(border)

    lines.append(f"\n  🎯  Goal     : {goal}")
    lines.append(f"  🧠  Analysis : {analysis}\n")

    lines.append(border)

    for day, tasks in schedule.items():
        lines.append(f"\n  {day}")
        lines.append("  " + "─" * 40)

        for i, task in enumerate(tasks, start=1):
            lines.append(f"    {i}. {task}")

    lines.append(f"\n{border}")
    lines.append("  ✅  Plan generated successfully.")
    lines.append(border + "\n")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# 3. REAL AGENT TOOL → CALENDAR EVENT
# ─────────────────────────────────────────────────────────────
def create_calendar_event(title: str, date: str, time: str) -> str:
    """
    Creates a real .ics calendar event file.
    """

    try:
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return f"📅 Reminder set successfully → {title} on {date} at {time} (file: goalpilot_event.ics)"

    content = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
SUMMARY:{title}
DTSTART:{dt.strftime("%Y%m%dT%H%M%S")}
DTEND:{dt.strftime("%Y%m%dT%H%M%S")}
DESCRIPTION:Created by GoalPilot AI Agent
END:VEVENT
END:VCALENDAR
"""

    filename = "goalpilot_event.ics"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return f"❌ Failed to create calendar file: {e}"

    return f"📅 Calendar event created successfully → {filename}"


# ─────────────────────────────────────────────────────────────
# 4. FILE EXPORT TOOL
# ─────────────────────────────────────────────────────────────
def save_plan_to_file(content: str, filename: str = "goalpilot_plan.txt") -> str:
    """
    Saves generated plan to a file.
    """

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return f"❌ File save failed: {e}"

    return f"📁 Plan saved as {filename}"


# ─────────────────────────────────────────────────────────────
# 5. NOTE TOOL (AGENT MEMORY SIMULATION)
# ─────────────────────────────────────────────────────────────
def save_note(content: str) -> str:
    """
    Saves user note (simulates memory/action).
    """

    filename = "goalpilot_note.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return f"❌ Note save failed: {e}"

    return f"📝 Note saved → {filename}"


# ─────────────────────────────────────────────────────────────
# 6. ROUTE TOOL (REAL-WORLD ACTION SIMULATION)
# ─────────────────────────────────────────────────────────────
def get_route(source: str, destination: str) -> str:
    """
    Provides basic route guidance.
    """

    if not source or not destination:
        return "❌ Missing source or destination."

    return f"""🗺 Route Guide

From: {source}
To: {destination}

Recommended Steps:
1. Travel via train/bus to Kolkata (Sealdah/Howrah)
2. Go to Salt Lake Sector V
3. Take auto/cab to destination

⏱ Estimated Time: 2–3 hours
💡 Tip: Avoid peak hours for faster travel
"""