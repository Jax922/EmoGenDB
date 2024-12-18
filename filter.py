# 
import os
import pandas as pd

dir_path = "/home/pci/dong/AIGC-image/MJ/1/"
csv_file = dir_path + "aggregated_data.csv"
imgs_path = dir_path + "imgs/"

# remove the non-extisting in the csv file
all_imgs_paths = []
pd_csv = pd.read_csv(csv_file)
for root, dirs, files in os.walk(imgs_path):
    for file in files:
        if file.endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(root, file)
            img_uuid = file.split(".")[0]
            if  not img_uuid in pd_csv["img_name"].values:
                # remove the non-extisting in the csv file
                os.remove(img_path)
                print(f"remove {img_path}")
            
            
