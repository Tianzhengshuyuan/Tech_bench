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
    # 可替换的海水质量范围（单位：kg）
    sea_water_mass_range = range(1, 21)

    # 可替换的燃料类型及其燃烧热量（单位：J）
    fuels = [
        {"name": "标准煤", "energy": 2.9e7, "unit": "千克"},
        {"name": "石油", "energy": 4.2e7, "unit": "千克"},
        {"name": "酒精", "energy": 2.7e7, "unit": "千克"},
        {"name": "焦炭", "energy": 3.0e7, "unit": "千克"},
        {"name": "煤油", "energy": 4.3e7, "unit": "千克"},
        {"name": "生物质燃料", "energy": 1.5e7, "unit": "千克"},
        {"name": "煤气", "energy": 1.7e7, "unit": "立方米"},
        {"name": "氢气", "energy": 1.2e8, "unit": "千克"},
        {"name": "天然气", "energy": 3.5e7, "unit": "立方米"},
        {"name": "木材", "energy": 1.6e7, "unit": "千克"},
        {"name": "柴油", "energy": 4.3e7, "unit": "千克"},
        {"name": "航空煤油", "energy": 4.5e7, "unit": "千克"},
        {"name": "液化石油气", "energy": 4.6e7, "unit": "千克"},
        {"name": "沼气", "energy": 2.2e7, "unit": "立方米"},
        {"name": "乙醇", "energy": 2.4e7, "unit": "千克"},
        {"name": "乙烷", "energy": 5.1e7, "unit": "千克"},
        {"name": "丙烷", "energy": 5.0e7, "unit": "千克"},
        {"name": "丁烷", "energy": 4.9e7, "unit": "千克"},
        {"name": "煤炭", "energy": 2.7e7, "unit": "千克"},
        {"name": "石蜡", "energy": 4.4e7, "unit": "千克"},
        {"name": "生物柴油", "energy": 3.9e7, "unit": "千克"},
        {"name": "甲烷", "energy": 5.5e7, "unit": "千克"}
    ]

    # 核聚变反应释放的能量（每次反应，单位：J）
    energy_per_reaction = 43.15 * 1.6e-13  # 1 MeV = 1.6e-13 J
    
    # 海水中氘核数量（单位：个/kg）
    hydrogen_nuclei_per_kg = 1.0e22

    # 随机选择海水质量和燃料类型
    sea_water_mass = random.choice(sea_water_mass_range)  # 单位：kg
    selected_fuel = random.choice(fuels)
    fuel_name = selected_fuel["name"]
    fuel_energy = selected_fuel["energy"]
    fuel_unit = selected_fuel["unit"]

    # 计算海水中氘核总数
    total_hydrogen_nuclei = sea_water_mass * hydrogen_nuclei_per_kg

    # 计算总聚变释放的能量
    num_reactions = total_hydrogen_nuclei / 6  # 每 6 个氘核发生一次聚变
    total_energy_released = num_reactions * energy_per_reaction  # 单位：J

    # 计算等效燃料质量或体积
    equivalent_fuel_mass = total_energy_released / fuel_energy  # 单位：千克或立方米

    # 四舍五入到最接近的选项
    equivalent_fuel_mass_rounded = round(equivalent_fuel_mass, -2)  # 四舍五入到百位

    # 生成选项
    options = [
        round(equivalent_fuel_mass_rounded * random.uniform(0.5, 0.9), -2),  # 错误选项
        equivalent_fuel_mass_rounded,  # 正确选项
        round(equivalent_fuel_mass_rounded * random.uniform(1.1, 1.5), -2),  # 错误选项
        round(equivalent_fuel_mass_rounded * random.uniform(1.5, 2.0), -2),  # 错误选项
    ]
    random.shuffle(options)  # 随机打乱选项

    # 确定正确答案的选项
    answer_index = options.index(equivalent_fuel_mass_rounded)
    answer_key = ["A", "B", "C", "D"][answer_index]

    # 动态生成题目
    if fuel_unit == "立方米":
        new_question = {
            "question": f" 氘核 _1^2\\mathbf{{H}} 可通过一系列聚变反应释放能量，其总效果可用反应式 6_1^2\\text{{H}} \\to 2_2^4\\text{{He}} + 2_1^1\\text{{H}} + 2_0^1\\text{{n}} + 43.15 \\ \\text{{MeV}} 表示。海水中富含氘，已知 {sea_water_mass} kg 海水中含有的氘核约为 {sea_water_mass} × 1.0 \\times 10^{{22}} 个，若全都发生聚变反应，其释放的能量与体积为 V 的 {fuel_name} 燃烧时释放的热量相等；已知 1 {fuel_unit} {fuel_name} 燃烧释放的热量约为 {fuel_energy:.1e} J， 1 MeV = 1.6 \\times 10^{{-13}} J，则 V 约为（  ）。",
            "A": f"{options[0]} {fuel_unit}",  
            "B": f"{options[1]} {fuel_unit}",  
            "C": f"{options[2]} {fuel_unit}",  
            "D": f"{options[3]} {fuel_unit}",
            "answer": answer_key,
            "exam": "自动生成试题"
        }
    else:
        new_question = {
            "question": f" 氘核 _1^2\\mathbf{{H}} 可通过一系列聚变反应释放能量，其总效果可用反应式 6_1^2\\text{{H}} \\to 2_2^4\\text{{He}} + 2_1^1\\text{{H}} + 2_0^1\\text{{n}} + 43.15 \\ \\text{{MeV}} 表示。海水中富含氘，已知 {sea_water_mass} kg 海水中含有的氘核约为 {sea_water_mass} × 1.0 \\times 10^{{22}} 个，若全都发生聚变反应，其释放的能量与质量为 M 的 {fuel_name} 燃烧时释放的热量相等；已知 1 {fuel_unit} {fuel_name} 燃烧释放的热量约为 {fuel_energy:.1e} J， 1 MeV = 1.6 \\times 10^{{-13}} J，则 M 约为（  ）。",
            "A": f"{options[0]} {fuel_unit}",  
            "B": f"{options[1]} {fuel_unit}",  
            "C": f"{options[2]} {fuel_unit}",  
            "D": f"{options[3]} {fuel_unit}",
            "answer": answer_key,
            "exam": "自动生成试题"
        }
    
    return new_question

# 生成新题目
new_question = generate_question()

# 将结果写入 generated_questions.json 文件
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")