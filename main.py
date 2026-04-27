#!/usr/bin/env python3
"""
GoalPilot AI – Autonomous Task Planning Agent
=============================================
MLH Hackathon: Bot to Agent
"""

import argparse
import sys
import time

# ── Local imports ─────────────────────────────────────────
from agent.reasoning import get_tasks_from_goal
from agent.tools import create_schedule, format_schedule
from config.gemini_config import GEMINI_MODEL


# ══════════════════════════════════════════════════════════
# CLI helpers
# ══════════════════════════════════════════════════════════

BANNER = r"""
  ____             _ ____  _ _       _        _    ___
 / ___| ___   __ _| |  _ \(_) | ___ | |_     / \  |_ _|
| |  _ / _ \ / _` | | |_) | | |/ _ \| __|   / _ \  | |
| |_| | (_) | (_| | |  __/| | | (_) | |_   / ___ \ | |
 \____|\___/ \__,_|_|_|   |_|_|\___/ \__| /_/   \_\___|

         Autonomous Task Planning Agent  🤖
"""


def print_step(step: int, total: int, message: str) -> None:
    print(f"\n  [{step}/{total}] {message}")


def print_separator() -> None:
    print("  " + "─" * 56)


def get_validated_days(raw: str) -> int:
    try:
        days = int(raw.strip())
    except ValueError:
        raise ValueError(f"'{raw}' is not a valid integer for days.")
    if not (1 <= days <= 30):
        raise ValueError("Number of days must be between 1 and 30.")
    return days


# ══════════════════════════════════════════════════════════
# Demo mode
# ══════════════════════════════════════════════════════════

DEMO_RESPONSE = {
    "goal": "Prepare for Signals exam in 5 days",
    "analysis": "Structured preparation strategy for Signals & Systems.",
    "tasks": [
        "Solve 5 problems on Fourier Transform duality",
        "Revise Laplace Transform pairs (30 min)",
        "Practice convolution numericals",
        "Solve previous year questions",
        "Revise sampling theorem",
        "Take mock test",
        "Final revision"
    ],
}


def run_demo(days: int) -> None:
    print("\n  [DEMO MODE] Using offline example.\n")
    time.sleep(0.4)

    data = DEMO_RESPONSE
    schedule = create_schedule(data["tasks"], days)
    output = format_schedule(schedule, data["goal"], data["analysis"])
    print(output)


# ══════════════════════════════════════════════════════════
# Main agent pipeline
# ══════════════════════════════════════════════════════════

def run_agent(goal: str, days: int) -> None:
    total_steps = 5

    print_separator()
    print_step(1, total_steps, "Validating inputs …")
    print(f"       Goal : {goal}")
    print(f"       Days : {days}")
    time.sleep(0.3)

    # Step 2: Reasoning
    print_step(2, total_steps, f"Agent Thinking … (calling {GEMINI_MODEL})")
    print(f"       > Context: Understanding '{goal}'")
    print(f"       > Strategy: Dividing into {days} structured execution blocks")
    print(f"       > Mode: Analytical + Action Planning")
    print("       Please wait — this takes a few seconds …")

    try:
        result = get_tasks_from_goal(goal)

    except Exception as exc:
        print(f"\n  [ERROR] {exc}")
        sys.exit(1)

    # ─────────────────────────────────────────
    # 🔥 TOOL MODE
    # ─────────────────────────────────────────
    if result["type"] == "tool":
        print("       > Agent selected TOOL execution")

        print_step(3, total_steps, "Executing tool …")

        print(f"       ✓ {result['message']}")
        print("       🚀 Autonomous execution completed successfully")

        print("\n🤖 Agent Pipeline: Reasoning → Decision → Tool Execution\n")
        return

    # ─────────────────────────────────────────
    # 🔥 MULTI MODE (PLAN + TOOL)
    # ─────────────────────────────────────────
    if result["type"] == "multi":
        data = result["data"]

        print("       > Agent selected MULTI-ACTION execution")

        print_step(3, total_steps, "Executing multi-step actions …")

        # 🔥 WOW EFFECT
        print("       🧠 Decision: PLAN + CALENDAR (multi-step execution)")
        print("       🤖 Agent completed planning + scheduling autonomously")

        print(f"       ✓ {result['tool_result']}")

        print_step(4, total_steps, "Generating execution plan …")

        schedule = create_schedule(data["tasks"], days)
        print("       ✓ Multi-step schedule created.")

        print_step(5, total_steps, "Rendering final plan …")

        output = format_schedule(schedule, data["goal"], data["analysis"])
        print(output)

        print("       🚀 Autonomous execution completed successfully")
        print("\n🤖 Agent Pipeline: Reasoning → Decision → Multi-Tool Execution\n")
        return

    # ─────────────────────────────────────────
    # ✅ PLAN MODE
    # ─────────────────────────────────────────
    data = result["data"]

    print("       ✓ Gemini generated structured execution plan.")

    print_step(3, total_steps, "Parsing structured JSON response …")
    print(f"       Tasks identified : {len(data['tasks'])}")

    for i, task in enumerate(data["tasks"], start=1):
        print(f"         {i}. {task}")

    print_step(4, total_steps, "Planning Execution …")

    schedule = create_schedule(data["tasks"], days)
    print("       ✓ Schedule created.")

    print_step(5, total_steps, "Rendering final plan …")

    output = format_schedule(schedule, data["goal"], data["analysis"])
    print(output)

    print("       🚀 Autonomous execution completed successfully")
    print("\n🤖 Agent Pipeline: Reasoning → Planning → Validation → Execution\n")


# ══════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal", type=str)
    parser.add_argument("--days", type=int)
    parser.add_argument("--demo", action="store_true")
    return parser.parse_args()


def main():
    print(BANNER)
    args = parse_args()

    if args.demo:
        run_demo(args.days or 5)
        return

    try:
        goal = args.goal or input("  Enter your goal  : ").strip()
        days = args.days or get_validated_days(input("  Enter number of days : "))
    except Exception as e:
        print(f"\n  [ERROR] {e}")
        sys.exit(1)

    run_agent(goal, days)


if __name__ == "__main__":
    main()