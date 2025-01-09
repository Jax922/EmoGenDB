import sqlite3
import pandas as pd

# 数据库路径
db_path = "./emotions.db"
# CSV 文件路径
# csv_path = "/home/pci/dong/emodb/dong/AIGC-image/MJ/all_cleaned_vicuna7b_balanced25.csv"
csv_path = "/root/dev/EmoGenDB/updated_file2.csv"

# 用户数量（从1开始分配用户 ID，假设有 10 个用户）
num_users = 10

# 连接到 SQLite 数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 确保 image_assignments 表存在
cursor.execute('''
    CREATE TABLE IF NOT EXISTS image_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        img_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        is_annotated INTEGER DEFAULT 0,
        FOREIGN KEY (img_id) REFERENCES images (id)
    )
''')
conn.commit()

# 读取 CSV 文件
df = pd.read_csv(csv_path)

# 插入数据到 images 表并分配用户
user_id = 11
assignments = []

for _, row in df.iterrows():
    # 检查是否已存在此图片
    cursor.execute("SELECT id FROM images WHERE img_name = ?", (row["img_name"],))
    img_id = cursor.fetchone()

    if not img_id:
        # 如果图片未存在，插入到 images 表
        cursor.execute('''
            INSERT INTO images (
                img_name, caption, emotion_categorical, valence, arousal, 
                dominance, annotation_count, image_path
            ) VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        ''', (
            row["img_name"],
            row["Caption"],
            row["Emotion_Categorical"],
            row["Valence"],
            row["Arousal"],
            row["Dominance"],
            row["image_path"]
        ))
        img_id = cursor.lastrowid  # 获取新插入记录的 ID
    else:
        img_id = img_id[0]  # 图片已存在，获取 ID

    # 为当前图片分配用户（分配 10 次）
    for _ in range(num_users):
        assignments.append((img_id, user_id))
        user_id += 1
        if user_id > 20:
            user_id = 11  # 循环分配用户

# 批量插入到 image_assignments 表
cursor.executemany('''
    INSERT INTO image_assignments (img_id, user_id, is_annotated)
    VALUES (?, ?, 0)
''', assignments)

# 提交并关闭连接
conn.commit()
conn.close()

print("图片分配完成！")
