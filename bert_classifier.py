import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from tqdm import tqdm
import numpy as np

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

# 提取文本和标签
texts = [item["text"] for item in all_data]
labels = [item["label"] for item in all_data]

# 2. 数据集划分
train_texts, test_texts, train_labels, test_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

# 3. 定义自定义数据集
class CustomDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        # 使用 BERT tokenizer 对文本进行编码
        encoded = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        return {
            "input_ids": encoded["input_ids"].squeeze(0),
            "attention_mask": encoded["attention_mask"].squeeze(0),
            "label": torch.tensor(label, dtype=torch.long),
        }

# 4. 加载预训练的 BERT 模型和 tokenizer
model_name = "bert-base-chinese"  # 使用中文的预训练 BERT 模型
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)  # 3 类分类

# 定义数据集
train_dataset = CustomDataset(train_texts, train_labels, tokenizer, max_length=128)
test_dataset = CustomDataset(test_texts, test_labels, tokenizer, max_length=128)

# 定义数据加载器
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16)

# 5. 定义训练参数
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
epochs = 3
loss_fn = torch.nn.CrossEntropyLoss()

# 6. 训练模型
def train_epoch(model, loader, optimizer, loss_fn, device, epoch, total_epochs):
    model.train()
    total_loss = 0
    loop = tqdm(loader, desc=f"Epoch {epoch}/{total_epochs}", position=0, leave=True)
    for batch in loop:
        optimizer.zero_grad()
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()

        # 更新进度条
        loop.set_postfix(loss=loss.item())
    return total_loss / len(loader)

# 7. 评估模型
def evaluate_model(model, loader, device, epoch):
    model.eval()
    predictions = []
    true_labels = []
    loop = tqdm(loader, desc=f"Evaluating Epoch {epoch}", position=0, leave=True)
    with torch.no_grad():
        for batch in loop:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1)
            predictions.extend(preds.cpu().numpy())
            true_labels.extend(labels.cpu().numpy())
    return predictions, true_labels

# 开始训练
for epoch in range(1, epochs + 1):
    train_loss = train_epoch(model, train_loader, optimizer, loss_fn, device, epoch, epochs)
    print(f"Epoch {epoch}/{epochs}, Training Loss: {train_loss:.4f}")

    # 评估模型
    predictions, true_labels = evaluate_model(model, test_loader, device, epoch)
    print("分类报告：")
    print(classification_report(true_labels, predictions, target_names=["生物", "化学", "物理"]))
    print("准确率：", accuracy_score(true_labels, predictions))

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
#     for item in tqdm(data_to_classify, desc="Classifying New Data"):
#         # 合并题干和选项
#         question = f"{item['question']} {item['A']} {item['B']} {item['C']} {item['D']}"
#         # 对问题进行编码
#         encoded = tokenizer(
#             question,
#             add_special_tokens=True,
#             max_length=128,
#             padding="max_length",
#             truncation=True,
#             return_tensors="pt",
#         )
#         input_ids = encoded["input_ids"].to(device)
#         attention_mask = encoded["attention_mask"].to(device)

#         # 预测类别
#         model.eval()
#         with torch.no_grad():
#             outputs = model(input_ids, attention_mask=attention_mask)
#             predicted_label = torch.argmax(outputs.logits, dim=1).item()

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