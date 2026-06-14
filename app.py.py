import os
import streamlit as st
from datetime import datetime


from smart_timetable import (
    get_conn,
    init_db,
    seed_data,
    parse_time,
    times_overlap,
    tool_view_schedule,
    tool_add_event,
    tool_find_free_slots,
    tool_view_assignments,
    tool_add_assignment,
    tool_suggest_study_plan,
    run_agent,
)


init_db()
seed_data()


def ui_add_event(day, subject, start, end):
    import json
    input_str = json.dumps({"day": day, "subject": subject, "start": start, "end": end})
    result = tool_add_event(input_str)
    success = result.startswith("✅")
    return success, result

def ui_add_assignment(subject, deadline, priority):
    import json
    input_str = json.dumps({"subject": subject, "deadline": str(deadline), "priority": priority})
    return tool_add_assignment(input_str)

def ui_find_free_slots(day):
    result = tool_find_free_slots(day)
    lines = result.split('\n')
    return [l.replace('  • ', '').strip() for l in lines if '•' in l]

def ui_get_assignments():
    conn = get_conn()
    c = conn.cursor()
    rows = c.execute('SELECT id,subject,deadline,priority,done FROM assignments ORDER BY deadline').fetchall()
    conn.close()
    return rows

def ui_mark_done(assignment_id):
    conn = get_conn()
    conn.execute('UPDATE assignments SET done=1 WHERE id=?', (assignment_id,))
    conn.commit()
    conn.close()

def ui_suggest_study_plan():
    result = tool_suggest_study_plan()
    return result


