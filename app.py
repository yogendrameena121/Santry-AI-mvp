import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# App Configuration
st.set_page_config(page_title="Virtual Physics Lab", layout="wide")

st.title("⚛️ Interactive Physics Explorer")
st.sidebar.title("Select a Concept")
concept = st.sidebar.selectbox("Choose a simulation:", ["Projectile Motion", "Simple Harmonic Motion"])

# --- PROJECTILE MOTION ---
if concept == "Projectile Motion":
    st.header("1. Projectile Motion")
    st.write("Explore how launch angle and velocity affect the trajectory of an object.")

    # Sidebar Controls
    st.sidebar.subheader("Parameters")
    v0 = st.sidebar.slider("Initial Velocity (m/s)", 1.0, 100.0, 50.0)
    angle_deg = st.sidebar.slider("Launch Angle (degrees)", 0.0, 90.0, 45.0)
    g = st.sidebar.select_slider("Gravity (m/s²)", options=[1.6, 3.7, 9.8, 24.8], value=9.8, 
                                 help="Moon: 1.6, Mars: 3.7, Earth: 9.8, Jupiter: 24.8")

    # Physics Calculations
    angle_rad = np.radians(angle_deg)
    t_flight = (2 * v0 * np.sin(angle_rad)) / g
    t_range = np.linspace(0, t_flight, num=200)
    
    x = v0 * t_range * np.cos(angle_rad)
    y = (v0 * t_range * np.sin(angle_rad)) - (0.5 * g * t_range**2)

    # Metrics
    max_range = (v0**2 * np.sin(2 * angle_rad)) / g
    max_height = (v0**2 * (np.sin(angle_rad))**2) / (2 * g)

    col1, col2 = st.columns(2)
    col1.metric("Max Range", f"{max_range:.2f} m")
    col2.metric("Max Height", f"{max_height:.2f} m")

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Trajectory', line=dict(color='firebrick', width=4)))
    fig.update_layout(xaxis_title="Distance (m)", yaxis_title="Height (m)", height=500)
    st.plotly_chart(fig, use_container_width=True)

# --- SIMPLE HARMONIC MOTION ---
elif concept == "Simple Harmonic Motion":
    st.header("2. Simple Pendulum")
    st.write("Visualize the displacement of a pendulum over time.")

    # Sidebar Controls
    L = st.sidebar.slider("Length of String (m)", 0.1, 5.0, 1.0)
    A = st.sidebar.slider("Amplitude (Initial Angle in degrees)", 1.0, 20.0, 10.0)
    t_max = st.sidebar.slider("Time Duration (s)", 5, 30, 10)

    # Physics Calculations
    g = 9.81
    omega = np.sqrt(g / L) # Angular frequency
    T = 2 * np.pi * np.sqrt(L / g) # Period
    
    t = np.linspace(0, t_max, 500)
    theta = A * np.cos(omega * t) # Simplified small-angle approximation

    st.metric("Period (T)", f"{T:.2f} seconds")

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=theta, mode='lines', name='Angular Displacement'))
    fig.update_layout(xaxis_title="Time (s)", yaxis_title="Angle (degrees)", height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.info("Note: This simulation uses the small-angle approximation $sin(\\theta) \\approx \\theta$.")