import os
import base64
import requests
from typing import Optional, Dict, Any, List
from openai import OpenAI
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ImageGenerator:
    """
    Handles the generation of images using OpenAI's DALL-E model.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the ImageGenerator with an API key.
        
        Args:
            api_key: OpenAI API key for image generation
        """
        self.api_key = api_key or os.environ.get("OPEN_AI_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it as an environment variable or pass it as a parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> Dict[str, Any]:
        """
        Generate an image using OpenAI's DALL-E model.
        
        Args:
            prompt: The text prompt to generate an image from
            size: Size of the generated image (e.g., "1024x1024", "512x512")
            quality: Quality of the generated image ("standard" or "hd")
            
        Returns:
            A dictionary containing the image URL and metadata
        """
        try:
            # Append instructions to avoid text in the image
            enhanced_prompt = f"{prompt} Create this as a clear educational diagram WITHOUT any text or labels. Do not include any text in the image."
            
            # Use DALL-E 2 which is more widely available
            response = self.client.images.generate(
                model="dall-e-2",  # Specify DALL-E 2 explicitly
                prompt=enhanced_prompt,
                n=1,  # Number of images to generate
                size=size,
                # quality parameter not needed for DALL-E 2
                response_format="url"  # Get a URL instead of base64 data
            )
            
            return {
                "url": response.data[0].url,
                "prompt": prompt,
                "enhanced_prompt": enhanced_prompt,
                "size": size,
                "success": True
            }
        except Exception as e:
            print(f"Error generating image: {e}")
            return {
                "url": None,
                "prompt": prompt,
                "size": size,
                "success": False,
                "error": str(e)
            }
    
    def save_image(self, url: str, output_path: str) -> bool:
        """
        Download and save an image from a URL.
        
        Args:
            url: URL of the image to download
            output_path: Path to save the image to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def generate_multiple(self, prompts: List[Dict[str, Any]], output_dir: str = None) -> List[Dict[str, Any]]:
        """
        Generate multiple images from a list of prompts.
        
        Args:
            prompts: List of prompt dictionaries with "prompt", optional "size", and optional "quality"
            output_dir: Directory to save images to (optional)
            
        Returns:
            List of dictionaries with image URLs and metadata
        """
        results = []
        
        # Create output directory if it doesn't exist
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for i, prompt_data in enumerate(prompts):
            prompt = prompt_data["prompt"]
            size = prompt_data.get("size", "1024x1024")
            quality = prompt_data.get("quality", "standard")
            
            # Generate the image
            result = self.generate_image(prompt, size, quality)
            result["id"] = prompt_data.get("id", f"image_{i+1}")
            
            # Save the image if output_dir is provided and generation was successful
            if output_dir and result["success"] and result["url"]:
                image_filename = f"{result['id']}.png"
                image_path = os.path.join(output_dir, image_filename)
                save_success = self.save_image(result["url"], image_path)
                result["local_path"] = image_path if save_success else None
            
            results.append(result)
        
        return results 