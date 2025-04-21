import random
import json
import os

# 定义五个概念
concepts = ["密度", "质量", "体积", "摩尔质量", "阿伏伽德罗常数"]

def add_new_item(new_question):
    """将新题目添加到 JSON 文件"""
    file_path = "json/generated_questions.json"
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 如果文件存在，读取现有内容
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []  # 如果文件内容不是列表，则重置为列表
            except json.JSONDecodeError:
                data = []  # 如果文件内容为空或解析失败，则重置为列表
    else:
        # 如果文件不存在，则初始化为空列表
        data = []

    # 将新的题目添加到列表中
    data.append(new_question)

    # 将更新后的列表写回文件
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 定义函数生成新题目
def generate_new_question():
    """基于基础题目生成新的题目"""

    # 正确答案必须包含的概念
    correct_concepts = ["阿伏伽德罗常数", "摩尔质量", "密度"]
    correct_answer = random.sample(correct_concepts, len(correct_concepts))  # 打乱顺序

    # 生成其他选项的组合
    all_combinations = []
    while len(all_combinations) < 3:  # 需要生成三个错误选项
        # 从 concepts 中随机选择三个不同的概念
        combination = random.sample(concepts, 3)
        # 跳过包含正确答案所有概念的组合
        if all(concept in combination for concept in correct_concepts):
            continue
        # 避免重复加入相同的组合
        if combination not in all_combinations:
            all_combinations.append(combination)

    # 生成选项
    options = [
        "、".join(all_combinations[0]),
        "、".join(all_combinations[1]),
        "、".join(correct_answer),  # 正确答案
        "、".join(all_combinations[2]),
    ]

    # 随机打乱选项顺序
    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index("、".join(correct_answer))
    answer_key = ["A", "B", "C", "D"][answer_index]


    # 生成新的题目
    new_question = {
        "question": "4.只要知道下列哪一组物理量，就可以估算出气体中分子间的平均距离?( )。\n　",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题",
    }

    return new_question

# 生成新题目
new_question = generate_new_question()

add_new_item(new_question)  # 将新题目添加到 JSON 文件

# 打印新题目
print(json.dumps(new_question, ensure_ascii=False, indent=4))