import os
import pandas as pd

def remove_all_target_columns(base_dir):
    """
    遍历所有子目录的 CSV 文件，删除所有与指定列相关的列。
    """
    target_columns = [
        "Average_Color", "Primary_Color", "Secondary_Color", "Brightness", "Contrast"
    ]

    for sub_dir in os.listdir(base_dir):
        sub_dir_path = os.path.join(base_dir, sub_dir)
        if not os.path.isdir(sub_dir_path):
            continue

        csv_file = os.path.join(sub_dir_path, "llm_result.csv")

        if not os.path.exists(csv_file):
            continue

        # 读取 CSV 文件
        df = pd.read_csv(csv_file)

        # 找到所有目标列及其重复版本
        columns_to_remove = [
            col for col in df.columns if any(col.startswith(target) for target in target_columns)
        ]

        # 删除目标列
        df = df.drop(columns=columns_to_remove)

        # 保存清理后的 CSV 文件
        df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    base_dir = "/home/pci/dong/AIGC-image/jouneryDB"  # 替换为你的实际目录路径
    remove_all_target_columns(base_dir)
