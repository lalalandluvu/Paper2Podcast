# Paper2Podcast: Codebase Walkthrough

This document provides a comprehensive explanation of the **Paper2Podcast** codebase. It is designed to help you understand the function of each file and the logic behind every code block, making it easier to present the project to your professor and classmates.

---

## 1. Project Overview

**Paper2Podcast** is an AI-powered application that transforms academic research papers (PDFs) into engaging audio podcasts.

### Architecture
1.  **Frontend (`app.py`)**: Built with **Streamlit**, this handles user interaction (uploading files, setting keys, playing audio).
2.  **Orchestrator (`agents.py`)**: Uses **CrewAI** to manage AI agents (Researcher and Host) that read the paper and write the script.
3.  **Knowledge Base (`rag_utils.py`)**: Uses **RAG (Retrieval-Augmented Generation)** to split the PDF into chunks and search for relevant facts.
4.  **Audio Engine (`audio_utils.py`)**: Uses **OpenAI TTS (Text-to-Speech)** to convert the script into a multi-speaker audio file.
5.  **Visual Engine (`image_utils.py`)**: Uses **Google Imagen 3** to generate custom album art for the podcast.

---

## 2. File-by-File Explanation

### 📄 `app.py` (The Main Application)
This is the entry point of the application. It runs the web interface.

**Key Code Blocks:**

*   **Imports & Setup**:
    ```python
    import streamlit as st
    ...
    st.set_page_config(page_title="Paper2Podcast", page_icon="🎙️")
    ```
    *   Sets up the page title and icon.

*   **Sidebar Configuration**:
    ```python
    with st.sidebar:
        if "OPENAI_API_KEY" in st.secrets: ...
    ```
    *   Securely loads API keys from `secrets.toml` or asks the user to input them.
    *   Allows the user to select a **Podcast Persona** (e.g., "Heated Debate") and **Voices** (Host/Guest).

*   **Main Logic (Generate Podcast)**:
    ```python
    if st.button("Generate Podcast"):
        with st.spinner(...):
            # 1. Save uploaded PDF to a temp file
            # 2. Run CrewAI to get the script
            script_result = create_podcast_crew(...)
            # 3. Generate Album Art
            image = generate_album_art(...)
            # 4. Generate Audio
            audio_path = generate_audio(...)
    ```
    *   This is the core workflow. It calls functions from other files to perform the heavy lifting.

*   **State Management**:
    ```python
    st.session_state.podcast_script = script_result
    ```
    *   Uses `st.session_state` so that the generated content (script, audio, image) doesn't disappear when you interact with the app.

---

### 🤖 `agents.py` (The AI Crew)
This file defines the AI agents and their tasks using the **CrewAI** framework.

**Key Code Blocks:**

*   **Setup**:
    ```python
    def create_podcast_crew(pdf_path, api_key, ...):
        # 1. Setup RAG Tool
        chunks = load_and_split_pdf(pdf_path)
        vector_store = create_vector_store(chunks, api_key)
    ```
    *   Prepares the PDF for searching by creating a "Vector Store" (a searchable database of the text).

*   **Tool Definition**:
    ```python
    @tool("Search PDF")
    def search_pdf_tool(query: str):
        docs = retriever.invoke(query)
        return ...
    ```
    *   Gives the AI a "tool" to look up facts in the PDF. The AI can ask questions like "What is the methodology?" and this tool returns the relevant text.

*   **Agents**:
    ```python
    researcher = Agent(role='Senior Academic Researcher', ...)
    host = Agent(role='Podcast Host', ...)
    ```
    *   **Researcher**: Reads the paper and extracts facts.
    *   **Host**: Takes the facts and writes a fun dialogue script.

*   **Tasks**:
    ```python
    research_task = Task(description='Search the PDF...', agent=researcher)
    script_task = Task(description='Write a dialogue script...', agent=host)
    ```
    *   Defines exactly what each agent should do.

*   **Crew Kickoff**:
    ```python
    crew = Crew(agents=[...], tasks=[...])
    result = crew.kickoff()
    ```
    *   Starts the AI team working.

---

### 📚 `rag_utils.py` (Retrieval-Augmented Generation)
This file handles the "reading" of the PDF.

**Key Code Blocks:**

*   **Loading & Splitting**:
    ```python
    def load_and_split_pdf(file_path):
        loader = PyPDFLoader(file_path)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, ...)
        chunks = text_splitter.split_documents(documents)
    ```
    *   Loads the PDF and cuts it into smaller pieces (chunks) of 2000 characters. This makes it easier for the AI to process.

*   **Vector Store**:
    ```python
    def create_vector_store(chunks, api_key):
        embeddings = OpenAIEmbeddings(...)
        vector_store = FAISS.from_documents(chunks, embeddings)
    ```
    *   Converts text chunks into numbers (embeddings) and stores them in FAISS. This allows us to search for "concepts" rather than just keywords.

---

### 🔊 `audio_utils.py` (Text-to-Speech)
This file converts the written script into audio.

**Key Code Blocks:**

*   **Parsing the Script**:
    ```python
    segments = re.split(r'(\**Host\**:|Guest:|Researcher:)', text)
    ```
    *   Uses Regular Expressions (Regex) to chop the script into parts whenever the speaker changes (e.g., "Host:", "Guest:").

*   **Generating Audio**:
    ```python
    for segment in segments:
        voice = host_voice if current_speaker == "Host" else guest_voice
        response = client.audio.speech.create(model="tts-1", voice=voice, input=segment)
        audio_data += response.content
    ```
    *   Loops through each part of the dialogue.
    *   Selects the correct voice (Male/Female) based on who is speaking.
    *   Calls OpenAI's API to generate the audio for that sentence and stitches it all together.

---

### 🎨 `image_utils.py` (Album Art Generation)
This file generates the cover art.

**Key Code Blocks:**

*   **Generation**:
    ```python
    def generate_album_art(prompt, api_key):
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt],
        )
    ```
    *   Uses Google's **Gemini 2.5 Flash** model to create an image based on a prompt (which was generated by the AI in `app.py`).

---

## 3. `requirements.txt`
Lists all the external libraries the project needs to run.

*   `streamlit`: For the web app.
*   `crewai`: For the AI agents.
*   `langchain`: For connecting LLMs and data.
*   `openai`: For GPT-4 and TTS.
*   `google-genai`: For image generation.
*   `pypdf`: For reading PDF files.
*   `faiss-cpu`: For the vector database (searching the PDF).
