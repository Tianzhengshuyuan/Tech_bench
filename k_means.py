import json
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

# 读取 JSON 文件
with open("conprehensive_questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 提取题目及选项文本
# 将 "text"、"A"、"B"、"C"、"D" 合并为一个整体文本
all_text = [
    f"{item['question']} {item['A']} {item['B']} {item['C']} {item['D']}" for item in data
]

# 2. 对中文文本进行分词
# 使用 jieba 分词，每个句子分词后用空格连接
def tokenize(text):
    return " ".join(jieba.cut(text))

# 对所有文本进行分词
segmented_questions = [tokenize(text) for text in all_text]

# 3. 文本向量化（TF-IDF）
# 不使用停用词
vectorizer = TfidfVectorizer(max_features=500)  # 最大特征数为 500，可根据需要调整
X = vectorizer.fit_transform(segmented_questions)

# 4. 应用 K-Means 聚类
# 假设有 3 类（物理、化学、生物）
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=200)
kmeans.fit(X)

# 获取聚类结果
labels = kmeans.labels_

# 5. 将聚类标签添加回原始数据
for i, item in enumerate(data):
    item["cluster"] = int(labels[i])


# 6. 将每个聚类保存为单独的文件
for cluster_id in range(n_clusters):
    cluster_items = [item for item in data if item["cluster"] == cluster_id]
    with open(f"cluster_{cluster_id}.json", "w", encoding="utf-8") as file:
        json.dump(cluster_items, file, ensure_ascii=False, indent=4)

print("聚类完成！每个聚类已保存为单独的文件。")