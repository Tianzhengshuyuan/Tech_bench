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
    # 随机生成 a, b, c 的值
    a = round(random.uniform(0.5, 10), 2)  # 生成 0.5 到 10 之间的随机小数，保留两位小数
    b = random.randint(30, 100)  # 生成 30 到 100 之间的随机整数
    c = random.randint(3, 10) * 100  # 生成 300 到 1000 之间的随机 10 的倍数

    # 计算正确答案
    correct_answer = round(b * c / 1000, 2)  # b * c / 1000，保留两位小数

    # 生成错误答案
    incorrect_answers = [
        round(correct_answer - 1, 2),
        round(correct_answer + 5, 2),
        round(correct_answer + 10, 2)
    ]

    # 确保选项数量为 4，且包含正确答案
    options = [correct_answer] + incorrect_answers

    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"1．（6分）将质量为{a}kg的模型火箭点火升空，{b}g燃烧的燃气以大小为{c}m/s的速度从火箭喷口在很短时间内喷出。在燃气喷出后的瞬间，火箭的动量大小为（喷出过程中重力和空气阻力可忽略）（　　）\n",
        "A": f"{options[0]}kg•m/s",
        "B": f"{options[1]}kg•m/s",
        "C": f"{options[2]}kg•m/s",
        "D": f"{options[3]}kg•m/s",
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_question_with_random_parameters()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")