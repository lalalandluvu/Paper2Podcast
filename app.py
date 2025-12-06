import streamlit as st
import os
import tempfile
from pypdf import PdfReader
from agents import create_podcast_crew
import importlib
import audio_utils
importlib.reload(audio_utils)
from audio_utils import generate_audio
import random

st.set_page_config(page_title="Paper2Podcast", page_icon="🎙️")

st.title("🎙️ Paper2Podcast")
st.markdown("Turn your academic papers into engaging podcasts.")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    google_api_key = st.text_input("Google API Key (for Album Art)", type="password", help="Get it from Google AI Studio")
    
    st.subheader("Podcast Persona")
    persona_type = st.selectbox(
        "Choose a Vibe",
        [
            "Standard (Informative & Balanced)",
            "Heated Debate (Skeptic vs Believer)",
            "ELI5 (Simple & Fun)",
            "Deep Dive (Technical & Niche)"
        ]
    )
    
    persona_descriptions = {
        "Standard (Informative & Balanced)": "You are professional but approachable. You want to understand the truth.",
        "Heated Debate (Skeptic vs Believer)": "You are a skeptic. You question everything and play devil's advocate. You want to find holes in the argument.",
        "ELI5 (Simple & Fun)": "You explain things like I'm 5. You use simple analogies and avoid jargon. You are super excited.",
        "Deep Dive (Technical & Niche)": "You are a technical expert. You love the gritty details and complex math. You use technical jargon freely."
    }
    
    persona_description = persona_descriptions[persona_type]
    
    st.subheader("Voice Selection")
    
    # Voice Options with Gender
    voice_options = {
        "Alloy (Female)": {"id": "alloy", "gender": "Female"},
        "Echo (Male)": {"id": "echo", "gender": "Male"},
        "Fable (Male)": {"id": "fable", "gender": "Male"},
        "Onyx (Male)": {"id": "onyx", "gender": "Male"},
        "Nova (Female)": {"id": "nova", "gender": "Female"},
        "Shimmer (Female)": {"id": "shimmer", "gender": "Female"}
    }
    
    host_voice_selection = st.selectbox("Host Voice", list(voice_options.keys()), index=0) # Default Alloy
    guest_voice_selection = st.selectbox("Guest Voice", list(voice_options.keys()), index=1) # Default Echo
    
    host_voice_id = voice_options[host_voice_selection]["id"]
    guest_voice_id = voice_options[guest_voice_selection]["id"]
    
    # Determine Host Name based on Voice Gender
    if voice_options[host_voice_selection]["gender"] == "Female":
        host_name = random.choice(["Sarah", "Emma", "Chloe", "Olivia", "Ava"])
    else:
        host_name = random.choice(["Mike", "David", "James", "Robert", "John"])
        


# Main Area
uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type="pdf")

if uploaded_file is not None and api_key:
    if st.button("Generate Podcast"):
        with st.spinner("Processing PDF and Generating Script... (This may take a minute)"):
            # Save uploaded file to temp
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            try:
                # Run CrewAI
                script_result = create_podcast_crew(tmp_path, api_key, persona_description, host_name)
                
                # Display Script
                st.subheader("Generated Podcast Script")
                st.text_area("Script", value=script_result, height=400)
                
                # Extract Title
                try:
                    reader = PdfReader(tmp_path)
                    title = reader.metadata.title
                    if not title:
                        # Fallback to filename
                        title = uploaded_file.name.replace(".pdf", "")
                except:
                    title = uploaded_file.name.replace(".pdf", "")
                    
                # Generate Album Art
                if google_api_key:
                    st.subheader("Album Art")
                    with st.spinner("Generating Album Art..."):
                        try:
                            from langchain_openai import ChatOpenAI
                            from image_utils import generate_album_art
                            
                            llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
                            prompt_response = llm.invoke(f"Generate a short, artistic, and descriptive image prompt for a podcast cover art based on this paper title: '{title}'. The style should be modern, digital art, and relevant to the topic. Output ONLY the prompt.")
                            image_prompt = prompt_response.content
                            
                            image = generate_album_art(image_prompt, google_api_key)
                            
                            if image:
                                # Save to temp file to avoid Streamlit 'format' attribute error
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                                    image.save(tmp_img.name)
                                    st.image(tmp_img.name, caption=f"Generated Cover Art (Google Imagen 3): {image_prompt}")
                            else:
                                st.warning("Failed to generate image with Google Imagen 3. Check your API Key and Model access.")
                        except Exception as e:
                            st.error(f"Error generating album art: {e}")

                # Generate Audio
                st.subheader("Audio Generation")
                with st.spinner("Synthesizing Audio..."):
                    audio_path = generate_audio(str(script_result), api_key, title, host_voice_id, guest_voice_id)
                    
                    st.audio(audio_path)
                    st.success("Podcast Generated Successfully!")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                # Cleanup
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

elif not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to proceed. (Google API Key is optional but required for Album Art generation).")
