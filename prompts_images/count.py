import json
count = 0
# 从文件中读取响应数据

with open('/data01/jingkun/prompts_images/final_prompts_images_qa_pairs.json', 'r') as file:
    all_responses = json.load(file)


# 初始化问题总数和提示总数
total_questions = 0
total_prompts = len(all_responses)
print(total_prompts)
# 遍历每个响应以计算问题数量
for response in all_responses:
    # 每个 responses_for_prompt 的问题数量是其内部元素的数量
    total_questions += len(response['qa_pairs'])

# 计算平均问题数量
average_questions_per_prompt = total_questions / total_prompts if total_prompts > 0 else 0

print(f"平均每个 responses_for_prompt 中有 {average_questions_per_prompt:.2f} 个问题。")
