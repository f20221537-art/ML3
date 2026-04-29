import streamlit as st
import pandas as pd
import time
from processing import identify_instruments

st.set_page_config(page_title="Audio Lens", layout="wide")

# Load Custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🎵 Audio Lens: Instrument Tracker")
st.markdown("Upload a track to see a breakdown of instruments and their timestamps.")

uploaded_file = st.file_uploader("Choose an audio file (MP3, WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button("Analyze Track"):
        with st.spinner("Analyzing frequencies and temporal patterns..."):
            # Mocking the processing delay
            results = identify_instruments(uploaded_file)
            
            st.success("Analysis Complete!")
            
            # Layout for Results
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Detected Instruments")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
            
            with col2:
                st.subheader("Timeline Visualization")
                # Creating a horizontal bar chart for timestamps
                st.vega_lite_chart(df, {
                    'mark': 'bar',
                    'encoding': {
                        'x': {'field': 'Start (s)', 'type': 'quantitative'},
                        'x2': {'field': 'End (s)'},
                        'y': {'field': 'Instrument', 'type': 'nominal'},
                        'color': {'field': 'Instrument', 'type': 'nominal'}
                    }
                }, use_container_width=True)
