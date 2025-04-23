import json
import random
import os
import math


def add_new_item(new_question):
    """
    将新的题目添加到 JSON 文件中
    """
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


def generate_question_with_random_planet():
    """
    生成新的行星题目
    """
    # 随机生成整数 a 和 b
    a = random.randint(2, 10)  # 地球半径的倍数
    b = random.randint(2, 10)  # 行星半径倍数

    # 计算正确答案
    correct_value = math.sqrt(((b + 1) ** 3 * 2) / (a + 1) ** 3) * 24
    correct_answer = int(round(correct_value))  # 取整后的正确答案

    # 生成错误答案
    wrong_answers = [
        correct_answer // 2,  # 正确答案的一半取整
        correct_answer * 2,  # 正确答案的二倍
        correct_answer * 3   # 正确答案的三倍
    ]
    wrong_answers = [int(round(ans)) for ans in wrong_answers]  # 确保答案为整数

    # 随机排列选项
    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"8．（6分）已知地球同步卫星离地面的高度约为地球半径的{a}倍．若某行星的平均密度为地球平均密度的一半，它的同步卫星距其表面的高度是其半径的{b}倍，则该行星的自转周期约为（　　）\n",
        "A": f"{options[0]}小时",
        "B": f"{options[1]}小时",
        "C": f"{options[2]}小时",
        "D": f"{options[3]}小时",
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_question_with_random_planet()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")