import json
import random
import os

def add_new_item(new_question):
    """
    将新生成的题目添加到文件中
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

def generate_satellite_question():
    """
    生成关于卫星周期、轨道半径和速度比的物理题目
    """
    # 随机生成一个整数 n
    n = random.randint(2, 10)  # 生成的整数范围
    n_cubed = n ** 3  # 计算 n 的三次方
    n_squared = n ** 2  # 计算 n 的平方

    # 正确答案
    correct_option = f"RA∶RB=1∶{n_squared}，vA∶vB={n}∶1"

    # 生成干扰选项
    wrong_option_1 = f"RA∶RB={n_squared}∶1，vA∶vB={n}∶1"  # 反转轨道半径比
    wrong_option_2 = f"RA∶RB=1∶{n_squared}，vA∶vB=1∶{n}"  # 反转速度比
    wrong_option_3 = f"RA∶RB={n_squared}∶1，vA∶vB=1∶{n}"  # 同时反转轨道半径和速度比

    # 将选项随机排列
    options = [correct_option, wrong_option_1, wrong_option_2, wrong_option_3]
    random.shuffle(options)

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_option)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 构造题目
    new_question = {
        "question": f"8．两颗人造卫星A、B绕地球作圆周运动，周期之比为TA∶TB=1∶{n_cubed}，则轨道半径之比和运动速率之比分别为",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question

# 生成新题目
new_question = generate_satellite_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")