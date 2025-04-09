# file: pages/2_Charts.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Visualizations: Discussions & Subreddit Posts")

def display_charts(df: pd.DataFrame):
    """
    Show line chart (discussions over time) & bar chart (posts by subreddit).
    """
    if df.empty:
        st.warning("No data to visualize.")
        return

    df['created'] = pd.to_datetime(df['created'], errors='coerce')
    df = df.dropna(subset=['created'])
    df["year_month"] = df["created"].dt.to_period("M").astype(str)

    df_posts = df[df['type'] == 'post']

    monthly_counts = df_posts.groupby("year_month").size().reset_index(name="discussion_count")
    monthly_counts = monthly_counts.sort_values("year_month")

    subreddit_counts = df_posts.groupby("subreddit").size().reset_index(name="post_count")

    sns.set_style("darkgrid")
    plt.rcParams.update({
        'axes.facecolor': '#1E1E1E', 'figure.facecolor': '#1E1E1E',
        'text.color': 'white', 'axes.labelcolor': 'white',
        'xtick.color': 'white', 'ytick.color': 'white',
        'axes.edgecolor': 'gray', 'grid.color': '#444',
        'grid.linestyle': '--', 'grid.linewidth': 0.5
    })

    st.subheader("Discussions Over Time")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(
        monthly_counts["year_month"],
        monthly_counts["discussion_count"],
        marker='o', linestyle='-', color='cyan', markersize=8, linewidth=2
    )
    ax.set_xlabel("Date", fontsize=12, fontweight="bold")
    ax.set_ylabel("Number of Discussions", fontsize=12, fontweight="bold")
    ax.set_title("Discussions Over Time", fontsize=14, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("gray")
    ax.spines["bottom"].set_color("gray")
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    st.pyplot(fig)

    # Sort subreddits by post_count descending
    subreddit_counts_sorted = subreddit_counts.sort_values("post_count", ascending=False)

    # Limit to top 20
    top_20 = subreddit_counts_sorted.head(20)

    st.subheader("Posts Grouped by Subreddit (Top 20)")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(
        top_20["subreddit"],
        top_20["post_count"],
        color="deepskyblue",
        alpha=0.8
    )

    ax.set_xlabel("Number of Posts", fontsize=12, fontweight="bold")
    ax.set_ylabel("Subreddit", fontsize=12, fontweight="bold")
    ax.set_title("Posts by Subreddit (Top 20)", fontsize=14, fontweight="bold")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("gray")
    ax.spines["bottom"].set_color("gray")

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # If you want the largest at the top, invert the y-axis
    ax.invert_yaxis()

    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    st.pyplot(fig)


if "df_filtered" not in st.session_state:
    st.info("No filtered data found. Please run analysis on the Home page first.")
else:
    display_charts(st.session_state["df_filtered"])
