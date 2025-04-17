import json
import random

# 定义关键词和反义词映射
antonym_dict = {
    "大于": "小于",
    "小于": "大于",
    "较大": "较小",
    "较小": "较大",
    "比较大": "比较小",
    "比较小": "比较大",
    "等于": "不等于",
    "不等于": "等于",
    "相等": "不相等",
    "变大": "变小",
    "变小": "变大",
    "增大": "减少",
    "减少": "增大",
    "升高": "降低",
    "降低": "升高",
    "低于": "高于",
    "高于": "低于",
    "相同": "不同",
    "相反": "相同",
    "不同": "相同",
    "较多": "较少",
    "较少": "较多",
    "<": ">",
    ">": "<"
}

# 加载 JSON 数据
file_path = "json/questions_with_comparation_selected.json"
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# 遍历题目并进行处理
for entry in data:

    change = entry["change"]
    correct_answer = entry["answer"]

    # 从 change 中随机选择选项
    change_options = list(change)

    selected_options = random.sample(change_options, k=random.randint(1, len(change_options)))
    print(selected_options)
    
    # 更新正确答案
    new_correct_answer = "".join(
        sorted(
            set(correct_answer).difference(selected_options)  # 原正确答案中未被选中修改的部分
            .union(set(selected_options).difference(correct_answer))  # 修改后可能新增的正确答案
        )
    )
    
    # 如果没有正确答案，放弃该题目
    if not new_correct_answer:
        continue
    
    # 替换选项中的关键词为反义词
    for option in selected_options:
        content = entry[option]
        for word, antonym in antonym_dict.items():
            if word in content:
                print(word, antonym)
                modified_content = content.replace(word, antonym)
                entry[option] = modified_content  # 更新修改后的选项内容
                print(modified_content)

    entry["answer"] = new_correct_answer

# 将修改后的数据保存到文件
output_file_path = "json/reverse_questions.json"
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print(f"处理完成，修改后的数据已保存到 {output_file_path}")