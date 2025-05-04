# RedditMind Project

Welcome to **RedditMind**, an intelligent application that leverages Reddit discussions to analyze products and topics using advanced AI agentic capabilities. This Streamlit-based project fetches data from Reddit via **PRAW** and uses a suite of AI-powered agents to generate insights, summaries, and detailed analyses.

## Prerequisites

Before installing RedditMind, you'll need:

1. **Reddit API Credentials:**
   * Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps).
   * Create a new application (select `script` type).
   * Note down the **client ID** and **client secret**.

2. **LLM API Key:**
   * You need either a Gemini or OpenAI API key for the AI analysis.

3. **Environment File:**
   Create a `.env` file in the project's root directory:
   ```env
   # Reddit API Credentials (required)
   REDDIT_CLIENT_ID=YOUR_CLIENT_ID
   REDDIT_CLIENT_SECRET=YOUR_CLIENT_SECRET
   REDDIT_USER_AGENT=RedditMind/1.0

   # LLM API Key (add either Gemini OR OpenAI)
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY
   # OPENAI_API_KEY=YOUR_OPENAI_API_KEY
   ```
   Replace the placeholder values with your actual keys.

4. **Config Files:**
   Ensure you have the `config/` directory with `agents.yaml` and `tasks.yaml` files.

   **LLM Configuration:**
   You can specify which Large Language Model (LLM) each agent should use directly within the `config/agents.yaml` file. Add an `llm:` key under the agent's definition. Make sure you have provided the corresponding API key in your `.env` file.


   **Available Models:**

   *   **OpenAI (Requires `OPENAI_API_KEY` in `.env`)**
       ```
       gpt-4
       gpt-4.1
       gpt-4.1-mini-2025-04-14
       gpt-4.1-nano-2025-04-14
       gpt-4o
       gpt-4o-mini
       o1-mini
       o1-preview
       ```

   *   **Anthropic (Requires `ANTHROPIC_API_KEY` in `.env`)**
       ```
       claude-3-5-sonnet-20240620
       claude-3-sonnet-20240229
       ```

   *   **Gemini (Requires `GEMINI_API_KEY` in `.env`)**
       ```
       gemini/gemini-1.5-flash
       gemini/gemini-1.5-pro
       gemini/gemini-2.0-flash-lite-001
       gemini/gemini-2.0-flash-001
       gemini/gemini-2.0-flash-thinking-exp-01-21
       gemini/gemini-2.5-flash-preview-04-17
       gemini/gemini-2.5-pro-exp-03-25
       gemini/gemini-gemma-2-9b-it
       gemini/gemini-gemma-2-27b-it
       gemini/gemma-3-1b-it
       gemini/gemma-3-4b-it
       gemini/gemma-3-12b-it
       gemini/gemma-3-27b-it
       ```

## Installation and Setup

You can run RedditMind either with Docker (recommended) or directly on your local machine.

### Option 1: Local Installation

1. **Clone or Download** this repository.

2. **Install Dependencies**  
   Open your terminal and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**  
   Start the Streamlit app with:
   ```bash
   streamlit run src/reddit_mind/app.py
   ```

### Option 2: Docker Installation

1. **Build the Docker Image:**
   ```bash
   docker build -t reddit-mind .
   ```

2. **Run the Container:**
   ```bash
   docker run --env-file .env -p 8501:8501 reddit-mind
   ```

3. **Access the App:**
   Open your browser and navigate to `http://localhost:8501`

## Usage Instructions

Once the app is running (via either method):

1. Enter your topic (e.g., "iPhone 16") and target subreddits.
2. Click "Fetch Data from Reddit" to retrieve posts and comments.
3. Filter the data if needed.
4. Click "Analysis the data" to run the AI analysis.
5. View the generated insights, including overall summary, features, competitors, and timeline analysis.

## License

This project is provided as-is for educational and prototyping purposes.
