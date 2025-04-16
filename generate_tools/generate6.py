import json
import random

def add_new_item(new_question):
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
        
# 制造干扰选项：改变数量级，例如 8e-07 改为 8e-08 或 8e-06
def generate_wrong_value_with_order(correct_value):
    # 提取数量级（10 的幂次）
    exponent = int(f"{correct_value:.1e}".split("e")[1])  # 获取科学计数法中的指数部分
    # 随机上下浮动一个数量级
    new_exponent = exponent + random.choice([-3, -2, -1, 1, 2, 3])
    # 构造新的值，保持基数不变，改变数量级
    base = float(f"{correct_value:.1e}".split("e")[0])
    return base * (10 ** new_exponent)

# 数字转为科学计数法，基数取整
def format_scientific(value):
    base, exponent = f"{value:.1e}".split("e")
    return f"{int(float(base))}e{int(exponent)}"

def generate_question():
    # 随机生成加速电场场强（1×10^4 N/C 到 5×10^5 N/C 范围内）
    field_strength = random.uniform(1e4, 5e5)  # 单位：N/C
    # 随机生成质子的最终速度（1×10^6 m/s 到 5×10^7 m/s 范围内）
    final_velocity = random.uniform(1e6, 5e7)  # 单位：m/s

    # 常量
    proton_mass = 1.67e-27  # 质子质量，单位：kg
    proton_charge = 1.6e-19  # 质子电荷量，单位：C

    # 计算质子所受的电场力（选项 B）
    force = proton_charge * field_strength

    # 计算加速度 a
    acceleration = force / proton_mass

    # 计算加速所需的时间（选项 C）
    time = final_velocity / acceleration

    # 计算加速器的直线长度（选项 D）
    distance = 0.5 * acceleration * time**2

    # 随机选择 B、C 或 D 作为正确答案
    correct_option = random.choice(["B", "C", "D"])

    print("force:", force)
    print("time:", time)
    print("distance:", distance)

    # 构造选项
    options = {
        "A": "加速过程中质子电势能增加",  # 固定干扰选项
        "B": f"质子所受到的电场力约为 {format_scientific(generate_wrong_value_with_order(force))} N",
        "C": f"质子加速需要的时间约为 {format_scientific(generate_wrong_value_with_order(time))} s",
        "D": f"加速器加速的直线长度约为 {format_scientific(generate_wrong_value_with_order(distance))} m",
    }

    # 设置正确选项
    if correct_option == "B":
        options["B"] = f"质子所受到的电场力约为 {format_scientific(force)} N"
    elif correct_option == "C":
        options["C"] = f"质子加速需要的时间约为 {format_scientific(time)} s"
    elif correct_option == "D":
        options["D"] = f"加速器加速的直线长度约为 {format_scientific(distance)} m"

    # 构造题目数据
    question_data = {
        "question": f"质子疗法进行治疗，该疗法用一定能量的质子束照射肿瘤杀死癌细胞。现用一直线加速器来加速质子，使其从静止开始被加速到 {format_scientific(final_velocity)} m/s。已知加速电场的场强为 {format_scientific(field_strength)} N/C，质子的质量为 1.67×10^-27 kg，电荷量为 1.6×10^-19 C，则下列说法正确的是：",
        "A": options["A"],
        "B": options["B"],
        "C": options["C"],
        "D": options["D"],
        "answer": correct_option,
    }

    return question_data

# 生成新题目并保存到 JSON 文件
new_question = generate_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")