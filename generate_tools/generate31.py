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


def generate_engine_power_question():
    """
    生成关于汽车发动机功率计算的题目
    """
    # 随机生成题目中的变量
    mass = round(random.uniform(1, 10), 1)  # 汽车质量（1 到 10 的1位小数）
    velocity = random.randint(10, 100)  # 汽车速度（10 到 100 的整数）
    resistance = round(random.uniform(1, 10), 1)  # 阻力（1 到 10 的1位小数）

    # 计算正确答案 (P = v * f * 10^3)
    correct_answer = velocity * resistance * 10**3  # 正确答案单位为瓦特（W）

    # 生成错误答案
    wrong_answers = {
        correct_answer // 10,  # 正确答案除以 10
        correct_answer * 10,  # 正确答案乘以 10
        correct_answer * 2    # 正确答案乘以 2
    }
    while len(wrong_answers) < 3:  # 确保错误答案数量为 3
        wrong_answers.add(random.randint(1, int(correct_answer * 2)))
    wrong_answers = list(wrong_answers)

    # 生成选项
    options = [f"{correct_answer / 10**3:.0f}\\mathrm{{kW}}"] + [f"{ans / 10**3:.0f}\\mathrm{{kW}}" for ans in wrong_answers]
    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(f"{correct_answer / 10**3:.0f}\\mathrm{{kW}}")
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"1.质量为 {mass}×10^3kg 的汽车在水平路面上匀速行驶，速度为 {velocity}\\mathrm{{m/s}} ，受到的阻力大小为 {resistance}\\times10^3\\text{{N}} 。此时，汽车发动机输出的实际功率是（　　）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_engine_power_question()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")