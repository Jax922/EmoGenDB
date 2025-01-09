import pandas as pd

# 读取两个 CSV 文件
file1 = "/root/dev/EmoGenDB/all_cleaned_5k_1.csv"  # 替换为第一个 CSV 文件路径
file2 = "/root/dev/EmoGenDB/all_cleaned_5k_2.csv"  # 替换为第二个 CSV 文件路径

# 加载数据
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# 替换 image_path 中的路径
df1['image_path'] = df1['image_path'].str.replace('/home/pci/dong/emodb/dong/', '/root/dev/', regex=False)
df2['image_path'] = df2['image_path'].str.replace('/home/pci/dong/emodb/dong/', '/root/dev/', regex=False)

# 检查结果
print("File 1 after replacement:\n", df1['image_path'].head())
print("File 2 after replacement:\n", df2['image_path'].head())

# 可选择保存结果
df1.to_csv("updated_file1.csv", index=False)
df2.to_csv("updated_file2.csv", index=False)