import json
import os
import random
import math


def add_new_item(new_question):
    """
    将新生成的题目保存到 JSON 文件中
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
        
def calculate_wavelength_ratio(radius):
    """
    计算电子与油滴的德布罗意波长之比的数量级
    :param radius: 油滴半径 (um)
    :return: 波长之比的数量级
    """

    # 波长之比
    wavelength_ratio = math.sqrt(4136 * 1e12 * radius**3)  
    print(wavelength_ratio)
    return int(math.log10(wavelength_ratio))  # 返回数量级

def format_to_scientific_notation(value):
    """
    格式化为科学计数法的指数部分
    """
    return f"10^{value}"

def generate_de_broglie_question():
    """
    生成德布罗意波长之比的题目
    """
    # 随机生成油滴半径
    oil_drop_radius = random.randint(1,10)

    # 计算德布罗意波长之比的数量级
    correct_exponent = calculate_wavelength_ratio(oil_drop_radius)
    print(correct_exponent)
    correct_option = format_to_scientific_notation(correct_exponent)
    print(correct_option)

    # 生成错误选项
    options = [
        correct_option,  # 正确选项
        format_to_scientific_notation(correct_exponent + 1),  # 比正确选项多一个数量级
        format_to_scientific_notation(correct_exponent - 1),  # 比正确选项少一个数量级
        format_to_scientific_notation(-correct_exponent)  # 正确选项的倒数
    ]
    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_option)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    question = {
        "question": f"13．已知普朗克常量 h=6.63\\times10^{{-34}}\\mathrm{{J}}\\cdot\\mathrm{{s}} ，电子的质量为 9.11\\times10^{{-31}}\\mathrm{{kg}} ，一个电子和一滴直径约为 {oil_drop_radius * 2}\\mathrm{{um}} 的油滴具有相同动能，则电子与油滴的德布罗意波长之比的数量级为（）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }
    return question


# 生成题目并保存
new_question = generate_de_broglie_question()
add_new_item(new_question)

print("新的德布罗意波长题目已生成，并保存到 generated_questions.json 文件中！")