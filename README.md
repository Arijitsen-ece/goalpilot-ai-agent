# 🤖 GoalPilot AI — Autonomous Task Planning Agent

![MLH Hackathon](https://img.shields.io/badge/MLH-Hackathon-blue)
![Gemini API](https://img.shields.io/badge/Powered%20By-Google%20Gemini-orange)
![Agent](https://img.shields.io/badge/Type-Autonomous%20Agent-purple)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

> ⚡ From Bot → Agent  
> 🚀 This is NOT a chatbot — it is an autonomous decision-making system.

---

## 🔥 What is GoalPilot AI?

GoalPilot AI is an **autonomous AI agent** that:

- 🧠 Understands user intent
- 🎯 Decides the correct action
- ⚙️ Executes real-world tools
- 📋 Generates structured execution plans

👉 Unlike chatbots, it **does not just respond — it acts.**

---

## 🧠 Agent Capabilities

- ✅ Multi-step reasoning (Gemini-powered)
- ✅ Decision engine (Plan / Tool / Multi-action)
- ✅ Real-world execution (Calendar + File output)
- ✅ Context-aware planning (domain-specific tasks)
- ✅ Autonomous workflow (no manual chaining)

---

## ⚙️ Agent Workflow


User Goal
↓
🧠 Gemini Reasoning Engine
↓
🎯 Decision Layer
├── Plan
├── Calendar
└── Multi-Action (Plan + Tool)
↓
⚙️ Tool Execution
↓
📋 Autonomous Execution Plan


---

## 🚀 Killer Demo (Multi-Action)

### Input:

Prepare for Signals exam in 3 days and remind me tomorrow at 6 PM


### Output:

🧠 Agent Decision: PLAN + CALENDAR

⚙️ Tool Execution:
📅 Reminder set for tomorrow at 6:00 PM
📁 goalpilot_event.ics created

📋 Autonomous Execution Plan:

Solve 5 Fourier Transform problems
Practice convolution numericals
Review Laplace Transform concepts
...

🚀 Autonomous execution completed successfully


👉 This demonstrates **true agent behavior**:
- Decision-making  
- Multi-tool execution  
- Real-world action  

---

## 🗂️ Project Structure


goalpilot/
├── main.py # CLI agent runner
├── app.py # Streamlit UI (web interface)
├── agent/
│ ├── reasoning.py # Gemini decision engine
│ └── tools.py # Calendar + scheduling tools
├── config/
│ └── gemini_config.py # API + system prompt
├── utils/
│ └── parser.py # JSON parsing + validation
├── requirements.txt
└── README.md


---

## ⚙️ Setup

### 1. Install dependencies

bash
pip install -r requirements.txt
2. Set Gemini API key

Get your key: https://aistudio.google.com/app/apikey

export GEMINI_API_KEY="your_api_key_here"

Windows:

setx GEMINI_API_KEY "your_api_key_here"
▶️ Run Project
CLI Mode
python main.py
Direct Command
python main.py --goal "Prepare for exam" --days 3
🌐 Web UI (Recommended for Demo)
streamlit run app.py
🧪 Test Cases
🔥 Multi-action (BEST DEMO)
Prepare for Signals exam and remind me tomorrow at 6 PM
📅 Tool execution
Schedule a meeting tomorrow at 5 PM
📋 Planning
Plan a trip to Midnapore
📊 Architecture Diagram

🧠 Why This is NOT a Chatbot
Chatbot ❌	GoalPilot AI ✅
Gives answers	Takes decisions
Static responses	Dynamic execution
No tools	Uses real tools
Single-step	Multi-step reasoning
🏆 Hackathon Highlights
🔥 Built for MLH Bot to Agent
⚡ Uses Google Gemini API
🧠 Demonstrates Agentic AI
⚙️ Real-world execution capability
🚀 Multi-action autonomy (rare feature)
🔮 Future Improvements
🌐 Google Calendar API integration
📍 Maps / navigation tools
🧠 Persistent memory
📧 Email / notification automation


👨‍💻 Author

Arijit Sen

BTech ECE | AI Developer

Linkedin - https://www.linkedin.com/in/arijit-sen-188864228


❤️ Acknowledgment

Built for MLH Hack Days — Bot to Agent
Powered by Google Gemini API
