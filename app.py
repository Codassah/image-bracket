
import streamlit as st
import os
import json
import random

STATE_FILE = "state.json"
IMAGE_FOLDER = "images"

# Load or create state
def load_state():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 2:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    else:
        images = os.listdir(IMAGE_FOLDER)
        images = [img for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
        random.shuffle(images)
        return {
            "round": 1,
            "current_match": 0,
            "bracket": images,
            "winners": []
        }

# Save state
def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

state = load_state()

st.title("🔥 Image Bracket Tournament")

# If winner exists
if len(state["bracket"]) == 1:
    st.header("🏆 Winner!")
    st.image(os.path.join(IMAGE_FOLDER, state["bracket"][0]))
    st.stop()

# Get current match
i = state["current_match"] * 2

# Safety check
if i + 1 >= len(state["bracket"]):
    st.error("Something went wrong with the bracket.")
    st.stop()

img1 = state["bracket"][i]
img2 = state["bracket"][i + 1]

col1, col2 = st.columns(2)

with col1:
    st.image(os.path.join(IMAGE_FOLDER, img1), use_column_width=True)
    if st.button("Vote Left"):
        state["winners"].append(img1)
        state["current_match"] += 1
        save_state(state)
        st.rerun()

with col2:
    st.image(os.path.join(IMAGE_FOLDER, img2), use_column_width=True)
    if st.button("Vote Right"):
        state["winners"].append(img2)
        state["current_match"] += 1
        save_state(state)
        st.rerun()

# Move to next round
if state["current_match"] >= len(state["bracket"]) // 2:
    state["bracket"] = state["winners"]
    state["winners"] = []
    state["current_match"] = 0
    state["round"] += 1
    save_state(state)
    st.rerun()

st.write(f"Round {state['round']}")
st.write(f"Match {state['current_match'] + 1}")
