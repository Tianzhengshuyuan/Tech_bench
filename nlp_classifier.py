import json
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# 1. 加载数据
def load_data(file_path, label):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    # 每条数据的 "question" 字段作为文本，附加类别标签
    return [{"text": item["question"], "label": label} for item in data]

# 加载三个学科的数据
physics_data = load_data("phy_only.json", label=2)  # 物理
chemistry_data = load_data("che_only.json", label=1)  # 化学
biology_data = load_data("bio_only.json", label=0)  # 生物

# 合并数据集
all_data = physics_data + chemistry_data + biology_data

# 2. 数据预处理
# 提取文本和标签
texts = [item["text"] for item in all_data]
labels = [item["label"] for item in all_data]

# 中文分词
def tokenize(text):
    return " ".join(jieba.cut(text))

# 对所有文本进行分词
tokenized_texts = [tokenize(text) for text in texts]

# 3. 特征提取（TF-IDF）
vectorizer = TfidfVectorizer(max_features=5000)  # 最大特征数为 5000，可调整
X = vectorizer.fit_transform(tokenized_texts)  # 转换为特征矩阵
y = labels  # 标签

# 4. 数据集划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. 训练分类模型（逻辑回归）
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train, y_train)

# 6. 模型评估
y_pred = model.predict(X_test)

# 打印分类报告
print("分类报告：")
print(classification_report(y_test, y_pred, target_names=["生物", "化学", "物理"]))

# 打印准确率
print("准确率：", accuracy_score(y_test, y_pred))

# 7. 测试单条问题的分类
def predict_category(question):
    # 对输入问题进行分词
    tokenized_question = tokenize(question)
    # 转换为 TF-IDF 特征向量
    vectorized_question = vectorizer.transform([tokenized_question])
    # 预测类别
    predicted_label = model.predict(vectorized_question)[0]
    # 标签映射
    label_mapping = {0: "生物", 1: "化学", 2: "物理"}
    return label_mapping[predicted_label]

# 测试模型
test_question = "某温度下向100g澄清的饱和石灰水中加入5.6g生石灰，充分反应后恢复到原来的温度。\n    下列叙述正确的是"
print(f"问题: {test_question}")
print(f"预测类别: {predict_category(test_question)}")