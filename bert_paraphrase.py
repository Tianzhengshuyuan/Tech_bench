import os
import json
import spacy
import argparse
import numpy as np
import torch
from tqdm import tqdm
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

# 加载 spacy 的中文模型
print("加载 spacy 的中文模型")
nlp = spacy.load("zh_core_web_sm")

# 加载 BERT 模型和分词器
print("加载预训练的 BERT 模型")
bert_model_name = "bert-base-chinese"  # 使用中文 BERT 模型
tokenizer = BertTokenizer.from_pretrained(bert_model_name)
bert_model = BertModel.from_pretrained(bert_model_name)
bert_model.eval()  # 设置为评估模式以禁用梯度计算

# 提取主语、谓语、宾语的函数
def extract_svo(sentence):
    doc = nlp(sentence)
    subject, predicate, obj = None, None, None

    for token in doc:
        if "nsubj" in token.dep_:
            subject = token.text
        if "ROOT" in token.dep_:
            predicate = token.text
        if "obj" in token.dep_:
            obj = token.text

    return subject, predicate, obj

# 使用 BERT 计算词嵌入的函数
def get_word_embedding(word):
    tokens = tokenizer(word, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = bert_model(**tokens)
    # 获取最后一层的输出，并取 [CLS] 或平均池化
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# 使用 BERT 找相似词的函数
def find_similar_word_bert(word, candidate_words):
    try:
        word_embedding = get_word_embedding(word)
        candidate_embeddings = [get_word_embedding(candidate) for candidate in candidate_words]
        # 计算余弦相似度
        similarities = cosine_similarity([word_embedding], candidate_embeddings)[0]
        # 找到相似度最高的词
        most_similar_idx = np.argmax(similarities)
        return candidate_words[most_similar_idx]
    except Exception as e:
        print(f"Error finding similar word for '{word}': {e}")
        return word  # 如果出错，返回原词

# 替换主语和谓语的函数
def replace_with_similar(sentence, candidate_words):
    subject, predicate, obj = extract_svo(sentence)
    if subject:
        subject_similar = find_similar_word_bert(subject, candidate_words)
        sentence = sentence.replace(subject, subject_similar, 1)
    if predicate:
        predicate_similar = find_similar_word_bert(predicate, candidate_words)
        sentence = sentence.replace(predicate, predicate_similar, 1)
    return sentence

def do_paraphrase(candidate_words):
    # 读取 JSON 文件
    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 遍历数据并替换内容
    for item in tqdm(data, desc="Processing items"):
        item["question"] = replace_with_similar(item["question"], candidate_words)
        for option in ["A", "B", "C", "D"]:
            item[option] = replace_with_similar(item[option], candidate_words)

    # 将修改后的数据写入新的 JSON 文件
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="将题目中的关键词进行同义词替换")
    parser.add_argument("--input_file", type=str, default="labeled_questions.json", help="原始 JSON 文件")
    parser.add_argument("--output_file", type=str, default="paraphrased_labeled_questions.json", help="进行同义词替换后的 JSON 文件")
    parser.add_argument("--candidate_words_file", type=str, default="candidate_words.json", help="候选同义词文件")
    args = parser.parse_args()

    # 加载候选同义词列表
    with open(args.candidate_words_file, "r", encoding="utf-8") as f:
        candidate_words = json.load(f)

    # 使用 BERT 进行近义词替换
    do_paraphrase(candidate_words)