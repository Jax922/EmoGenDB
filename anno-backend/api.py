from flask import Flask, jsonify, request
import sqlite3
import os

# FastAPI 服务
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

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
    插入标注记录并更新图片标注次数及 image_assignments 的 is_annotated 字段
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. 插入标注记录到 annotations 表
        cursor.execute('''
            INSERT INTO annotations (user_id, img_name, emotion_categorical, valence, arousal, dominance)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, img_name, emotion_categorical, valence, arousal, dominance))

        # 2. 更新 images 表的 annotation_count
        cursor.execute('''
            UPDATE images
            SET annotation_count = annotation_count + 1
            WHERE img_name = ?
        ''', (img_name,))

        # 3. 根据 img_name 找到 images 表中的 id (img_id)
        new_img_name = img_name.split('/')[-1]
        new_img_name = new_img_name.split('.')[0]
        cursor.execute('''
            SELECT id
            FROM images
            WHERE img_name = ?
        ''', (new_img_name,))
        row = cursor.fetchone()
        if not row:
            # 如果没有查到对应的图片记录，看你是否要抛异常，或者可以直接跳过
            raise ValueError(f"Image not found for img_name: {img_name}")

        img_id = row[0]  # 拿到图片主键ID
        print("img_id:", img_id)

        # 4. 更新 image_assignments 表，让 is_annotated = 1
        cursor.execute('''
            UPDATE image_assignments
            SET is_annotated = 1
            WHERE user_id = ? AND img_id = ?
        ''', (user_id, img_id))

        # 成功则提交
        conn.commit()

    except Exception as e:
        conn.rollback()  # 出现异常，回滚
        raise e

    finally:
        cursor.close()
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
    user_id: str
    img_name: str
    emotion_categorical: str
    valence: float
    arousal: float
    dominance: float

# @app.on_event("startup")
# def startup():
#     create_database_and_tables()

app.mount("/images", StaticFiles(directory="/home/pci/dong/emodb/dong/AIGC-image/MJ/sample_images_200"), name="images")

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
        print(user)
        return {"success": True, "message": "Login successful", "user_id": user[0]}
    else:
        raise HTTPException(status_code=401, detail="用户名不存在或者密码错误")


@app.get("/images")
def get_images():
    images = fetch_images()
    return {"images": images}

@app.post("/annotate")
def annotate(annotation: Annotation):
    if annotation.user_id is None:
        raise HTTPException(status_code=400, detail="user_id cannot be null")
    try:
        print(annotation)
        annotate_image(
            annotation.user_id, 
            annotation.img_name, 
            annotation.emotion_categorical, 
            annotation.valence, 
            annotation.arousal, 
            annotation.dominance
        )
        return {"message": "Annotation recorded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/annotations/{user_id}")
def get_user_annotations(user_id: int):
    annotations = fetch_annotations(user_id)
    return {"annotations": annotations}

@app.get("/fetch_image/{user_id}")
def fetch_image(user_id: int):
    """
    Fetch a single image assigned to the user but not yet annotated.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 查询分配给用户但未标注的图片（只取一张）
    cursor.execute('''
        SELECT images.id, images.img_name, images.caption, images.image_path,
               images.emotion_categorical, images.valence, images.arousal, images.dominance
        FROM images
        JOIN image_assignments
        ON images.id = image_assignments.img_id
        WHERE image_assignments.user_id = ? AND image_assignments.is_annotated = 0
        LIMIT 1
    ''', (user_id,))

    image = cursor.fetchone()
    conn.close()

    # 如果没有未标注的图片
    if not image:
        return {"message": "所有图片已标注完成"}

    # 格式化返回数据
    result = {
        "img_id": image[0],
        "img_name": image[1],
        "caption": image[2],
        "image_path": image[3],
        "emotion_categorical": image[4],
        "valence": image[5],
        "arousal": image[6],
        "dominance": image[7],
    }

    return {"image": result}


@app.get("/remaining_images/{user_id}")
def get_remaining_images(user_id: int):
    """
    查询当前用户还剩多少张未标注的图片
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 查询分配给用户的图片中未标注的数量
    cursor.execute('''
        SELECT COUNT(*)
        FROM image_assignments
        WHERE user_id = ? AND is_annotated = 0
    ''', (user_id,))
    remaining_count = cursor.fetchone()[0]

    conn.close()

    return {"remaining_images": remaining_count}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)