import json
import os
import sympy as sp
import random

# 定义公式库
formula_library = {
    "动能": "E - (1/2) * m * v**2",  # 动能公式 E = (1/2) * m * v^2
    "动量": "p - m * v",             # 动量公式 p = m * v
    "洛伦兹力": "F - q * v * B",     # 洛伦兹力公式 F = q * v * B
    "向心力": "F - (m * v**2) / r"   # 向心力公式 F = (m * v^2) / r
}

def add_new_item(new_question):
    """将新题目添加到 JSON 文件"""
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

def parse_formula(physical_quantity):
    """
    从公式库中解析公式，返回 SymPy 的等式对象。
    """
    if physical_quantity not in formula_library:
        raise ValueError(f"公式库中未找到物理量：{physical_quantity}")
    return sp.sympify(formula_library[physical_quantity])

def get_conversion_formula(from_quantity, to_quantity, specified_common_var=None, target_var=None):
    """
    动态生成从一个物理量转换到另一个物理量的公式。
    支持人工指定公共变量。
    """
    # 获取公式
    from_formula = parse_formula(from_quantity)
    to_formula = parse_formula(to_quantity)
    
    # 提取变量
    from_symbols = from_formula.free_symbols
    to_symbols = to_formula.free_symbols
    common_symbols = list(from_symbols & to_symbols)  # 找到两个公式的公共变量（如 v）
    print(f"from_symbols: {from_symbols}, to_symbols: {to_symbols}")
    if not common_symbols:
        raise ValueError(f"{from_quantity} 和 {to_quantity} 无法通过公式直接关联")
    
    print(f"公共变量: {common_symbols}")
    
    # 使用人工指定的公共变量（如果提供）
    if specified_common_var:
        common_var = sp.Symbol(specified_common_var)
        if common_var not in common_symbols:
            raise ValueError(f"指定的公共变量 {specified_common_var} 不在公共变量列表 {common_symbols} 中")
    else:
        # 如果未指定公共变量，默认选择第一个
        common_var = common_symbols[0]
    
    print(f"使用的公共变量: {common_var}")
    
    # 从 from_formula 解出公共变量
    solved_var = sp.solve(from_formula, common_var)[0]
    
    # 将公共变量代入 to_formula，解出目标物理量
    if target_var is None:
        # 如果没有指定目标变量，则默认选择 to_formula 中的第一个变量
        target_var = list(to_formula.free_symbols - {common_var})[0]
    else:
        target_var = sp.Symbol(target_var)
    print(f"目标变量: {target_var}")
    conversion_formula = to_formula.subs(common_var, solved_var)
    solved_target = sp.solve(conversion_formula, target_var)[0]
    
    return solved_target

def generate_options(correct_ratio):
    """
    根据正确答案生成选项，包括干扰项。
    """
    correct_numerator, correct_denominator = map(int, correct_ratio.split(":"))
    options = [correct_ratio]
    
    # 生成干扰项
    while len(options) < 4:
        # 随机生成干扰项
        numerator = random.randint(1, 5)
        denominator = random.randint(1, 5)
        if numerator != correct_numerator or denominator != correct_denominator:
            option = f"{numerator}:{denominator}"
            if option not in options:
                options.append(option)
    
    # 随机打乱选项顺序
    random.shuffle(options)
    return options

def modify_question_to_momentum(question_data, specified_common_var=None, target_var=None):
    """
    将题目中的动能转换为动量，并重新计算选项。
    支持人工指定公共变量。
    """
    # 粒子参数
    m_proton = 1  # 质子质量（单位化处理）
    m_alpha = 4   # α粒子质量是质子的 4 倍

    # 动能比 E1:E2
    E_ratio = sp.Rational(1, 1)  # 假定动能比为 1:2

    # 获取转换公式
    conversion_formula = get_conversion_formula("动能", "动量", specified_common_var, target_var)
    print(f"转换公式为: {conversion_formula}")

    # 利用公式计算动量比
    p1 = conversion_formula.subs({"m": m_proton, "E": E_ratio * 1})  # 质子动量
    p2 = conversion_formula.subs({"m": m_alpha, "E": 1})  # α粒子动量
    p_ratio = sp.simplify(p1 / p2)  # 计算动量比

    # 将动量比转换为字符串形式
    p_ratio_str = f"{p_ratio.numerator}:{p_ratio.denominator}"
    print("p_ratio_str is: " + p_ratio_str)
    
    # 修改题目内容
    new_question = question_data["question"].replace("动能E_1和α粒子的动能E_2", "动量p_1和α粒子的动量p_2")
    
    # 生成选项
    options = generate_options(p_ratio_str)
    
    # 确定正确答案选项
    correct_option = None
    for key, value in zip(["A", "B", "C", "D"], options):
        if value == p_ratio_str:
            correct_option = key

    # 构建新的题目数据
    new_question_data = {
        "question": new_question,
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": correct_option,
        "exam": question_data["exam"]
    }

    return new_question_data

# 示例题目
question_data = {
    "question": "10.质子和α粒子在同一匀强磁场中作半径相同的圆周运动。由此可知质子的动能E_1和α粒子的动能E_2之比E_1:E_2等于( ).",
    "A": "4:1",
    "B": "1:1",
    "C": "1:2",
    "D": "2:1",
    "index": "10",
    "answer": "C",
    "exam": "经典物理题"
}

# 主程序
specified_var = "v"  # 用户人工指定公共变量
target_var = "p"  # 目标物理量为动量
new_question = modify_question_to_momentum(question_data, specified_var, target_var)
add_new_item(new_question)

print("新的题目已生成：")
print(json.dumps(new_question, ensure_ascii=False, indent=4))