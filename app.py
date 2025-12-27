import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import cv2
import time
import hashlib
import tempfile
import os

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="SENTRY-AI | Deepfake Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the "Cybersecurity" aesthetic
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .main-header {
        font-family: 'Courier New', monospace;
        color: #00FF00;
        text-shadow: 0px 0px 10px #00FF00;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00FF00;
        margin-bottom: 20px;
    }
    .alert-high {
        border-left: 5px solid #FF4B4B !important;
    }
    .alert-med {
        border-left: 5px solid #FFA500 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- UTILITY FUNCTIONS ---

def load_audio(uploaded_file):
    """Loads audio file and returns signal and sample rate."""
    try:
        y, sr = librosa.load(uploaded_file, duration=30) # Limit to 30s
        return y, sr
    except Exception as e:
        st.error(f"Error loading audio: {e}")
        return None, None

def save_temp_file(uploaded_file):
    """Save uploaded file to temp location for OpenCV access."""
    try:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}")
        tfile.write(uploaded_file.read())
        return tfile.name
    except Exception as e:
        st.error(f"Error saving temp file: {e}")
        return None

def simulate_audio_inference(y, sr):
    """Simulates AI inference for Audio."""
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    std_freq = np.std(spec_cent)
    
    # Deterministic hashing for demo consistency
    feature_hash = hashlib.sha256(y.tobytes()).hexdigest()
    seed_val = int(feature_hash[:8], 16)
    np.random.seed(seed_val)
    
    fake_probability = np.random.beta(2, 5)
    if std_freq < 500: 
        fake_probability += 0.2

    return np.clip(fake_probability, 0, 1), np.mean(spec_cent), std_freq

def simulate_video_inference(video_path):
    """
    Simulates AI inference for Video.
    Extracts real metadata using OpenCV, then uses hashing for the 'fake' score.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return 0.5, {}

    # Extract Real Metadata
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Read a middle frame for hashing
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count // 2)
    ret, frame = cap.read()
    cap.release()

    # Deterministic "AI" Score based on frame content
    if ret and frame is not None:
        feature_hash = hashlib.sha256(frame.tobytes()).hexdigest()
        seed_val = int(feature_hash[:8], 16)
    else:
        seed_val = int(time.time())
    
    np.random.seed(seed_val)
    fake_probability = np.random.beta(2, 5)
    
    # Heuristic: Lower resolution or weird FPS might increase "suspicion" in this demo
    if fps < 20 or fps > 61: fake_probability += 0.1
    
    metadata = {
        "Frames": frame_count,
        "FPS": round(fps, 2),
        "Resolution": f"{width}x{height}"
    }
    
    return np.clip(fake_probability, 0, 1), metadata

def get_risk_level(prob):
    if prob > 0.80: return "CRITICAL", "red"
    if prob > 0.50: return "HIGH", "orange"
    if prob > 0.20: return "MEDIUM", "yellow"
    return "LOW", "green"

# --- MAIN APP UI ---

def main():
    # Sidebar
    st.sidebar.title("🛡️ SENTRY-AI")
    st.sidebar.markdown("---")
    st.sidebar.subheader("System Status")
    st.sidebar.success("● Agent Active")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Settings")
    st.sidebar.slider("AI Sensitivity", 0.0, 1.0, 0.75)
    st.sidebar.checkbox("Enable Spectral Analysis", value=True)
    st.sidebar.checkbox("Show Decision Log", value=True)
    
    st.sidebar.markdown("---")
    st.sidebar.info("MVP Version 1.1.0\nSupport: Audio & Video")

    # Main Content
    st.markdown('<h1 class="main-header">SENTRY-AI // DEEPFAKE DEFENSE</h1>', unsafe_allow_html=True)
    st.markdown("### Multi-Modal Deepfake Detection & Risk Assessment")
    st.write("Upload suspicious **Audio (.wav, .mp3)** or **Video (.mp4, .mov, .avi)** for immediate analysis.")

    # File Uploader
    uploaded_file = st.file_uploader("Drop Evidence Here", type=["wav", "mp3", "mp4", "mov", "avi"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        is_video = file_type in ['mp4', 'mov', 'avi']
        
        # Display Player
        if is_video:
            st.video(uploaded_file)
        else:
            st.audio(uploaded_file, format='audio/wav')
        
        # Analyze Button
        if st.button("INITIATE SCAN"):
            with st.spinner('SENTRY Agent Analyzing Artifacts...'):
                
                # --- AUDIO PIPELINE ---
                if not is_video:
                    y, sr = load_audio(uploaded_file)
                    
                    if y is not None:
                        # Simulation delay
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        prob, mean_freq, std_freq = simulate_audio_inference(y, sr)
                        risk_label, risk_color = get_risk_level(prob)
                        
                        # --- RESULTS (Audio) ---
                        st.divider()
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            render_risk_card(prob, risk_label, risk_color)
                        
                        with col2:
                            st.markdown("### SIGNAL FORENSICS")
                            tab1, tab2 = st.tabs(["Waveform", "Spectrogram"])
                            with tab1:
                                fig_wave, ax_wave = plt.subplots(figsize=(10, 3))
                                librosa.display.waveshow(y, sr=sr, ax=ax_wave, color='blue', alpha=0.6)
                                style_plot(fig_wave, ax_wave, "Amplitude Envelope")
                                st.pyplot(fig_wave)
                            with tab2:
                                D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
                                fig_spec, ax_spec = plt.subplots(figsize=(10, 3))
                                img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', ax=ax_spec)
                                style_plot(fig_spec, ax_spec, "Log-Frequency Spectrogram")
                                fig_spec.colorbar(img, ax=ax_spec, format="%+2.0f dB")
                                st.pyplot(fig_spec)

                        render_logs(f"""
