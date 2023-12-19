import json

def read_data(file_path):
    """读取 JSON 数据文件"""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data(data, file_path):
    """保存数据到 JSON 文件"""
    with open(file_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def clean_responses(data):
    """清理 responses：移除 'Not mentioned' 答案和答案不在 choices 中的元素"""
    for item in data:
        # 移除 'flag' 为 '0' 或不存在的元素
        item["qa_pairs"] = [
            resp for resp in item["qa_pairs"] 
            if resp.get("flag") is not None and int(resp.get("flag")) != 0
        ]
        # 移除答案不在 'choices' 中的元素
        item["qa_pairs"] = [
            resp for resp in item["qa_pairs"] 
            if resp.get('answer') in resp.get('choices', [])
        ]
    return data

def main():
    # 定义文件路径
    input_file = './combined_sorted_results.json'  # 原始数据文件路径
    output_file = './useful_prompts_images_qa_pairs.json'  # 最终数据文件路径

    # 读取数据
    data = read_data(input_file)

    # 清理数据
    cleaned_data = clean_responses(data)

    # 保存清理后的数据
    save_data(cleaned_data, output_file)

    print("数据处理完成，结果已保存到:", output_file)

if __name__ == "__main__":
    main()
