

import os
import pandas as pd
from tqdm import tqdm
import shutil

def move_imgs(output_dir):
    # 遍历目录中的图片文件，创建一个imgs 目录，把所有图片移动到imgs目录下
    imgs_dir = os.path.join(output_dir, "imgs")
    os.makedirs(imgs_dir, exist_ok=True)
    for root, dirs, files in os.walk(output_dir):
        for file in tqdm(files):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                shutil.move(file_path, os.path.join(imgs_dir, file))
                print(f"Moved {file} to {imgs_dir}")
                    
def traverse_all_subdirectories(base_dir):
    """
    遍历 base_dir 目录下的所有子目录，并处理每个子目录中的文件。
    """
    for i in range(42, 45):  # 假设目录名称是 1 到 22
        sub_dir = os.path.join(base_dir, f"mj{i}")
        if os.path.exists(sub_dir) and os.path.isdir(sub_dir):
            print(f"Processing directory: {sub_dir}")
            move_imgs(sub_dir)
    

# 使用示例
if __name__ == "__main__":
    # 主 CSV 文件路径

    # 子目录主路径
    output_dir = "/home/pci/dong/AIGC-image/jouneryDB-2"

    # 为每个子目录生成对应的 CSV 文件
    # generate_csv_per_directory(csv_path, output_dir)
    traverse_all_subdirectories(output_dir)
