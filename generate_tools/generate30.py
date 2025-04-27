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


def generate_hydrogen_atom_question():
    """
    生成关于氢原子跃迁的题目
    """
    # 随机生成 n 的值 (2 到 7)
    n = random.randint(2, 7)

    # 计算正确答案
    correct_answer = sum(range(1, n))  # 正确答案为 1 + 2 + ... + (n-1)

    # 生成错误答案
    wrong_answers = {correct_answer - 1, correct_answer + 1, correct_answer + 2}

    wrong_answers = list(wrong_answers)

    # 生成选项
    options = [f"{correct_answer}种"] + [f"{answer}种" for answer in wrong_answers]
    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(f"{correct_answer}种")
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"1．（6分）处于 n={n} 能级的大量氢原子，向低能级跃迁时，辐射光的频率有（　　）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_hydrogen_atom_question()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")