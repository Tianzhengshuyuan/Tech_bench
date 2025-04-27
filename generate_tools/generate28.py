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


def calculate_correct_answer(p, m, c):
    """
    根据替换后的参数计算正确答案
    """
    # 计算正确答案
    N_A = 6 * 10**23  # 阿伏加德罗常数
    molecular_weight = 18  # 水的摩尔质量
    result = (N_A * m) / molecular_weight / p / (10**8) / c
    result_year = result / (24 * 365)  # 转换为年
    # 取和结果最近的 10 的幂
    nearest_power = round(math.log10(result_year))
    return nearest_power


def generate_question_with_random_parameters():
    """
    生成新的题目
    """
    # 随机选择 p, m, c 的值
    p = random.randint(50, 70)  # 替换 60 为 50 到 70 的整数
    m = random.randint(1, 20)  # 替换 1g 为 1 到 20 的整数
    c = random.randint(3000, 7000)  # 替换 5000 为 3000 到 7000 的整数
    p=60
    m=1
    c=5000
    # 计算正确答案
    correct_answer_power = calculate_correct_answer(p, m, c)

    # 生成正确答案和错误答案
    correct_answer = f"10^{correct_answer_power}年"
    wrong_answer_1 = f"10^{correct_answer_power - 1}年"
    wrong_answer_2 = f"10^{correct_answer_power + 3}年"
    wrong_answer_3 = f"10^{correct_answer_power + 5}年"

    # 生成选项
    options = [correct_answer, wrong_answer_1, wrong_answer_2, wrong_answer_3]
    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"3．（4分）假如全世界{p}亿人同时数{m}g水的分子个数，每人每小时可以数{c}个，不间断地数，则完成任务所需时间最接近（阿伏加德罗常数N_A取6×10^23 mol^﹣1）（　　）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_question_with_random_parameters()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")