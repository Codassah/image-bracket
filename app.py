import streamlit as st
import os
import json
import random

STATE_FILE = "state.json"
IMAGE_FOLDER = "images"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    
    # Initialize new tournament
    images = [img for img in os.listdir(IMAGE_FOLDER) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(images)
    return {
        "round": 1,
        "current_pair_idx": 0, # Index of the pair (0, 1, 2...)
        "bracket": images,
        "winners": []
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# Initialize Session State
if "tournament" not in st.session_state:
    st.session_state.tournament = load_state()

state = st.session_state.tournament

st.title("🔥 Image Bracket Tournament")

# --- WINNER SCREEN ---
if len(state["bracket"]) == 1:
    st.balloons()
    st.header("🏆 The Ultimate Winner!")
    st.image(os.path.join(IMAGE_FOLDER, state["bracket"][0]), use_container_width=True)
    if st.button("Reset Tournament"):
        if os.path.exists(STATE_FILE): os.remove(STATE_FILE)
        st.rerun()
    st.stop()

# --- TOURNAMENT LOGIC ---
bracket = state["bracket"]
pair_idx = state["current_pair_idx"]
i = pair_idx * 2

# Check if we have finished all pairs in the current round
if i >= len(bracket):
    # Transition to next round
    state["bracket"] = state["winners"]
    state["winners"] = []
    state["current_pair_idx"] = 0
    state["round"] += 1
    save_state(state)
    st.rerun()

# Display Current Match
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
    if st.button(f"Vote for Left", key="btn1"):
        handle_vote(img1)
        st.rerun()

with col2:
    st.image(os.path.join(IMAGE_FOLDER, img2), use_container_width=True)
    if st.button(f"Vote for Right", key="btn2"):
        handle_vote(img2)
        st.rerun()

# Progress Bar (Optional but cool)
progress = pair_idx / (len(bracket) / 2)
st.progress(progress)
