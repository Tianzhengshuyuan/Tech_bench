import random
import json

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
        
def generate_voltage_and_power():
    """
    自动生成符合条件的额定电压和额定功率：
    1. 额定电压 U 为偶数。
    2. 额定功率 P 为 U 的因数。
    3. U^2 / P 可以被 4 整除。
    """
    while True:
        # 随机生成偶数额定电压（范围：2V 到 100V）
        voltage = random.choice(range(2, 101, 2))

        # 生成额定功率，要求是 voltage 的因数
        factors = [p for p in range(4, voltage + 1) if voltage % p == 0]

        # 遍历因数，找到满足 U^2 / P 可以整除 4 的功率
        for power in factors:
            if (voltage ** 2 / power) % 4 == 0:
                return voltage, power


def generate_question():
    """
    自动生成题目，动态调整额定电压和额定功率，且实际电压为额定电压的一半。
    """
    # 生成符合条件的额定电压和额定功率
    rated_voltage, rated_power = generate_voltage_and_power()

    # 实际电压为额定电压的一半
    actual_voltage = rated_voltage / 2  # 保留浮点数

    # 计算灯泡电阻
    resistance = rated_voltage ** 2 / rated_power  # 计算灯泡电阻
    # 计算实际功率
    actual_power = (actual_voltage ** 2) / resistance  # 计算实际功率

    # 构造选项，保留小数点后两位
    options = {
        "A": f"等于 {rated_power} W",
        "B": f"小于 {rated_power} W，大于 {rated_power / 4} W",
        "C": f"等于 {rated_power / 4} W",
        "D": f"小于 {rated_power / 4} W",
    }

    # 构造题目
    new_question = {
        "question": f"一白炽灯泡的额定功率与额定电压分别为 {rated_power} W 与 {rated_voltage} V。若把此灯泡接到输出电压为 {actual_voltage:.2f} V 的电源两端，则灯泡消耗的电功率",
        "A": options["A"],
        "B": options["B"],
        "C": options["C"],
        "D": options["D"],
        "actual_power": f"{actual_power:.2f} W",  # 显示实际功率作为检查
        "answer": "B",
    }

    return new_question


# 自动生成题目
new_question = generate_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")