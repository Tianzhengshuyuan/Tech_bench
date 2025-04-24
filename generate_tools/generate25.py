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


def generate_question_with_dynamic_exponent():
    """
    生成新的题目
    """
    # 随机生成波长 l（150 到 450 之间的整数）
    l = random.randint(150, 450)

    # 随机生成初动能 e（1.00 到 3.00 之间的两位小数）
    e = round(random.uniform(1.00, 3.00), 2)

    # 计算正确答案的频率（科学计数法）
    raw_frequency = ((1989 / l) - e) / 6.63 * 10**15  # 计算频率
    correct_exponent = int(math.floor(math.log10(raw_frequency)))  # 动态确定指数
    correct_mantissa = round(raw_frequency / (10**correct_exponent), 1)  # 确保有效数字在 1-10 之间
    correct_answer = f"{correct_mantissa}\\text{{X}}10^{correct_exponent} Hz"

    # 错误答案生成
    incorrect_answers = [
        f"{correct_mantissa - 2 if correct_mantissa - 2 > 0 else correct_mantissa + 2}\\text{{X}}10^{correct_exponent} Hz",
        f"{correct_mantissa + 2}\\text{{X}}10^{correct_exponent} Hz",
        f"{correct_mantissa + 4}\\text{{X}}10^{correct_exponent + 1} Hz"
    ]

    # 生成选项并随机化
    options = [correct_answer] + incorrect_answers
    random.shuffle(options)

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"4．用波长为{l} nm的光照射锌板，电子逸出锌板表面的最大初动能为{e} \\text{{X}} 10^-19 J。已知普朗克常量为6.63 \\text{{X}} 10^-34 J·s，真空中的光速为3.00 \\text{{X}} 10^8 m·s^-1，能使锌产生光电效应的单色光的最低频率约为\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_question_with_dynamic_exponent()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")