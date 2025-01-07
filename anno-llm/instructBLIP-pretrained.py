from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration, BitsAndBytesConfig
import pandas as pd
import torch
from PIL import Image
import os
from tqdm import tqdm
from lavis.models import load_model_and_preprocess

# 模型和处理器
model_name = "Salesforce/instructblip-vicuna-7b"
model_path = "/home/pci/dong/emodb/dong/local_model"
weight_path = "/home/pci/dong/emodb/dong/lavis_with_weight/LAVIS/model_weights1.pth"
processor = InstructBlipProcessor.from_pretrained(model_path)

# 配置量化
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)
model = InstructBlipForConditionalGeneration.from_pretrained(
    model_path,
    quantization_config=quant_config,
    torch_dtype=torch.float16,
    device_map="auto"
)

# 加载权重

# model.load_state_dict(torch.load(weight_path))
ckpt = torch.load(weight_path)
model.load_state_dict(ckpt)
model.eval()



# 设备配置
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)

# 加载 CSV 文件
csv_path = "/home/pci/dong/emodb/dong/AIGC-image/MJ/all_cleaned.csv"
output_csv_path = "/home/pci/dong/emodb/dong/AIGC-image/MJ/all_cleaned_emovit.csv"
df = pd.read_csv(csv_path)

df["image_path"] = df["image_path"].str.replace(
        "/home/pci/dong",
        "/home/pci/dong/emodb/dong",
        regex=False
    )

# 新增列
if "Emotion_Categorical_Vicuna7b" not in df.columns:
    df["Emotion_Categorical_Vicuna7b"] = ""

# 定义情绪分类的 Prompt
def generate_emotion_prompt(caption):
    return f'The caption of this image is: "{caption}" ' \
           f'Please select the emotion closest to the image from the following options: ' \
           f'Amusement, Anger, Awe, Contentment, Disgust, Excitement, Fear, Sadness. ' \
           f'Do not provide answers outside of the candidates options.'\
           f'Please answer in the following format:  Predict emotion:'
            

# 遍历每行并生成情绪分类
for index, row in tqdm(df.iterrows()):
# max_samples = 5
# for index, row in tqdm(df.iterrows(), total=min(len(df), max_samples)):
    # print(f"Processing index {index}...")
    # if index >= max_samples:
    #     break 
    try:
        # # 跳过已经处理的行
        # if pd.notna(row["Emotion_Categorical_Vicuna7b"]):
        #     continue
        
        image_path = row["image_path"]
        caption = row["Caption"]

        # 检查图片路径是否存在
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            df.at[index, "Emotion_Categorical_Vicuna7b"] = "Image not found"
            continue

        # 加载图片
        image = Image.open(image_path).convert("RGB")

        # 构造 Prompt
        prompt = generate_emotion_prompt(caption)

        # 预处理输入
        inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)

        # 推理
        outputs = model.generate(
            **inputs,
            do_sample=False,
            num_beams=5,
            max_length=256,
            repetition_penalty=1.5,
            length_penalty=1.0,
            temperature=1,
        )

        # 解码输出
        generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
        print(f"Generated for index {index}: {generated_text}")

        # # 写入结果
        df.at[index, "Emotion_Categorical_Vicuna7b"] = generated_text
        

    except Exception as e:
        print(f"Error processing index {index}: {e}")
        df.at[index, "Emotion_Categorical_Vicuna7b"] = "Error"

    # 定期保存结果
    if index % 10 == 0:
        df.to_csv(output_csv_path, index=False)

# 保存最终结果
df.to_csv(output_csv_path, index=False)
print("Processing complete. Results saved.")
