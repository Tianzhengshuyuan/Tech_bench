import json
import random
import os

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

def format_to_scientific_notation(value):
    """
    将值格式化为科学计数法，确保有效数字在 1 和 10 之间
    """
    exponent = 0
    while value >= 10:
        value /= 10
        exponent += 1
    while value < 1:
        value *= 10
        exponent -= 1
    return "{:.1f}e{}".format(value, exponent)

def calculate_correct_answer(c, t, u1, u2):
    """
    计算正确答案
    """
    # 公式：c * 10^(-2) * (u2 - u1) / t
    result = (c * 10**-8 * (u2 - u1)) / t
    # 格式化为科学计数法，确保有效数字在 1 和 10 之间
    return format_to_scientific_notation(result)

def generate_question_with_random_parameters():
    """
    生成新的题目
    """
    # 随机生成参数
    c = random.randint(1, 50)  # c 为 1 到 50 的整数
    t = random.randint(1, 10)  # t 为 1 到 10 的整数
    u1 = random.randint(-100, -30)  # u1 为 -100 到 -30 的整数
    u2 = random.randint(10, 70)  # u2 为 10 到 70 的整数

    # 计算正确答案
    correct_answer = calculate_correct_answer(c, t, u1, u2)

    # 生成错误答案
    correct_value = float(correct_answer.split("e")[0])
    magnitude = int(correct_answer.split("e")[1])

    wrong_answers = [
        format_to_scientific_notation((correct_value - 1) * 10**magnitude),
        format_to_scientific_notation((correct_value + 1) * 10**magnitude),
        format_to_scientific_notation((correct_value + 2) * 10**magnitude)
    ]
    random.shuffle(wrong_answers)

    # 将正确答案插入选项
    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"2. 有研究发现，某神经细胞传递信号时，离子从细胞膜一侧流到另一侧形成跨膜电流，若将该细胞膜视为 {c}\\times10^{{-8}}\\mathrm{{F}} 的电容器，在 {t}\\mathrm{{ms}} 内细胞膜两侧的电势差从 \\text{{{u1}mV}} 变为 \\mathrm{{{u2}mV}} ，则该过程中跨膜电流的平均值为（　　）\n",
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