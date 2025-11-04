# growth_mindset.py
import streamlit as st
import pandas as pd
from datetime import date, timedelta
import random

st.set_page_config(page_title="Growth Mindset", page_icon="Growing Plant", layout="centered")

# Dark mode
dark = st.sidebar.checkbox("Dark Mode", value=False)
if dark:
    st.markdown("<style>body {background-color: #1a1a1a; color: white;}</style>", unsafe_allow_html=True)

st.title("30-Day Growth Mindset Challenge")
st.markdown("---")

# Challenge Tasks (30 Days)
tasks = [
    "Learn one new word", "Read 10 pages", "Do 10 push-ups", "Write 3 things you're grateful for",
    "Meditate 5 minutes", "Drink 8 glasses of water", "No social media for 1 hour", "Help someone",
    "Try a new food", "Walk 5000 steps", "Learn a new skill (5 min)", "Say 'I can' 10 times",
    "Write your goal", "Smile at 3 strangers", "Sleep 8 hours", "No complaints today",
    "Compliment someone", "Organize your desk", "Listen to a podcast", "Draw something",
    "Call a friend", "No sugar today", "Wake up at 6 AM", "Write a journal entry",
    "Do something scary", "Forgive someone", "Say thank you 5 times", "Plan tomorrow",
    "Reflect: What did I learn?", "Celebrate your progress!"
]

# Initialize data
if 'start_date' not in st.session_state:
    st.session_state.start_date = None
if 'completed' not in st.session_state:
    st.session_state.completed = [False] * 30
if 'streak' not in st.session_state:
    st.session_state.streak = 0

# Start Challenge
if st.session_state.start_date is None:
    if st.button("Start 30-Day Challenge!"):
        st.session_state.start_date = date.today()
        st.success("Challenge started today!")
        st.rerun()

else:
    start = st.session_state.start_date
    today = date.today()
    day_num = (today - start).days + 1

    if day_num > 30:
        st.balloons()
        st.success("**Congratulations! You completed the 30-Day Challenge!**")
    else:
        st.info(f"**Day {day_num} of 30**")

        # Today's Task
        task = tasks[day_num - 1]
        st.markdown(f"### Today's Task: **{task}**")

        # Mark Complete
        completed_today = st.checkbox("I did it!", value=st.session_state.completed[day_num - 1])
        st.session_state.completed[day_num - 1] = completed_today

        # Update Streak
        if completed_today:
            if day_num == 1 or st.session_state.completed[day_num - 2]:
                st.session_state.streak = st.session_state.streak + 1 if day_num > 1 else 1
            else:
                st.session_state.streak = 1
        else:
            if day_num > 1 and not st.session_state.completed[day_num - 2]:
                st.session_state.streak = 0

        # Progress
        progress = sum(st.session_state.completed) / 30
        st.progress(progress)
        st.write(f"**Progress: {sum(st.session_state.completed)}/30 days**")

        # Streak
        st.metric("Current Streak", f"{st.session_state.streak} days")

        # Motivational Quote
        quotes = [
            "Growth begins at the end of your comfort zone.",
            "Mistakes are proof that you are trying.",
            "You are stronger than you think.",
            "Every expert was once a beginner.",
            "Believe you can and you're halfway there."
        ]
        st.info(f"**Quote of the Day:**\n> {random.choice(quotes)}")

        # Calendar View
        st.markdown("### Challenge Calendar")
        cols = st.columns(7)
        for i in range(30):
            with cols[i % 7]:
                day = i + 1
                if day < day_num:
                    if st.session_state.completed[i]:
                        st.success(f"**{day}**")
                    else:
                        st.error(f"**{day}**")
                elif day == day_num:
                    st.warning(f"**{day}**")
                else:
                    st.write(f"{day}")

        # Export
        data = []
        for i in range(30):
            d = start + timedelta(days=i)
            data.append({
                "Day": i+1,
                "Date": d.strftime("%Y-%m-%d"),
                "Task": tasks[i],
                "Completed": st.session_state.completed[i]
            })
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False).encode()
        st.download_button("Download Report (CSV)", csv, "growth_report.csv", "text/csv")

st.markdown("---")
st.caption("Daily Growth | 30-Day Challenge | Made with Streamlit")