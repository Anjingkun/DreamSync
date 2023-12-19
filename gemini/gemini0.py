# -- coding: utf-8 --
import json
import google.generativeai as genai
import concurrent.futures

# 定义API密钥列表
api_keys = ["AIzaSyCjA9AiKk1VuIRk-YIiKffx7_xC46JXj80", "AIzaSyCNtxGitqvu71zQMhbUaH0cySLt2iTXYj8", "AIzaSyB2iBco1DcHhjUoUeE7711oWqhnWtF5mwE", "AIzaSyDPWX60bfuacpWwMQN5X7giaR9q9z3_ahI", "AIzaSyC28O9gDQFt5ICozShi2ns_NXQwXz9a_D0","AIzaSyBoaMTkilVennwCZxShj638K28JF1I_Ef4","AIzaSyCF4jYktgbGgxmCgsEbmy0czVtbdO1pDeY","AIzaSyDlNrioSI09MELPgERJdQ_Jd_V9LnTk-x0","AIzaSyCIxhwH5qBKWh1L1Vv8SRxoFbdYtNSi8ds","AIzaSyBUi5sKVbiUKRwu8tJcRuNb4lpBCEvcOjc"]

# 设置当前脚本应使用的API密钥的索引（0到9之间）
key_index = 0  # 修改这个值以适应不同的脚本

# 配置API密钥
genai.configure(api_key=api_keys[key_index])

def process_prompt(item, system_prompt):
    """处理单个prompt，获取6次有效响应"""
    model = genai.GenerativeModel('gemini-pro')
    user_prompt = item['content']
    prompt_id = item['id']
    image_paths = item['images_paths']

    combined_prompt = [{"role": "system", "content": system_prompt}, {"role":
"user", "content": user_prompt}]
    combined_prompt = str(combined_prompt)
    responses_for_prompt = []
    success_count = 0
    while success_count < 6:  # 确保每个 prompt 得到6次有效响应
        try:
            response = model.generate_content(combined_prompt).text

            # 尝试解析 response JSON 数据
            response_content = json.loads(response)
            
            responses_for_prompt.extend(response_content)  # 添加到响应数组
            success_count += 1
        except Exception as e:
            # 如果解析失败，继续尝试直到成功为止
            continue
    print(prompt_id)

    return {
        "id": prompt_id,
        "prompt": user_prompt,
        "image_paths": image_paths,
        "qa_pairs": responses_for_prompt
    }

# 读取系统提示
with open('./prompts/system_prompt.txt', 'r') as file:
    system_prompt = file.read().strip()

# 读取并分割用户提示
with open('/data01/jingkun/prompts_images/numbered_texts_with_images.json', 'r') as file:
    all_prompts = json.load(file)
    total_prompts = len(all_prompts)
    chunk_size = total_prompts // len(api_keys)
    remainder = total_prompts % len(api_keys)

    if key_index < len(api_keys) - 1:
        start_index = key_index * chunk_size
        end_index = start_index + chunk_size
    else:
        # 最后一个API密钥处理剩余的所有提示
        start_index = key_index * chunk_size
        end_index = total_prompts  # 包括余数部分

    prompts_with_images = all_prompts[start_index:end_index]

# 使用多线程处理每个prompt
all_responses = []

with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    futures = [executor.submit(process_prompt, item, system_prompt) for item in prompts_with_images]
    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
        all_responses.append(future.result())
        if i % 10 == 0:  # 每10个prompts保存一次
            with open(f'/data01/jingkun/prompts_images/intermediate_qa_pairs_gemini_{key_index}.json', 'w') as intermediate_file:
                json.dump(all_responses, intermediate_file, ensure_ascii=False, indent=4)
# 将结果保存到JSON文件
output_file = f'/data01/jingkun/prompts_images/processed_results_{key_index}.json'
with open(output_file, 'w') as file:
    json.dump(all_responses, file, ensure_ascii=False, indent=4)
