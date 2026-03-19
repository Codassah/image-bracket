import streamlit as st
import os
import json
import random

STATE_FILE = "state.json"
IMAGE_FOLDER = "images"

st.set_page_config(page_title="Image Tournament", layout="centered")
st.title("🔥 Image Bracket Tournament")

# --- 1. PRE-FLIGHT CHECKS ---
if not os.path.exists(IMAGE_FOLDER):
    st.error(f"❌ Folder '{IMAGE_FOLDER}' not found. Please create it and add images.")
    st.stop()

image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if len(image_files) < 2:
    st.error(f"❌ Need at least 2 images in '{IMAGE_FOLDER}'. Found: {len(image_files)}")
    st.stop()

# --- 2. STATE INITIALIZATION ---
def init_tournament():
    random.shuffle(image_files)
    return {
        "round": 1,
        "current_match": 0,
        "bracket": image_files,
        "winners": []
    }

# Load from file or create new
if "tournament" not in st.session_state:
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        try:
            with open(STATE_FILE, "r") as f:
                saved_data = json.load(f)
                # Verify the structure is correct
                if "bracket" in saved_data:
                    st.session_state.tournament = saved_data
                else:
                    st.session_state.tournament = init_tournament()
        except:
            st.session_state.tournament = init_tournament()
    else:
        st.session_state.tournament = init_tournament()

state = st.session_state.tournament

def save_and_rerun():
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
    st.rerun()

# --- 3. WINNER SCREEN ---
if len(state["bracket"]) == 1:
    st.balloons()
    st.header(f"🏆 The Winner: {state['bracket'][0]}")
    st.image(os.path.join(IMAGE_FOLDER, state["bracket"][0]), use_container_width=True)
    if st.button("Restart Tournament"):
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        del st.session_state.tournament
        st.rerun()
    st.stop()

# --- 4. MATCH LOGIC ---
i = state["current_match"] * 2

# Check if we need to advance to the next round
if i >= len(state["bracket"]):
    state["bracket"] = state["winners"]
    state["winners"] = []
    state["current_match"] = 0
    state["round"] += 1
    save_and_rerun()

# Safely get current pair
try:
    img1 = state["bracket"][i]
    img2 = state["bracket"][i+1]
except IndexError:
    # This handles odd-numbered brackets by auto-advancing the last image
    state["winners"].append(state["bracket"][i])
    state["current_match"] += 1
    save_and_rerun()

# --- 5. UI DISPLAY ---
st.write(f"### Round {state['round']} | Match {state['current_match'] + 1}")
progress = i / len(state["bracket"])
st.progress(progress)

col1, col2 = st.columns(2)

with col1:
    st.image(os.path.join(IMAGE_FOLDER, img1), use_container_width=True)
    if st.button("Vote Left", key=f"v1_{img1}", use_container_width=True):
        state["winners"].append(img1)
        state["current_match"] += 1
        save_and_rerun()

with col2:
    st.image(os.path.join(IMAGE_FOLDER, img2), use_container_width=True)
    if st.button("Vote Right", key=f"v2_{img2}", use_container_width=True):
        state["winners"].append(img2)
        state["current_match"] += 1
        save_and_rerun()
