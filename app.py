import streamlit as st
import time
import random
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="Innovative Snake Game PRO", layout="wide")

# 1. --- STYLES & CUSTOMIZATION ---
st.title("⚡ Modern AI-Powered Snake Game (Pro Edition)")
st.sidebar.header("🎨 Environment Customization")

# Visual themes selection
environment = st.sidebar.selectbox("Select Theme Zone", ["Futuristic Neon", "Retro Dark", "Desert Hazard"])
snake_color = st.sidebar.color_picker("Choose Snake Skin Color", "#00FF00")
base_speed = st.sidebar.slider("Set Base Game Speed (Lower is faster)", 0.05, 0.4, 0.15, step=0.05)

# Initialize Session States
if 'snake' not in st.session_state:
    st.session_state.snake = [[10, 10], [10, 11], [10, 12]]
    st.session_state.direction = "UP"
    st.session_state.food = [random.randint(2, 17), random.randint(2, 17)]
    st.session_state.powerup = [random.randint(2, 17), random.randint(2, 17)]
    st.session_state.powerup_active = False
    st.session_state.powerup_timer = 0
    st.session_state.obstacle = [random.randint(3, 16), random.randint(3, 16)]
    st.session_state.obstacle_dir = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.logs = []

def reset_game():
    st.session_state.snake = [[10, 10], [10, 11], [10, 12]]
    st.session_state.direction = "UP"
    st.session_state.food = [random.randint(2, 17), random.randint(2, 17)]
    st.session_state.powerup = [random.randint(2, 17), random.randint(2, 17)]
    st.session_state.powerup_active = False
    st.session_state.powerup_timer = 0
    st.session_state.obstacle = [random.randint(3, 16), random.randint(3, 16)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = True

if st.sidebar.button("🎮 Launch / Reset Simulation"):
    reset_game()

# 2. --- CONTROLS GUI ---
st.write("### 🕹️ Real-time Controls")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⬅️ TURN LEFT") and st.session_state.direction != "RIGHT": st.session_state.direction = "LEFT"
with col2:
    if st.button("⬆️ TURN UP") and st.session_state.direction != "DOWN": st.session_state.direction = "UP"
with col3:
    if st.button("⬇️ TURN DOWN") and st.session_state.direction != "UP": st.session_state.direction = "DOWN"
with col4:
    if st.button("➡️ TURN RIGHT") and st.session_state.direction != "LEFT": st.session_state.direction = "RIGHT"

# 3. --- CORE GAME ENGINE ---
grid_size = 20
current_speed = base_speed

if st.session_state.powerup_active:
    current_speed = base_speed + 0.15
    st.session_state.powerup_timer -= 1
    if st.session_state.powerup_timer <= 0:
        st.session_state.powerup_active = False

if st.session_state.game_started and not st.session_state.game_over:
    st.session_state.obstacle[1] += st.session_state.obstacle_dir
    if st.session_state.obstacle[1] >= grid_size - 2 or st.session_state.obstacle[1] <= 1:
        st.session_state.obstacle_dir *= -1

    head = st.session_state.snake[0].copy()
    if st.session_state.direction == "UP": head[0] -= 1
    elif st.session_state.direction == "DOWN": head[0] += 1
    elif st.session_state.direction == "LEFT": head[1] -= 1
    elif st.session_state.direction == "RIGHT": head[1] += 1

    if (head[0] < 0 or head[0] >= grid_size or head[1] < 0 or head[1] >= grid_size or 
        head in st.session_state.snake or head == st.session_state.obstacle):
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, head)
        if head == st.session_state.food:
            st.session_state.score += 10
            st.session_state.food = [random.randint(1, grid_size-2), random.randint(1, grid_size-2)]
        elif head == st.session_state.powerup:
            st.session_state.powerup_active = True
            st.session_state.powerup_timer = 20
            st.session_state.powerup = [random.randint(1, grid_size-2), random.randint(1, grid_size-2)]
        else:
            st.session_state.snake.pop()

    st.session_state.logs.append({
        "Head_X": head[0], "Head_Y": head[1], 
        "Target_X": st.session_state.food[0], "Target_Y": st.session_state.food[1],
        "Obstacle_X": st.session_state.obstacle[0], "Obstacle_Y": st.session_state.obstacle[1],
        "Score": st.session_state.score,
        "PowerUp_Active": st.session_state.powerup_active
    })

