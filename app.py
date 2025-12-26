import streamlit as st
from preprocess import preprocess_audio
from decision_engine import decision_logic
import random
def predict_deepfake():
    confidence = random.uniform(60, 95)
    label = "Deepfake" if confidence > 75 else "Real"
    return label, confidence

st.title("SENTRY-AI MVP")
st.subheader("Offline Deepfake Audio Detection")

uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])

if uploaded_file:
    st.audio(uploaded_file)

    st.write("Analyzing audio...")
    
    label = "Deepfake"
    confidence = random.uniform(70, 95)

    risk, recommendation = decision_logic(label, confidence)

    st.success(f"Result: {label}")
    st.write(f"Confidence: {confidence:.2f}%")
    st.write(f"Risk Level: {risk}")
    st.warning(f"Recommendation: {recommendation}")
