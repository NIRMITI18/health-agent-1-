import streamlit as st
import requests

# --- CONFIGURATION ---
API_BASE_URL = "https://health-care-agent-wyre.onrender.com"

st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="💪",
    layout="centered",
)

st.title("💪 AI Health & Fitness Planner")
st.write("Generate personalized **meal** and **fitness** plans using Gemini AI Agents.")

# --- USER INPUT FORM ---
with st.form("health_form"):
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
    submitted = st.form_submit_button("Generate Plan")

# --- API CALLS ---
def call_api(endpoint, payload):
    try:
        response = requests.post(f"{API_BASE_URL}/{endpoint}", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

# --- PROCESS FORM SUBMISSION ---
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

    st.info("⏳ Generating personalized health recommendations...")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🍽️ Get Meal Plan"):
            result = call_api("meal-plan", payload)
            if result:
                st.success("Meal Plan Generated Successfully!")
                st.markdown(result["meal_plan"])

    with col2:
        if st.button("🏋️ Get Fitness Plan"):
            result = call_api("fitness-plan", payload)
            if result:
                st.success("Fitness Plan Generated Successfully!")
                st.markdown(result["fitness_plan"])

    if st.button("🧠 Get Full Health Plan"):
        result = call_api("full-health-plan", payload)
        if result:
            st.success("Full Health Plan Generated Successfully!")
            st.markdown(result["full_health_plan"])
