# file: pages/2_Features.py
import streamlit as st

st.title("Features")

if "features_data" not in st.session_state:
    st.warning("No features found. Please run analysis on Home page.")
else:
    features = st.session_state["features_data"]
    if not features:
        st.info("Features list is empty.")
    else:
        for feature in features:
            name_escaped = feature["feature_name"]
            summary_escaped = feature["summary"]

            html_block = (
                f"<div style='display: flex; flex-direction: row; margin-bottom: 1rem; "
                f"background-color: #2B2B2B; padding: 15px; border-radius: 6px; border: 1px solid #3A3A3A;'>"
                f"<div style='width: 240px; font-weight: bold; font-size: 1.05rem; color: #FFFFFF; margin-right: 1.5rem;'>"
                f"{name_escaped}</div>"
                f"<div style='flex: 1; color: #DDDDDD; line-height: 1.5; font-size: 0.95rem;'>"
                f"{summary_escaped}</div>"
                f"</div>"
            )

            st.markdown(html_block, unsafe_allow_html=True)
