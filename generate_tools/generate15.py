import json
import os
import random

def add_new_item(new_question):
    """
    将新生成的题目保存到 JSON 文件中
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

def generate_neutron_star_question():
    """
    生成关于双中子星合并的题目
    """
    # 随机生成参数
    time_before_merge = random.randint(50, 150)  # 合并前的时间，范围 50-150 秒
    distance = random.randint(300, 500)  # 中子星之间的距离，范围 300-500 km
    rotation_speed = random.randint(5, 20)  # 每秒转动的圈数，范围 5-20 圈

    # 构造题目
    question = {
        "question": f"20．2017年，人类第一次直接探测到来自双中子星合并的引力波。根据科学家们复原的过程，在两颗中子星合并前约{time_before_merge}s时，它们相距约{distance}km，绕二者连线上的某点每秒转动{rotation_speed}圈，将两颗中子星都看作是质量均匀分布的球体，由这些数据、万有引力常量并利用牛顿力学知识，可以估算出这一时刻两颗中子星\n",
        "A": "质量之积",
        "B": "质量之和",
        "C": "速率之和",
        "D": "各自的自转角速度",
        "answer": "BC",
        "exam": "自动生成试题"
    }
    return question

# 生成题目
new_question = generate_neutron_star_question()

# 将生成的题目保存到 generated_questions.json 文件中
add_new_item(new_question)

print("新的中子星合并题目已生成，并保存到 generated_questions.json 文件中！")