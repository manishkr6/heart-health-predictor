import streamlit as st
import pandas as pd
import joblib

# Load model & preprocessing objects
model = joblib.load("logReg_heart.pkl")
scaler = joblib.load("scaler.pkl")
expected_columns = joblib.load("columns.pkl")

# App Title
st.set_page_config(page_title="Heart Health Predictor ❤️", page_icon="❤️", layout="centered")
st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>❤️ Heart Stroke Risk Prediction</h1>", 
    unsafe_allow_html=True
)
st.markdown("<p style='text-align:center;'>By <b>Manish</b> — Enter your health details to check your risk level</p>", unsafe_allow_html=True)
st.write("---")

# Input Layout
col1, col2 = st.columns(2)

with col1:
    age = st.slider("🧑 Age", 18, 100, 40)
    sex = st.selectbox("⚧ Sex", ["M", "F"])
    chest_pain = st.selectbox("💔 Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])
    resting_bp = st.number_input("💓 Resting BP (mm Hg)", 80, 200, 120)
    cholesterol = st.number_input("🩸 Cholesterol (mg/dL)", 100, 600, 200)

with col2:
    fasting_bs = st.selectbox("🍬 Fasting Blood Sugar > 120 mg/dL", [0, 1])
    resting_ecg = st.selectbox("📊 Resting ECG", ["Normal", "ST", "LVH"])
    max_hr = st.slider("🏃 Max Heart Rate", 60, 220, 150)
    exercise_angina = st.selectbox("🚴 Exercise-Induced Angina", ["Y", "N"])
    oldpeak = st.slider("📉 Oldpeak (ST Depression)", 0.0, 6.0, 1.0)
    st_slope = st.selectbox("📈 ST Slope", ["Up", "Flat", "Down"])

# Prediction Button
st.write("")
if st.button("🔍 Predict", use_container_width=True):
    raw_input = {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,
        "sex_" + sex: 1,
        "ChestPainType_" + chest_pain: 1,
        "RestingECG_" + resting_ecg: 1,
        "ExerciseAngina_" + exercise_angina: 1,
        "ST_Slope_" + st_slope: 1   # fixed typo
    }
    
    input_df = pd.DataFrame([raw_input])
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[expected_columns]

    scaled_input = scaler.transform(input_df)
    prediction = model.predict(scaled_input)[0]

    st.write("---")
    if prediction == 1:
        st.error("⚠️ **High Risk of Heart Disease**\n\nPlease consult a doctor immediately.")
    else:
        st.success("✅ **Low Risk of Heart Disease**\n\nKeep up the healthy lifestyle!")

# Footer
st.markdown(
    "<hr><p style='text-align:center; color: grey;'>© 2025 Manish Kumar Baitha | Built with ❤️ using Streamlit</p>", 
    unsafe_allow_html=True
)
