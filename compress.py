#
#

import os
from PIL import Image
from tqdm import tqdm
    
dir_path = "/home/pci/dong/AIGC-image/MJ/1/"

# traverse the dir_path all images and compress them

def compress_image(image_path, output_image_path):
    image = Image.open(image_path)
    image.save(output_image_path, format="JPEG", quality=50, optimize=True)

for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith((".jpg", ".jpeg", ".png")):
            suffix = file.split(".")[-1]
            image_path = os.path.join(root, file)
            output_image_path = image_path.replace(f".{suffix}", f"_compressed.{suffix}")
            compress_image(image_path, output_image_path)
            os.remove(image_path)
            os.rename(output_image_path, image_path)
            print(f"Compressed {image_path}")