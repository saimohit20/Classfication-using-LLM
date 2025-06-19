# FH/src/agents/gemini_agent.py

import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Corrected imports based on your file structure
from agents.models import DetectionResponse # This assumes 'agents' is a package relative to src
from prompts.prompt import DETECTION_PROMPT # This assumes 'prompts' is a package relative to src

from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.gemini import GeminiModel
 
# Load environment variables from .env
load_dotenv()

def detect_objects_from_image(image_path: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment.")

    file_extension = os.path.splitext(image_path)[1].lower()
    if file_extension == ".jpg" or file_extension == ".jpeg":
        media_type = "image/jpeg"
    elif file_extension == ".png":
        media_type = "image/png"
    else:
        raise ValueError(f"Unsupported image format: {file_extension}. Only .jpg and .png are supported.")

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    img_part = BinaryContent(data=img_bytes, media_type=media_type)

    model = GeminiModel("gemini-2.0-flash")
    agent = Agent(
        model=model,
        result_type=DetectionResponse,
        system_prompt=DETECTION_PROMPT,
    )

    try:
        response = agent.run_sync([img_part])
        return response.output.label_ids
    except Exception as e:
        print(f"Gemini agent error for {image_path}: {e}")
        return []

# Test snippet
if __name__ == "__main__":
    
    test_image_path = "data/selected_1000_llm/2023-09-01T06-51-11-891000Z.jpg" 
    if os.path.exists(test_image_path):
        print(f"Attempting to detect objects in: {test_image_path}")
        result = detect_objects_from_image(test_image_path)
        print(f"Detection result: {result}")
    else:
        print(f"Error: Test image not found at '{test_image_path}'. Please provide a valid path to a .jpg image in your 'data/selected_1000_llm' directory and ensure your GEMINI_API_KEY is set in a .env file in the FH root.")