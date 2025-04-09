# RedditMind Project

Welcome to **RedditMind**, an intelligent application that leverages Reddit discussions to analyze products and topics using advanced AI agentic capabilities. This Streamlit-based project fetches data from Reddit via **PRAW** and uses a suite of AI-powered agents to generate insights, summaries, and detailed analyses.

## Overview

**RedditMind** is designed to quickly gather and analyze Reddit discussions about any product or topic you specify. With a few clicks, you can retrieve posts and comments from multiple subreddits and see:
  
- A concise summary of the conversation, including an overall sentiment rating.
- Detailed extraction of key product features along with their pros and cons.
- A comparative analysis of competitors mentioned in the discussion.
- A timeline analysis highlighting key trends and events that influence sentiment over time.

## Key Features

- **Reddit Data Fetching:**  
  Uses **PRAW** to search and collect relevant posts and comments across various subreddits within a chosen time frame.

- **AI Agentic Analysis:**  
  The core of RedditMind’s functionality lies in its AI agents—powered by the Crew framework. These agents perform specific tasks:
  
  - **Summarizer:**  
    Provides an overall summary, highlighting the discussion’s primary viewpoints, key pros and cons, and an overall rating expressed as a percentage.
  
  - **Features Extraction:**  
    Extracts and categorizes user feedback on different product features, summarizing the strengths and weaknesses noted in the discussion.
  
  - **Competitor Analysis:**  
    Compares alternative or competitor products mentioned, giving you insights into how the product stands relative to its competitors.
  
  - **Timeline Analyzer:**  
    Reviews the progression of discussions over time, pinpointing significant peaks in activity or shifts in sentiment that can indicate product updates or market changes.

- **Interactive Dashboard:**  
  Built with Streamlit, the app provides a user-friendly interface to configure search parameters, filter results, and display visualizations including charts, tables, and timelines.

## Installation

1. **Clone or Download** this repository.

2. **Install Dependencies**  
   Open your terminal and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install CrewAI Separately**  
   RedditMind uses the Crew framework for its AI agentic analysis. Please install CrewAI separately by following the instructions available at https://docs.crewai.com/installation

4. **Set Up Environment Variables**  
   Create an `.env` file in the project directory and include your API key for the LLM. For example:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   # or
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **(Optional) Setup a Virtual Environment**  
   It’s recommended to use a virtual environment (like `venv` or `conda`) to manage dependencies without affecting your system-wide packages.

## Usage

1. **Run the Streamlit App**  
   Start the application with:
   ```bash
   streamlit run app.py
   ```
2. **Configure Your Query:**  
   Use the sidebar to provide:
   - **Topic:** The product or topic you want to analyze (e.g., “iPhone 16”).
   - **Subreddits:** A comma-separated list (e.g., "Apple, technology").
   - **Time Range:** Options ranging from "All Time" to "Past Week".
   - **Number of Posts/Comments:** Set the fetch limits for posts and comments.

3. **Data Fetching and Filtering:**  
   After clicking “Fetch Data from Reddit,” the app retrieves and displays the data. You can then filter this dataset by subreddit and score range to tailor your analysis.

4. **Run AI Analysis:**  
   Hit the “Analysis the data” button to trigger the AI agents. The Crew-based agents will process the filtered data and generate:
   - A summary (overview, pros, cons, and rating).
   - Detailed feature extraction.
   - Competitor analysis.
   - Timeline analysis.
  
   The results are displayed across different pages, such as the Features, Competitor, Timeline, Charts, and Top Titles pages.

## License

This project is provided as-is for educational and prototyping purposes. Feel free to adapt it to your needs. For any further details on licensing, please refer to the repository or contact the project maintainer.