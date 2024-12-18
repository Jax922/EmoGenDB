import openai
import base64
import os
import json
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import pandas as pd

# Initialize OpenAI client
# client = openai.OpenAI(
#     api_key="sk-uurmtknAiStkVFLOxMiWONWVTlMcTyFPAHp2ToA7w0PEGRH7",
#     base_url="https://api.feidaapi.com/v1"
# )

client = openai.OpenAI(
    api_key="sk-xwDnb4uN1aJC89lS7OD0dHxabjMAPi1cWsOUcmB7PHmrc49H",
    base_url="https://api.chatanywhere.tech/v1"
)


dir_path = "/home/pci/dong/AIGC-image/jouneryDB/mj37/"
csv_file = dir_path + "aggregated_data.csv"
imgs_path = dir_path + "imgs/"

# Load local image and encode in Base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to analyze image
def analyze_local_image(image_path, prompting):
    print("Analyzing image...")
    # Encode local image to Base64
    base64_image = encode_image_to_base64(image_path)
    
    # print(f"base64: {base64_image}")

    # Construct the prompt
    llm_prompt = f"""
    You are an AI visual assistant that analyzes a local AIGC-generated image and its description.
    You receive one prompting of the image, describing the same image you are looking at.
    The prompting is "{prompting}".

    Your task is to analyze the image and provide the following information in valid JSON format:
    1. "Caption": A description of the image.
    2. "ANP": A list of adjective-noun pairs (e.g., ["serene beach", "calm waves", "golden light"]).
    3. "Emotion": An object with:
       - "Categorical": One emotion category from Mikels model ["Amusement", "Anger", "Awe", "Contentment", "Disgust", "Excitement", "Fear", "Sad"].
       - "VAD": An object with integer values between -4 and 4 for "Valence", "Arousal", and "Dominance".
    4. "Style": A list of one or more styles inferred from the image and prompt (e.g., ["realistic", "vintage"]).
    5. "Scene_Type": A string describing the type of scene (e.g., "indoor", "outdoor", "natural", "urban").
    6. "Object_Types": A list of main objects in the image (e.g., ["natural landscapes", "buildings"]).
    7. "Facial_Expression": If people are present, describe their facial expressions (e.g., "happy", "angry"). If not, return null.
    8. "Human_Action": If people are present, describe their actions (e.g., "running", "sitting"). If not, return null.
    9. "Reason_for_Emotion": A string explaining why the image might evoke the selected emotion.

    Return the analysis in the following JSON format, it should be a single line without any line breaks:
    {{"Caption": "XXXX","ANP": [],"Emotion": {{"Categorical": "","VAD": {{"Valence": 0,"Arousal": 0,"Dominance": 0}}}},"Style": [],"Scene_Type": "","Object_Types": [],"Facial_Expression": null,"Human_Action": null,"Reason_for_Emotion": ""}}
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { 
                "role": "user", 
                "content": [  
                    { 
                        "type": "text", 
                        "text": llm_prompt.strip() 
                    },
                    { 
                        "type": "image_url", 
                        "image_url": { 
                            "url": f"""data:image/jpeg;base64,{base64_image}""" ,
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        # max_tokens=2000
    )
    
    print(response)

    # Parse and return the JSON response
    output = response.choices[0].message.content
    return output

def append_to_csv(result_csv_file, result, img_uuid):
    # result_json = json.loads(result)
    result_json = clean_and_parse_json(result)
    if result_json is None:
        print("Failed to parse JSON, skipping.")
        return

    # 扁平化 JSON
    flat_result = {
        "img_name": img_uuid,
        "Caption": result_json["Caption"],
        "ANP": ", ".join(result_json["ANP"]),
        "Emotion_Categorical": result_json["Emotion"]["Categorical"],
        "Valence": result_json["Emotion"]["VAD"]["Valence"],
        "Arousal": result_json["Emotion"]["VAD"]["Arousal"],
        "Dominance": result_json["Emotion"]["VAD"]["Dominance"],
        "Style": ", ".join(result_json["Style"]),
        "Scene_Type": result_json["Scene_Type"],
        "Object_Types": ", ".join(result_json["Object_Types"]),
        "Facial_Expression": result_json["Facial_Expression"],
        "Human_Action": result_json["Human_Action"],
        "Reason_for_Emotion": result_json["Reason_for_Emotion"]
    }

    # 转换为 DataFrame
    result_df = pd.DataFrame([flat_result])

    # 保存到 CSV 文件，使用追加模式
    # dir_path = "./"  # 设置保存路径
    # result_csv_file = dir_path + "llm_result.csv"

    # 检查文件是否存在，决定是否写入表头
    header = not os.path.exists(result_csv_file)

    # 追加到文件
    result_df.to_csv(result_csv_file, index=False, mode='a', header=header, encoding="utf-8")
    
def clean_and_parse_json(result):
    try:
        # 修复可能的 JSON 格式问题
        cleaned_result = result.strip()
        # 解析 JSON
        return json.loads(cleaned_result)
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e)
        print("Attempting to clean JSON...")
        
        # 修复问题：仅保留第一个完整的 JSON 对象
        if "{" in cleaned_result and "}" in cleaned_result:
            start = cleaned_result.find("{")
            end = cleaned_result.rfind("}") + 1
            cleaned_result = cleaned_result[start:end]
            try:
                return json.loads(cleaned_result)
            except json.JSONDecodeError as e:
                print("Still failed to parse JSON:", e)
                return None
        else:
            print("Invalid JSON structure, cannot recover.")
            return None

# Example usage
# image_path = "path/to/your/local/image.jpg"  # Replace with your local image path
# dynamic_prompting = '"A serene beach during sunset with calm waves and golden light."'
# result = analyze_local_image(image_path, dynamic_prompting)
# print(result)


# fetch all image paths
all_imgs_paths = []
for root, dirs, files in os.walk(imgs_path):
    for file in files:
        if file.endswith((".jpg", ".jpeg", ".png")):
            all_imgs_paths.append(os.path.join(root, file))

print(f"Total images in the folder: {len(all_imgs_paths)}")
            
# test the first image
csv_df = pd.read_csv(csv_file)
# print(csv_df.head())
# all_imgs_paths = all_imgs_paths[1165:]

# for image_path in tqdm(all_imgs_paths):
#     # # find the prompt from the csv file
#     img_uuid = image_path.split("/")[-1].split(".")[0]
#     if img_uuid not in csv_df["img_name"].values:
#         continue
#     img_prompting = csv_df[csv_df["img_name"] == img_uuid]["prompt_text"].values[0]
#     # print(f"Prompting for image {img_uuid}: {img_prompting}")
#     result = analyze_local_image(image_path, img_prompting)
#     result_csv_file = dir_path + "llm_result.csv"
#     append_to_csv(result_csv_file, result, img_uuid)
# image_path = all_imgs_paths
# # find the prompt from the csv file
# csv_df = pd.read_csv(csv_file)
# img_uuid = image_path.split("/")[-1].split(".")[0]
# img_prompting = csv_df[csv_df["img_name"] == img_uuid]["prompt_text"].values[0]
# print(f"Prompting for image {img_uuid}: {img_prompting}")
# result = analyze_local_image(image_path, img_prompting)
# print(result)
# print(type(result))

result_csv_file = dir_path + "llm_result.csv"

# save the result json to a csv file
try:
    existing_results = set(pd.read_csv(result_csv_file)["img_name"].values)
except FileNotFoundError:
    existing_results = set()
    
print(f"Existing results: {len(existing_results)}")

def process_image(image_path):
    img_uuid = image_path.split("/")[-1].split(".")[0]
    # print(f"Processing image {img_uuid}...")
    if img_uuid in existing_results or img_uuid not in csv_df["img_name"].values:
        # print(f"Skipping image {img_uuid}.")
        return None
    img_prompting = csv_df[csv_df["img_name"] == img_uuid]["prompt_text"].values[0]
    result = analyze_local_image(image_path, img_prompting)
    return (img_uuid, result)

# Use ThreadPoolExecutor for parallel processing
with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust `max_workers` as needed
    futures = {executor.submit(process_image, img): img for img in all_imgs_paths}
    for future in tqdm(as_completed(futures), total=len(futures)):
        result = future.result()
        if result:
            img_uuid, result_data = result
            append_to_csv(result_csv_file, result_data, img_uuid)




