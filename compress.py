import os
from PIL import Image
from tqdm import tqdm

dir_path = "/home/pci/dong/emodb/dong/AIGC-image/DiffusionDB/group_imgs/"

def compress_image(image_path, output_image_path, quality=50):
    """
    Compress a single image to a specified quality.
    """
    try:
        image = Image.open(image_path)
        image = image.convert("RGB")  # Ensure compatibility with JPEG format
        image.save(output_image_path, format="JPEG", quality=quality, optimize=True)
    except Exception as e:
        print(f"Error compressing {image_path}: {e}")

def process_directory(directory_path):
    """
    Compress all images in the 'imgs' directory inside the given directory path.
    """
    imgs_path = os.path.join(directory_path, "imgs")
    if not os.path.exists(imgs_path):
        return  # Skip directories without 'imgs' folder

    # Find all image files in the 'imgs' folder
    image_files = [
        os.path.join(imgs_path, file)
        for file in os.listdir(imgs_path)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    
    # Compress each image
    for image_path in tqdm(image_files, desc=f"Processing {imgs_path}"):
        try:
            suffix = image_path.split(".")[-1]
            output_image_path = image_path.replace(f".{suffix}", f"_compressed.{suffix}")
            
            # Compress the image
            compress_image(image_path, output_image_path)
            
            # Replace the original file with the compressed file
            os.remove(image_path)
            os.rename(output_image_path, image_path)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

# Traverse the top-level directory and process each subdirectory
for root, dirs, files in os.walk(dir_path):
    for subdir in tqdm(dirs):
        print(f"Processing directory: {subdir}")
        process_directory(os.path.join(root, subdir))
        print("=================================Done!=================================")
