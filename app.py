import streamlit as st
from PIL import Image

st.set_page_config(page_title="Pocket Macro Tracker", page_icon="🎯", layout="centered")

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

if uploaded_file is not None:
    st.image(uploaded_file, caption="Captured Meal", use_container_width=True)
    
    st.subheader("Log Meal Details")
    food_name = st.text_input("Food Name", value="Chicken Wrap")
    add_cals = st.number_input("Calories", value=500, step=50)
    add_prot = st.number_input("Protein (g)", value=40, step=5)
    
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