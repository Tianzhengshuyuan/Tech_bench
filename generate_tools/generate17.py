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


def generate_charge_question():
    """
    生成雨滴电荷量题目
    """
    # 随机生成电场强度 E（范围为 0.5×10^4 到 5×10^4）
    E = random.randint(5, 50) * 10**3  # 电场强度 (V/m)

    # 随机生成雨滴半径 r（范围为 1 到 10 的整数，单位为 mm）
    r = random.randint(1, 10)  # 半径 (mm)

    # 计算正确答案的电荷量 Q
    Q = 4.19 * (r**3) * 10**-5 / E  # 计算电荷量 (C)

    # 将结果转换为整数×10^次方的形式
    exponent = 0
    while Q < 1:
        Q *= 10
        exponent -= 1
    while Q >= 10:
        Q /= 10
        exponent += 1

    correct_answer = f"{int(Q)}×10^{exponent}C"

    # 设计错误答案
    incorrect_answers = [
        f"{int(Q) + 6}×10^{exponent}C",
        f"{int(Q) + 2}×10^{exponent}C",
        f"{int(Q) + 4}×10^{exponent}C"
    ]

    # 随机打乱选项
    options = [correct_answer] + incorrect_answers
    random.shuffle(options)

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目内容
    new_question = {
        "question": f"4．（6分）在雷雨云下沿竖直方向的电场强度为{E}V/m，已知一半径为{r}mm的雨滴在此电场中不会下落，取重力加速度大小为10m/s^2，水的密度为10^3kg/m^3．这雨滴携带的电荷量的最小值约为（　　）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新题目
new_question = generate_charge_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")