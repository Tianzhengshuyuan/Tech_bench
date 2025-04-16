import random
import json
import math

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
    """
    自动生成题目，随机改变电场强度和雨滴半径，计算正确答案。
    """
    # 随机生成电场强度 E（单位 V/m），范围 1 × 10^3 ~ 1 × 10^5
    E = random.randint(1, 100) * 10**3  # 随机生成的电场强度，比如 10^3 ~ 10^5 V/m

    # 随机生成雨滴半径 r（单位 m），范围 0.5mm ~ 2mm
    r = random.uniform(0.5, 2) * 10**-3  # 转换为米，例如 0.5mm = 0.0005m

    # 固定值
    g = 10  # 重力加速度 (m/s^2)
    rho = 10**3  # 水的密度 (kg/m^3)

    # 计算雨滴的体积 V 和质量 m
    V = (4 / 3) * math.pi * r**3  # 体积公式 V = (4/3) π r^3
    m = rho * V  # 质量公式 m = ρV

    # 计算雨滴的最小电荷量 q，使其不下落
    q = (m * g) / E
    scientific_q = f"{q:.2e}"  # 将 q 转换为科学计数法字符串
    base, exponent = scientific_q.split("e")  # 提取科学计数法的基数和指数
    base = round(float(base))  # 对基数保留两位小数
    correct_option = f"{base}e{int(exponent)}"  # 将基数和指数重新拼接

    print(q)
    options = [
        correct_option,
        f"{base-1}e{int(exponent)}",
        f"{base*2}e{int(exponent)}",
        f"{base*4}e{int(exponent)}",
    ]
    
    random.shuffle(options)

    # 构造选项
    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_option)
    answer_key = ["A", "B", "C", "D"][answer_index]
    
    # 构造题目数据
    new_question = {
        "question": f"在雷雨云下沿竖直方向的电场强度为 {E} V/m，已知一半径为 {r * 10**3:.2f} mm 的雨滴在此电场中不会下落，取重力加速度大小为10m/s^2，水的密度为10^3kg/m^3。这雨滴携带的电荷量的最小值约为（    ）",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }

    return new_question


# 自动生成题目
new_question = generate_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")