import json
import random 

# 常量定义
EARTH_RADIUS = 6371  # 地球半径 (单位：km)
MAX_RADIUS = 1500000  # 最大轨道半径 (单位：km)
MIN_RADIUS = 160  # 最小轨道高度 (单位：km)

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
        
def calculate_period_ratio(r1, r2):
    """
    根据轨道半径计算周期之比
    :param r1: 第一颗卫星轨道半径
    :param r2: 第二颗卫星轨道半径
    :return: 周期之比
    """
    return (r1 / r2) ** (3 / 2)

def is_perfect_square(n):
    """
    判断一个数是否为完全平方数
    :param n: 输入的数
    :return: 如果是完全平方数则返回 True，否则返回 False
    """
    if n <= 0:
        return False
    root = int(n ** 0.5)
    return root * root == n

# 输入为250和2
def find_valid_combinations(max_multiplier, min_multiplier):
    """
    找到所有可能的 P 和 Q 半径组合，并计算周期之比
    """
    valid_combinations = []
    for p_multiplier in range(max_multiplier, min_multiplier - 1, -1):
        for q_multiplier in range(p_multiplier - 1, min_multiplier - 1, -1):
            p_radius = EARTH_RADIUS * p_multiplier # P的实际半径
            q_radius = EARTH_RADIUS * q_multiplier # Q的实际半径
            # 检查半径是否在范围内
            if MIN_RADIUS <= p_radius <= MAX_RADIUS and MIN_RADIUS <= q_radius <= MAX_RADIUS:
                ratio = p_multiplier / q_multiplier
                if ratio.is_integer() and is_perfect_square(int(ratio)):  # 判断是否为平方数
                    period_ratio = calculate_period_ratio(p_radius, q_radius)
                    valid_combinations.append((p_multiplier, q_multiplier, period_ratio))
    return valid_combinations


max_multiplier = 250  # P 的最大倍数
min_multiplier = 2  # P 的最小倍数

# 查找符合条件的组合
combinations = find_valid_combinations(max_multiplier, min_multiplier)

if combinations:
    # 随机选择一个组合
    selected_combo = random.choice(combinations)
    p_multiplier, q_multiplier, period_ratio = selected_combo
    ratio = p_multiplier / q_multiplier
    # 创建一个新的条目
    new_question = {
        "question": f"2．（6分）为了探测引力波，“天琴计划”预计发射地球卫星P，其轨道半径约为地球半径的{p_multiplier}倍；另一地球卫星Q的轨道半径约为地球半径的{q_multiplier}倍。P与Q的周期之比约为（　　）\n",
        "A": f"{int(ratio)}：1",
        "B": f"{int(4*period_ratio)}：1",
        "C": f"{int(period_ratio)}：1",
        "D": f"{int(2*period_ratio)}：1",
        "answer": "C",
        "exam": "自动生成试题"
    }

    # 将结果写入 generated_questions.json 文件
    add_new_item(new_question)

    print("新的题目已生成，并保存到 generated_questions.json 文件中！")
