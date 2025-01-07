import os
import pandas as pd

# Define the base directory and output file
base_dir = "/home/pci/dong/emodb/dong/AIGC-image/DiffusionDB/"
output_file = os.path.join(base_dir, "all.csv")

# List to store DataFrame from each file
dataframes = []

# Iterate through each subfolder
for subfolder in os.listdir(base_dir):
    subfolder_path = os.path.join(base_dir, subfolder)
    csv_file_path = os.path.join(subfolder_path, "llm_result_with_paths.csv")
    if os.path.isdir(subfolder_path) and os.path.exists(csv_file_path):
        # Read the CSV file and append to the list
        df = pd.read_csv(csv_file_path)
        dataframes.append(df)

# Concatenate all DataFrames
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a CSV file
combined_df.to_csv(output_file, index=False)

output_file
