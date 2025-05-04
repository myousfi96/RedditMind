import streamlit as st
import pandas as pd
import json
import praw
from typing import List
from datetime import datetime
import os
from crew import RedditMind
from dotenv import load_dotenv

load_dotenv()

############################
# 1) PRAW Setup
############################

def init_reddit():
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "reddit_gpt_analysis by /u/YOUR_USERNAME")

    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        st.error("Missing Reddit API credentials. Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables.")
        st.stop()

    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

@st.cache_resource
def get_reddit_instance():
    return init_reddit()

@st.cache_data(show_spinner=True)
def fetch_reddit_data(
    topic: str,
    subreddits: List[str],
    num_posts: int,
    num_comments: int,
    time_filter: str
) -> pd.DataFrame:
    """
    Fetch data from Reddit, return as a DataFrame.
    """
    reddit = get_reddit_instance()
    retrieved_data = []

    time_filter_map = {
        "All Time": "all",
        "Past Year": "year",
        "Past 3 Months": "3_months",
        "Past Month": "month",
        "Past Week": "week"
    }
    reddit_time_filter = time_filter_map.get(time_filter, "all")

    for sub in subreddits:
        try:
            sub_obj = reddit.subreddit(sub)
            if topic:
                submissions = sub_obj.search(topic, limit=num_posts, time_filter=reddit_time_filter)
            else:
                submissions = sub_obj.hot(limit=num_posts)

            for submission in submissions:
                post_entry = {
                    "text": submission.selftext or submission.title,
                    "score": submission.score,
                    "created": datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d"),
                    "subreddit": submission.subreddit.display_name,
                    "type": "post",
                    "url": submission.url,
                    "title": submission.title
                }
                retrieved_data.append(post_entry)

                if num_comments > 0:
                    submission.comments.replace_more(limit=0)
                    top_comments = submission.comments[:num_comments]
                    for c in top_comments:
                        retrieved_data.append({
                            "text": c.body,
                            "score": c.score,
                            "created": datetime.utcfromtimestamp(c.created_utc).strftime("%Y-%m-%d"),
                            "subreddit": c.subreddit.display_name,
                            "type": "comment"
                        })
        except Exception as e:
            st.warning(f"Error fetching subreddit '{sub}': {e}")

    return pd.DataFrame(retrieved_data)

############################
# 2) Display Overview
############################

def display_overview():
    """
    Show the LLM summary (rating, pros, cons) if 'review_data' is in session state.
    """
    st.header("Overview")

    if "review_data" not in st.session_state:
        st.info("No overview data yet. Please run the analysis.")
        return

    data = st.session_state["review_data"]

    # Summaries
    st.info(data.get("summary", "No summary provided."))

    st.subheader("Rating")
    rating_str = data.get("rating", "0%").replace("%", "").strip()
    rating_value = int(rating_str) if rating_str.isdigit() else 0
    st.progress(rating_value / 100)
    st.write(f"⭐ {rating_value}%")

    st.subheader("Pros")
    pros_str = data.get("pros", "")
    for point in pros_str.split(";"):
        p = point.strip()
        if p:
            st.success(f"✔️ {p}")

    st.subheader("Cons")
    cons_str = data.get("cons", "")
    for point in cons_str.split(";"):
        c = point.strip()
        if c:
            st.warning(f"⚠️ {c}")


