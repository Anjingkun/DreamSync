from diffusers import StableDiffusionPipeline
import torch
import json

# 初始化模型
model_id = "./stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

# 加载captions数据
with open("./TIFA/tifa_v1.0_text_inputs.json", "r") as file:
    captions_data = json.load(file)
# 生成并保存图片
images = []
for item in captions_data:
    caption_id = item["id"]
    caption = item["caption"]
    image = pipe(caption).images[0]
    image_path = f"./images/generated_image_{caption_id}.png"
    image.save(image_path)
    images.append({
        "caption_id":caption_id,
        "image_path":image_path
    })
    print({
        "caption_id":caption_id,
        "caption":caption,
        "image_path":image_path
    })
# 写入结果到JSON文件
with open("images_path.json", "w") as file:
    json.dump(images, file, indent=4)

