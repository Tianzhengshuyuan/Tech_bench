import random

def generate_question():
    # 可替换的海水质量范围（单位：kg）
    sea_water_mass_range = range(1, 21)

    # 可替换的燃料类型及其燃烧热量（单位：J/kg）
    fuels = {
        "标准煤": 2.9e7,  # 焦耳
        "石油": 4.2e7,
        "天然气": 3.5e7,
        "酒精": 2.7e7,
        "生物质燃料": 1.5e7,
        "氢气": 1.2e8,
    }

    # 核聚变反应释放的能量（每次反应，单位：J）
    energy_per_reaction = 43.15 * 1.6e-13  # 1 MeV = 1.6e-13 J
    
    # 海水中氘核数量（单位：个/kg）
    hydrogen_nuclei_per_kg = 1.0e22

    # 随机选择海水质量和燃料类型
    sea_water_mass = random.choice(sea_water_mass_range)  # 单位：kg
    fuel_name, fuel_energy = random.choice(list(fuels.items()))  # 燃料和燃烧热量

    # 计算海水中氘核总数
    total_hydrogen_nuclei = sea_water_mass * hydrogen_nuclei_per_kg

    # 计算总聚变释放的能量
    num_reactions = total_hydrogen_nuclei / 6  # 每 6 个氘核发生一次聚变
    total_energy_released = num_reactions * energy_per_reaction  # 单位：J

    # 计算等效燃料质量
    equivalent_fuel_mass = total_energy_released / fuel_energy  # 单位：kg

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
    correct_index = options.index(equivalent_fuel_mass_rounded)
    correct_letter = ["A", "B", "C", "D"][correct_index]

    # 生成题目文本
    question = f"""
    氘核 _1^2\\mathbf{{H}} 可通过一系列聚变反应释放能量，其总效果可用反应式 
    6_1^2\\text{{H}} \\to 2_2^4\\text{{He}} + 2_1^1\\text{{H}} + 2_0^1\\text{{n}} + 43.15 \\ \\text{{MeV}} 表示。
    海水中富含氘，已知 {sea_water_mass} kg 海水中含有的氘核约为 1.0 \\times 10^{{22}} 个，
    若全都发生聚变反应，其释放的能量与质量为 M 的 {fuel_name} 燃烧时释放的热量相等；
    已知 1 kg {fuel_name} 燃烧释放的热量约为 {fuel_energy:.1e} J，
    1 MeV = 1.6 \\times 10^{{-13}} J，则 M 约为（  ）。
    """

    # 格式化选项
    choices = f"""
    A: {options[0]} kg  
    B: {options[1]} kg  
    C: {options[2]} kg  
    D: {options[3]} kg
    """

    return {
        "question": question.strip(),
        "choices": choices.strip(),
        "answer": correct_letter,
    }

# 测试生成题目
for _ in range(5):
    data = generate_question()
    print("题目：")
    print(data["question"])
    print("选项：")
    print(data["choices"])
    print(f"答案：{data['answer']}\n")