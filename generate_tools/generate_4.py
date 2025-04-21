import json
import os
import random

# 定义可替换的城市列表
cities = [
    "北京", "上海", "广州", "深圳", "成都", "重庆", "杭州", "西安", "武汉", "南京", 
    "天津", "青岛", "苏州", "厦门", "长沙", "郑州", "合肥", "福州", "大连", "昆明",
    "哈尔滨", "济南", "南昌", "南宁", "太原", "石家庄", "沈阳", "长春", "贵阳", "海口", 
    "兰州", "乌鲁木齐", "呼和浩特", "银川", "西宁", "澳门", "香港", "宁波", "无锡", "扬州", 
    "温州", "佛山", "东莞", "珠海", "汕头", "中山", "台州", "嘉兴", "常州", "洛阳"
]


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

def generate_question():
    """生成新题目，随机替换城市"""
    # 随机选择一个城市
    selected_city = random.choice(cities)

    # 原始题目数据
    base_question = {
        "question": "6．（6分）2019年5月17日，我国成功发射第45颗北斗导航卫星，该卫星属于地球静止轨道卫星（同步卫星）。该卫星（　　）\n",
        "A": "入轨后可以位于   京正上方",
        "B": "入轨后的速度大于第一宇宙速度",
        "C": "发射速度大于第二宇宙速度",
        "D": "若发射到近地圆轨道所需能量较少",
        "index": "6",
        "answer": "D",
        "exam": "2019年北京市高考物理试卷"
    }

    # 替换题目中的“北京”为随机选中的城市
    new_A_text = base_question["A"].replace("北京", selected_city)

    # 生成新题目
    new_question = {
        "question": base_question["question"],
        "A": new_A_text,
        "B": base_question["B"],        
        "C": base_question["C"],
        "D": base_question["D"],
        "answer": base_question["answer"],
        "exam": "自动生成试题"  # 更新试卷信息为“自动生成试题”
    }

    return new_question

# 生成新题目并保存到 JSON 文件
new_question = generate_question()
add_new_item(new_question)

print("新的题目已生成，并保存到 generated_questions.json 文件中！")