import json

# 读取原始 JSON 文件
with open('./prompts_squeeze.json', 'r', encoding='utf-8') as file:
    texts = json.load(file)

# 为每个文本创建一个包含编号、内容和图片路径的字典
numbered_texts = []
for i, text in enumerate(texts):
    text_dict = {
        "id": i,
        "content": text,
        "images_paths": [
            f"{i}_0.png",
            f"{i}_1.png",
            f"{i}_2.png",
            f"{i}_3.png"
        ]
    }
    numbered_texts.append(text_dict)

# 将新的数组保存到新的 JSON 文件
with open('numbered_texts_with_images.json', 'w', encoding='utf-8') as file:
    json.dump(numbered_texts, file, ensure_ascii=False, indent=4)
