import json
import random

# 元素周期表数据，包含元素的名称、密度（kg/m³）和原子量
elements_data = [
    {"name": "氢", "density": 0.1, "atomic_weight": 1},
    {"name": "氦", "density": 0.2, "atomic_weight": 4},
    {"name": "锂", "density": 0.5, "atomic_weight": 7},
    {"name": "铍", "density": 1.8, "atomic_weight": 9},
    {"name": "硼", "density": 2.3, "atomic_weight": 11},
    {"name": "碳", "density": 2.3, "atomic_weight": 12},
    {"name": "氮", "density": 1.3, "atomic_weight": 14},
    {"name": "氧", "density": 1.4, "atomic_weight": 16},
    {"name": "氟", "density": 1.7, "atomic_weight": 19},
    {"name": "氖", "density": 0.9, "atomic_weight": 20},
    {"name": "钠", "density": 1.0, "atomic_weight": 23},
    {"name": "镁", "density": 1.7, "atomic_weight": 24},
    {"name": "铝", "density": 2.7, "atomic_weight": 27},
    {"name": "硅", "density": 2.3, "atomic_weight": 28},
    {"name": "磷", "density": 1.8, "atomic_weight": 31},
    {"name": "硫", "density": 2.1, "atomic_weight": 32},
    {"name": "氯", "density": 3.2, "atomic_weight": 35},
    {"name": "氩", "density": 1.8, "atomic_weight": 40},
    {"name": "钾", "density": 0.9, "atomic_weight": 39},
    {"name": "钙", "density": 1.6, "atomic_weight": 40},
    {"name": "钛", "density": 4.5, "atomic_weight": 48},
    {"name": "锰", "density": 7.2, "atomic_weight": 55},
    {"name": "铁", "density": 7.9, "atomic_weight": 56},
    {"name": "钴", "density": 8.9, "atomic_weight": 59},
    {"name": "镍", "density": 8.9, "atomic_weight": 59},
    {"name": "铜", "density": 8.9, "atomic_weight": 64},
    {"name": "锌", "density": 7.1, "atomic_weight": 65},
    {"name": "砷", "density": 5.7, "atomic_weight": 75},
    {"name": "硒", "density": 4.8, "atomic_weight": 79},
    {"name": "溴", "density": 3.1, "atomic_weight": 80},
    {"name": "银", "density": 10.5, "atomic_weight": 108},
    {"name": "锡", "density": 7.3, "atomic_weight": 119},
    {"name": "碘", "density": 4.9, "atomic_weight": 127},
    {"name": "金", "density": 19.3, "atomic_weight": 197},
    {"name": "汞", "density": 13.5, "atomic_weight": 201},
    {"name": "铅", "density": 11.3, "atomic_weight": 207},
]

# 物理常量
AVOGADRO_CONSTANT = 6.022e23  # 阿伏伽德罗常数

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
        
def calculate_atomic_volume(density, atomic_weight):
    """
    计算每个原子所占的体积
    """
    molar_mass = atomic_weight * 1e-3  # 摩尔质量 (kg/mol)
    volume_per_atom = molar_mass / density / AVOGADRO_CONSTANT  # 每个原子的体积
    return volume_per_atom

def format_to_integer_scientific_notation(value):
    """
    将浮点数转换为四舍五入后的科学记数法整数形式
    """
    exponent = int(f"{value:.1e}".split("e")[1])  # 获取指数部分
    coefficient = round(value / (10 ** exponent))  # 四舍五入系数部分
    return f"{coefficient}e{exponent}m³"

def generate_question(element):
    """
    根据元素生成题目
    :param element: 元素数据，包括 name, density, atomic_weight
    :return: 新的题目条目
    """
    atomic_volume = calculate_atomic_volume(element["density"], element["atomic_weight"])
    print(atomic_volume)
    # 生成选项，随机扰动
    correct_option = format_to_integer_scientific_notation(atomic_volume)
    options = [
        format_to_integer_scientific_notation(atomic_volume),
        format_to_integer_scientific_notation(atomic_volume * random.uniform(0.1, 0.5)),
        format_to_integer_scientific_notation(atomic_volume * random.uniform(1.5, 2.0)),
        format_to_integer_scientific_notation(atomic_volume * random.uniform(0.5, 1.5)),
    ]
    random.shuffle(options)  # 随机打乱选项

    # 找到正确答案的选项 (A, B, C, D)
    answer_index = options.index(correct_option)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 生成题目
    new_question = {
        "question": f"3．已知{element['name']}的密度为 {element['density']:.1e}kg/m³ ，原子量为{element['atomic_weight']}．通过估算可知{element['name']}中每个原子所占的体积为\n",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
        "exam": "自动生成试题"
    }
    return new_question

# 随机选择一个元素生成题目
selected_element = random.choice(elements_data)
new_question = generate_question(selected_element)

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")