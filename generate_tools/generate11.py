import json
import random
import os

def add_new_item(new_question):
    """
    将生成的新题目追加到 JSON 文件中
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


def generate_voltage_question():
    """
    生成电学题目
    """
    # 随机生成电源电压 U（范围为 10 到 50 的整数）
    U = random.randint(2, 9000)

    # 随机生成电压表的示数 V1（范围为 1 到 U-1 的整数）
    V1 = random.randint(1, U - 1)

    correct_answer = f"小于{U - V1}伏"
    # 动态生成选项
    options = [
        f"小于{U - V1}伏",
        f"等于{U - V1}伏",
        f"大于{U - V1}伏小于{V1}伏",
        f"等于或大于{V1}伏．"
    ]

    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]


    # 生成题目内容
    new_question = {
        "question": f"7．两个定值电阻R1、R2串联后接在输出电压U稳定于{U}伏的直流电源上．有人把一个内阻不是远大于R1、R2的电压表接在R1两端，电压表的示数为{V1}伏．如果把此电压表改接在R2的两端，则电压表的示数将\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新题目
new_question = generate_voltage_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")