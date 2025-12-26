import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

st.set_page_config(page_title="Advanced Physics Lab", layout="wide")

st.title("🚀 Advanced Physics: ODE Solvers & 3D Fields")

# Sidebar navigation
menu = st.sidebar.selectbox("Select Simulation", ["Projectile with Air Resistance", "3D Lorentz Force"])

# 1. PROJECTILE MOTION WITH DRAG
if menu == "Projectile with Air Resistance":
    st.header("Projectile Motion with Air Resistance")
    st.write("Solving $m\\ddot{x} = -k|v|\\dot{x}$ and $m\\ddot{z} = -k|v|\\dot{z} - mg$ using Runge-Kutta (RK45).")

    # Parameters
    col1, col2, col3 = st.columns(3)
    v0 = col1.slider("Initial Velocity (m/s)", 10, 100, 50)
    angle = col2.slider("Launch Angle (°)", 0, 90, 45)
    k = col3.slider("Drag Coefficient (k)", 0.0, 0.5, 0.1, help="Higher k = more air resistance")
    
    # ODE System
    def deriv(t, state):
        x, vx, z, vz = state
        g = 9.81
        speed = np.hypot(vx, vz)
        ax = -(k) * speed * vx
        az = -(k) * speed * vz - g
        return [vx, ax, vz, az]

    # Initial conditions
    rad = np.radians(angle)
    u0 = [0, v0 * np.cos(rad), 0, v0 * np.sin(rad)]
    
    # Event to stop when hitting ground
    def hit_ground(t, state): return state[2]
    hit_ground.terminal = True
    hit_ground.direction = -1

    sol = solve_ivp(deriv, (0, 100), u0, events=hit_ground, max_step=0.1)

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sol.y[0], y=sol.y[2], mode='lines', name='With Drag'))
    fig.update_layout(xaxis_title="Distance (m)", yaxis_title="Height (m)")
    st.plotly_chart(fig)

# 2. 3D LORENTZ FORCE
elif menu == "3D Lorentz Force":
    st.header("3D Charged Particle in Magnetic Field")
    st.write("Simulation of a particle spiraling in a magnetic field: $\\vec{F} = q(\\vec{v} \\times \\vec{B})$.")

    # Parameters
    B_strength = st.sidebar.slider("Magnetic Field Strength (B_z)", 0.1, 5.0, 1.0)
    q = st.sidebar.radio("Particle Charge", [1, -1], format_func=lambda x: "Proton (+)" if x==1 else "Electron (-)")
    
    # Physics (Simplified Cyclotron Motion)
    t = np.linspace(0, 20, 1000)
    # If B is in Z direction, particle spirals in XY plane
    x = np.cos(t * B_strength * q)
    y = np.sin(t * B_strength * q)
    z = 0.2 * t # Constant velocity in Z

    # 3. 3D Visualization
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color='blue', width=4))])
    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'), title="Helical Path")
    st.plotly_chart(fig)