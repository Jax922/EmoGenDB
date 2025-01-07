import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 读取人类标注的CSV文件
human_labels = pd.read_csv("/home/pci/dong/emodb/dong/EmoGenDB/anno-backend/human_anno_label.csv")

# 1. 情绪类别分布
emotion_dist = human_labels['emotion_categorical'].value_counts(normalize=True)
plt.figure(figsize=(8, 6))
sns.barplot(x=emotion_dist.index, y=emotion_dist.values)
plt.title("Emotion Categorical Distribution (Human)")
plt.ylabel("Percentage")
plt.xlabel("Emotion Category")
plt.show()

# 2. Valence/Arousal/Dominance 分布
for col in ['valence', 'arousal', 'dominance']:
    plt.figure(figsize=(8, 6))
    sns.histplot(human_labels[col], bins=30, kde=True)
    plt.title(f"{col.capitalize()} Distribution (Human)")
    plt.xlabel(col.capitalize())
    plt.ylabel("Frequency")
    plt.show()

# 3. 用户标注贡献
user_contribution = human_labels['user_id'].value_counts()
plt.figure(figsize=(8, 6))
sns.histplot(user_contribution, bins=20)
plt.title("User Contribution Distribution")
plt.xlabel("Number of Annotations")
plt.ylabel("Number of Users")
plt.show()

# 4. 标注一致性分析
std_valence = human_labels.groupby('img_name')['valence'].std()
plt.figure(figsize=(8, 6))
sns.histplot(std_valence, bins=30, kde=True)
plt.title("Valence Standard Deviation Across Images")
plt.xlabel("Standard Deviation")
plt.ylabel("Frequency")
plt.show()
