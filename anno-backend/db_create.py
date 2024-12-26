from flask import Flask, jsonify, request
import sqlite3
import os

DB_PATH = 'emotions.db'

# 创建数据库和表

def create_database_and_tables():
    """
    创建数据库及所需的表，包括账户表、标注记录表。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 创建账户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # 创建标注记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS annotations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        img_name TEXT NOT NULL,
        emotion_categorical TEXT NOT NULL,
        valence REAL,
        arousal REAL,
        dominance REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES accounts(id)
    )
    ''')

    # 创建图片信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        img_name TEXT UNIQUE NOT NULL,
        caption TEXT,
        emotion_categorical TEXT,
        valence REAL,
        arousal REAL,
        dominance REAL,
        annotation_count INTEGER DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    create_database_and_tables()
    print("数据库及表创建成功！")