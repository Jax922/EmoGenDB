import sqlite3
import pandas as pd

# 数据库路径
db_path = "./emotions.db"
# CSV 文件路径
csv_path = "/root/dev/EmoGenDB/updated_file1.csv"

# 连接到 SQLite 数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查并添加缺少的字段
cursor.execute('''
    ALTER TABLE images ADD COLUMN image_path TEXT
''')
conn.commit()

# 创建表（如果表不存在，则创建）
cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        img_name TEXT UNIQUE NOT NULL,
        caption TEXT,
        emotion_categorical TEXT,
        valence REAL,
        arousal REAL,
        dominance REAL,
        annotation_count INTEGER DEFAULT 0,
        image_path TEXT
    )
''')
conn.commit()

# 读取 CSV 文件
df = pd.read_csv(csv_path)

# 插入数据
for _, row in df.iterrows():
    try:
        cursor.execute('''
            INSERT INTO images (
                img_name, caption, emotion_categorical, valence, arousal, 
                dominance, image_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row["img_name"],
            row["Caption"],
            row["Emotion_Categorical"],
            row["Valence"],
            row["Arousal"],
            row["Dominance"],
            row["image_path"]
        ))
    except sqlite3.IntegrityError:
        print(f"Skipping duplicate entry for img_name: {row['img_name']}")
    except Exception as e:
        print(f"Error inserting row: {e}")

# 提交事务并关闭连接
conn.commit()
conn.close()

print("Data synchronized successfully!")
