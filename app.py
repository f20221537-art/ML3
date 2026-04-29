import streamlit as st
import pandas as pd
import altair as alt
from processing import identify_instruments

# Page Config
st.set_page_config(page_title="SonicTrace AI", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a sleek "Studio" look
st.markdown("""
    <style>
    .main { background-color: #0b0d10; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stAudio { margin-bottom: 2rem; }
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Inter', sans-serif; }
    .stButton>button {
        background: linear-gradient(45deg, #238636, #2ea043);
        color: white; border: none; padding: 10px 24px; border-radius: 8px; font-weight: bold;
        transition: 0.3s; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4); }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🎙️ Controls")
    uploaded_file = st.file_uploader("Upload Master Track", type=["mp3", "wav", "flac"])
    sensitivity = st.slider("Detection Sensitivity", 0.0, 1.0, 0.5)
    st.info("Higher sensitivity may detect quieter background instruments.")

st.title("SonicTrace: Multi-Instrument Timeline")

if uploaded_file:
    # Top Row: Player and Summary
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.audio(uploaded_file)
    
    if st.button("Start AI Decomposition"):
        with st.spinner("Isolating stems and mapping temporal features..."):
            # Fetch data from processing logic
            results = identify_instruments(uploaded_file)
            df = pd.DataFrame(results)
            
            # Summary Metrics
            with col_b:
                st.metric("Instruments Found", len(df['Instrument'].unique()))

            st.divider()

            # Main View: The Timeline Chart
            st.subheader("Instrument Activity Map")
            
            # Altair Chart: Handles multiple segments for the same instrument
            chart = alt.Chart(df).mark_bar(
                cornerRadius=5,
                height=20
            ).encode(
                x=alt.X('Start:Q', title='Time (seconds)'),
                x2='End:Q',
                y=alt.Y('Instrument:N', sort='-x', title=None),
                color=alt.Color('Instrument:N', scale=alt.Scale(scheme='tableau20'), legend=None),
                tooltip=['Instrument', 'Start', 'End']
            ).properties(height=400).interactive()

            st.altair_chart(chart, use_container_width=True)

            # Detailed Breakdown Table
            with st.expander("See Raw Timestamp Data"):
                st.table(df.sort_values(by='Start'))
else:
    st.warning("Please upload an audio file in the sidebar to begin.")
