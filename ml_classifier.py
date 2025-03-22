import json
import sys
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# 1. 加载数据
def load_data(file_path, label):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    # 每条数据的 "question" 和选项字段合并为一个完整的文本，附加类别标签
    return [
        {
            "text": f"{item['question']} {item['A']} {item['B']} {item['C']} {item['D']}",
            "label": label
        }
        for item in data
    ]

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

# 5. 选择分类模型
if len(sys.argv) < 2:
    print("请在命令行中指定分类方法，例如：python script.py logistic/svm/naive_bayes")
    sys.exit(1)

method = sys.argv[1].lower()

if method == "logistic":
    print("使用逻辑回归进行分类...")
    model = LogisticRegression(random_state=42, max_iter=1000)
elif method == "svm":
    print("使用支持向量机（SVM）进行分类...")
    model = LinearSVC(random_state=42, max_iter=1000)
elif method == "naive_bayes":
    print("使用朴素贝叶斯进行分类...")
    model = MultinomialNB()
else:
    print("未知分类方法，请选择 logistic、svm 或 naive_bayes")
    sys.exit(1)

# 6. 训练分类模型
model.fit(X_train, y_train)

# 7. 模型评估
y_pred = model.predict(X_test)

# 打印分类报告
print("分类报告：")
print(classification_report(y_test, y_pred, target_names=["生物", "化学", "物理"]))

# 打印准确率
print("准确率：", accuracy_score(y_test, y_pred))

# # 8. 使用训练好的模型对新数据分类
# def classify_and_append(file_to_classify, bio_file, che_file, phy_file):
#     # 加载需要分类的数据
#     with open(file_to_classify, "r", encoding="utf-8") as file:
#         data_to_classify = json.load(file)
    
#     # 加载现有的分类文件
#     with open(bio_file, "r", encoding="utf-8") as file:
#         bio_data = json.load(file)
#     with open(che_file, "r", encoding="utf-8") as file:
#         che_data = json.load(file)
#     with open(phy_file, "r", encoding="utf-8") as file:
#         phy_data = json.load(file)

#     # 分类数据
#     for item in data_to_classify:
#         # 合并题干和选项
#         question = f"{item['question']} {item['A']} {item['B']} {item['C']} {item['D']}"
#         # 对问题进行分词
#         tokenized_question = tokenize(question)
#         # 转换为 TF-IDF 特征向量
#         vectorized_question = vectorizer.transform([tokenized_question])
#         # 预测类别
#         predicted_label = model.predict(vectorized_question)[0]

#         # 根据类别追加到对应的文件
#         if predicted_label == 0:
#             bio_data.append(item)
#         elif predicted_label == 1:
#             che_data.append(item)
#         elif predicted_label == 2:
#             phy_data.append(item)

#     # 将更新后的数据写回文件
#     with open(bio_file, "w", encoding="utf-8") as file:
#         json.dump(bio_data, file, ensure_ascii=False, indent=4)
#     with open(che_file, "w", encoding="utf-8") as file:
#         json.dump(che_data, file, ensure_ascii=False, indent=4)
#     with open(phy_file, "w", encoding="utf-8") as file:
#         json.dump(phy_data, file, ensure_ascii=False, indent=4)

# # 调用分类并追加的函数
# classify_and_append(
#     file_to_classify="conprehensive_questions.json",
#     bio_file="bio_only.json",
#     che_file="che_only.json",
#     phy_file="phy_only.json"
# )

# print("分类完成，数据已追加到对应的文件中！")