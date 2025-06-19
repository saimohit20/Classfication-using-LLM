import os
import pandas as pd  # Import the pandas library

def extract_ground_truth_to_dataframe(folder_path):
    data_for_df = []  # List to hold dictionaries, one for each row in the DataFrame

    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            image_id = os.path.splitext(filename)[0]  # Use filename (without extension) as ImageID
            class_labels = []

            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if parts:
                            try:
                                class_labels.append(int(parts[0]))
                            except ValueError:
                                print(f"Warning: Could not parse class label in file {filename}, line: {line.strip()}")
                
                # Append a dictionary for the current file's data
                data_for_df.append({'ImageID': image_id, 'Labels': class_labels})
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
    
    # Create the DataFrame from the list of dictionaries
    df = pd.DataFrame(data_for_df)
    return df

# --- How to use the script ---
if __name__ == "__main__":
    # Replace with the actual path to your folder
    folder_path = 'D:\\Kiel\\FH\\data\\selected_1000_llm'  # <--- IMPORTANT: CHANGE THIS PATH

    if not os.path.exists(folder_path):
        print(f"Error: Folder not found at '{folder_path}'. Please update the 'folder_path' variable.")
    else:
        ground_truth_df = extract_ground_truth_to_dataframe(folder_path)

        if not ground_truth_df.empty:
            print("Ground Truth DataFrame:")
            print(ground_truth_df.head()) 
            print(f"\nDataFrame shape: {ground_truth_df.shape}")

            # Save the DataFrame to an Excel file
            output_excel_path = os.path.join(folder_path, 'ground_truth_labels.xlsx')
            try:
                ground_truth_df.to_excel(output_excel_path, index=False)
                print(f"\nDataFrame successfully saved to Excel at: {output_excel_path}")
            except Exception as e:
                print(f"Error saving DataFrame to Excel: {e}")
        else:
            print(f"No ground truth data found or extracted into DataFrame from '{folder_path}'.")
