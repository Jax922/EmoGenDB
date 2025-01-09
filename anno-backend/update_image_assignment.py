import sqlite3

# 连接到 SQLite 数据库（如果数据库不存在，会自动创建）
db_path = 'emotions.db'  # 替换为你的数据库文件路径
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 更新 user_id 从 11 到 10
    update_query = """
    UPDATE image_assignments
    SET user_id = 10
    WHERE user_id = 11;
    """
    cursor.execute(update_query)

    # 提交事务
    conn.commit()
    print("更新成功！")

except sqlite3.Error as e:
    # 如果发生错误，回滚事务
    conn.rollback()
    print(f"更新失败: {e}")

finally:
    # 关闭数据库连接
    conn.close()