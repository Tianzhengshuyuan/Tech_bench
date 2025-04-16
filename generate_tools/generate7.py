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
        
def calculate_distance(power, intensity):
    """
    根据球面波公式计算特定功率密度下的最远距离。
    :param power: 微波发射功率 (W)
    :param intensity: 功率密度 (W/m^2)
    :return: 距离 (m)
    """
    return math.sqrt(power / (4 * math.pi * intensity))


def generate_question():
    """
    自动生成题目，随机设置微波发射功率并计算有效攻击范围。
    :return: 一个包含题目和答案的数据字典。
    """
    # 随机生成微波发射功率 P (范围 1×10^7 W 到 1×10^8 W)
    power = random.uniform(1e7, 1e8)

    # 固定的功率密度阈值
    intensity_neural = 250  # 引起神经混乱的功率密度 (W/m^2)
    intensity_heart = 1000  # 引起心肺功能衰竭的功率密度 (W/m^2)

    # 计算最远距离
    distance_neural = calculate_distance(power, intensity_neural)
    distance_heart = calculate_distance(power, intensity_heart)

    # 距离取整到最近的 1 米
    distance_neural = round(distance_neural)
    distance_heart = round(distance_heart)

    # 构造选项
    options = [
        f"{distance_neural}m {distance_heart}m",
        f"{distance_neural}m {distance_heart * 0.5}m",
        f"{distance_neural * 2}m {distance_heart * 2}m",
        f"{distance_neural * 2}m {distance_heart}m",
    ]

    # 随机化选项顺序
    random.shuffle(options)
    answer_index = options.index(f"{distance_neural}m {distance_heart}m")
    answer_key = ["A", "B", "C", "D"][answer_index]


    # 构造题目
    new_question = {
        "question": f"大功率微波对人和其他生物有一定的杀伤作用。实验表明，当人体单位面积接收的微波功率达到 250W/m^2 时会引起神经混乱，达到 1000W/m^2 时会引起心肺功能衰竭。现有一微波武器，其发射功率 P={power:.2e} W。若发射的微波可视为球面波，则引起神经混乱和心肺功能衰竭的有效攻击的最远距离约为：",
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_key,
    }

    return new_question


# 自动生成题目并保存为 JSON 文件
new_question = generate_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")