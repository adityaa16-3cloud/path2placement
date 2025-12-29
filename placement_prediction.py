import streamlit as st
import pickle
import numpy as np

# Page config
st.set_page_config(
    page_title="Placement Prediction System",
    layout="centered"
)

# Title
st.title("🎯 Placement Prediction System")
st.markdown("Predict whether a student is likely to get placed based on academic and skill factors.")

# Load trained model
with open("models/placement_model.pkl", "rb") as f:
    model = pickle.load(f)

# ---- INPUT SECTION ----
st.subheader("📌 Enter Student Details")

cgpa = st.number_input("CGPA (0–10)", min_value=0.0, max_value=10.0, value=7.0)
internships = st.number_input("Number of Internships", min_value=0, max_value=10, value=1)
projects = st.number_input("Number of Projects", min_value=0, max_value=10, value=2)
aptitude = st.slider("Aptitude Score (0–100)", 0, 100, 70)
technical_skills = st.slider("Technical Skills (1–5)", 1, 5, 3)
communication_skills = st.slider("Communication Skills (1–5)", 1, 5, 3)
backlogs = st.number_input("Number of Backlogs", min_value=0, max_value=10, value=0)

# ---- PREDICTION ----
if st.button("🔮 Predict Placement"):
    input_data = np.array([
        cgpa,
        internships,
        projects,
        aptitude,
        technical_skills,
        communication_skills,
        backlogs
    ]).reshape(1, -1)

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] * 100

    if prediction == 1:
        st.success(f"✅ Student is likely to be PLACED ({probability:.2f}%)")
    else:
        st.error(f"❌ Student is NOT likely to be placed ({probability:.2f}%)")
