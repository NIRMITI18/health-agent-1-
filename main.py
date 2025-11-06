import streamlit as st
import requests
import time

# --- HARD-CODED API BASE URL ---
API_BASE_URL = "https://health-care-agent-wyre.onrender.com"

# --- PAGE SETTINGS ---
st.set_page_config(page_title="AI Health & Fitness Planner", page_icon="💪", layout="centered")

# --- HEADER ---
st.title("💪 AI Health & Fitness Planner")
st.markdown("""
Generate personalized **Meal**, **Fitness**, and **Full Health** plans using Gemini AI Agents.  
Just fill out your details and choose what you’d like to generate!
""")

# --- USER INPUT FORM ---
with st.form("user_input_form"):
    name = st.text_input("👤 Name", "John Doe")
    age = st.number_input("🎂 Age", min_value=10, max_value=100, value=25)
    weight = st.number_input("⚖️ Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
    height = st.number_input("📏 Height (cm)", min_value=100.0, max_value=220.0, value=175.0)
    activity_level = st.selectbox(
        "🏃 Activity Level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]
    )
    dietary_preference = st.selectbox(
        "🥗 Dietary Preference",
        ["Balanced", "Vegetarian", "Keto", "Low Carb", "Vegan"]
    )
    fitness_goal = st.selectbox(
        "🎯 Fitness Goal",
        ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility", "Overall Health"]
    )

    submitted = st.form_submit_button("Generate Options")

# --- API CALL HELPER ---
def call_api(endpoint: str, payload: dict):
    """Helper to make API POST requests"""
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"⚠️ Request failed: {e}")
        return None

# --- AFTER FORM SUBMISSION ---
if submitted:
    payload = {
        "name": name,
        "age": age,
        "weight": weight,
        "height": height,
        "activity_level": activity_level,
        "dietary_preference": dietary_preference,
        "fitness_goal": fitness_goal,
    }

    st.success("✅ Input received! Select what you’d like to generate below 👇")

    col1, col2, col3 = st.columns(3)

    # --- MEAL PLAN BUTTON ---
    with col1:
        if st.button("🍽️ Meal Plan"):
            with st.spinner("Generating your Meal Plan... Please wait ⏳"):
                time.sleep(1)
                result = call_api("meal-plan", payload)
            if result:
                st.subheader("🍴 Your Personalized Meal Plan")
                st.markdown(result["meal_plan"])

    # --- FITNESS PLAN BUTTON ---
    with col2:
        if st.button("🏋️ Fitness Plan"):
            with st.spinner("Building your Fitness Routine... 💪"):
                time.sleep(1)
                result = call_api("fitness-plan", payload)
            if result:
                st.subheader("🏃 Your Personalized Fitness Plan")
                st.markdown(result["fitness_plan"])

    # --- FULL PLAN BUTTON ---
    with col3:
        if st.button("🧠 Full Health Plan"):
            with st.spinner("Creating a complete Health Strategy... 🤖"):
                time.sleep(1)
                result = call_api("full-health-plan", payload)
            if result:
                st.subheader("🧩 Your Full Health Plan")
                st.markdown(result["full_health_plan"])
