import pandas as pd
import os


def re_name(dir_path):
# dir_path = "/home/pci/dong/AIGC-image/jouneryDB/mj5/"
    csv_file = dir_path + "aggregated_data.csv"
    df = pd.read_csv(csv_file)
    # rename img_name and remove the suffix ".jpg"
    df["img_name"] = df["img_name"].apply(lambda x: x.split(".")[0])
    # rename prompt to prompt_text
    df = df.rename(columns={"prompt": "prompt_text"})
    df.to_csv(csv_file, index=False)

def traverse_all_subdirectories(base_dir):
    """
    遍历 base_dir 目录下的所有子目录，并处理每个子目录中的文件。
    """
    for i in range(12, 23):  # 假设目录名称是 1 到 22
        sub_dir = os.path.join(base_dir, f"mj{i}/")
        if os.path.exists(sub_dir) and os.path.isdir(sub_dir):
            print(f"Processing directory: {sub_dir}")
            re_name(sub_dir)

base_dir = "/home/pci/dong/AIGC-image/jouneryDB/"
traverse_all_subdirectories(base_dir)