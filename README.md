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
*   **Audio Generation**: Produces a high-quality MP3 file of the conversation.

## 🚀 How to Run

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/lalalandluvu/Paper2Podcast.git
    cd Paper2Podcast
    ```

2.  **Run the Setup Script**:
    *   Double-click `setup_and_run.bat` (Windows).
    *   *Or run in terminal:* `.\setup_and_run.bat`

    This script will automatically:
    *   Create a Python virtual environment.
    *   Install all required dependencies.
    *   Launch the application in your browser.

3.  **Enter your OpenAI API Key**:
    *   You will need a valid OpenAI API Key to generate the script and audio. Enter it in the sidebar when prompted.

## 🛠️ Tech Stack

*   **Python**: Core logic.
*   **Streamlit**: Web interface.
*   **CrewAI**: Orchestrates the AI agents (Researcher & Host).
*   **LangChain**: PDF processing and RAG (Retrieval Augmented Generation).
*   **OpenAI GPT-4o**: Powers the research and scripting.
*   **OpenAI TTS (Text-to-Speech)**: Generates the lifelike audio.

## 📄 License

[MIT License](LICENSE)
