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


def generate_custom_question():
    """
    生成新的自定义题目
    """
    while True:
        # 随机生成跑道长度（30到1000之间的10的倍数）
        track_length = random.choice(range(30, 100, 10))

        # 随机生成声波波长（2到20之间的整数）
        wavelength = random.randint(2, 20)

        # 计算移动距离（波长的两倍）
        move_distance = wavelength * 2

        # 检查移动距离是否小于跑道长度的一半
        if move_distance < track_length / 2:
            break

    # 固定选项和正确答案
    options = {
        "A": "2",
        "B": "4",
        "C": "6",
        "D": "8"
    }
    correct_answer_key = "B"  # 正确答案为 B

    # 生成题目文本，替换变量
    question_text = (
        f"8．（6分）在学校运动场上{track_length}m直跑道的两端，分别安装了由同一信号发生器带动的两个相同的扬声器．"
        f"两个扬声器连续发出波长为{wavelength}m的声波．一同学从该跑道的中点出发，向某一段点缓慢行进{move_distance}m．"
        f"在此过程中，他听到扬声器声音由强变弱的次数为（　　）\n"
    )

    # 构建题目字典
    new_question = {
        "question": question_text,
        "A": options["A"],
        "B": options["B"],
        "C": options["C"],
        "D": options["D"],
        "answer": correct_answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_custom_question()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")