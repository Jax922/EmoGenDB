from flask import Flask, jsonify, request
import sqlite3
import os

# FastAPI 服务
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = 'emotions.db'


# CURD 操作封装
def insert_account(username, password):
    """
    插入新账户
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO accounts (username, password)
    VALUES (?, ?)
    ''', (username, password))
    conn.commit()
    conn.close()

def fetch_images():
    """
    获取所有图片信息
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM images''')
    data = cursor.fetchall()
    conn.close()
    return data

def annotate_image(user_id, img_name, emotion_categorical, valence, arousal, dominance):
    """
    插入标注记录并更新图片标注次数
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO annotations (user_id, img_name, emotion_categorical, valence, arousal, dominance)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, img_name, emotion_categorical, valence, arousal, dominance))

    cursor.execute('''
    UPDATE images
    SET annotation_count = annotation_count + 1
    WHERE img_name = ?
    ''', (img_name,))

    conn.commit()
    conn.close()

def fetch_annotations(user_id):
    """
    获取用户标注记录
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM annotations WHERE user_id = ?
    ''', (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的前端地址，例如 ["http://localhost:3000"]
    allow_credentials=True,  # 是否允许发送 cookies
    allow_methods=["*"],  # 允许的 HTTP 方法，例如 ["GET", "POST"]
    allow_headers=["*"],  # 允许的请求头，例如 ["Authorization", "Content-Type"]
)

class Annotation(BaseModel):
    user_id: int
    img_name: str
    emotion_categorical: str
    valence: float
    arousal: float
    dominance: float

# @app.on_event("startup")
# def startup():
#     create_database_and_tables()

@app.get("/register")
def register(username: str, password: str):
    try:
        insert_account(username, password)
        return {"message": "注册成功"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="用户名已注册")
    
@app.get("/login")
def login(username: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM accounts WHERE username = ? AND password = ?", (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return {"success": True, "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="用户名不存在或者密码错误")


@app.get("/images")
def get_images():
    images = fetch_images()
    return {"images": images}

@app.get("/annotate")
def annotate(user_id: int, img_name: str, emotion_categorical: str, valence: float, arousal: float, dominance: float):
    try:
        annotate_image(user_id, img_name, emotion_categorical, valence, arousal, dominance)
        return {"message": "Annotation recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/annotations/{user_id}")
def get_user_annotations(user_id: int):
    annotations = fetch_annotations(user_id)
    return {"annotations": annotations}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)