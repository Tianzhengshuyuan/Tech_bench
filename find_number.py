import re
import json
import math
import argparse
import numpy as np
from sklearn.svm import SVC
from scipy.sparse import hstack
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

# 加载数据
def load_data(file_path):
    """
    从文件中加载 JSON 数据
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

import re
from fractions import Fraction  # 用于处理分数

def filter_questions(data):
    """
    筛选符合条件的问题。
    条件：A、B、C、D 键的值不为空，且存在 answer 键。
    :param data: 原始问题数据
    :return: 筛选后的问题列表
    """
    valid_questions = []
    for item in data:
        # 检查 question 中是否包含“图”
        if "question" in item and "图" in item["question"]:
            continue  # 跳过包含“图”的问题
                
        # 检查 A, B, C, D 是否为空
        if all(item.get(option, "").strip() for option in ["A", "B", "C", "D"]):
            # 检查是否存在 answer 键
            if "answer" in item and item["answer"].strip():
                valid_questions.append(item)
    return valid_questions

def extract_multiple_relationship_features(question, options):
    """
    提取"倍数"关系
    """
    features = []

    # 匹配数字间的空格并移除
    question = re.sub(r'(\d)\s+(\d)', r'\1\2', question)
    options = re.sub(r'(\d)\s+(\d)', r'\1\2', options)

    # 扩展正则表达式以提取分数和科学计数法形式的数字
    question_raw_numbers = re.findall(r'\d+/\d+|\d+\.\d+|\d+(?:\.\d+)?×10\^[-－]?\d+|(?<![a-zA-Z])\d+(?![\.、．分])', question)
    options_raw_numbers = re.findall(r'\d+/\d+|\d+\.\d+|\d+(?:\.\d+)?×10\^[-－]?\d+|(?<![a-zA-Z])\d+(?![\.、．分])', options)

    numbers = question_raw_numbers + options_raw_numbers
    if numbers:
        return 1

    return 0

def Analyze_data():
    """
    分析数据
    """
    data = load_data(args.data_file)  # 加载数据
    filtered_data = filter_questions(data)  # 筛选完整且不包含“图”的问题

    output_data = []
    for item in filtered_data:
        result = extract_multiple_relationship_features(
            item["question"][2:],
            ", ".join(
                [
                    item.get("A", ""),
                    item.get("B", ""),
                    item.get("C", ""),
                    item.get("D", ""),
                ]
            )
        )
        if result != 0:
            output_data.append(item)
    print(f"筛选出 {len(output_data)} 个包含数字的问题")

    # 输出筛选后的数据
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="筛选包含数字的题目")
    parser.add_argument("--data_file", type=str, default="json/phy_no_picture.json", help="输入的 JSON 文件路径")
    parser.add_argument("--output_file", type=str, default="json/questions_with_number.json", help="输出文件")
    args = parser.parse_args()

    Analyze_data()

    print(f"把包含数字的题目保存在 {args.output_file}")