import sqlite3

# 数据库路径
DB_PATH = "./emotions.db"  # 请替换为你的实际数据库路径

def delete_image_assignments(user_id):
    """
    删除 image_assignments 表中所有指定 user_id 的记录。
    
    参数：
    - user_id (int): 要删除的用户ID
    """
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 打印删除前的记录数（可选，用于验证）
        cursor.execute("SELECT COUNT(*) FROM image_assignments WHERE user_id = ?", (user_id,))
        count_before = cursor.fetchone()[0]
        print(f"删除前，user_id={user_id} 的记录数：{count_before}")
        
        # 执行删除操作
        cursor.execute("DELETE FROM image_assignments WHERE user_id = ?", (user_id,))
        
        # 获取删除的记录数
        deleted_rows = cursor.rowcount
        print(f"已删除 {deleted_rows} 条记录。")
        
        # 提交事务
        conn.commit()
        
        # 可选：再次查询以确认删除
        cursor.execute("SELECT COUNT(*) FROM image_assignments WHERE user_id = ?", (user_id,))
        count_after = cursor.fetchone()[0]
        print(f"删除后，user_id={user_id} 的记录数：{count_after}")
        
    except sqlite3.Error as e:
        print(f"SQLite 错误: {e}")
        if conn:
            conn.rollback()  # 回滚事务
    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 调用函数删除 user_id=11 的所有记录
# delete from 11 to 20
for i in range(11, 21):
    delete_image_assignments(i)
