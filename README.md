# 📅 Smart Timetable Agent

An AI-powered timetable management system built with **LangChain**, **Gemini AI**, and **Streamlit**. It helps students manage their weekly schedule, track assignments, find free slots, and get AI-powered study suggestions.

---

## 🚀 Features

- 📋 **View Weekly Schedule** — See your full timetable day by day
- ➕ **Add Events** — Add new classes or study sessions with conflict detection
- ✅ **Assignment Tracker** — Track deadlines with urgency indicators
- 🔍 **Free Slot Finder** — Find available time slots in your schedule
- 📚 **Study Plan Generator** — Auto-generate study plans based on deadlines
- 💬 **AI Assistant** — Chat with Gemini AI to manage your timetable naturally

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| LangChain | AI Agent framework |
| Google Gemini AI | Language model |
| SQLite | Database |

---

## 📁 Project Structure

```
smart_timetable_agent/
├── smart_timetable.py   ← Backend + AI Agent
├── app.py               ← Streamlit UI
├── requirements.txt     ← Dependencies
└── README.md            ← Project description
```

---

## ⚙️ Installation

**Step 1 — Clone the repo**
```bash
git clone https://github.com/YourUsername/smart_timetable_agent.git
cd smart_timetable_agent
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Run the app**
```bash
streamlit run app.py
```

**Step 4 — Add Gemini API Key**

Enter your Gemini API key in the sidebar of the app.
Get your key at [aistudio.google.com](https://aistudio.google.com)

---

## 🌐 Live Demo

👉 [Click here to open the app](https://smart-timetable-agent-jjsxhfrmnn4esji9tyxfo4.streamlit.app/)
---

## 📸 Screenshots

### Dashboard
- Shows today's schedule
- Upcoming deadlines
- Quick metrics

### AI Assistant
- Chat with Gemini AI
- Ask about your schedule
- Get study suggestions

---

## 🤖 AI Agent Tools

The agent has access to these tools:

| Tool | Description |
|---|---|
| `ViewSchedule` | View timetable for a day or full week |
| `AddEvent` | Add new event with conflict detection |
| `FindFreeSlots` | Find free time slots on a day |
| `ViewAssignments` | List pending assignments by urgency |
| `AddAssignment` | Add new assignment with deadline |
| `SuggestStudyPlan` | Generate study plan from free slots |

---

## 💬 Example Queries

```
"What classes do I have on Monday?"
"Find free slots on Wednesday"
"What assignments are due soon?"
"Suggest a study plan for my deadlines"
"Add a study session on Friday from 5pm to 6pm"
```

---

## 📝 License

This project is for educational purposes.

---

## 👨‍💻 Author

Made with ❤️ using LangChain + Gemini AI + Streamlit
