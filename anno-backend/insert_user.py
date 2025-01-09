import sqlite3

# 连接到 SQLite 数据库（如果数据库不存在，会自动创建）
db_path = 'emotions.db'  # 替换为你的数据库文件路径
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建 accounts 表（如果表不存在）
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# 插入数据
try:
    for i in range(1, 21):  # 从 1 到 20
        username = str(i)
        password = str(i)
        cursor.execute('''
        INSERT INTO accounts (username, password)
        VALUES (?, ?)
        ''', (username, password))

    # 提交事务
    conn.commit()
    print("数据插入成功！")

except sqlite3.Error as e:
    # 如果发生错误，回滚事务
    conn.rollback()
    print(f"数据插入失败: {e}")

finally:
    # 关闭数据库连接
    conn.close()