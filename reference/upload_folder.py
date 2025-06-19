import os
import base64
import requests

# === Settings ===
api_url = "http://localhost:3000/api/chat/completions"
api_key = ""
model = "gemma3:12b"
folder_path = "images"  # Folder with input images
output_text_path = "found_descriptions"  # Folder to save the output text descriptions

# === Create output folder if it doesn't exist ===
os.makedirs(output_text_path, exist_ok=True)

# === Function to encode image to base64 ===
def encode_image_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# === Iterate over all images in the folder ===
for filename in os.listdir(folder_path):
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue  # Skip non-image files

    file_path = os.path.join(folder_path, filename)
    image_base64 = encode_image_base64(file_path)

    print(f"\n📸 Processing: {filename}")

    # === Prepare request payload ===
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What can you see on the image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer sk-c33cca75fbfd49cfae31d6b9112320e4",
        "Content-Type": "application/json"
    }

    # === Send request to the model ===
    response = requests.post(api_url, json=payload, headers=headers)

    # Prepare path for saving the response
    txt_filename = os.path.splitext(filename)[0] + ".txt"
    output_file = os.path.join(output_text_path, txt_filename)

    if response.status_code == 200:
        result = response.json()
        message = result["choices"][0]["message"]["content"]
        print(f"✅ Model response: {message}")

        # Save response to a text file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(message)

    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        # Save error message to a text file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"[Request Error]: {response.status_code}\n{response.text}")
