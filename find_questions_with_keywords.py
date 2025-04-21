import json
import os
import argparse

# 定义比较关键词列表
comparison_keywords = [
    "大于", "小于", "较大", "较小", "比较大", "比较小", "等于", "相等", "变大", "变小", 
    "增大", "减少", "低于", "高于", "相同", "相反", "较多", "较少", "<", ">"
]

formula_keywords = [
    "动量", "动能"
]

certainty_keywords = [
    "一定", "必然", "肯定", "必定", "总是", "从不", "有时", "可能", "不一定", "不可能"
]
fuel_keywords = [
    "汽油", "柴油", "煤", "燃料", "燃气", "天然气"
]

def extract_questions_with_keywords(input_file, output_file, class_name):
    """从 JSON 文件中提取包含比较关键词的题目"""
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"输入文件 {input_file} 不存在！")
        return

    # 读取输入文件内容
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 存储匹配关键词的条目
    filtered_questions = []

    for entry in data:
        # 检查 question 中是否包含“图”关键词
        if "图" in entry.get("question", ""):
            continue  # 如果包含“图”，跳过该条目
        
        # 检查选项 A, B, C, D 是否包含比较关键词
        options = ["A", "B", "C", "D"]
        found = 0
        if class_name == "comparison":
            for option in options:
                if option in entry:
                    for keyword in comparison_keywords:
                        if keyword in entry[option]:
                            filtered_questions.append(entry)
                            found = 1
                            break  # 如果找到一个关键词，就跳出内层循环
                if found == 1:
                    break

        elif class_name == "formula":
            for option in options:
                if option in entry:
                    for keyword in formula_keywords:
                        if keyword in entry[option]:
                            filtered_questions.append(entry)
                            found = 1
                            break  # 如果找到一个关键词，就跳出内层循环
                if found == 1:
                    break
        elif class_name == "certainty":
            for option in options:
                if option in entry:
                    for keyword in certainty_keywords:
                        if keyword in entry[option]:
                            filtered_questions.append(entry)
                            found = 1
                            break  # 如果找到一个关键词，就跳出内层循环
                if found == 1:
                    break
        elif class_name == "fuel":
            for option in options:
                if option in entry:
                    for keyword in fuel_keywords:
                        if keyword in entry[option]:
                            print(entry[option])
                            filtered_questions.append(entry)
                            found = 1
                            break  # 如果找到一个关键词，就跳出内层循环
                if found == 1:
                    break
            if found == 0:
                for keyword in fuel_keywords:
                    if keyword in entry["question"]:
                        print(entry["question"])
                        filtered_questions.append(entry)
                        break
    # 将匹配的条目写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_questions, f, ensure_ascii=False, indent=4)

    print(f"已将匹配的 {len(filtered_questions)} 个条目提取到 {output_file} 中！")

# 解析命令行参数
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提取包含比较关键词的题目")
    parser.add_argument("--input_file", type=str, default="json/phy_only.json", help="输入 JSON 文件路径")
    parser.add_argument("--output_file", type=str, default="json/questions_with_comparison.json", help="输出 JSON 文件路径")
    parser.add_argument("--class_name", type=str, default="comparison", help="要找的关键词类别, 可选值：comparison, formula, certainty, fuel")

    args = parser.parse_args()

    # 调用函数
    extract_questions_with_keywords(args.input_file, args.output_file, args.class_name)