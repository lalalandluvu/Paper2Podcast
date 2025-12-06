from google import genai
from google.genai import types
import base64
from io import BytesIO
from PIL import Image

def generate_album_art(prompt, api_key):
    """
    Generates an image using Google's Imagen 3 model via the google-genai library.
    
    Args:
        prompt (str): The prompt for the image.
        api_key (str): The Google Cloud API Key.
        
    Returns:
        PIL.Image.Image: The generated image object.
    """
    try:
        client = genai.Client(api_key=api_key)
        
        print("Trying model: gemini-2.5-flash-image")
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt],
        )
        
        for part in response.parts:
            if part.inline_data is not None:
                return part.as_image()
                
    except Exception as e:
        print(f"Error generating image with Gemini 2.5 Flash: {e}")
        return None
