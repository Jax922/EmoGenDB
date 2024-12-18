# print the info of the image folder
import os

dir_path = "/home/pci/dong/AIGC-image/MJ/1/"
imgs_path = dir_path + "imgs/"

# print the how many images in the folder
all_imgs_paths = []
for root, dirs, files in os.walk(imgs_path):
    for file in files:
        if file.endswith((".jpg", ".jpeg", ".png")):
            all_imgs_paths.append(os.path.join(root, file))
print(f"Total images in the folder: {len(all_imgs_paths)}")