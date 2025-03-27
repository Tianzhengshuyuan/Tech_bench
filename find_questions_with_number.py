import json
import numpy as np
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack


# **1. 加载数据**
def load_data(file_path):
    """
    从文件中加载 JSON 数据
    """
    file_path += ".json"
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# **2. 特征提取函数**
def extract_handcrafted_features(question):
    """
    提取手工设计的特征，包括数字关系、关键词等。
    """
    features = []
    # 数字特征提取
    numbers = [int(n) for n in question.split() if n.isdigit()]
    features.append(1 if any(n % 2 == 0 for n in numbers) else 0)  # 是否有偶数
    features.append(1 if any(n1 == 2 * n2 for n1 in numbers for n2 in numbers if n1 != n2) else 0)  # 成倍数关系
    features.append(1 if "之比" in question else 0)  # 是否有“之比”
    features.append(1 if any(n1 + n2 in numbers for n1 in numbers for n2 in numbers if n1 != n2) else 0)  # 和差关系

    # 关键词特征
    keywords = ["之比", "倍", "平方", "开方", "和", "差"]
    features.append(1 if any(keyword in question for keyword in keywords) else 0)

    # 其他特征
    adjustable_params = ["电阻", "电压", "质量", "半衰期"]
    features.append(1 if any(param in question for param in adjustable_params) else 0)

    return features


def train_and_label_test_data():
    # 加载训练数据和测试数据
    train_data = load_data(args.train_file)  # 加载训练数据
    test_data = load_data(args.test_file)    # 加载测试数据

    # 提取训练数据的特征
    X_handcrafted = np.array([extract_handcrafted_features(item["question"]) for item in train_data])
    y = np.array([item["label"] for item in train_data])

    # 提取 TF-IDF 特征
    questions = [item["question"] for item in train_data]
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # 限制最大特征数为 1000
    X_tfidf = tfidf_vectorizer.fit_transform(questions)

    # 合并手工特征和 TF-IDF 特征
    X_combined = hstack([X_tfidf, X_handcrafted])  # 合并稀疏矩阵（TF-IDF 是稀疏的）

    # 训练 SVM 模型**
    # 为手工特征标准化
    scaler = StandardScaler(with_mean=False)  # 稀疏矩阵不能使用 `with_mean=True`
    X_combined = scaler.fit_transform(X_combined)

    # 训练 SVM 模型
    model = SVC(kernel='linear')
    model.fit(X_combined, y)

    # 从测试数据中标注每个条目的标签
    labeled_test_data = []  # 用于存储标注后的测试数据
    for item in test_data:
        handcrafted_features = extract_handcrafted_features(item["question"])
        tfidf_features = tfidf_vectorizer.transform([item["question"]])
        combined_features = hstack([tfidf_features, [handcrafted_features]])
        combined_features = scaler.transform(combined_features)

        # 预测标签
        predicted_label = model.predict(combined_features)[0]
        # 将预测的标签添加到条目中
        item["label"] = int(predicted_label)  # 确保标签是整数
        labeled_test_data.append(item)

    # 输出标注后的测试数据
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(labeled_test_data, f, ensure_ascii=False, indent=4)


# **3. 主逻辑**
if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="筛选并标注符合规律的题目条目")
    parser.add_argument("--train_file", type=str, required=True, help="用于训练模型的 JSON 文件")
    parser.add_argument("--test_file", type=str, required=True, help="需要标注的 JSON 文件")
    parser.add_argument("--output_file", type=str, default="labeled_test_data.json", help="标注结果输出文件")
    args = parser.parse_args()

    train_and_label_test_data()

    print(f"测试数据已标注，结果保存在 {args.output_file}")