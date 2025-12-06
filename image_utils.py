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
        # Initialize client with v1beta API version which is often required for Imagen 3 on AI Studio
        client = genai.Client(api_key=api_key, http_options={'api_version': 'v1beta'})
        
        response = client.models.generate_images(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )
        
        # The response contains the image bytes
        for generated_image in response.generated_images:
            image_bytes = generated_image.image.image_bytes
            image = Image.open(BytesIO(image_bytes))
            return image
            
    except Exception as e:
        print(f"Error generating image with Google Imagen 3: {e}")
        # Return None to signal failure
        return None
