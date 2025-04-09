# file: pages/3_TopTitles.py

import streamlit as st
import pandas as pd

st.title("Top 10 Highest-Score Titles")

def display_top_titles_table(df: pd.DataFrame):
    """
    Show the top 10 highest-score posts as a table with columns: Title, Score, Created, URL.
    """
    df_posts = df[df["type"] == "post"].copy()

    if df_posts.empty or "score" not in df_posts.columns or "title" not in df_posts.columns:
        st.info("No posts or missing columns for top titles.")
        return

    df_top = df_posts.sort_values("score", ascending=False).head(10)

    df_display = df_top[["title", "score", "created", "url"]].copy()
    df_display.rename(columns={"title": "Title", "score": "Score", "created": "Date", "url": "URL"}, inplace=True)

    st.dataframe(df_display)

if "df_filtered" not in st.session_state:
    st.info("No filtered data found. Please run analysis on the Home page first.")
else:
    df_filtered = st.session_state["df_filtered"]
    st.write("Below is a table of the top 10 highest-score posts from your filtered data.")
    display_top_titles_table(df_filtered)
