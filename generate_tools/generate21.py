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


def generate_mars_question():
    """
    生成新的火星探测器相关题目
    """
    # 随机生成运行周期中的 r 和最近距离中的 t
    r = round(random.uniform(1.0, 3.0), 1)  # r 是 1.0 到 3.0 的一位小数
    t = round(random.uniform(2.0, 4.0), 1)  # t 是 2.0 到 4.0 的一位小数

    # 计算正确答案
    constant = 9.38 * 10**18
    term1 = constant * (34 + r)**2 * t**2  # 9.38 * 10^18 * (3.4 + r)^2 * t^2
    root = math.pow(term1, 1/3)  # 开三次根号
    final_result = 2 * root - 6.8 * 10**6 - r * 10**5  # 最终结果
    
    # 获取科学计数法的指数部分
    exponent = int(math.floor(math.log10(final_result)))
    mantissa = round(final_result / 10**exponent, 1)  # 科学计数法的前半部分

    correct_answer = f"{mantissa}\\times10^{exponent}\\mathrm{{m}}"  # 正确答案

    # 错误答案设置为正确答案指数 -1、+1、+2
    wrong_answers = [
        f"{mantissa}\\times10^{exponent - 1}\\mathrm{{m}}",
        f"{mantissa}\\times10^{exponent + 1}\\mathrm{{m}}",
        f"{mantissa}\\times10^{exponent + 2}\\mathrm{{m}}"
    ]

    # 将正确答案和错误答案合并并打乱顺序
    options = [correct_answer] + wrong_answers
    random.shuffle(options)

    # 获取正确答案的选项位置
    answer_index = options.index(correct_answer)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目文本
    question_text = (
        f"18. 2021 年 \\text{{2}} 月，执行我国火星探测任务的“天问一号”探测器在成功实施三次近火制动后，"
        f"进入运行周期约为 {r}\\times10^5\\mathrm{{s}} 的椭圆形停泊轨道，轨道与火星表面的最近距离约为 "
        f"{t}\\times10^5\\text{{m}} 。已知火星半径约为 3.4\\times10^6\\text{{m}} ，火星表面处自由落体的加速度大小约为 "
        f"3.7\\mathrm{{m/s}}^2 ，则“天问一号”的停泊轨道与火星表面的最远距离约为（   ）\\n"
    )

    # 构建题目字典
    new_question = {
        "question": question_text,
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 生成新的题目
new_question = generate_mars_question()

# 将题目写入 JSON 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")