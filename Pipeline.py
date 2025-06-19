# FH/src/pipeline.py

import os
import sys
import pandas as pd
import re
#import syslog
from agents.gemma_agent import call_gemma_model
from agents.gemini_agent import detect_objects_from_image

def run_pipeline(input_dir: str, output_excel_path: str, model_choice: str, num_images_to_process: int = 10):
   
    print(f"\nStarting classification pipeline...")
    print(f"Input directory       : {input_dir}")
    print(f"Output Excel Path     : {output_excel_path}")
    print(f"Model selected        : {model_choice}\n")

    if num_images_to_process is not None:
        print(f"Processing first {num_images_to_process} images for testing...\n")
    else:
        print("Processing all images...\n")

    model_func = detect_objects_from_image if model_choice.lower() == "gemini" else call_gemma_model

    results_data = []

    image_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith((".jpg", ".jpeg"))
    ]
    
    if num_images_to_process is not None:
        images_to_process = image_files[:num_images_to_process]
    else:
        images_to_process = image_files

    if not images_to_process:
        print(f"No JPG/JPEG images found in {input_dir} or no images to process based on limit.")
        return

    for file_path in images_to_process:

        filename = os.path.basename(file_path)
        match = re.match(r"([^.]+)\.(jpg|jpeg)", filename, re.IGNORECASE)
        image_id = match.group(1) if match else filename 

        print(f"Processing: {filename} (ImageID: {image_id})")
        
        try:
            # calling the LLM function
            label_ids = model_func(file_path) 
            print(f"Detected Label IDs: {label_ids}")

            results_data.append({
                "ImageID": image_id,
                "Labels": label_ids
            })
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            results_data.append({
                "ImageID": image_id,
                "Labels": [] 
            })
        print("-" * 30) 

    
    if results_data:
        df = pd.DataFrame(results_data)
        
        try:
            df.to_excel(output_excel_path, index=False)
            print(f"\nPipeline finished. Results saved to: {output_excel_path}")
        except Exception as e:
            print(f"Error saving DataFrame to Excel: {e}")
            print(f"Please ensure the file '{output_excel_path}' is not open and you have write permissions.")
    else:
        print("\nNo data processed. DataFrame not created.")


if __name__ == "__main__":
    
    print("Image Classification Pipeline using LLMs")
    input_dir = "D:\\Kiel\\FH\\data\\selected_1000_llm"
    output_excel_file_name = "output_detection_results.xlsx" 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_excel_path = os.path.join(script_dir, '..', output_excel_file_name)
    
    model_choice = input("Choose model (gemma/gemini): ").strip().lower()

    if not os.path.isdir(input_dir):
        print(f"Error: Input directory not found at '{os.path.abspath(input_dir)}'. Please ensure it exists.")
    elif model_choice not in ["gemma", "gemini"]:
        print("Invalid model choice. Please choose 'gemma' or 'gemini'.")
    else:

        sys.path.insert(0, os.path.abspath(os.path.join(script_dir, '..')))
        run_pipeline(input_dir, output_excel_path, model_choice, num_images_to_process=10)
        