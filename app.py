

import streamlit as st
from air_canvas import run_air_canvas

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="LIVE WRITING MODEL",
    page_icon="✍️",
    layout="wide"
)

# =========================
# HEADER DESIGN
# =========================
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #00ffcc;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #bbbbbb;
    }
    .box {
        padding: 15px;
        border-radius: 15px;
        background-color: #111827;
        border: 1px solid #00ffcc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>✍️ LIVE WRITING MODEL</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Write in air using your index finger • Real-time AI tracking</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# SIDEBAR CONTROLS
# =========================
st.sidebar.title("⚙️ Controls")

mode = st.sidebar.selectbox(
    "Choose Mode",
    ["✍️ Writing Mode", "🎯 Demo Mode"]
)

color_theme = st.sidebar.selectbox(
    "Theme",
    ["Neon Green", "Cyber Blue", "Hot Red"]
)

# =========================
# COLOR THEMES
# =========================
colors = {
    "Neon Green": "#00ff00",
    "Cyber Blue": "#00ccff",
    "Hot Red": "#ff0033"
}

selected_color = colors[color_theme]

# =========================
# MAIN UI BOX
# =========================
st.markdown("<div class='box'>", unsafe_allow_html=True)

st.write("### 📌 Project Status")
st.success("System Ready ✔")

st.write("### ✋ Instructions")
st.info("""
1. Show your hand to camera  
2. Use index finger to write 
3. Open palm to erase
4. Lift finger to stop drawing  
5. Press ESC to exit camera  
""")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# START BUTTON
# =========================
col1, col2, col3 = st.columns([1,2,1])

with col2:
    if st.button("🚀 START AIR WRITING", use_container_width=True):
        st.warning("Camera starting... Please allow access")
        run_air_canvas()

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray'>Made with AI + Computer Vision ✨</p>",
    unsafe_allow_html=True
)