############################
# 3) Main Flow
############################
def main():
    st.set_page_config(page_title="Reddit Mind", layout="wide")
    st.title("Reddit Mind")

    # A) Sidebar for initial Reddit fetch
    with st.sidebar.expander("Reddit Search Params", expanded=True):
        topic_input = st.text_input("Topic (Required)", placeholder="Iphone16")
        subreddits_str = st.text_input("Subreddits (comma-separated)", placeholder="e.g. Apple, technology")
        time_filter = st.selectbox("Time Range", ["All Time","Past Year","Past 3 Months","Past Month","Past Week"], 0)
        num_posts = st.number_input("Posts per subreddit", min_value=1, max_value=1000, value=10)
        num_comments = st.number_input("Comments per post (0=disable)", min_value=0, max_value=1000, value=0)

        if st.button("Fetch Data from Reddit"):
            if not topic_input.strip():
                st.error("Please enter a topic.")
                st.stop()

            subreddits = ["all"] if not subreddits_str.strip() else [
                s.strip() for s in subreddits_str.split(",") if s.strip()
            ]

            with st.spinner("Fetching from Reddit..."):
                df_raw = fetch_reddit_data(topic_input, subreddits, num_posts, num_comments, time_filter)

            st.session_state["df_raw"] = df_raw
            st.success("Data fetched successfully!")


    # B) Filter Section
    st.header("Filter the Data")

    if "df_raw" not in st.session_state:
        st.info("No data found yet. Use the sidebar to fetch from Reddit.")
        return

    df_raw = st.session_state["df_raw"]
    if df_raw.empty:
        st.warning("The retrieved data is empty. No posts/comments found.")
        return

    sub_list = sorted(df_raw["subreddit"].unique())
    chosen_subs = st.multiselect("Filter by Subreddit(s):", options=sub_list, default=sub_list)

    min_score = int(df_raw["score"].min())
    max_score = int(df_raw["score"].max())
    cols = st.columns(2)
    with cols[0]:
        chosen_min = st.number_input("Minimum Score:", min_value=min_score, max_value=max_score, value=min_score)
    with cols[1]:
        chosen_max = st.number_input("Maximum Score:", min_value=min_score, max_value=max_score, value=max_score)


    df_filtered = df_raw.copy()
    df_filtered = df_filtered[df_filtered["subreddit"].isin(chosen_subs)]
    df_filtered = df_raw[(df_filtered["score"] >= chosen_min) & (df_filtered["score"] <= chosen_max)]

    st.write(f"**Filtered Rows**: {len(df_filtered)} / {len(df_raw)} total")
    st.session_state["df_filtered"] = df_filtered

    # C) Crew Setup
    dev_crew = RedditMind()
    crew = dev_crew.crew()

    if st.button("Analysis the data"):
        if df_filtered.empty:
            st.error("No data to pass to Crew. Your filters returned 0 rows.")
            return

        discussion_str = df_filtered.to_json(orient="records")

        with st.spinner("Running AI on the retrieved data..."):
            try:
                crew.kickoff(inputs={
                    "product": topic_input,
                    "discussion": discussion_str
                })
                st.success("Crew analysis completed on the data!")
            except Exception as e:
                st.error(f"Error running Crew: {e}")
                return

        # Load review.json into session_state
        if os.path.exists("review.json"):
            try:
                with open("review.json","r") as f:
                    review_data = json.load(f)
                st.session_state["review_data"] = review_data
            except:
                st.warning("Could not parse review.json")

        # Re-insert code for features.json, competition.json, timeline_analysis.json
        if os.path.exists("features.json"):
            try:
                with open("features.json", "r") as f:
                    feat_data = json.load(f)
                st.session_state["features_data"] = feat_data.get("features", [])
            except json.JSONDecodeError:
                st.warning("Error parsing features.json")

        if os.path.exists("competition.json"):
            try:
                with open("competition.json", "r") as f:
                    comp_data = json.load(f)
                st.session_state["competitor_data"] = comp_data
            except json.JSONDecodeError:
                st.warning("Error parsing competition.json")

        if os.path.exists("timeline_analysis.json"):
            try:
                with open("timeline_analysis.json", "r") as f:
                    timeline_data = json.load(f)
                st.session_state["timeline_data"] = timeline_data
            except json.JSONDecodeError:
                st.warning("Error parsing timeline_analysis.json")

    display_overview()


if __name__ == "__main__":
    main()
