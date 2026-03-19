import streamlit as st
import os
import json
import random

STATE_FILE = "state.json"
IMAGE_FOLDER = "images"

# 1. Improved Load Function
def load_state():
    # If file exists and isn't empty, load it
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass # If file is corrupted, move to initialization
    
    # Initialize new tournament if file is missing or broken
    if not os.path.exists(IMAGE_FOLDER):
        st.error(f"Folder '{IMAGE_FOLDER}' not found!")
        st.stop()
        
    images = [img for img in os.listdir(IMAGE_FOLDER) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if len(images) < 2:
        st.error("Need at least 2 images to start a tournament!")
        st.stop()
        
    random.shuffle(images)
    return {
        "round": 1,
        "current_pair_idx": 0,
        "bracket": images,
        "winners": []
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# 2. Secure Session State Initialization
if "tournament" not in st.session_state:
    st.session_state.tournament = load_state()

# Short reference for easier typing
state = st.session_state.tournament

st.title("🔥 Image Bracket Tournament")

# 3. Extra Safety Check: Ensure 'bracket' key exists
if "bracket" not in state:
    st.session_state.tournament = load_state()
    st.rerun()

# --- WINNER SCREEN ---
if len(state["bracket"]) == 1:
    st.balloons()
    st.header("🏆 The Ultimate Winner!")
    st.image(os.path.join(IMAGE_FOLDER, state["bracket"][0]), use_container_width=True)
    if st.button("Reset Tournament"):
        if os.path.exists(STATE_FILE): 
            os.remove(STATE_FILE)
        del st.session_state.tournament
        st.rerun()
    st.stop()

# --- TOURNAMENT LOGIC ---
bracket = state["bracket"]
pair_idx = state["current_pair_idx"]
i = pair_idx * 2

# Check if we finished the round
if i >= len(bracket):
    state["bracket"] = state["winners"]
    state["winners"] = []
    state["current_pair_idx"] = 0
    state["round"] += 1
    save_state(state)
    st.rerun()

# --- DISPLAY MATCH ---
img1 = bracket[i]
img2 = bracket[i + 1]

st.subheader(f"Round {state['round']} | Match {pair_idx + 1}")

col1, col2 = st.columns(2)

def handle_vote(winner_img):
    state["winners"].append(winner_img)
    state["current_pair_idx"] += 1
    save_state(state)

with col1:
    st.image(os.path.join(IMAGE_FOLDER, img1), use_container_width=True)
    if st.button(f"Vote Left", key=f"L_{state['round']}_{pair_idx}"):
        handle_vote(img1)
        st.rerun()

with col2:
    st.image(os.path.join(IMAGE_FOLDER, img2), use_container_width=True)
    if st.button(f"Vote Right", key=f"R_{state['round']}_{pair_idx}"):
        handle_vote(img2)
        st.rerun()
