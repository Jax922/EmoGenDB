import torch
from PIL import Image
from lavis.models import load_model_and_preprocess
import pandas as pd
import os

# 配置设备
device = torch.device("cuda") if torch.cuda.is_available() else "cpu"

# 加载模型
def load_model():
    _, vis_processors, _ = load_model_and_preprocess(
        name="blip2_vicuna_instruct", 
        model_type="vicuna7b", 
        is_eval=True, 
        device=device
    )
    
    # 修改模型权重路径为你的自定义路径
    load_path = './LAVIS/model_weights1.pth'
    model = torch.load(load_path)
    model = model.to(device)
    model.eval()
    return model, vis_processors

# 加载图片
def load_image(image_path):
    image = Image.open(image_path).convert('RGB')
    return image

# 推理函数
def infer_emotion(model, vis_processors, image_path, prompt):
    # 加载图片并进行预处理
    raw_image = load_image(image_path)
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    
    # 执行推理
    text = model.generate({"image": image, "prompt": prompt})
    answer = text[0].split('\n')[0]
    return answer

# 逐张图片写入结果
def process_and_save(csv_file, output_file, num_images=1000):
    # 加载 CSV 数据
    data = pd.read_csv(csv_file)
    data = data.head(num_images)  # 只处理前 num_images 张图片

    # 定义情绪类别
    emo = ['Amusement', 'Anger', 'Awe', 'Contentment', 'Disgust', 'Excitement', 'Fear', 'Sadness']

    # 加载模型
    model, vis_processors = load_model()

    # 推理的文本 Prompt
    prompt = 'Please select the emotion closest to the image from the following options:\
    amusement, \
    anger, \
    awe, \
    contentment, \
    disgust, \
    excitement, \
    fear and sadness \
    (Do not provide answers outside of the candidates options.) Please answer in the following format:  Predict emotion:'

    # 打开新的 CSV 文件进行写入
    with open(output_file, 'w') as f_out:
        # 写入 CSV 头部
        f_out.write(','.join(data.columns.tolist() + ['emovit_cat']) + '\n')

        # 遍历每张图片
        for idx, row in data.iterrows():
            image_path = row['image_path']
            img_name = row['img_name']
            print(f"Processing Image {idx+1}/{num_images}: {img_name}")

            try:
                # 推理情绪分类
                answer = infer_emotion(model, vis_processors, image_path, prompt)
                print(f"Predicted: {answer}")

                # 确定预测情绪
                predicted_emotion = None
                for label in emo:
                    if label in answer.lower():
                        predicted_emotion = label
                        break

                # 写入结果
                row['emovit_cat'] = predicted_emotion
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                row['emovit_cat'] = None

            # 将当前行写入到新的 CSV 文件
            f_out.write(','.join(str(row[col]) for col in data.columns.tolist() + ['emovit_cat']) + '\n')

    print(f"Results saved to {output_file}")

# 主程序入口
if __name__ == "__main__":
    # 输入 CSV 文件路径
    input_csv = "/home/pci/dong/AIGC-image/MJ/all_cleaned.csv"  # 替换为您的 CSV 文件路径
    output_csv = "/home/pci/dong/AIGC-image/MJ/all_emovit7b.csv"  # 输出结果路径
    # 如果输出文件不存在，则创建
    if not os.path.exists(output_csv):
        with open(output_csv, 'w') as f:
            f.write('')
        
    

    # 开始处理
    process_and_save(input_csv, output_csv, num_images=1000)
