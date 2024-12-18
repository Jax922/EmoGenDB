
import os
from PIL import Image
from tqdm import tqdm
    
dir_path = "/home/pci/dong/AIGC-image/MJ/1/"

def resize_image(input_path, output_path, max_size=512):
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
    # 保存调整后的图像
    resized_image.save(output_path)
    print(f"图像已保存到 {output_path}，新尺寸为 {new_width}x{new_height}")


for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith((".jpg", ".jpeg", ".png")):
            suffix = file.split(".")[-1]
            image_path = os.path.join(root, file)
            output_image_path = image_path.replace(f".{suffix}", f".{suffix}")
            resize_image(image_path, output_image_path)
            # os.remove(image_path)
            # os.rename(image_path, output_image_path)
            # print(f"reszie {image_path}")
