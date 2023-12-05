from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering
import json
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base").to("cuda")

# 加载questions数据
with open("./TIFA/tifa_v1.0_question_answers.json", "r") as file:
    questions_data = json.load(file)

# 用于存储最终结果的列表
results = []

# 加载图片路径数据
with open("images_path.json", "r") as file:
    images_data = json.load(file)
images_dict = {item["caption_id"]: item["image_path"] for item in images_data}

# 对每个问题进行问答并保存结果
for item in questions_data:
    caption_id = item["id"]
    detailed_question = item["question"] + "\nYou can choose the correct answer from the following options based on the content of the image:\n" + ", ".join(item["choices"])
    real_answer = item["answer"]
    image_path = images_dict.get(caption_id)
    
    if image_path:
        raw_image = Image.open(image_path).convert('RGB')
        inputs = processor(raw_image, detailed_question, return_tensors="pt").to("cuda")
        out = model.generate(**inputs)
        model_answer = processor.decode(out[0], skip_special_tokens=True)

        # 保存结果
        results.append({
            "caption_id": caption_id,
            "question": detailed_question,
            "model_answer": model_answer,
            "real_answer": real_answer,
            "element_type": item.get("element_type"),
            "element": item.get("element")
        })

# 写入结果到JSON文件
with open("qa_results.json", "w") as file:
    json.dump(results, file, indent=4)
