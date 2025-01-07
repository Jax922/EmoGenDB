import os
import csv
import cv2
import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm

def calculate_image_features(image_path, num_clusters=3):
    """
    计算图片特征：平均色调、主色调、次主色调、亮度和对比度
    """
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Cannot read image at {image_path}")
        return None
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 平均色调
    avg_color = np.mean(image, axis=(0, 1))

    # 主色调和次主色调
    pixels = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(pixels)
    dominant_colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    label_counts = np.bincount(labels)

    # 按像素数量排序
    sorted_indices = np.argsort(label_counts)[::-1]
    primary_color = dominant_colors[sorted_indices[0]]
    secondary_color = dominant_colors[sorted_indices[1]] if len(sorted_indices) > 1 else [0, 0, 0]

    # 亮度
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    brightness = np.mean(gray_image)

    # 对比度
    contrast = np.std(gray_image)

    return avg_color, primary_color, secondary_color, brightness, contrast


def process_csv_and_images(base_dir):
    """
    遍历所有子目录，逐行处理 CSV 文件，并实时写入计算结果
    """
    for subdir in tqdm(os.listdir(base_dir)):
        print(f"Processing {subdir}...")
        subdir_path = os.path.join(base_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue

        # 子目录中的 imgs 文件夹和 llm_result.csv
        imgs_folder = os.path.join(subdir_path, "imgs")
        csv_file = os.path.join(subdir_path, "llm_result.csv")

        if not os.path.exists(imgs_folder) or not os.path.exists(csv_file):
            print(f"Skipping {subdir_path}: Missing imgs folder or CSV file.")
            continue

        # 临时文件，用于实时写入更新后的数据
        temp_csv_file = os.path.join(subdir_path, "llm_result_temp.csv")

        # 读取 CSV 文件
        with open(csv_file, 'r', encoding='utf-8') as file_in, open(temp_csv_file, 'w', encoding='utf-8', newline='') as file_out:
            reader = csv.DictReader(file_in)
            headers = reader.fieldnames

            # 检查是否需要添加新列
            new_columns = ["Average_Color", "Primary_Color", "Secondary_Color", "Brightness", "Contrast"]
            if not all(col in headers for col in new_columns):
                headers += [col for col in new_columns if col not in headers]

            writer = csv.DictWriter(file_out, fieldnames=headers)
            writer.writeheader()

            for row in reader:
                # img  name 可以 尝试多个后缀
                img_name = row["img_name"] + ".jpg"
                image_path = os.path.join(imgs_folder, img_name)
                if not os.path.exists(image_path):
                    image_path = os.path.join(imgs_folder, img_name.replace(".jpg", ".jpeg"))
                    if not os.path.exists(image_path):
                        image_path = os.path.join(imgs_folder, img_name.replace(".jpg", ".png"))
                        if not os.path.exists(image_path):
                            print(f"Warning: Image not found at {image_path}.")
                            continue

                # 跳过已计算的行
                if all(col in row and row[col] for col in new_columns):
                    writer.writerow(row)
                    continue

                # 如果图片存在，则计算特征
                if os.path.exists(image_path):
                    features = calculate_image_features(image_path)
                    if features:
                        avg_color, primary_color, secondary_color, brightness, contrast = features
                        # 保存为逗号分隔的字符串
                        row["Average_Color"] = ":".join(map(str, map(int, avg_color)))
                        row["Primary_Color"] = ":".join(map(str, map(int, primary_color)))
                        row["Secondary_Color"] = ":".join(map(str, map(int, secondary_color)))
                        row["Brightness"] = round(brightness, 2)
                        row["Contrast"] = round(contrast, 2)
                        # print(f"Updated {img_name} with calculated features.")
                    else:
                        print(f"Warning: Failed to compute features for {image_path}.")
                else:
                    print(f"Warning: Image not found at {image_path}.")

                writer.writerow(row)

        # 用临时文件替换原 CSV 文件
        os.replace(temp_csv_file, csv_file)


if __name__ == "__main__":
    base_dir = "/home/pci/dong/emodb/dong/AIGC-image/DiffusionDB"  # 替换为你的实际路径
    process_csv_and_images(base_dir)
