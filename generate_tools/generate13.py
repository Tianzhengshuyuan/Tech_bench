import json
import random
import os

def add_new_item(new_question):
    """
    将新的题目添加到 JSON 文件中
    """
    # 文件路径
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

def generate_question():
    """
    随机生成题目，包含指定的数值范围和正确答案
    """
    # 随机生成时间、速度等参数
    time1 = random.randint(250, 350)  # 250-350 内的整数
    speed1 = round(random.uniform(4.5, 5.5), 1)  # 4.5-5.5 的一位小数
    speed2 = round(random.uniform(4.0, 5.0), 1)  # 4.0-5.0 的一位小数
    time2 = random.randint(50, 150)  # 50-150 内的整数
    speed3 = round(random.uniform(0.5, 1.5), 1)  # 0.5-1.5 的一位小数

    # 生成题目文本
    question_text = (
        f"4．2021年5月15日，天问一号着陆器在成功着陆火星表面的过程中，经大气层 {time1}\\mathrm{{s}} 的减速，"
        f"速度从 {speed1}\\times10^3\\mathrm{{m/s}} 减为 {speed2}\\times10^2\\mathrm{{m/s}}；"
        f"打开降落伞后，经过 {time2}\\mathbf{{s}} 速度进一步减为 {speed3}\\times10^2\\mathrm{{m/s}}；"
        f"与降落伞分离，打开发动机减速后处于悬停状态；经过对着陆点的探测后平稳着陆．"
        f"若打开降落伞至分离前的运动可视为竖直向下运动，则着陆器（）\n"
    )

    # 固定选项和正确答案
    options = {
        "A": "打开降落伞前，只受到气体阻力的作用",
        "B": "打开降落伞至分离前，受到的合力方向竖直向上",
        "C": "打开降落伞至分离前，只受到浮力和气体阻力的作用",
        "D": "悬停状态中，发动机喷火的反作用力与气体阻力是平衡力"
    }
    correct_answer = "B"

    # 生成完整题目结构
    new_question = {
        "question": question_text,
        "A": options["A"],
        "B": options["B"],
        "C": options["C"],
        "D": options["D"],
        "answer": correct_answer,
        "exam": "自动生成试题"
    }

    return new_question

# 生成题目并保存到文件
new_question = generate_question()
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")