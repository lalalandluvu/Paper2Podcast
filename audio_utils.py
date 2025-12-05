from openai import OpenAI
import os

import re

def generate_audio(text, api_key, title="podcast", host_voice="alloy", guest_voice="echo"):
    """Generates audio from text using OpenAI TTS with multiple voices."""
    client = OpenAI(api_key=api_key)
    
    # Sanitize title for filename
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title) # Remove invalid chars
    safe_title = safe_title[:50].strip() # Truncate to 50 chars
    safe_title = safe_title[:50].strip() # Truncate to 50 chars
    
    # Ensure output directory exists
    output_dir = "generated podcasts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, f"{safe_title}.mp3")
    
    # Split the text by speaker
    # We use regex to find the speaker labels (Host: or Guest:)
    # We also handle potential markdown bolding like **Host:**
    segments = re.split(r'(\**Host\**:|Guest:|Researcher:)', text)
    
    # If no speakers found, just generate the whole thing
    if len(segments) < 2:
        return generate_single_audio(text, client, host_voice, output_path)
    
    audio_data = b""
    current_speaker = None # Start as None to skip metadata/titles
    
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
            
        # Check if this segment is just a label
        if re.match(r'^\**Host\**:$', segment) or segment in ["Guest:", "Researcher:"]:
            current_speaker = "Host" if "Host" in segment else "Guest"
            continue
            
        # If we haven't found a speaker yet, this is likely metadata/title text -> Skip it
        if current_speaker is None:
            continue

        # Determine voice based on speaker
        voice = host_voice if current_speaker == "Host" else guest_voice
        
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=segment
            )
            audio_data += response.content
        except Exception as e:
            print(f"Error generating audio for segment: {e}")

    with open(output_path, "wb") as f:
        f.write(audio_data)
        
    return output_path

def generate_single_audio(text, client, voice, output_path="output_podcast.mp3"):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    response.stream_to_file(output_path)
    return output_path
