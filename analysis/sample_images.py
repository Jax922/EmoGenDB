#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sample 25 entries per emotion (balanced sampling),
copy images to a new folder, and update `image_path` in the new CSV.
"""

import os
import shutil
import pandas as pd

# ========== 1) 配置部分，根据实际情况修改 ==========

# 原始 CSV 文件
mj_csv = "/home/pci/dong/emodb/dong/AIGC-image/DiffusionDB/all_cleaned.csv"
# 采样后输出的新 CSV 文件路径
output_csv = "/home/pci/dong/emodb/dong/EmoGenDB/all_cleaned_5k_2.csv"
# 新建一个文件夹，用来保存采样到的图片
sample_images_folder = "/home/pci/dong/emodb/dong/EmoGenDB/sample_images_5k"

# 情绪列名（在原 CSV 中的列名）
emotion_column = "Emotion_Categorical"

# 定义情绪类别列表（与 CSV 中实际出现的情绪保持一致）
emotion_cat = [
    "Amusement", "Anger", "Awe", "Contentment",
    "Disgust", "Excitement", "Fear", "Sad"
]

# 每个情绪要采样多少张
SAMPLES_PER_CLASS = 625

# ========== 2) 读取原 CSV，并执行平衡抽样 ==========

df = pd.read_csv(mj_csv)

df["image_path"] = df["image_path"].str.replace(
        "/home/pci/dong/",
        "/home/pci/dong/emodb/dong/",
        regex=False
)



sampled_dfs = []

for cat in emotion_cat:
    subset = df[df[emotion_column] == cat]

    if len(subset) < SAMPLES_PER_CLASS:
        print(f"Warning: '{cat}' only has {len(subset)} records, taking all.")
        sampled_df = subset
    else:
        # 固定随机种子为 42，确保可复现。如需每次随机不同，可去掉 random_state
        sampled_df = subset.sample(n=SAMPLES_PER_CLASS, random_state=42)

    sampled_dfs.append(sampled_df)

final_df = pd.concat(sampled_dfs, ignore_index=True)

# ========== 3) 为存放样本图像，新建文件夹 ==========

os.makedirs(sample_images_folder, exist_ok=True)

# ========== 4) 复制采样到的图片，并更新 image_path ==========

# 假设原 CSV 里 image_path 列的列名是 "image_path"
IMAGE_PATH_COL = "image_path"

for i, row in final_df.iterrows():
    old_path = row[IMAGE_PATH_COL]
    print("old path", old_path)

    if not os.path.isfile(old_path):
        print(f"Warning: image file not found: {old_path}")
        # 也可以在这里做一些缺失处理，比如跳过或在 CSV 里标注
        continue

    # 获取图像文件名
    img_name = os.path.basename(old_path)
    # 准备复制到的新路径
    new_path = os.path.join(sample_images_folder, img_name)

    # 复制文件到新文件夹
    shutil.copy2(old_path, new_path)

    # 更新 CSV 中的 image_path 字段为新路径
    final_df.loc[i, IMAGE_PATH_COL] = new_path

# ========== 5) 保存更新后的新 CSV ==========
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

final_df.to_csv(output_csv, index=False, encoding="utf-8")

print("Balanced sampling done!")
print(f"Sampled images copied to: {sample_images_folder}")
print(f"New CSV with updated image_path saved to: {output_csv}")
