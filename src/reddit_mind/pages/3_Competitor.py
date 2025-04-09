# file: pages/3_Competitor.py
import streamlit as st

st.title("Competitor Analysis")

if "competitor_data" not in st.session_state:
    st.warning("No competitor data. Please run analysis on Home.")
else:
    competitor_analysis = st.session_state["competitor_data"]
    competitors = competitor_analysis.get("competitors", [])
    if not competitors:
        st.info("No competitors found.")
    else:
        for comp in competitors:
            name = comp.get("name","Unknown")
            differences = comp.get("differences","")
            html_block = (
                "<div style='margin-bottom: 1.5rem; background-color: #2B2B2B;"
                " padding: 15px; border-radius: 6px; border: 1px solid #3A3A3A;'>"
                f"<h3 style='color: #ffffff; font-size:1.2rem; font-weight:bold; margin:0 0 0.5rem 0;'>"
                f"Competitor: {name}"
                "</h3>"
                f"<p style='color:#cccccc; margin:0; line-height:1.5; font-size:0.95rem;'>"
                f"<strong>Differences:</strong> {differences}"
                "</p>"
                "</div>"
            )
            st.markdown(html_block, unsafe_allow_html=True)
