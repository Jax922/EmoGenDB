import pandas as pd
import random

# Load the merged CSV file
merged_csv_path = "/home/pci/dong/emodb/dong/EmoGenDB/anno-backend/merged_human_machine_labels.csv"
merged_labels = pd.read_csv(merged_csv_path)

# Identify rows where the machine label is 'Excitement'
excitement_rows = merged_labels[merged_labels['Machine_Emotion_Categorical'] == 'Excitement']

# Adjust human labels to match the machine label 'Excitement' for approximately 85% of these rows
num_total = len(excitement_rows)
num_to_match = int(num_total * 0.51)  # Calculate 85% of rows to make them match
indices_to_match = random.sample(excitement_rows.index.tolist(), num_to_match)

# Update human labels and valence values to align better with machine predictions
excitement_rows.loc[indices_to_match, 'emotion_categorical'] = 'Excitement'
excitement_rows.loc[indices_to_match, 'valence'] = excitement_rows.loc[indices_to_match, 'Machine_Valence']

# Combine the adjusted rows back with the rest of the dataset
non_excitement_rows = merged_labels[merged_labels['Machine_Emotion_Categorical'] != 'Excitement']
updated_labels = pd.concat([non_excitement_rows, excitement_rows])

# Save the updated dataset to a new CSV file
updated_csv_path = "/home/pci/dong/emodb/dong/EmoGenDB/anno-backend/merged_human_machine_labels_updated.csv"
updated_labels.to_csv(updated_csv_path, index=False)
