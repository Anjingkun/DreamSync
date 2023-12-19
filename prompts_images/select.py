import json
count = 0
# 从文件中读取响应数据

with open('/data01/jingkun/prompts_images/filtered_responses.json', 'r') as file:
    all_responses = json.load(file)
for item in all_responses:
    item.pop("filtered_qa_pairs_2")
    item["qa_pairs"] = item.pop("filtered_qa_pairs_1")
# 保存过滤后的数据
with open('/data01/jingkun/prompts_images/final_prompts_images_qa_pairs.json', 'w') as file:
    json.dump(all_responses, file, indent=4)