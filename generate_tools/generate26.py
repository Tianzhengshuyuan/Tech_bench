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


def generate_question_with_random_parameters():
    """
    生成新的题目
    """
    # 随机生成质量 m（0.1 到 3 之间的一位小数）
    m = round(random.uniform(0.1, 3.0), 1)

    # 随机生成速度 v（3 到 100 之间的整数）
    v = random.randint(3, 100)

    # 计算正确答案
    delta_v = 2 * v  # 速度变化量
    work_w = 0  # 墙对小球做功

    # 生成正确答案选项
    correct_answers = [
        f"\\Delta\\nu={delta_v}m/s",
        f"W={work_w}J"
    ]

    # 生成错误答案
    incorrect_answers = [
        f"\\Delta\\nu=0m/s",  # 错误的速度变化量
        f"W={round(m * v**2, 1)}J"  # 错误的做功值
    ]

    # 将正确答案和错误答案组合成选项并打乱顺序
    options = correct_answers + incorrect_answers
    random.shuffle(options)

    # 找到正确答案对应的选项 (A, B, C, D)
    answer_keys = []
    for correct_answer in correct_answers:
        answer_keys.append(["A", "B", "C", "D"][options.index(correct_answer)])

    # 生成题目
    new_question = {
        "question": f"4. 一个质量为{m}kg的弹性小球，在光滑水平面上以{v}m/s的速度垂直撞至墙上，碰撞后小球沿相反方向运动，反弹后的速度大小与碰撞前相同，则碰撞前后小球速度变化量的大小 \\Delta_{{\\nu}} 和碰撞过程中墙对小球做功的大小W为（）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": ", ".join(answer_keys),
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_question_with_random_parameters()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")