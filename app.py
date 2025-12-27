import streamlit as st
import random

# -----------------------------
# Preprocessing (inline to avoid import errors)
# -----------------------------
def preprocess_audio(file):
    # MVP placeholder preprocessing
    return "processed_audio"

# -----------------------------
# Agentic Decision Engine
# -----------------------------
def decision_logic(label, confidence):
    if label == "Deepfake" and confidence >= 80:
        risk = "HIGH"
        recommendation = "Do not trust source. Verify identity immediately."
    elif confidence >= 60:
        risk = "MEDIUM"
        recommendation = "Secondary verification recommended."
    else:
        risk = "LOW"
        recommendation = "Likely authentic."
    return risk, recommendation

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="SENTRY-AI MVP", layout="centered")

st.title("SENTRY-AI MVP")
st.subheader("AI + Cybersecurity Deepfake Detection (Offline Prototype)")

st.write(
    "Upload an audio file to analyze whether it is **Real or Deepfake** "
    "and receive a cybersecurity risk assessment."
)

uploaded_file = st.file_uploader(
    "Upload Audio File",
    type=["wav", "mp3"]
)

if uploaded_file is not None:
    st.audio(uploaded_file)

    with st.spinner("Analyzing audio offline..."):
        preprocess_audio(uploaded_file)

        # Simulated AI prediction (valid for hackathon MVP)
        confidence = random.uniform(65, 95)
        label = "Deepfake" if confidence > 75 else "Real"

        risk, recommendation = decision_logic(label, confidence)

    st.success(f"Detection Result: {label}")
    st.write(f"Confidence Score: {confidence:.2f}%")
    st.write(f"Risk Level: {risk}")
    st.warning(f"Recommendation: {recommendation}")

st.markdown("---")
st.caption(
    "This is a hackathon MVP demonstrating an edge-based, agentic AI system "
    "for deepfake detection and cybersecurity decision support."
)
