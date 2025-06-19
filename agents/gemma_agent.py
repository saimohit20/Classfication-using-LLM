import base64
import json
import sys
import requests
import re
import os 
from dotenv import load_dotenv 
from agents.models import DetectionResponse
from prompts.prompt import DETECTION_PROMPT


API_KEY = "sk-c33cca75fbfd49cfae31d6b9112320e4"
FILE_PATH = "D:\\Kiel\\FH\\data\\selected_1000_llm\\2023-09-01T06-51-11-891000Z.jpg"
MODEL = "gemma3:27b"
API_URL = "http://localhost:3000/api/chat/completions"

def encode_image_to_base64(path):
    
    file_extension = os.path.splitext(path)[1].lower()
    if file_extension == ".jpg" or file_extension == ".jpeg":
        media_type = "image/jpeg"
    elif file_extension == ".png":
        media_type = "image/png"
    else:
        raise ValueError(f"Unsupported image format: {file_extension}. Only .jpg and .png are supported.")

    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:{media_type};base64,{encoded}"

def extract_json_label_ids(text):
    
    candidates = re.findall(r'\{.*?\}', text, re.DOTALL)
    for c in candidates:
        try:
            raw = json.loads(c)
            validated = DetectionResponse(**raw)
            return validated.label_ids
        except Exception as e:
            continue
    return []

def call_gemma_model(image_path: str):
    image_base64 = encode_image_to_base64(image_path)

    messages_content = [
        {
            "type": "image_url",
            "image_url": {
                "url": image_base64
            }
        },
        {
            "type": "text",
            "text": DETECTION_PROMPT
        }
    ]

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": messages_content
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"


    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        detected_label_ids = extract_json_label_ids(answer)
        return detected_label_ids
    except requests.exceptions.RequestException as e:
        print(f"Gemma API request error for {image_path}: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Gemma API JSON decode error for {image_path}: {e}")
        print(f"Raw response content: {response.text}")
        return []
    except Exception as e:
        print(f"Unexpected error in call_gemma_model for {image_path}: {e}")
        return []

if __name__ == "__main__":
   

    test_image_path = "D:\\Kiel\\FH\\data\\selected_1000_llm\\2023-09-01T06-51-11-891000Z.jpg"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(current_dir, '..', '..')))

    if os.path.exists(test_image_path):
        print(f"Attempting to detect objects in: {test_image_path}")
        result_label_ids = call_gemma_model(test_image_path)
        print(f"Detection result (label IDs): {result_label_ids}")
    else:
        print(f"Error: Test image not found at '{test_image_path}'. Please provide a valid path to a .jpg image in your 'data/selected_1000_llm' directory.")
