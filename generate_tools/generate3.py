import json
import random

def generate_question():
# 放射性元素列表（扩展为包含锂、铍、硼、碳、氮、氧、氟、钠、镁、铝、硅、氯、氩、钾）
    elements = [
        "_{3}^{8}\\mathbb{Li}",   # 锂
        "_{4}^{11}\\mathbb{Be}",   # 铍
        "_{5}^{12}\\mathbb{B}",   # 硼
        "_{6}^{15}\\mathbb{C}",   # 碳
        "_{7}^{13}\\mathbb{N}",   # 氮
        "_{8}^{15}\\mathbb{O}",   # 氧
        "_{9}^{18}\\mathbb{F}",   # 氟
        "_{11}^{24}\\mathbb{Na}", # 钠
        "_{12}^{27}\\mathbb{Mg}", # 镁
        "_{13}^{29}\\mathbb{Al}", # 铝
        "_{14}^{31}\\mathbb{Si}", # 硅
        "_{17}^{38}\\mathbb{Cl}", # 氯
        "_{18}^{35}\\mathbb{Ar}", # 氩
        "_{19}^{38}\\mathbb{K}"   # 钾
    ]   
    # 剩余比例对应的小时数选项
    time_options = {
        "1/4": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],  # 1/2^2
        "1/8": [3, 6, 9, 12, 15, 18, 21, 24, 27, 30],  # 1/2^3
        "1/16": [4, 8, 12, 16, 20, 24, 28],  # 1/2^4
        "1/32": [5, 10, 15, 20, 25, 30],  # 1/2^5
        "1/64": [6, 12, 18, 24, 30],  # 1/2^6
    }
    
    # 随机选择元素
    element = random.choice(elements)
    
    # 随机选择剩余比例
    remaining_ratio = random.choice(list(time_options.keys()))
    
    # 随机选择小时数
    hours = random.choice(time_options[remaining_ratio])
    
    # 计算半衰期
    # 剩余比例 = (1/2)^(hours / t_half) => t_half = hours / log2(1/remaining_ratio)
    power = {
        "1/4": 2,
        "1/8": 3,
        "1/16": 4,
        "1/32": 5,
        "1/64": 6
    }
    t_half = hours / power[remaining_ratio]
    
    # 生成选项
    options = [
        t_half,  # 正确答案
        round(t_half * random.uniform(0.5, 0.9), 2),  # 错误答案
        round(t_half * random.uniform(1.1, 1.5), 2),  # 错误答案
        round(t_half * random.uniform(1.5, 2.0), 2)   # 错误答案
    ]
    random.shuffle(options)  # 随机打乱选项
    
    # 确定正确答案
    answer_index = options.index(t_half)
    answer_key = ["A", "B", "C", "D"][answer_index]
    
    # 生成题目
    new_question = {
        "question": f"放射性元素 {element} 的样品经过 {hours} 小时后还有 {remaining_ratio} 没有衰变，它的半衰期是：\n",
        "A": f"{options[0]} 小时",  
        "B": f"{options[1]} 小时",  
        "C": f"{options[2]} 小时",  
        "D": f"{options[3]} 小时",
        "answer": answer_key,
        "exam": "自动生成试题"
    }
    return new_question

new_question = generate_question()

# 将结果写入 news.json 文件
with open("json/news.json", "w", encoding="utf-8") as f:
    json.dump(new_question, f, ensure_ascii=False, indent=4)

print("新的题目已生成，并保存到 news.json 文件中！")