import os
import shutil

# 定义路径
base_dir = "/home/pci/dong/emodb/dong/AIGC-image/DiffusionDB"
group_imgs_dir = os.path.join(base_dir, "group_imgs")

# 检查 group_imgs 目录是否存在
if not os.path.exists(group_imgs_dir):
    print(f"目录 {group_imgs_dir} 不存在！")
else:
    # 遍历 group_imgs 下的子目录
    for sub_dir in os.listdir(group_imgs_dir):
        sub_dir_path = os.path.join(group_imgs_dir, sub_dir)

        # 如果是目录，将其移动到 base_dir
        if os.path.isdir(sub_dir_path):
            destination_path = os.path.join(base_dir, sub_dir)
            
            # 检查目标目录是否已存在
            if os.path.exists(destination_path):
                print(f"目标目录 {destination_path} 已存在，跳过移动 {sub_dir_path}！")
            else:
                try:
                    shutil.move(sub_dir_path, destination_path)
                    print(f"已移动：{sub_dir_path} -> {destination_path}")
                except Exception as e:
                    print(f"移动 {sub_dir_path} 时出错：{e}")
    
    print("操作完成！")
