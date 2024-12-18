
import os
import sys
import json
from PIL import Image
from tqdm import tqdm
import csv
import re
import shutil

dir_path = "/home/pci/dong/AIGC-image/MJ/2/"
csv_file = dir_path + "aggregated_data.csv"
imgs_path = dir_path + "imgs/"

def resize_image(input_path, output_path, max_size=512, quality=85):
    """
    调整图像大小并压缩。
    
    :param input_path: 输入图像路径
    :param output_path: 输出图像路径
    :param max_size: 调整后的图像最大宽度或高度
    :param quality: 保存图像的压缩质量（1-100）
    """
    # 打开图像
    image = Image.open(input_path)
    
    # 获取原始尺寸
    original_width, original_height = image.size
    
    # 计算缩放比例
    width_ratio = max_size / original_width
    height_ratio = max_size / original_height
    
    # 选择较小的比例以保持宽高比
    scale_factor = min(width_ratio, height_ratio, 1)  # 确保不放大图像
    
    # 计算新的尺寸
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    
    # 调整图像大小
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # 保存图像并指定压缩质量
    resized_image.save(output_path, quality=quality, optimize=True)
    
    # print(f"图像已保存到 {output_path}，新尺寸为 {new_width}x{new_height}，压缩质量为 {quality}")



for root, dirs, files in os.walk(imgs_path):
    print(f"Processing {root}...")
    for file in tqdm(files):
        if file.endswith((".jpg", ".jpeg", ".png")):
            suffix = file.split(".")[-1]
            image_path = os.path.join(root, file)
            output_image_path = image_path.replace(f".{suffix}", f".{suffix}")
            resize_image(image_path, output_image_path)