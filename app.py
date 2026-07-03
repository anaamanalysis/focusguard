# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime, date

st.set_page_config(page_title="FocusGuard Dashboard", page_icon="🎯")
st.title("🎯 FocusGuard — Focus Dashboard")
if st.button("🔄 Refresh Stats"):
    st.rerun()
# --- Schedule Setup ---
st.sidebar.header("⏰ Your Schedule")
SCHEDULE_FILE = "schedule.json"

if st.sidebar.button("Reset Schedule"):
    if os.path.exists(SCHEDULE_FILE):
        os.remove(SCHEDULE_FILE)

st.sidebar.markdown("**Add Focus Block:**")
start = st.sidebar.time_input("Start time", value=None)
end = st.sidebar.time_input("End time", value=None)
label = st.sidebar.text_input("Label (e.g. Deep Work)")

if st.sidebar.button("Add Block") and start and end and label:
    schedule = []
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE) as f:
            schedule = json.load(f)
    schedule.append({
        "start": start.strftime('%H:%M'),
        "end": end.strftime('%H:%M'),
        "label": label
    })
    with open(SCHEDULE_FILE, 'w') as f:
        json.dump(schedule, f)
    st.sidebar.success(f"Added: {label}")

# --- Load Log Data ---
LOG_FILE = "focus_log.csv"

if not os.path.exists(LOG_FILE):
    st.info("No focus sessions recorded yet. Run detector.py to start monitoring.")
    st.stop()

df = pd.read_csv(LOG_FILE)
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# --- Today's Stats ---
today = date.today().strftime('%Y-%m-%d')
today_df = df[df['date'] == today]

total_distractions = len(today_df)
phone_count = len(today_df[today_df['event_type'] == 'phone_detected'])
desk_count = len(today_df[today_df['event_type'] == 'left_desk'])

# Focus Score — fewer distractions = higher score
focus_score = max(0, 100 - (total_distractions * 5))

# --- Display ---
st.markdown("## 📊 Today's Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🎯 Focus Score", f"{focus_score}/100")
col2.metric("📱 Phone Pickups", phone_count)
col3.metric("🚶 Desk Leaves", desk_count)
col4.metric("⚠️ Total Distractions", total_distractions)

# Motivational message
st.markdown("---")
if focus_score >= 80:
    st.success("🔥 Excellent focus today! You're building a strong habit.")
elif focus_score >= 60:
    st.warning("💪 Good effort! Keep reducing those phone pickups.")
else:
    st.error("😤 Rough session. Tomorrow is a fresh start — you've got this.")

# --- Distraction Timeline ---
if not today_df.empty:
    st.markdown("## ⏱️ Distraction Timeline — Today")
    timeline = today_df.groupby('hour')['event_type'].count().reset_index()
    timeline.columns = ['Hour', 'Distractions']
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(timeline['Hour'], timeline['Distractions'], color='#FF4B4B')
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Distractions")
    ax.set_title("When Were You Most Distracted?")
    st.pyplot(fig)

# --- Weekly Trend ---
st.markdown("## 📈 Weekly Focus Score Trend")
daily = df.groupby('date').size().reset_index(name='distractions')
daily['score'] = (100 - daily['distractions'] * 5).clip(lower=0)

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(daily['date'], daily['score'], 
         marker='o', color='#00CC88', linewidth=2)
ax2.set_ylim(0, 100)
ax2.set_xlabel("Date")
ax2.set_ylabel("Focus Score")
ax2.set_title("Your Focus Score Over Time")
plt.xticks(rotation=45)
st.pyplot(fig2)

st.caption("FocusGuard — built by Anaam Bind Hussain")
