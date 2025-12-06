# 🎙️ Paper2Podcast

**Turn your academic papers into engaging audio podcasts.**

Paper2Podcast is an AI-powered tool that transforms dense research papers (PDFs) into entertaining, conversational podcast scripts and then synthesizes them into high-quality audio using OpenAI's text-to-speech technology.

## 🌐 Live Demo

Try the app here: [**Paper2Podcast on Streamlit**](https://paper2podcast-5ch697ezum7npp4r84lven.streamlit.app/)

## ✨ Features

*   **PDF to Podcast**: Upload any research paper PDF.
*   **AI Research & Scripting**: Uses a multi-agent system (CrewAI) to research the paper and write a dialogue script.
*   **Custom Personas**: Choose the "vibe" of your podcast:
    *   Standard (Informative & Balanced)
    *   Heated Debate (Skeptic vs Believer)
    *   ELI5 (Simple & Fun)
    *   Deep Dive (Technical & Niche)
*   **Voice Selection**: Customize the voices for your Host and Guest.
    *   **Host**: Select from Alloy, Nova, Shimmer (Female) or Echo, Fable, Onyx (Male).
    *   **Guest**: Select from the same range of high-quality voices.
    *   *The system automatically assigns a gender-appropriate name to the Host based on your selection.*
*   **🎨 AI Album Art**: Generates unique, artistic cover art for your podcast episode using **Google Imagen 3 (via Gemini)** based on the paper's title.
*   **📝 Cheat Sheet Download**: Automatically creates and lets you download a **Study Guide** (Markdown) containing Key Findings, Methodology, and a Glossary.
*   **Audio Generation**: Produces a high-quality MP3 file of the conversation.

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/lalalandluvu/Paper2Podcast.git
cd Paper2Podcast
```

### 2. Setup API Keys (Secrets)
This app requires an **OpenAI API Key** (for scripts & audio) and an optional **Google API Key** (for Album Art).

**Option A: Using `secrets.toml` (Recommended for Local Dev)**
1.  Create a folder named `.streamlit` in the project root.
2.  Create a file named `secrets.toml` inside it.
3.  Add your keys:
    ```toml
    OPENAI_API_KEY = "sk-..."
    GOOGLE_API_KEY = "..."
    ```
    *Note: This file is ignored by Git for security.*

**Option B: UI Input**
*   If no secrets file is found, the app will prompt you to enter your keys in the sidebar.

### 3. Run the App
*   **Windows**: Double-click `setup_and_run.bat`.
*   **Terminal**: `.\setup_and_run.bat`

This script will automatically:
*   Create a Python virtual environment.
*   Install all required dependencies.
*   Launch the application in your browser.

## 🛠️ Tech Stack

*   **Python**: Core logic.
*   **Streamlit**: Web interface.
*   **CrewAI**: Orchestrates the AI agents (Researcher & Host).
*   **LangChain**: PDF processing and RAG.
*   **OpenAI GPT-4o**: Powers the research and scripting.
*   **OpenAI TTS**: Generates the lifelike audio.
*   **Google Gemini / Imagen 3**: Generates the album art.

## 📄 License

[MIT License](LICENSE)
