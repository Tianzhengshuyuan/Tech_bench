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
        
def generate_question():
    while True:  # 使用循环，确保生成的电压符合范围
        # 原始电压范围（330 到 1200，且为 10 的倍数）
        base_voltage = random.choice(range(330, 1210, 10))  # 1210 是因为 range 上限是开区间
        multiplier = random.choice([2, 3, 4])  # 倍数关系（2 倍、3 倍或 4 倍）
        new_voltage = base_voltage * multiplier  # 新电压，单位：kV

        # 判断是否符合行业标准（特高压一般是 330kV ~ 1200kV）
        if 330 <= new_voltage <= 1200:
            break  # 如果符合范围，跳出循环，继续生成题目

    # 根据倍数修改答案
    if multiplier == 2:
        delta_p_relationship = "∆P′=\\frac14∆P"
        delta_u_relationship = "∆U′=\\frac12∆U"
    elif multiplier == 3:
        delta_p_relationship = "∆P′=\\frac19∆P"
        delta_u_relationship = "∆U′=\\frac13∆U"
    elif multiplier == 4:
        delta_p_relationship = "∆P′=\\frac1{16}∆P"
        delta_u_relationship = "∆U′=\\frac14∆U"
    else:
        raise ValueError("不支持的倍数关系")

    # 生成选项
    options = {
        "A": delta_p_relationship,
        "B": delta_p_relationship.replace("\\frac14", "\\frac12").replace("\\frac19", "\\frac13").replace("\\frac1{16}", "\\frac18"),  # 错误选项
        "C": delta_u_relationship.replace("\\frac12", "\\frac14").replace("\\frac13", "\\frac16").replace("\\frac14", "\\frac18"),  # 错误选项
        "D": delta_u_relationship,
    }

    # 正确答案
    correct_answers = ["A", "D"]

    # 生成题目
    question_data = {
        "question": f"特高压输电可使输送中的电能损耗和电压损失大幅降低。我国已成功掌握并实际应用了特高压输电技术。假设从 A 处采用 {base_voltage} kV 的超高压向 B 处输电，输电线上损耗的电功率为 ∆P，到达 B 处时电压下降了 ∆U。在保持 A 处输送的电功率和输电线电阻都不变的条件下，改用 {new_voltage} kV 特高压输电，输电线上损耗的电功率变为 ∆P′，到达 B 处时电压下降了 ∆U′。不考虑其他因素的影响，则（　　）",
        "A": options["A"],
        "B": options["B"],
        "C": options["C"],
        "D": options["D"],
        "answer": "".join(correct_answers),
        "exam": "自动生成试题",
    }

    return question_data

# 生成新题目并保存到 JSON 文件
new_question = generate_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")