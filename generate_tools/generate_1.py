import json
import os
import random

# 定义可替换的燃料列表
fuels = ["汽油", "天然气", "乙醇", "甲醇", "煤油"]


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

def generate_question():
    """生成新题目，随机替换燃料"""
    # 随机选择一个燃料
    selected_fuel = random.choice(fuels)

    # 原始题目数据
    base_question = {
        "question": "3.金属制成的气缸中装有柴油与空气的混合物。有可能使气缸中柴油达到燃点的过程是( ).\n",
        "A": "迅速向里推活塞",
        "B": "迅速向外拉活塞",
        "C": "缓慢向里推活塞",
        "D": "缓慢向外拉活塞",
        "index": "3",
        "answer": "A",
        "exam": "1994年新疆高考物理"
    }

    # 替换题目中的“柴油”为随机选中的燃料
    new_question_text = base_question["question"].replace("柴油", selected_fuel)

    # 生成新题目
    new_question = {
        "question": new_question_text,
        "A": base_question["A"],
        "B": base_question["B"],        
        "C": base_question["C"],
        "D": base_question["D"],
        "answer": base_question["answer"],
        "exam": "自动生成试题"  # 更新试卷信息为“自动生成试题”
    }

    return new_question

# 生成新题目并保存到 JSON 文件
new_question = generate_question()
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")