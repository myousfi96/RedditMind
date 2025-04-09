# file: pages/4_Timeline.py
import streamlit as st
import pandas as pd

st.title("Timeline Analysis")

if "timeline_data" not in st.session_state:
    st.warning("No timeline data. Please run analysis on Home.")
else:
    timeline_data = st.session_state["timeline_data"]
    overall_summary = timeline_data.get("overall_trend_summary","")
    if overall_summary:
        st.info(f"Overall Trend: {overall_summary}")

    sig_peaks = timeline_data.get("significant_peaks","")
    if sig_peaks:
        st.warning(f"Significant Peaks: {sig_peaks}")

    timeline_segments = timeline_data.get("timeline",[])
    if not timeline_segments:
        st.info("No timeline segments found.")
    else:
        df_timeline = pd.DataFrame(timeline_segments)
        if "period" in df_timeline.columns:
            df_timeline.sort_values("period", inplace=True, ignore_index=True)

        st.subheader("Sentiment & Highlights")
        for _, row in df_timeline.iterrows():
            period_label = row.get("period","N/A")
            volume_val = row.get("volume",0)
            sentiment = row.get("sentiment","neutral")
            highlights = row.get("highlights","")

            st.write(f"**{period_label}** — Volume: {volume_val}, Sentiment: `{sentiment}`")
            if highlights:
                st.write(f"> {highlights}")
            st.write("---")
