import json
from FlagEmbedding import FlagModel

# 加载数据
with open('/data01/jingkun/prompts_images/useful_prompts_images_qa_pairs.json', 'r') as file:
    data = json.load(file)

# 初始化模型
model = FlagModel('BAAI/bge-large-en-v1.5', 
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True)

# 设置相似度阈值
similarity_threshold1 = 0.8


# 处理每个 prompt
for prompt_data in data:
    sentences = [qa_pair["question"]+" "+ str(qa_pair["answer"]) for qa_pair in prompt_data['qa_pairs']]
    embeddings = model.encode(sentences)
    similarity_matrix = embeddings @ embeddings.T

    # 过滤重复项
    filtered_responses_1 = []


    for i, qa_pair in enumerate(prompt_data['qa_pairs']):
        is_duplicate_1 = False


        for j in range(i):
            if similarity_matrix[i, j] >= similarity_threshold1:
                is_duplicate_1 = True


            # 如果已经确定是duplicate，不需要进一步检查
            if is_duplicate_1 :
                break

        if not is_duplicate_1:
            filtered_responses_1.append(qa_pair)


    # 保存过滤结果
    prompt_data['qa_pairs'] = filtered_responses_1
    print(prompt_data['id'])

# 保存过滤后的数据
with open('/data01/jingkun/prompts_images/filtered_responses.json', 'w') as file:
    json.dump(data, file, indent=4)