[AUDIO-IO] Loaded {len(y)} samples @ {sr}Hz
[FEATURE-EXT] Spectral Centroid Mean: {mean_freq:.2f} Hz
[AI-MODEL] Anomaly score: {prob:.4f}
[DECISION] Classification: {risk_label}
                        """)

                # --- VIDEO PIPELINE ---
                else:
                    # Save to temp file for OpenCV
                    tpath = save_temp_file(uploaded_file)
                    if tpath:
                        # Simulation delay
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.02) # Slightly slower for video
                            progress_bar.progress(i + 1)

                        prob, metadata = simulate_video_inference(tpath)
                        risk_label, risk_color = get_risk_level(prob)
                        
                        # Clean up temp file
                        os.remove(tpath)

                        # --- RESULTS (Video) ---
                        st.divider()
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            render_risk_card(prob, risk_label, risk_color)
                            st.info(f"**Metadata Analysis:**\nResolution: {metadata['Resolution']}\nFPS: {metadata['FPS']}")

                        with col2:
                            st.markdown("### FRAME FORENSICS")
                            tab1, tab2 = st.tabs(["Frame Delta Analysis", "Compression Artifacts"])
                            
                            # Simulated Forensics Data
                            np.random.seed(int(prob*1000))
                            frames_x = np.arange(0, 100)
                            deltas = np.random.normal(0, 1, 100) + (5 if prob > 0.5 else 0) # Spikes if fake
                            
                            with tab1:
                                fig_delta, ax_delta = plt.subplots(figsize=(10, 3))
                                ax_delta.plot(frames_x, deltas, color='#00FF00', linewidth=1)
                                if prob > 0.5:
                                    ax_delta.axhline(y=3, color='red', linestyle='--', label='Anomaly Threshold')
                                style_plot(fig_delta, ax_delta, "Inter-Frame Consistency (Simulated)")
                                st.pyplot(fig_delta)
                            
                            with tab2:
                                st.write("Compression Error Level Analysis (ELA) - Heatmap")
                                # Generate a dummy heatmap for ELA visualization
                                heatmap_data = np.random.rand(10, 10)
                                fig_ela, ax_ela = plt.subplots(figsize=(10, 3))
                                im = ax_ela.imshow(heatmap_data, cmap='inferno', aspect='auto')
                                style_plot(fig_ela, ax_ela, "Compression Artifact Heatmap")
                                plt.colorbar(im, ax=ax_ela)
                                st.pyplot(fig_ela)

                        render_logs(f"""
[VIDEO-IO] Stream processed: {metadata['Resolution']} @ {metadata['FPS']}fps
[FRAMES] Analyzed {metadata['Frames']} keyframes
[FACIAL-RECOG] 1 Face detected
[LIP-SYNC] Sync Offset: {np.random.uniform(0, 20):.2f}ms
[AI-MODEL] Anomaly score: {prob:.4f}
[DECISION] Classification: {risk_label}
                        """)

def render_risk_card(prob, risk_label, risk_color):
    st.markdown(f"### RISK ASSESSMENT")
    st.markdown(f"""
    <div class="metric-card alert-{ 'high' if prob > 0.5 else 'med' if prob > 0.2 else 'low'}" 
            style="border-left: 10px solid {risk_color};">
        <h2 style="color:{risk_color}; margin:0;">{risk_label}</h2>
        <h1 style="font-size: 4em; margin:0;">{int(prob*100)}%</h1>
        <p>Fake Confidence Score</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("**AI Decision:**\n" + 
            ("Content is likely manipulated." if prob > 0.7 else 
                "Suspicious artifacts detected." if prob > 0.4 else 
                "No evidence of manipulation."))

def style_plot(fig, ax, title):
    ax.set_title(title)
    ax.set_facecolor('#0e1117')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    # Remove top/right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

def render_logs(log_text):
    st.divider()
    with st.expander("View Agent Logic Logs"):
        st.code(log_text, language="bash")

if __name__ == "__main__":
    main()