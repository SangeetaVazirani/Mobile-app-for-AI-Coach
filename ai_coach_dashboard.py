# Install required packages if not already installed
# !pip install streamlit plyer transformers torch

import streamlit as st
import datetime
import sqlite3
from plyer import notification
from transformers import pipeline

# Initialize sentiment model
sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
label_map = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

# ------------------------- DATABASE SETUP -------------------------
def init_db():
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        name TEXT,
                        event_type TEXT,
                        reminder INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# ------------------------- HEALTH & FITNESS -------------------------
def fitness_tracker():
    IDEAL_STEPS = 8000
    CALORIES_PER_STEP = 0.04

    steps = st.number_input("Enter the number of steps you walked today:", min_value=0)
    if st.button("Track Steps"):
        calories_burnt = steps * CALORIES_PER_STEP
        st.success(f"You burned approximately {calories_burnt:.2f} calories today.")
        if steps < IDEAL_STEPS:
            shortfall = IDEAL_STEPS - steps
            st.warning(f"You walked {shortfall} steps less than the ideal goal of {IDEAL_STEPS}.")
        else:
            st.success("Great job! You met or exceeded your step goal for the day!")

# ------------------------- MENTAL WELLNESS -------------------------
def mental_wellness():
    user_input = st.text_input("How are you feeling today?")
    if st.button("Check Mood"):
        if user_input:
            result = sentiment_model(user_input)[0]
            sentiment = label_map.get(result["label"], "Unknown")
            st.write(f"**Mood detected:** {sentiment} (Confidence: {result['score']:.2f})")
            if sentiment == "Negative":
                st.warning("Consider taking a break, talking to a friend, or going for a walk. 💛")
            elif sentiment == "Neutral":
                st.info("You're feeling neutral. Try something uplifting like music or a hobby. 😊")
            else:
                st.success("Glad to hear you're feeling positive! Keep it up! 🌟")
        else:
            st.error("Please enter your mood to analyze.")

# ------------------------- BIRTHDAYS & ANNIVERSARIES -------------------------
def save_event(event_date, name, event_type, reminder):
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (date, name, event_type, reminder) VALUES (?, ?, ?, ?)",
                   (event_date, name, event_type, reminder))
    conn.commit()
    conn.close()

def birthday_reminder():
    with st.form("event_form"):
        event_date = st.date_input("Select date of event")
        name = st.text_input("Person's Name")
        event_type = st.selectbox("Type of Event", ["Birthday", "Anniversary"])
        reminder_minutes = st.slider("Reminder before event (in minutes)", 0, 1440, 60)
        submit = st.form_submit_button("Save Event")

        if submit:
            save_event(event_date.strftime("%Y-%m-%d"), name, event_type, reminder_minutes)
            st.success(f"{event_type} for {name} saved successfully!")

# ------------------------- MAIN DASHBOARD -------------------------
st.title("🤖 AI-Powered Coach Dashboard")

choice = st.radio("Select Coaching Type:", ("Personal Coaching", "Professional Coaching"))

if choice == "Personal Coaching":
    st.subheader("📋 Personal Coaching Categories")
    option = st.selectbox("Choose a category", ["Select", "Health & Fitness", "Mental Wellness", "Birthdays/Anniversaries Reminder"])

    if option == "Health & Fitness":
        fitness_tracker()

    elif option == "Mental Wellness":
        mental_wellness()

    elif option == "Birthdays/Anniversaries Reminder":
        birthday_reminder()

elif choice == "Professional Coaching":
    st.subheader("📋 Professional Coaching Categories")
    st.write("- Reports generation")
    st.write("- Meetings/Events Reminder")
    st.write("- Project Deadlines Reminder")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