# 4. --- VISUAL DISPLAY SURFACE ---
bg_color = "#050508" if environment == "Futuristic Neon" else ("black" if environment == "Retro Dark" else "#2b1d0c")
grid_html = f'<div style="grid-template-columns: repeat({grid_size}, 18px); display: grid; background-color: {bg_color}; padding: 12px; border: 3px solid #444; border-radius: 12px; width: fit-content; margin: auto;">'

for r in range(grid_size):
    for c in range(grid_size):
        current_pos = [r, c]
        if current_pos in st.session_state.snake:
            color = "#FFF" if current_pos == st.session_state.snake[0] else snake_color
            grid_html += f'<div style="width: 16px; height: 16px; background-color: {color}; margin: 1px; border-radius: 4px; box-shadow: 0 0 5px {snake_color};"></div>'
        elif current_pos == st.session_state.food:
            grid_html += '<div style="width: 16px; height: 16px; background-color: #FF3333; margin: 1px; border-radius: 50%; box-shadow: 0 0 8px #FF3333;"></div>'
        elif current_pos == st.session_state.powerup and not st.session_state.powerup_active:
            grid_html += '<div style="width: 16px; height: 16px; background-color: #33CCFF; margin: 1px; border-radius: 2px; box-shadow: 0 0 8px #33CCFF;"></div>'
        elif current_pos == st.session_state.obstacle:
            grid_html += '<div style="width: 16px; height: 16px; background-color: #FFA500; margin: 1px; border-radius: 4px; clip-path: polygon(50% 0%, 0% 100%, 100% 100%);"></div>'
        else:
            grid_html += '<div style="width: 16px; height: 16px; background-color: #1a1a24; margin: 1px; border-radius: 1px;"></div>'
grid_html += '</div>'

main_col, side_col = st.columns([2, 1])

with main_col:
    st.markdown(grid_html, unsafe_allow_html=True)
    hud_col1, hud_col2 = st.columns(2)
    hud_col1.metric("Score Potential", f"{st.session_state.score} PTS")
    hud_col2.metric("Matrix Engine Speed", f"{round(1/current_speed, 1)} FPS")
    
    if st.session_state.powerup_active:
        st.info(f"🛡️ TIME WARP ACTIVE: Speed stabilized. Remaining: {st.session_state.powerup_timer} frames.")
    if not st.session_state.game_started:
        st.warning("⚡ Engine Offline: Click 'Launch / Reset Simulation' on the sidebar panel.")
    elif st.session_state.game_over:
        st.error("🚨 CRITICAL COLLISION: Simulation terminated. Reset via sidebar.")

# 5. --- NEURAL AI COACH ANALYTICS ---
with side_col:
    st.subheader("🤖 Neural AI Coach Analytics")
    if st.session_state.game_started and len(st.session_state.snake) > 0:
        head_now = st.session_state.snake[0]
        obs_now = st.session_state.obstacle
        
        st.write("---")
        st.write("**📡 Live Hazard Telemetry:**")
        distance_to_obstacle = abs(head_now[0] - obs_now[0]) + abs(head_now[1] - obs_now[1])
        
        if distance_to_obstacle <= 3:
            st.error(f"🚨 EVASIVE MANEUVER REQUIRED! Moving hazard is only {distance_to_obstacle} blocks away!")
        elif head_now[0] < 3 or head_now[0] > grid_size - 4 or head_now[1] < 3 or head_now[1] > grid_size - 4:
            st.warning("⚠️ WALL PROXIMITY ALERT: Core grid boundaries close. Plan turns.")
        else:
            st.success("🎯 OPTIMAL SECTOR: Area safe. Move towards the Target Core (Red dot).")

        if st.session_state.logs:
            st.write("**📊 Historical Deep Learning Logs:**")
            df = pd.DataFrame(st.session_state.logs[-4:])
            st.dataframe(df[["Head_X", "Head_Y", "Target_X", "Obstacle_X", "PowerUp_Active"]], use_container_width=True)
    else:
        st.info("Awaiting telemetry stream... Start game to feed neural network.")

if st.session_state.game_started and not st.session_state.game_over:
    time.sleep(current_speed)
    st.rerun()
