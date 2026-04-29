import streamlit as st
import pandas as pd
import altair as alt
import time
from processing import get_quick_data, get_realtime_frame

st.set_page_config(page_title="SonicTrace Pro", layout="wide")

# Modern Studio Styling
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); }
    .reportview-container { background: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 SonicTrace AI: Multi-Track Analysis")

with st.sidebar:
    st.header("Analysis Settings")
    uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav"])
    mode = st.radio("Choose Mode:", ["Quick Analysis", "Real-Time Playback"])
    st.info("Quick Analysis processes the whole file at once. Real-Time animates as you listen.")

if uploaded_file:
    audio_bytes = uploaded_file.read()
    st.audio(audio_bytes)
    
    if st.button("Start Analysis"):
        if mode == "Quick Analysis":
            with st.spinner("Processing full track..."):
                data = get_quick_data()
                df = pd.DataFrame(data)
                
                # Render the final static chart
                chart = alt.Chart(df).mark_bar(cornerRadius=5).encode(
                    x=alt.X('Start:Q', title='Time (s)'),
                    x2='End:Q',
                    y=alt.Y('Instrument:N', sort=None),
                    color='Instrument:N',
                    tooltip=['Instrument', 'Start', 'End']
                ).properties(height=300)
                st.altair_chart(chart, use_container_width=True)
                st.success("Analysis Complete!")

        else:
            # REAL-TIME ANIMATION MODE
            st.subheader("Live Instrument Feed")
            progress_bar = st.progress(0)
            status_text = st.empty()
            chart_holder = st.empty()
            
            live_data = []
            duration = 30  # Total duration for your test case
            
            for second in range(duration + 1):
                # Update progress and text
                step = second / duration
                progress_bar.progress(step)
                
                # Fetch currently active instruments for this specific second
                current_active = get_realtime_frame(second)
                status_text.markdown(f"**Current Time:** {second}s | **Detecting:** {', '.join(current_active)}")
                
                # Update the chart data
                for inst in current_active:
                    live_data.append({"Instrument": inst, "Start": second, "End": second + 1})
                
                df_live = pd.DataFrame(live_data)
                
                # Dynamic Altair Chart
                live_chart = alt.Chart(df_live).mark_bar(size=15).encode(
                    x=alt.X('Start:Q', scale=alt.Domain(0, duration), title="Timeline (s)"),
                    x2='End:Q',
                    y=alt.Y('Instrument:N', sort=['Guitar', 'Drums', 'Voice']),
                    color='Instrument:N'
                ).properties(height=300)
                
                chart_holder.altair_chart(live_chart, use_container_width=True)
                
                time.sleep(0.5) # Simulate real-time processing lag
            
            st.balloons()
