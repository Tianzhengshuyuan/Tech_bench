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


def generate_moon_mass_question():
    """
    生成新的月球质量估算题目
    """
    # 随机生成高度 h 和运行周期 t
    h = random.randint(150, 250)  # 距月球表面高度（km）
    t = random.randint(110, 140)  # 运行周期（分钟）

    # 月球半径（km）、引力常量 G 和正确答案的计算
    R = 1740  # 月球半径（km）
    correct_answer = 1.64 * 10**17 * (R + h)**3 / (t**2)

    # 转换为科学计数法
    correct_answer_scientific = f"{correct_answer:.2e}".replace("e", "×10^").replace("+", "")

    # 生成干扰项
    correct_mantissa, correct_exponent = map(float, correct_answer_scientific.split("×10^"))
    options = [
        f"{correct_mantissa:.1f}×10^{int(correct_exponent)}",
        f"{correct_mantissa + 1:.1f}×10^{int(correct_exponent - 1)}",
        f"{correct_mantissa - 1:.1f}×10^{int(correct_exponent + 1)}",
        f"{correct_mantissa + 2:.1f}×10^{int(correct_exponent + 2)}"
    ]
    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(f"{correct_mantissa:.1f}×10^{int(correct_exponent)}")
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"5．（6分）“嫦娥一号”是我国首次发射的探月卫星，它在距月球表面高度为{h} km的圆形轨道上运行，运行周期为{t}分钟．已知引力常量 G=6.67×10^﹣11 N•m^2/kg^2，月球的半径为1.74×10^3 km．利用以上数据估算月球的质量约为（　　）\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_moon_mass_question()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")