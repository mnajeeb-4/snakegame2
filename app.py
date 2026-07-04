import streamlit as st
import time
import random
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="Innovative Snake Game", layout="wide")

# 1. --- STYLES & CUSTOMIZATION ---
st.title("🐍 Innovative Snake Game with AI Coach")
st.sidebar.header("🎨 Snake Customization")

# Skin color customization
snake_color = st.sidebar.color_picker("Choose Snake Skin Color", "#00FF00")
environment = st.sidebar.selectbox("Select Environment Theme", ["Futuristic Neon", "Retro Dark", "Desert Hazard"])

# Difficulty / Speed
speed_choice = st.sidebar.slider("Game Speed (Difficulty)", 0.1, 0.5, 0.2, step=0.1)

# Initialize Session States for Game Loop
if 'snake' not in st.session_state:
    st.session_state.snake = [[10, 10], [10, 11], [10, 12]]
    st.session_state.direction = "UP"
if 'food' not in st.session_state:
    st.session_state.food = [random.randint(2, 18), random.randint(2, 18)]
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_started' not in st.session_state:
    st.session_state.game_started = False # Game shuru mein ruka rahega
if 'logs' not in st.session_state:
    st.session_state.logs = [] 

# Start / Reset Game Function
def reset_game():
    st.session_state.snake = [[10, 10], [10, 11], [10, 12]]
    st.session_state.direction = "UP"
    st.session_state.food = [random.randint(2, 18), random.randint(2, 18)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.game_started = True # Button dabane par start hoga

if st.sidebar.button("▶️ Start / Reset Game"):
    reset_game()

# 2. --- CONTROLS GUI ---
st.write("### 🎮 Controls")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⬅️ LEFT"): st.session_state.direction = "LEFT"
with col2:
    if st.button("⬆️ UP"): st.session_state.direction = "UP"
with col3:
    if st.button("⬇️ DOWN"): st.session_state.direction = "DOWN"
with col4:
    if st.button("➡️ RIGHT"): st.session_state.direction = "RIGHT"

# 3. --- GAME ENGINE & LOGIC ---
grid_size = 20

# Game sirf tabhi chalega jab game_started True ho aur game_over False ho
if st.session_state.game_started and not st.session_state.game_over:
    head = st.session_state.snake[0].copy()
    
    if st.session_state.direction == "UP": head[0] -= 1
    elif st.session_state.direction == "DOWN": head[0] += 1
    elif st.session_state.direction == "LEFT": head[1] -= 1
    elif st.session_state.direction == "RIGHT": head[1] += 1

    if head[0] < 0 or head[0] >= grid_size or head[1] < 0 or head[1] >= grid_size or head in st.session_state.snake:
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, head)
        
        if head == st.session_state.food:
            st.session_state.score += 10
            st.session_state.food = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]
        else:
            st.session_state.snake.pop()

    st.session_state.logs.append({
        "Head_X": head[0], "Head_Y": head[1], 
        "Food_X": st.session_state.food[0], "Food_Y": st.session_state.food[1],
        "Score": st.session_state.score
    })

# 4. --- RENDER GRID GUI ---
bg_color = "black" if environment == "Retro Dark" else "#0e1117"
grid_html = f'<div style="grid-template-columns: repeat({grid_size}, 15px); display: grid; background-color: {bg_color}; padding: 10px; border-radius: 10px; width: fit-content; margin: auto;">'

for r in range(grid_size):
    for c in range(grid_size):
        if [r, c] in st.session_state.snake:
            grid_html += f'<div style="width: 13px; height: 13px; background-color: {snake_color}; margin: 1px; border-radius: 3px;"></div>'
        elif [r, c] == st.session_state.food:
            grid_html += '<div style="width: 13px; height: 13px; background-color: red; margin: 1px; border-radius: 50%;"></div>'
        else:
            grid_html += '<div style="width: 13px; height: 13px; background-color: #333; margin: 1px;"></div>'
grid_html += '</div>'

# Display Grid & Metrics
main_col, side_col = st.columns([2, 1])

with main_col:
    st.markdown(grid_html, unsafe_allow_html=True)
    st.write(f"### Current Score: {st.session_state.score}")
    
    if not st.session_state.game_started:
        st.info("💡 Please click '▶️ Start / Reset Game' in the sidebar to begin playing!")
    elif st.session_state.game_over:
        st.error("💥 GAME OVER! Border or Self Collision occurred.")

# 5. --- AI COACH REAL-TIME ANALYSIS ---
with side_col:
    st.subheader("🤖 AI Coach Insights")
    if st.session_state.game_started and len(st.session_state.snake) > 0:
        head_now = st.session_state.snake[0]
        
        st.write("**Real-time Analysis:**")
        if head_now[0] < 2 or head_now[0] > grid_size - 3 or head_now[1] < 2 or head_now[1] > grid_size - 3:
            st.warning("⚠️ Danger: You are too close to the wall! Change direction soon.")
        else:
            st.success("✅ Path Clear: Move freely toward the red food target.")
            
        if st.session_state.logs:
            st.write("**Performance Tracking Logs:**")
            df = pd.DataFrame(st.session_state.logs[-5:])
            st.dataframe(df, use_container_width=True)
    else:
        st.write("Waiting for game to start...")

# Auto-refresh loop sirf tab chalega jab game start ho chuka ho aur khatam na hua ho
if st.session_state.game_started and not st.session_state.game_over:
    time.sleep(speed_choice)
    st.rerun()
