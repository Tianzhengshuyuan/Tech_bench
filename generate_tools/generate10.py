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


def generate_question_with_random_divisor():
    """
    生成新的题目
    """
    # 随机生成整数分母
    divisor = random.randint(2, 20)  # 生成 2 到 20 之间的随机整数

    # 计算正确答案
    correct_answer = f"{divisor}倍"

    # 生成选项
    options = [
        correct_answer
    ]
    options = list(set(options))  # 去重
    while len(options) < 4:  # 确保选项数量为 4
        options.append(f"{random.randint(2, 20)}倍")
    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"4．（6分）在一斜面顶端，将甲、乙两个小球分别以 v 和 \\frac{{v}}{{{divisor}}} 的速度沿同一方向水平抛出，两球都落在该斜面上。甲球落至斜面时的速率是乙球落至斜面时速率的（　　）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_question_with_random_divisor()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")