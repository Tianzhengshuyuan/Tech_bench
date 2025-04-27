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


def generate_question_with_random_length_and_fraction():
    """
    生成新的题目
    """
    # 随机生成题号和分母
    question_number = random.randint(2, 20)  # 随机生成题号 2 到 20
    fraction_denominator = random.randint(2, 20)  # 随机生成分母 2 到 20

    # 确定分数形式
    fraction = f"1/{fraction_denominator}"

    # 固定正确答案和选项
    correct_answer = "频率不变，振幅改变"
    options = [
        "频率、振幅都不变",
        "频率、振幅都改变",
        "频率不变，振幅改变",
        "频率改变，振幅不变"
    ]
    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"{question_number}．做简谐振动的单摆摆长不变，若摆球质量增加为原来的4倍，摆球经过平衡位置时速度减小为原来的{fraction}，则单摆振动的（　　）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_question_with_random_length_and_fraction()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")