import json
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

# 1. 读取 JSON 文件
with open("output_deduplicated.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 提取题目文本，要求 item 中存在 "exam" 键，并且 "exam" 包含“理综”二字
filtered_items = [item for item in data if "exam" in item and "理综" in item["exam"] and not "物理" in item["exam"]]
questions = [item["question"] for item in filtered_items]

# 2. 对中文文本进行分词
# 使用 jieba 分词，每个句子分词后用空格连接
def tokenize(text):
    return " ".join(jieba.cut(text))

# 对所有题目文本进行分词
segmented_questions = [tokenize(question) for question in questions]

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

# 5. 将聚类标签添加回过滤后的数据（filtered_items），而不是原始数据（data）
for i, item in enumerate(filtered_items):
    item["cluster"] = int(labels[i])

# 6. 分析每个聚类的题目内容
clusters_df = pd.DataFrame({"question": questions, "cluster": labels})

# 打印每个聚类的前几条题目
for cluster_id in range(n_clusters):
    print(f"Cluster {cluster_id}:\n")
    print(clusters_df[clusters_df["cluster"] == cluster_id].head(5)["question"])
    print("\n")

# 7. 将每个聚类保存为单独的文件
for cluster_id in range(n_clusters):
    cluster_items = [item for item in filtered_items if item["cluster"] == cluster_id]
    with open(f"cluster_{cluster_id}.json", "w", encoding="utf-8") as file:
        json.dump(cluster_items, file, ensure_ascii=False, indent=4)

print("聚类完成！每个聚类已保存为单独的文件。")