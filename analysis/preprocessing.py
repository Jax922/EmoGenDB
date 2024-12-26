import pandas as pd

# 定义情感标签映射规则
emotion_mapping = {
    "Amusement": "Amusement",
    "Anger": "Anger",
    "Awe": "Awe",
    "Contentment": "Contentment",
    "Disgust": "Disgust",
    "Excitement": "Excitement",
    "Fear": "Fear",
    "Sad": "Sad",
    # 以下是需要映射的其他标签
    "Happiness": "Contentment",
    "Joy": "Contentment",
    "Surprise": "Excitement",
    "Curiosity": "Excitement",
    "Anxiety": "Fear",
    "Confusion": "Fear",
    "Frustration": "Anger",
    "Calm": "Contentment",
    "Nostalgia": "Sad",
    "Thoughtfulness": "Sad",
    # 其他不在 Mikels 模型中的情感标签映射为 None 或 "Unknown"
    "Neutral": "Neutral",
    "Contempt": "Disgust",
    # 自定义处理
    "Puzzlement": "Confusion",  # 如果不需要此标签，可以设置为 None
    
    "Concentration": "Excitement",
    "Skepticism": "Fear",
    "Contemplation": "Sad",
    "Seriousness": "Sad",
    "Serenity": "Contentment",
}

# 读取 CSV 文件
input_csv = "/home/pci/dong/AIGC-image/MJ/all.csv"  # 替换为你的文件名
output_csv = "/home/pci/dong/AIGC-image/MJ/all_cleaned.csv"

df = pd.read_csv(input_csv)

# 假设情感标签列名为 "Emotion"
if "Emotion_Categorical" not in df.columns:
    raise ValueError("CSV 文件中未找到 'Emotion_Categorical' 列，请检查列名是否正确。")

df["Emotion_Categorical"] = df["Emotion_Categorical"].str.strip().str.title()
df["Emotion_Categorical"] = df["Emotion_Categorical"].str.replace(r"[^\w\s]", "", regex=True)
# 将情感标签映射到 Mikels 模型
df["Emotion_Categorical"] = df["Emotion_Categorical"].map(emotion_mapping)

# 如果你希望去掉未映射的情感标签（即 None 值）
df = df[df["Emotion_Categorical"].notna()]

# 保存结果到新的 CSV 文件
df.to_csv(output_csv, index=False)

print(f"转换完成，结果已保存到 {output_csv}")
