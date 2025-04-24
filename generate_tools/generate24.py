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


def generate_question_with_random_period():
    """
    生成新的题目
    """
    # 随机生成周期 t，范围为 5 到 5.99，两位小数
    t = round(random.uniform(5.00, 5.99), 2)  # 周期 t，单位为 ms
    # 计算正确答案
    correct_density = (1.41 * 10**17) / (t**2)  # 计算密度
    correct_mantissa = round(correct_density / (10 ** int(math.log10(correct_density))), 1)  # 小数部分
    correct_exponent = int(math.log10(correct_density))  # 指数部分
    correct_answer = f"{correct_mantissa}\\times10^{{{correct_exponent}}}\\:\\mathrm{{kg}}/\\mathrm{{m}}^3"

    # 错误答案生成
    incorrect_answers = [
        f"{correct_mantissa}\\times10^{{{correct_exponent - 1}}}\\:\\mathrm{{kg}}/\\mathrm{{m}}^3",
        f"{correct_mantissa}\\times10^{{{correct_exponent + 1}}}\\:\\mathrm{{kg}}/\\mathrm{{m}}^3",
        f"{correct_mantissa}\\times10^{{{correct_exponent + 2}}}\\:\\mathrm{{kg}}/\\mathrm{{m}}^3"
    ]

    # 生成选项并随机化
    options = [correct_answer] + incorrect_answers
    random.shuffle(options)

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"3．2018年2月，我国500 m口径射电望远镜（天眼）发现毫秒脉冲星“J0318+0253”，其自转周期T={t} ms，假设星体为质量均匀分布的球体，已知万有引力常量为 6.67\\times10^{{-11}}\\text{{N m}}^2/\\mathrm{{kg}}^2 。以周期T稳定自转的星体的密度最小值约为\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_question_with_random_period()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")