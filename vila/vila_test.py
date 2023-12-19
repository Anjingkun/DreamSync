import tensorflow_hub as hub
import tensorflow as tf
import json

def load_image_bytes(image_path):
    """Load image and return its bytes."""
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    return image_bytes

# 加载模型
model = hub.load('model_weight')
predict_fn = model.signatures['serving_default']

# 加载图片路径数据
with open("images_path.json", "r") as file:
    images_data = json.load(file)

scores = []

# 对每个图片进行打分
for item in images_data:
    image_bytes = load_image_bytes(item['image_path'])
    predictions = predict_fn(tf.constant((image_bytes)))  # 注意：这里将字节数据放入一个列表中
    aesthetic_score = predictions['predictions'].numpy()[0]
    print({ "caption_id": item['caption_id'],"aesthetic_score":aesthetic_score})
    scores.append({
        "caption_id": item["caption_id"],
        "aesthetic_score": aesthetic_score.tolist()
    })

# 将分数保存到JSON文件
with open("image_scores.json", "w") as file:
    json.dump(scores, file, indent=4)
