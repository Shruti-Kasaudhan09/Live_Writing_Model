import streamlit as st
import cv2
import numpy as np
import mediapipe as mp

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Air Writing", layout="wide")

st.title("✍️ Air Writing System")

# =========================
# BUTTONS
# =========================
start = st.button("🚀 Start Camera")
stop = st.button("🛑 Stop")

frame_placeholder = st.empty()

# =========================
# MEDIAPIPE
# =========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# =========================
# SESSION STATE
# =========================
if "run" not in st.session_state:
    st.session_state.run = False

if start:
    st.session_state.run = True

if stop:
    st.session_state.run = False

if "canvas" not in st.session_state:
    st.session_state.canvas = None

if "prev" not in st.session_state:
    st.session_state.prev = None

# =========================
# CAMERA LOOP (FIXED)
# =========================
cap = cv2.VideoCapture(0)

if st.session_state.run:

    while st.session_state.run:

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        if st.session_state.canvas is None:
            st.session_state.canvas = np.zeros_like(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:

            hand = result.multi_hand_landmarks[0]

            ix = int(hand.landmark[8].x * w)
            iy = int(hand.landmark[8].y * h)

            tx = hand.landmark[4].x
            ty = hand.landmark[4].y

            dist = abs(ix - tx) + abs(iy - ty)

            # ERASE
            if dist < 0.05:
                st.session_state.canvas[:] = 0
                st.session_state.prev = None

            # DRAW
            else:
                if st.session_state.prev is not None:
                    cv2.line(
                        st.session_state.canvas,
                        st.session_state.prev,
                        (ix, iy),
                        (0, 255, 0),
                        5
                    )

                st.session_state.prev = (ix, iy)

        else:
            st.session_state.prev = None

        output = cv2.addWeighted(frame, 0.7, st.session_state.canvas, 0.3, 0)

        frame_placeholder.image(output, channels="BGR")

cap.release()