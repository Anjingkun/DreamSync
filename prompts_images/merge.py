import json

# 文件名列表
filenames = ['processed_results_0.json', 'processed_results_1.json',
             'processed_results_2.json', 'processed_results_3.json',
             'processed_results_4.json']

all_results = []

# 从每个文件读取数据并添加到all_results列表
for filename in filenames:
    with open(filename, 'r') as file:
        data = json.load(file)
        all_results.extend(data)

# 按id从小到大排序
all_results.sort(key=lambda x: x['id'])

# 将排序后的结果保存到一个新文件
with open('combined_sorted_results.json', 'w') as file:
    json.dump(all_results, file, ensure_ascii=False, indent=4)
