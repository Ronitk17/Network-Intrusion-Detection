import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import time

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Cyber AI IDS",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------
# Clean Dark Theme
# -----------------------
st.markdown("""
<style>
.stApp {
    background-color: #0b0f1a;
    color: #FFFFFF;
}
h1, h2, h3 {
    color: #FFFFFF;
}
div[data-testid="stMetric"] {
    background-color: #111827;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# Load Model
# -----------------------
model = joblib.load("nids_model.pkl")

# -----------------------
# Attack Labels
# -----------------------
attack_labels = {
    0: "Normal",
    1: "DoS Attack",
    2: "Probe Attack",
    3: "R2L Attack"
}

# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("💻 Network Intrusion Detection")

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Detection", "Live Monitor"]
)

# =======================
# 🏠 HOME PAGE
# =======================
if menu == "Home":

    st.markdown("# 🛡️ Network Intrusion Detection Terminal")


    st.markdown("""
    ### ⚡ Capabilities
    - Detect DoS, Probe, R2L attacks  
    - Real-time monitoring  
    - AI-powered classification  
    """)

    # Dataset selector
    platform = st.selectbox(
        "📂 Select Dataset",
        ["Network Data", "UNSW"]
    )

    # Load dataset
    if platform == "Network Data":
        df = pd.read_csv("network_data.csv")
    else:
        df = pd.read_csv("UNSW-NB15.csv")

    # Show dataset
    st.markdown("### 📊 Dataset Overview")
    st.dataframe(df.head())

    # Show stats
    st.markdown("### 📈 Dataset Info")
    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

# =======================
# 🔍 DETECTION PAGE
# =======================
elif menu == "Detection":

    st.title("💻 Intrusion Detection Terminal")

    # Status cards
    c1, c2, c3 = st.columns(3)
    c1.metric("System Status", "ACTIVE")
    c2.metric("Threat Level", "LOW")
    c3.metric("Monitoring", "LIVE")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        duration = st.slider("Connection Duration", 0, 1000, 100)
        src_bytes = st.slider("Source Bytes", 0, 50000, 1000)
        dst_bytes = st.slider("Destination Bytes", 0, 50000, 1000)

    with col2:
        st.markdown("### 📡 INPUT STREAM")
        st.write(f"Duration: {duration}")
        st.write(f"Src Bytes: {src_bytes}")
        st.write(f"Dst Bytes: {dst_bytes}")

    if st.button("🚀 SCAN NETWORK"):

        data = np.array([[duration, src_bytes, dst_bytes]])

        prediction = model.predict(data)[0]
        prob = model.predict_proba(data)[0].max()

        result = attack_labels[prediction]

        st.markdown("### 🧠 SYSTEM OUTPUT")

        if prediction == 0:
            st.success("🟢 STATUS: SAFE")
        else:
            st.error(f"🔴 ALERT: {result}")

        st.metric("Confidence", f"{prob*100:.2f}%")

# =======================
# 📡 LIVE MONITOR
# =======================
elif menu == "Live Monitor":

    st.title("📡 Real-Time Threat Monitor")

    placeholder = st.empty()
    chart_placeholder = st.empty()

    results = []

    for i in range(20):

        duration = np.random.randint(0, 1000)
        src_bytes = np.random.randint(0, 50000)
        dst_bytes = np.random.randint(0, 50000)

        data = np.array([[duration, src_bytes, dst_bytes]])
        prediction = model.predict(data)[0]

        result = attack_labels[prediction]
        results.append(result)

        # Packet display
        with placeholder.container():
            st.markdown(f"""
            ### 🔄 PACKET {i+1}
            - Duration: {duration}
            - Src Bytes: {src_bytes}
            - Dst Bytes: {dst_bytes}
            """)

            if prediction == 0:
                st.success("Normal Traffic")
            else:
                st.error(f"{result} Detected!")

        # Graph
        df_chart = pd.DataFrame({
            "Packet": list(range(1, len(results)+1)),
            "Type": results
        })

        fig = px.histogram(
            df_chart,
            x="Packet",
            color="Type",
            title="Live Threat Activity",
            template="plotly_dark"
        )

        chart_placeholder.plotly_chart(fig, use_container_width=True)

        time.sleep(1)