st.set_page_config(
    page_title="Smart Timetable",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0f1117; color: #e8eaf0; }

[data-testid="stSidebar"] {
    background: #161b27 !important;
    border-right: 1px solid #252d3d;
}

.page-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem; font-weight: 700;
    color: #c4b5fd; letter-spacing: -0.5px; margin-bottom: 0;
}
.page-sub { color: #6b7280; font-size: 0.9rem; margin-bottom: 1.5rem; }

.card {
    background: #161b27; border: 1px solid #252d3d;
    border-radius: 12px; padding: 1rem 1.4rem; margin-bottom: 0.7rem;
}
.card-accent { border-left: 3px solid #7c3aed; }
.break-row { opacity: 0.4; font-style: italic; }

.time-tag { color: #6b7280; font-size: 0.82rem; }
.subject-name { font-weight: 600; font-size: 0.95rem; color: #e8eaf0; }

.urgency-high   { color: #f87171; font-weight: 600; }
.urgency-medium { color: #fbbf24; font-weight: 600; }
.urgency-low    { color: #34d399; font-weight: 600; }

.free-slot {
    background: #052e16; border: 1px solid #166534;
    border-radius: 8px; padding: 6px 14px;
    color: #4ade80; font-size: 0.85rem; margin: 4px 0;
}

.chat-user {
    background: #1e1b4b; border-radius: 12px 12px 4px 12px;
    padding: 10px 16px; margin: 8px 0 8px auto;
    max-width: 75%; color: #c4b5fd; font-size: 0.9rem;
}
.chat-bot {
    background: #161b27; border: 1px solid #252d3d;
    border-radius: 12px 12px 12px 4px;
    padding: 10px 16px; margin: 8px auto 8px 0;
    max-width: 85%; color: #e8eaf0; font-size: 0.9rem;
}

.day-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem; font-weight: 700;
    color: #7c3aed; margin-bottom: 0.6rem;
}

.metric-box {
    background: #161b27; border: 1px solid #252d3d;
    border-radius: 10px; padding: 1rem; text-align: center;
}
.metric-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem; font-weight: 700; color: #a78bfa;
}
.metric-label { color: #6b7280; font-size: 0.8rem; margin-top: 2px; }

.stButton > button {
    background: #7c3aed !important; color: white !important;
    border: none !important; border-radius: 8px !important; font-weight: 600 !important;
}
.stButton > button:hover { background: #6d28d9 !important; }

.stTabs [data-baseweb="tab-list"] { background: #161b27; border-radius: 8px; }
.stTabs [data-baseweb="tab"] { color: #6b7280; }
.stTabs [aria-selected="true"] { color: #a78bfa !important; }

hr { border-color: #252d3d; }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## 📅 Smart Timetable")
    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠 Dashboard",
        "📆 Schedule",
        "✅ Assignments",
        "🔍 Free Slots",
        "💬 AI Assistant"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### ⚙️ Gemini API Key")
    api_key = st.text_input("API Key", type="password", placeholder="AIza...",
                            help="Required for AI Assistant tab")
    if api_key:
        os.environ['GEMINI_API_KEY'] = api_key
    st.caption("Get your key at [aistudio.google.com](https://aistudio.google.com)")


if page == "🏠 Dashboard":
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    today_name = datetime.now().strftime('%A')
    st.markdown(f'<div class="page-sub">Today is {datetime.now().strftime("%A, %d %B %Y")}</div>',
                unsafe_allow_html=True)

    conn = get_conn(); c = conn.cursor()
    total_classes  = c.execute("SELECT COUNT(*) FROM schedule WHERE subject NOT IN ('Break','Lunch')").fetchone()[0]
    pending        = c.execute("SELECT COUNT(*) FROM assignments WHERE done=0").fetchone()[0]
    urgent         = c.execute("SELECT COUNT(*) FROM assignments WHERE done=0 AND deadline <= date('now','+3 days')").fetchone()[0]
    today_classes  = c.execute("SELECT COUNT(*) FROM schedule WHERE day=? AND subject NOT IN ('Break','Lunch')", (today_name,)).fetchone()[0]
    conn.close()

    col1, col2, col3, col4 = st.columns(4)
    for col, num, label in [
        (col1, today_classes,  "Today's Classes"),
        (col2, total_classes,  "Total This Week"),
        (col3, pending,        "Pending Tasks"),
        (col4, urgent,         "Urgent (≤3 days)"),
    ]:
        with col:
            st.markdown(f"""<div class="metric-box">
                <div class="metric-number">{num}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown(f'<div class="day-header">📋 {today_name}\'s Schedule</div>', unsafe_allow_html=True)
        conn = get_conn(); c = conn.cursor()
        rows = c.execute('SELECT subject,start,end FROM schedule WHERE day=? ORDER BY start', (today_name,)).fetchall()
        conn.close()
        now = datetime.now().time()
        if rows:
            for subject, start, end in rows:
                is_break   = subject in ('Break', 'Lunch')
                is_current = parse_time(start) <= now <= parse_time(end)
                accent = ' card-accent' if is_current else ''
                dim    = ' break-row'   if is_break   else ''
                now_badge = "&nbsp;&nbsp;<span style='color:#7c3aed;font-size:0.75rem;'>● NOW</span>" if is_current else ""
                st.markdown(f"""<div class="card{accent}{dim}">
                    <span class="time-tag">{start} – {end}</span>
                    <span class="subject-name" style="margin-left:12px">{subject}</span>
                    {now_badge}
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No classes today.")

    with col_r:
        st.markdown('<div class="day-header">⏰ Upcoming Deadlines</div>', unsafe_allow_html=True)
        today = datetime.now().date()
        for _, subject, deadline, priority, done in ui_get_assignments():
            if done: continue
            due       = datetime.strptime(deadline, '%Y-%m-%d').date()
            days_left = (due - today).days
            cls  = 'urgency-high' if days_left <= 3 else 'urgency-medium' if days_left <= 7 else 'urgency-low'
            icon = '🔴' if days_left <= 3 else '🟡' if days_left <= 7 else '🟢'
            st.markdown(f"""<div class="card">
                {icon} <span class="subject-name">{subject}</span><br>
                <span class="time-tag">Due {deadline}</span>
                &nbsp;&nbsp;<span class="{cls}">{days_left}d left</span>
            </div>""", unsafe_allow_html=True)


elif page == "📆 Schedule":
    st.markdown('<div class="page-title">Weekly Schedule</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">View and manage your timetable</div>', unsafe_allow_html=True)

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    tabs = st.tabs(days)
    for tab, day in zip(tabs, days):
        with tab:
            conn = get_conn(); c = conn.cursor()
            rows = c.execute('SELECT subject,start,end FROM schedule WHERE day=? ORDER BY start', (day,)).fetchall()
            conn.close()
            for subject, start, end in rows:
                is_break = subject in ('Break', 'Lunch')
                dim = ' break-row' if is_break else ''
                st.markdown(f"""<div class="card{dim}">
                    <span class="time-tag">{start} – {end}</span>
                    <span class="subject-name" style="margin-left:14px">{subject}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ➕ Add New Event")
    c1, c2, c3, c4 = st.columns([2, 3, 1.5, 1.5])
    with c1: add_day   = st.selectbox("Day", days, key="add_day")
    with c2: add_sub   = st.text_input("Subject", placeholder="e.g. Study Group", key="add_sub")
    with c3: add_start = st.text_input("Start (HH:MM)", placeholder="17:00", key="add_start")
    with c4: add_end   = st.text_input("End (HH:MM)",   placeholder="18:30", key="add_end")

    if st.button("Add Event"):
        if add_sub and add_start and add_end:
            ok, msg = ui_add_event(add_day, add_sub, add_start, add_end)
            if ok: st.success(msg)
            else:  st.error(msg)
        else:
            st.warning("Please fill in all fields.")


elif page == "✅ Assignments":
    st.markdown('<div class="page-title">Assignments</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Track your deadlines and priorities</div>', unsafe_allow_html=True)

    today = datetime.now().date()
    all_rows  = ui_get_assignments()
    pending   = [(i,s,d,p) for i,s,d,p,done in all_rows if not done]
    completed = [(i,s,d,p) for i,s,d,p,done in all_rows if done]

    st.markdown(f"**{len(pending)} pending · {len(completed)} completed**")

    for aid, subject, deadline, priority in pending:
        due       = datetime.strptime(deadline, '%Y-%m-%d').date()
        days_left = (due - today).days
        cls  = 'urgency-high' if days_left <= 3 else 'urgency-medium' if days_left <= 7 else 'urgency-low'
        icon = '🔴' if days_left <= 3 else '🟡' if days_left <= 7 else '🟢'
        col_a, col_b = st.columns([10, 1])
        with col_a:
            st.markdown(f"""<div class="card card-accent">
                {icon} <span class="subject-name">{subject}</span>
                &nbsp;&nbsp;<span class="{cls}">{days_left} days left</span><br>
                <span class="time-tag">Due: {deadline} &nbsp;|&nbsp; Priority: {priority}</span>
            </div>""", unsafe_allow_html=True)
        with col_b:
            if st.button("✓", key=f"done_{aid}", help="Mark as done"):
                ui_mark_done(aid)
                st.rerun()

    if completed:
        with st.expander(f"✅ Completed ({len(completed)})"):
            for _, subject, deadline, _ in completed:
                st.markdown(f"~~{subject}~~ · {deadline}")

    st.markdown("---")
    st.markdown("### ➕ Add Assignment")
    ca, cb, cc = st.columns([3, 2, 2])
    with ca: new_sub  = st.text_input("Subject", key="new_sub")
    with cb: new_date = st.date_input("Deadline", key="new_date")
    with cc: new_pri  = st.selectbox("Priority", ["High","Medium","Low"], key="new_pri")

    if st.button("Add Assignment"):
        if new_sub:
            ui_add_assignment(new_sub, new_date, new_pri)
            st.success(f'"{new_sub}" added!')
            st.rerun()
        else:
            st.warning("Enter a subject name.")

    st.markdown("---")
    st.markdown("### 📚 Suggested Study Plan")
    if st.button("Generate Plan"):
        result = ui_suggest_study_plan()
        st.markdown(f"""<div class="card"><pre style="color:#e8eaf0;background:transparent;white-space:pre-wrap">{result}</pre></div>""",
                    unsafe_allow_html=True)


elif page == "🔍 Free Slots":
    st.markdown('<div class="page-title">Free Slots</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Find open time in your schedule</div>', unsafe_allow_html=True)

    selected_day = st.selectbox("Choose a day", ['Monday','Tuesday','Wednesday','Thursday','Friday'])
    slots = ui_find_free_slots(selected_day)
    if slots:
        st.markdown(f"**{len(slots)} free slot(s) on {selected_day}:**")
        for s in slots:
            st.markdown(f'<div class="free-slot">🟢 {s}</div>', unsafe_allow_html=True)
    else:
        st.warning(f"No free slots on {selected_day}.")

    st.markdown("---")
    st.markdown("### 📊 All Week Overview")
    for day in ['Monday','Tuesday','Wednesday','Thursday','Friday']:
        slots = ui_find_free_slots(day)
        c1, c2 = st.columns([2, 5])
        with c1: st.markdown(f"**{day}**")
        with c2:
            if slots:
                pills = " &nbsp; ".join(
                    f'<span style="background:#1e1b4b;color:#a78bfa;border-radius:6px;padding:2px 10px;font-size:0.78rem">{s}</span>'
                    for s in slots)
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.markdown('<span style="color:#6b7280;font-size:0.85rem">Fully booked</span>', unsafe_allow_html=True)


elif page == "💬 AI Assistant":
    st.markdown('<div class="page-title">AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Ask anything about your schedule or assignments</div>', unsafe_allow_html=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if not api_key:
        st.warning("⚠️ Enter your Gemini API key in the sidebar to use the AI Assistant.")
    else:
        
        st.markdown("**Quick questions:**")
        qcols = st.columns(4)
        quick = ["What's on Monday?", "Free slots Wednesday", "What's due soon?", "Suggest a study plan"]
        for col, q in zip(qcols, quick):
            with col:
                if st.button(q, key=f"q_{q}"):
                    st.session_state.chat_history.append(("user", q))
                    with st.spinner("Thinking..."):
                        reply = run_agent(q, verbose=False)
                    st.session_state.chat_history.append(("bot", reply))
                    st.rerun()

        st.markdown("---")

        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f'<div class="chat-user">🧑 {msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bot">🤖 {msg}</div>', unsafe_allow_html=True)

        user_input = st.chat_input("Ask about your schedule, assignments, or free time...")
        if user_input:
            st.session_state.chat_history.append(("user", user_input))
            with st.spinner("Thinking..."):
                reply = run_agent(user_input, verbose=False)
            st.session_state.chat_history.append(("bot", reply))
            st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑 Clear chat"):
                st.session_state.chat_history = []
                st.rerun()
