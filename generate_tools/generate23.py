import json
import random
import os
import math


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


def round_to_nearest_power_of_ten(value):
    """
    将数值四舍五入到最近的10的次方
    """
    if value <= 0:
        return 1  # 防止无效值
    exponent = round(math.log10(value))  # 四舍五入到最近的指数
    return 10 ** exponent


def generate_question_with_random_parameters():
    """
    生成高空坠物题目
    """
    # 随机生成参数
    m = random.randint(40, 60)  # 鸡蛋质量，40到60之间的整数
    h = random.randint(2, 50)  # 楼层高度，2到50之间的整数
    t = round(random.uniform(1, 3), 1)  # 撞击时间，1到3之间的一位小数

    # 计算正确答案
    g = 9.8  # 重力加速度
    velocity = math.sqrt(2 * g * h * 3)  # 每层楼高度取3米，计算自由落体速度
    impulse = m * velocity / t  # 冲击力公式 F = mv / t

    # 将冲击力结果四舍五入到最近的10的次方
    correct_answer_value = round_to_nearest_power_of_ten(impulse)
    correct_answer = f"10^{int(math.log10(correct_answer_value))} N"

    # 生成错误答案
    correct_order_of_magnitude = int(math.log10(correct_answer_value))
    incorrect_answers = [
        f"10^{correct_order_of_magnitude - 1} N",
        f"10^{correct_order_of_magnitude + 1} N",
        f"10^{correct_order_of_magnitude + 2} N"
    ]

    # 随机排列选项
    options = [correct_answer] + incorrect_answers
    random.shuffle(options)

    # 找到正确答案选项的位置
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"2．高空坠物极易对行人造成伤害。若一个{m} g的鸡蛋从一居民楼的{h}层坠下，与地面的撞击时间约为{t} ms，则该鸡蛋对地面产生的冲击力约为\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_question_with_random_parameters()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")