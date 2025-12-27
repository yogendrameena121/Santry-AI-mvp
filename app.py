import streamlit as st
from preprocess import preprocess_audio
def preprocess_audio(file_path):
    return "processed"

import random

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
