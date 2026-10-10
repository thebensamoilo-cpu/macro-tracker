import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Pocket Macro Tracker", page_icon="🎯", layout="centered")

# Configure Gemini API using Streamlit secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

if "calories" not in st.session_state:
    st.session_state.calories = 0
if "protein" not in st.session_state:
    st.session_state.protein = 0
if "logs" not in st.session_state:
    st.session_state.logs = []

st.title("📱 Local Macro Tracker")
st.write("Goal: **2500 kcal** | **80g - 110g Protein**")

col1, col2 = st.columns(2)
col1.metric("Calories", f"{st.session_state.calories} / 2500 kcal")
col2.metric("Protein", f"{st.session_state.protein} / 110g")

st.divider()

uploaded_file = st.file_uploader("Upload or take a picture of your food", type=["jpg", "jpeg", "png"])

# Fallback default values
detected_name = "Food Item"
detected_cals = 100
detected_prot = 5

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Captured Meal", use_container_width=True)
    
    # Analyze image with AI
    if "GEMINI_API_KEY" in st.secrets:
        with st.spinner("Analyzing food image with AI..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = """Analyze this food image carefully. 
                1. Identify the dish accurately.
                2. Estimate realistic portions based on visual cues.
                Return ONLY a valid string in this exact format with pipe separators:
                FoodName | Calories | ProteinGrams
                Example: Egg & Avocado Toast | 380 | 18"""
                
                response = model.generate_content([image, prompt])
                parts = response.text.strip().split('|')
                if len(parts) == 3:
                    detected_name = parts[0].strip()
                    detected_cals = int(float(parts[1].strip()))
                    detected_prot = int(float(parts[2].strip()))
            except Exception as e:
                st.error(f"AI Analysis error: {e}")

st.subheader("Log Meal Details")
food_name = st.text_input("Food Name", value=detected_name)
add_cals = st.number_input("Calories", value=detected_cals, step=10)
add_prot = st.number_input("Protein (g)", value=detected_prot, step=5)

if st.button("Add to Daily Total"):
    st.session_state.calories += add_cals
    st.session_state.protein += add_prot
    st.session_state.logs.append(f"{food_name}: {add_cals} kcal, {add_prot}g protein")
    st.success("Successfully logged!")
    st.rerun()

st.divider()
st.subheader("Today's History")
if st.session_state.logs:
    for item in st.session_state.logs:
        st.write(f"- {item}")
else:
    st.write("No meals logged yet today.")

if st.button("Reset Day"):
    st.session_state.calories = 0
    st.session_state.protein = 0
    st.session_state.logs = []
    st.rerun()
