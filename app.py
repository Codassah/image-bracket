import streamlit as st
import os
import json
import random

STATE_FILE = "state.json"
IMAGE_FOLDER = "images"

st.title("🔥 Image Bracket Tournament")

# --- DEBUG: CHECK FOLDER ---
if not os.path.exists(IMAGE_FOLDER):
    st.error(f"📁 Folder '{IMAGE_FOLDER}' does not exist! Please create it.")
    st.stop()

all_files = os.listdir(IMAGE_FOLDER)
image_files = [img for img in all_files if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

if len(image_files) < 2:
    st.warning(f"Found {len(image_files)} images in '{IMAGE_FOLDER}'. You need at least 2 to play!")
    st.info(f"Files found: {all_files}") # Shows you what is actually there
    st.stop()

# --- STATE MANAGEMENT ---
def load_state():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    
    random.shuffle(image_files)
    return {
        "round": 1,
        "current_pair_idx": 0,
        "bracket": image_files,
        "winners": []
    }

if "tournament" not in st.session_state:
    st.session_state.tournament = load_state()

state = st.session_state.tournament

# --- WINNER CHECK ---
if len(state["bracket"]) == 1:
    st.balloons()
    st.header(f"🏆 Winner: {state['bracket'][0]}")
    st.image(os.path.join(IMAGE_FOLDER, state["bracket"][0]))
    if st.button("Reset"):
        if os.path.exists(STATE_FILE): os.remove(STATE_FILE)
        del st.session_state.tournament
        st.rerun()
    st.stop()

# --- ROUND TRANSITION ---
# If we have finished all pairs, move to next round
if (state["current_pair_idx"] * 2) >= len(state["bracket"]):
    if len(state["winners"]) > 0:
        state["bracket"] = state["winners"]
        state["winners"] = []
        state["current_pair_idx"] = 0
        state["round"] += 1
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
        st.rerun()

# --- DISPLAY MATCH ---
i = state["current_pair_idx"] * 2
img1 = state["bracket"][i]
img2 = state["bracket"][i+1]

st.subheader(f"Round {state['round']} | Match {state['current_pair_idx'] + 1}")

col1, col2 = st.columns(2)

with col1:
    st.image(os.path.join(IMAGE_FOLDER, img1), use_container_width=True)
    if st.button("Vote Left", key=f"L_{img1}"):
        state["winners"].append(img1)
        state["current_pair_idx"] += 1
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
        st.rerun()

with col2:
    st.image(os.path.join(IMAGE_FOLDER, img2), use_container_width=True)
    if st.button("Vote Right", key=f"R_{img2}"):
        state["winners"].append(img2)
        state["current_pair_idx"] += 1
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
        st.rerun()
