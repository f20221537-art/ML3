import streamlit as st
import pandas as pd
import altair as alt
import time
import numpy as np
from processing import get_quick_data, get_realtime_frame

st.set_page_config(page_title="SonicTrace Pro", layout="wide")

# Enhanced CSS for a "Dark Studio" feel
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e1e4e8; }
    .stMetric { background-color: #1c2128; border: 1px solid #30363d; border-radius: 12px; }
    .stProgress > div > div > div > div { background-color: #238636; }
    [data-testid="stSidebar"] { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ SonicTrace Pro")
st.caption("AI-Powered Multi-Instrument Temporal Mapping")

with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("Upload Track", type=["mp3", "wav"])
    mode = st.radio("Processing Mode", ["Quick Analysis", "Real-Time Playback"])
    st.divider()
    st.markdown("### Model Stats\n- Model: Polyphonic-CNN\n- Latency: <150ms")

if uploaded_file:
    st.audio(uploaded_file)
    
    if st.button("Initialize Analysis"):
        if mode == "Quick Analysis":
            with st.status("Analyzing audio frequencies...", expanded=True) as status:
                data = get_quick_data()
                df = pd.DataFrame(data)
                time.sleep(1.5) # Simulate processing
                status.update(label="Analysis Complete!", state="complete")
                
            chart = alt.Chart(df).mark_bar(cornerRadius=4).encode(
                x=alt.X('Start:Q', title='Time (s)'),
                x2='End:Q',
                y=alt.Y('Instrument:N', sort=None, title=None),
                color=alt.Color('Instrument:N', scale=alt.Scale(scheme='darkmulti')),
                tooltip=['Instrument', 'Start', 'End']
            ).properties(height=300).interactive()
            st.altair_chart(chart, use_container_width=True)

        else:
            # REAL-TIME MODE
            col1, col2 = st.columns([3, 1])
            with col1:
                chart_holder = st.empty()
            with col2:
                st.write("### Live Activity")
                status_text = st.empty()
                viz_holder = st.empty() # For the "Audio Wave" animation

            progress_bar = st.progress(0)
            live_data = []
            duration = 30 
            
            for second in range(duration + 1):
                progress_bar.progress(second / duration)
                current_active = get_realtime_frame(second)
                
                # Update text UI
                status_text.write(f"**Detected:** \n" + "\n".join([f"- {i}" for i in current_active]))
                
                # Animation: Visual Spectrum simulation
                spec_data = pd.DataFrame({
                    'Freq': range(10),
                    'Val': np.random.randint(1, 10, 10)
                })
                spec_chart = alt.Chart(spec_data).mark_bar(color='#238636').encode(
                    x=alt.X('Freq:O', axis=None),
                    y=alt.Y('Val:Q', axis=None)
                ).properties(height=100)
                viz_holder.altair_chart(spec_chart, use_container_width=True)

                # Update Timeline
                for inst in current_active:
                    live_data.append({"Instrument": inst, "Start": second, "End": second + 1})
                
                df_live = pd.DataFrame(live_data)
                
                # FIXED ALTAIR SCALE HERE
                live_chart = alt.Chart(df_live).mark_bar(size=12).encode(
                    x=alt.X('Start:Q', scale=alt.Scale(domain=[0, duration]), title="Timeline (s)"),
                    x2='End:Q',
                    y=alt.Y('Instrument:N', sort=['Guitar', 'Drums', 'Voice'], title=None),
                    color=alt.Color('Instrument:N', legend=None)
                ).properties(height=350)
                
                chart_holder.altair_chart(live_chart, use_container_width=True)
                time.sleep(0.4) 

            st.success("Playback and analysis finished.")
