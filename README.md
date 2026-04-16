# 📚 Book Review Agent

An AI-powered tool that transforms draft book reviews into polished, engaging Chinese reviews styled for **小红书 (Xiaohongshu)** — China's popular lifestyle and social media platform.

## Overview

Book Review Agent takes your rough book review draft (in English, Chinese, or a mix of both) and refines it into a natural, conversational Chinese review that resonates with 小红书's young reader audience. It preserves your personal voice and genuine opinions while adapting the tone and structure for the platform.

## Features

- **Draft-to-Review Generation** — Paste a draft review in any language and get a polished 小红书-style Chinese review
- **Iterative Refinement** — Not satisfied with the output? Choose from quick improvement options:
  - ✨ More Engaging
  - ✂️ More Concise
  - ❤️ More Emotional
  - 😄 Add Humor
  - 📐 Better Structure
- **Powered by Gemini 2.5 Flash** — Uses Google's Gemini model for high-quality text generation
- **Streamlit Web UI** — Clean, user-friendly interface for generating and refining reviews
- **Docker Support** — Containerized deployment with Docker Compose

## Tech Stack

- **Frontend/App**: [Streamlit](https://streamlit.io/)
- **LLM**: [Google Gemini 2.5 Flash](https://ai.google.dev/) via `google-generativeai`
- **Containerization**: Docker & Docker Compose
- **Language**: Python 3.11


## Getting Started

### Prerequisites

- Python 3.11+
- A [Google Gemini API key](https://ai.google.dev/)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/joeylim0328/Book-Review-Agent.git
   cd Book-Review-Agent
   ```

2. **Create a `.env` file** in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Install dependencies**
   ```bash
   pip install -r book_review_app/requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run book_review_app/app.py
   ```

5. Open your browser at `http://localhost:8501`


## Usage

1. Enter the **book title** and **author**
2. Paste your **draft review** (English, Chinese, or mixed)
3. Click **Generate Review**
4. Optionally click any refinement button to further improve the output

## Review Style Guidelines

Generated reviews follow these principles:

- Natural, conversational Chinese — like chatting with a friend
- Short paragraph breaks optimized for mobile reading
- Character names kept in their original language
- Under 1,000 Chinese characters when possible
- Sparing use of emojis
- Structured as: introduction → plot summary → personal thoughts → recommendation → closing quote
