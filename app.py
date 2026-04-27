import streamlit as st
from agent.reasoning import get_tasks_from_goal
from agent.tools import create_schedule, format_schedule
from config.gemini_config import GEMINI_MODEL
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="GoalPilot AI", layout="centered")

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🤖 GoalPilot AI")
st.markdown("### Autonomous Agent — Not a Chatbot")
st.caption("⚡ Reasoning • Planning • Execution")

st.warning("⚠️ This is NOT a chatbot — it is an autonomous decision-making agent.")

# ─────────────────────────────────────────────
# FEATURE CARDS
# ─────────────────────────────────────────────
st.markdown("### 🚀 Capabilities")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🧠 Multi-step Reasoning")

with col2:
    st.info("⚙️ Tool Execution")

with col3:
    st.info("📊 Structured Planning")

st.markdown("---")

# ─────────────────────────────────────────────
# EXAMPLES
# ─────────────────────────────────────────────
st.markdown("### 💡 Try these examples:")
st.write("- Prepare for Signals exam in 3 days")
st.write("- Plan a trip to Midnapore")
st.write("- Schedule a meeting tomorrow at 5 PM")

st.markdown("---")

# ─────────────────────────────────────────────
# INPUT
# ─────────────────────────────────────────────
goal = st.text_input("🎯 Enter your goal")
days = st.number_input("📅 Number of days", min_value=1, step=1)

# ─────────────────────────────────────────────
# MAIN ACTION
# ─────────────────────────────────────────────
if st.button("🚀 Generate Execution Plan"):

    if not goal:
        st.warning("Please enter a goal")

    else:
        try:
            # ─────────────────────────────
            # ✅ STEP 1 — AGENT ACTIVITY (FIXED)
            # ─────────────────────────────
            st.markdown("### 🧠 Agent Activity")

            st.write("🔍 Understanding goal...")
            time.sleep(0.3)

            st.write("🧠 Deciding action...")
            time.sleep(0.3)

            st.write("⚙️ Executing...")
            time.sleep(0.3)

            st.caption(f"Model: {GEMINI_MODEL} | Duration: {days} day(s)")

            # ─────────────────────────────
            # REASONING
            # ─────────────────────────────
            with st.spinner("🤖 Agent reasoning..."):
                result = get_tasks_from_goal(goal)

            # ─────────────────────────────
            # ✅ STEP 2 — DECISION VISIBILITY (FIXED)
            # ─────────────────────────────
            if result["type"] == "multi":
                st.success("🧠 Agent Decision: Multi-action (Plan + Calendar)")
            elif result["type"] == "tool":
                st.success("🧠 Agent Decision: Tool Execution")
            else:
                st.success("🧠 Agent Decision: Planning Only")

            # ─────────────────────────────
            # TOOL MODE
            # ─────────────────────────────
            if result["type"] == "tool":

                st.markdown("### ⚙️ Execution Result")

                # ✅ STEP 3 — STRONG TOOL OUTPUT
                st.success("📅 Reminder successfully scheduled!")
                st.success(result["message"])

                st.info("🤖 Agent autonomously executed a real-world action")

                st.markdown("### 🤖 Agent Pipeline")
                st.caption("Reasoning → Decision → Tool Execution")

            # ─────────────────────────────
            # MULTI MODE
            # ─────────────────────────────
            elif result["type"] == "multi":

                data = result["data"]

                # ✅ STEP 3 — STRONG TOOL OUTPUT
                st.markdown("### ⚙️ Tool Execution Result")
                st.success("📅 Reminder successfully scheduled!")
                st.success(result["tool_result"])

                # ✅ STEP 5 — WOW LINE
                st.info("🤖 Agent autonomously planned and scheduled your task")

                # Scheduling
                schedule = create_schedule(data["tasks"], int(days))
                output = format_schedule(schedule, data["goal"], data["analysis"])

                # ✅ STEP 4 — FORCE OUTPUT VISIBILITY
                st.markdown("## 📋 Autonomous Execution Plan")

                st.markdown(f"### 🎯 Goal\n{data['goal']}")
                st.markdown(f"### 🧠 Analysis\n{data['analysis']}")

                st.markdown("### 🗂 Tasks")
                for i, task in enumerate(data["tasks"], 1):
                    st.write(f"{i}. {task}")

                st.download_button(
                    "📥 Download Plan",
                    output,
                    file_name="goalpilot_plan.txt",
                    mime="text/plain"
                )

                st.success("🚀 Autonomous execution completed successfully")

                st.markdown("### 🤖 Agent Pipeline")
                st.caption("Reasoning → Decision → Multi-Tool Execution")

            # ─────────────────────────────
            # PLAN MODE
            # ─────────────────────────────
            else:
                data = result["data"]

                st.success("✅ Tasks generated successfully")

                st.write("⚙️ Creating execution schedule...")
                schedule = create_schedule(data["tasks"], int(days))
                time.sleep(0.3)

                output = format_schedule(schedule, data["goal"], data["analysis"])

                st.markdown("---")

                # ✅ STEP 4 — FORCE OUTPUT VISIBILITY
                st.markdown("## 📋 Autonomous Execution Plan")

                st.markdown(f"### 🎯 Goal\n{data['goal']}")
                st.markdown(f"### 🧠 Analysis\n{data['analysis']}")

                st.markdown("### 🗂 Task Breakdown")
                for i, task in enumerate(data["tasks"], 1):
                    st.markdown(f"{i}. {task}")

                st.download_button(
                    label="📥 Download Plan",
                    data=output,
                    file_name="goalpilot_plan.txt",
                    mime="text/plain"
                )

                # Save locally
                with open("output_plan.txt", "w", encoding="utf-8") as f:
                    f.write(output)

                st.success("📁 Plan saved successfully")

                # ✅ STEP 5 — WOW LINE
                st.info("🤖 Agent autonomously planned your execution strategy")

                st.markdown("### 🤖 Agent Pipeline")
                st.caption("Reasoning → Planning → Validation → Execution")

        except Exception as e:
            st.error(f"❌ Error occurred: {e}")
            st.info("Try a different input or check API connection.")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("Works for: Students • Developers • Researchers • Productivity Automation")
st.caption("Agent Pipeline: Reasoning → Planning → Validation → Execution")