import os
import pandas as pd

# 主目录路径
base_dir = "/home/pci/dong/AIGC-image/MJ/"

# 遍历所有子目录
for subdir in os.listdir(base_dir):
    subdir_path = os.path.join(base_dir, subdir)
    if not os.path.isdir(subdir_path):
        continue  # 跳过非目录项

    # 子目录中的 CSV 文件路径
    csv_path = os.path.join(subdir_path, "llm_result.csv")
    imgs_dir = os.path.join(subdir_path, "imgs")

    if not os.path.exists(csv_path) or not os.path.exists(imgs_dir):
        print(f"跳过子目录 {subdir}: 找不到 CSV 或 imgs 目录")
        continue

    # 读取 CSV 文件
    df = pd.read_csv(csv_path)

    # 增加 image_path 列
    image_paths = []
    for img_name in df["img_name"]:
        # 在 imgs 目录中查找匹配的图片文件（忽略大小写）
        found_image = None
        for ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
            candidate_path = os.path.join(imgs_dir, f"{img_name}{ext}")
            if os.path.exists(candidate_path):
                found_image = candidate_path
                break

        if found_image:
            image_paths.append(found_image)
        else:
            print(f"警告: {img_name} 在 {imgs_dir} 中未找到对应的图片文件")
            image_paths.append(None)  # 如果未找到图片，则设置为 None

    # 将 image_path 列添加到 DataFrame
    df["image_path"] = image_paths

    # 保存回 CSV 文件
    output_csv_path = os.path.join(subdir_path, "llm_result_with_paths.csv")
    df.to_csv(output_csv_path, index=False)
    print(f"已更新 {subdir} 中的 llm_result.csv，保存到 {output_csv_path}")

print("处理完成！")
