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
    file_path += ".json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

import re
from fractions import Fraction  # 用于处理分数

def get_numbers(raw_numbers):
    numbers = []
    for num in raw_numbers:
        if '/' in num:  # 分数形式
            try:
                numbers.append(float(Fraction(num)))  # 将分数转换为浮点数
            except ValueError:
                pass  # 忽略无法解析的分数
        elif '×10^' in num:  # 科学计数法形式
            try:
                # 将科学计数法字符串转换为浮点数
                numbers.append(float(num.replace('×10^', 'e').replace('－', '-')))  # 将 '×10^' 替换为 'e'
            except ValueError:
                pass  # 忽略无法解析的科学计数法
        else:  # 普通数字
            try:
                numbers.append(float(num))
            except ValueError:
                pass  # 忽略无法解析的数字
        
    return numbers    
    
def extract_handcrafted_features(question, options):
    """
    提取手工设计的特征，包括数字关系、关键词等。
    """
    features = []

    # 匹配数字间的空格并移除
    question = re.sub(r'(\d)\s+(\d)', r'\1\2', question)
    options = re.sub(r'(\d)\s+(\d)', r'\1\2', options)

    # 扩展正则表达式以提取分数和科学计数法形式的数字
    question_raw_numbers = re.findall(r'\d+/\d+|\d+\.\d+|\d+(?:\.\d+)?×10\^[-－]?\d+|(?<![a-zA-Z])\d+(?![\.、．分])', question)
    options_raw_numbers = re.findall(r'\d+/\d+|\d+\.\d+|\d+(?:\.\d+)?×10\^[-－]?\d+|(?<![a-zA-Z])\d+(?![\.、．分])', options)

    # 解析提取出的数字（分数和科学计数法）
    question_numbers = get_numbers(question_raw_numbers)
    options_numbers = get_numbers(options_raw_numbers)
    numbers = question_numbers + options_numbers

    # 数字特征
    features.append(1 if numbers else 0) # 判断是否存在数字
    features.append(1 if any(n1 + n2 in numbers for n1 in numbers for n2 in numbers if n1 != n2) else 0)  # 和差关系
    features.append(1 if any(n1 != 0 and n1 != 1 and (n2 / n1).is_integer() for n1 in question_numbers for n2 in question_numbers if n1 != n2) else 0) # 判断是否存在任意倍数关系（n2 / n1 是整数）
    features.append(1 if any(any(math.lcm(int(n1), int(n2)) == n3 for n3 in question_numbers if n3 != n1 and n3 != n2) 
                             for n1 in question_numbers for n2 in question_numbers if n1 != n2 and n1.is_integer() and n2.is_integer()) else 0)  # 最小公倍数关系
    # 关键词特征
    keywords = ["之比", "倍", "和", "差", "一半"]
    features.append(1 if any(keyword in question for keyword in keywords) else 0)
    features.append(1 if any(keyword in options for keyword in keywords) else 0)

    print("question: ", end="")
    print(question)
    print("numbers: ",end="")
    print(numbers)  # 打印解析后的数字
    print("features: ",end="")
    print(features)
    return features

def train_and_label_test_data():
    # 加载训练数据和测试数据
    train_data = load_data(args.train_file)  # 加载训练数据
    test_data = load_data(args.test_file)    # 加载测试数据

    # 提取训练数据的特征        
    print("<<<<<<<<<<<<< TRAIN >>>>>>>>>>>>>")
    X_handcrafted = np.array(
        [
            extract_handcrafted_features(
                item["question"],
                ", ".join(
                    [
                        item.get("A", ""),
                        item.get("B", ""),
                        item.get("C", ""),
                        item.get("D", ""),
                    ]
                )
            )
            for item in train_data
        ]
    )
    y = np.array([item["label"] for item in train_data])

    # 提取 TF-IDF 特征
    questions = [
        ", ".join(
            [
                item["question"],
                item.get("A", ""),
                item.get("B", ""),
                item.get("C", ""),
                item.get("D", ""),
            ]
        )
        for item in train_data
    ]
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # 限制最大特征数为 1000
    X_tfidf = tfidf_vectorizer.fit_transform(questions)

    # 合并手工特征和 TF-IDF 特征
    X_combined = hstack([X_tfidf*0.1, X_handcrafted])  # 合并稀疏矩阵（TF-IDF 是稀疏的）

    # 训练 SVM 模型
    scaler = StandardScaler(with_mean=False)  # 稀疏矩阵不能使用 `with_mean=True`
    X_combined = scaler.fit_transform(X_combined)

    model = SVC(kernel='linear')
    model.fit(X_combined, y)

    # 标注测试数据中每个条目的标签
    print("<<<<<<<<<<<<< TEST >>>>>>>>>>>>>")
    labeled_test_data = []  # 用于存储标注后的测试数据
    for item in test_data:
        item_all = ", ".join(
            [
                item.get("A", ""),
                item.get("B", ""),
                item.get("C", ""),
                item.get("D", ""),
            ]
        )
        handcrafted_features = extract_handcrafted_features(item["question"], item_all)
        tfidf_features = tfidf_vectorizer.transform([item_all])
        combined_features = hstack([tfidf_features*0.1, [handcrafted_features]])
        combined_features = scaler.transform(combined_features)

        # 预测标签
        predicted_label = model.predict(combined_features)[0]
        # 将预测的标签添加到条目中
        item["label"] = int(predicted_label)  # 确保标签是整数
        labeled_test_data.append(item)

    # 输出标注后的测试数据
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(labeled_test_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="筛选并标注符合规律的题目条目")
    parser.add_argument("--train_file", type=str, required=True, help="用于训练模型的 JSON 文件")
    parser.add_argument("--test_file", type=str, required=True, help="需要标注的 JSON 文件")
    parser.add_argument("--output_file", type=str, default="labeled_test_data.json", help="标注结果输出文件")
    args = parser.parse_args()

    train_and_label_test_data()

    print(f"测试数据已标注，结果保存在 {args.output_file}")