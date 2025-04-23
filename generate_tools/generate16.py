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


def generate_wave_question():
    """
    生成简谐横波题目
    """
    # 随机生成频率 f（范围为 10 到 1000 的整数）
    f = random.randint(10, 1000)

    # 波速为频率的 2 倍
    v = f * 2

    # 选项和答案保持不变
    options = [
        "位移方向相同，速度方向相反",
        "位移方向相同，速度方向相同",
        "位移方向相反，速度方向相反",
        "位移方向相反，速度方向相同"
    ]

    # 正确答案为 A
    answer_key = "A"

    # 生成题目内容
    new_question = {
        "question": f"5．（6分）平衡位置处于坐标原点的波源S在y轴上振动，产生频率为{f}Hz的简谐横波向x轴正、负两个方向传播，波速均为{v}m/s，平衡位置在x轴上的P、Q两个质点随波源振动着，P、Q的x轴坐标分别为x_P＝3.5m，x_Q＝﹣3m，当S位移为负且向﹣y方向运动时，P、Q两质点的（　　）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新题目
new_question = generate_wave_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")