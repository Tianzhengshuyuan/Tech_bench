import os
import json
import spacy
import argparse
import numpy as np
from tqdm import tqdm
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

# 加载 spacy 的中文模型
print("加载 spacy 的中文模型")
nlp = spacy.load("zh_core_web_sm")

# 提取主语、谓语、宾语的函数
def extract_svo(sentence):

    doc = nlp(sentence)
    subject, predicate, obj = None, None, None

    for token in doc:
        # 提取主语
        if "nsubj" in token.dep_:
            subject = token.text
        # 提取谓语
        if "ROOT" in token.dep_:
            predicate = token.text
        # 提取宾语
        if "obj" in token.dep_:
            obj = token.text

    return subject, predicate, obj

def train_word2vec_on_custom_data():
    """
    在预训练的 Word2Vec 模型基础上，使用 JSON 文件中的 "question" 内容继续训练。
    """
    # 加载 Word2Vec 模型
    print("加载预训练好的 word2vec 模型")
    model_path = "./word2vec/sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5"
    pretrained_model = KeyedVectors.load_word2vec_format(model_path, binary=False)
    
    # 原始词汇表和对应向量
    original_vocab = pretrained_model.index_to_key
    original_vectors = pretrained_model.vectors

    # 过滤掉 None 值
    filtered_vocab = [word for word in original_vocab if word is not None]
    filtered_vectors = np.array([
        vector for word, vector in zip(original_vocab, original_vectors) if word is not None
    ])

    # 更新 pretrained_model 的词汇表和向量
    pretrained_model.index_to_key = filtered_vocab
    pretrained_model.vectors = filtered_vectors
    pretrained_model.key_to_index = {word: idx for idx, word in enumerate(filtered_vocab)}
    
    print("预训练 word2vec 模型加载完成！！")
    print("词向量维度为："+str(pretrained_model.vector_size))
    print("词汇表大小为："+str(len(pretrained_model.index_to_key)))
    # 将加载的 KeyedVectors 转换为 Word2Vec 模型
    word2vec_model = Word2Vec(vector_size=pretrained_model.vector_size, min_count=1, workers=4)
    word2vec_model.build_vocab([list(pretrained_model.index_to_key)])
    word2vec_model.wv.vectors = pretrained_model.vectors
    word2vec_model.wv.index_to_key = pretrained_model.index_to_key
    word2vec_model.wv.key_to_index = pretrained_model.key_to_index

    # 从 JSON 文件加载训练数据
    train_file = "./phy_only.json"
    print(f"从{train_file}中加载微调word2vec模型的数据...")
    with open(train_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 提取所有 "question" 字段的内容，并分词
    sentences = []
    for item in data:
        question = item.get("question", "")
        if question:
            # 使用 spaCy 分词
            doc = nlp(question)
            tokens = [token.text for token in doc]
            sentences.append(tokens)

    # 检查是否有有效的训练数据
    if not sentences:
        print("No valid training data found in the JSON file.")
        return

    # 更新词汇表并训练
    word2vec_model.build_vocab(sentences, update=True)
    print("基于自定义数据微调 word2vec 模型")
    word2vec_model.train(sentences, total_examples=word2vec_model.corpus_count, epochs=5) #word2vec_model.corpus_count是sentences中句子的数量

    # 保存新的模型
    save_path = "./word2vec/trained_word2vec.model"
    print(f"保存微调后的模型到 {save_path}...")
    word2vec_model.save(save_path)
    print("微调完成！！")
    return word2vec_model
    
# 使用 Word2Vec 找相似词的函数
def find_similar_word(word, word2vec_model):
    try:
        similar_words = word2vec_model.wv.most_similar(word, topn=1)
        if similar_words:
            return similar_words[0][0]
    except KeyError:
        # 如果词不在词汇表中，返回原词
        return word
    return word

# 替换主语和谓语的函数
def replace_with_similar(sentence, word2vec_model):
    sub, pred, obj = extract_svo(sentence)
    print("sentence is: "+sentence)
    if sub:
        sub_similar = find_similar_word(sub, word2vec_model)
        print("sub is: "+sub)
        print("similar sub is: ", end="")
        print(sub_similar)
        sentence = sentence.replace(sub, sub_similar, 1)
    if obj:
        obj_similar = find_similar_word(obj, word2vec_model)
        print("obj is: "+obj)
        print("similar ojb is: ", end="")
        print(obj_similar)
        sentence = sentence.replace(obj, obj_similar, 1)
    return sentence

def do_paraphrase(word2vec_model):
    # 读取 JSON 文件
    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 遍历数据并替换内容
    for item in tqdm(data, desc="Processing items"):
        item["question"] = replace_with_similar(item["question"], word2vec_model)
        for option in ["A", "B", "C", "D"]:
            item[option] = replace_with_similar(item[option], word2vec_model)

    # 将修改后的数据写入新的 JSON 文件
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="将题目中的关键词进行同义词替换")
    parser.add_argument("--input_file", type=str, default = "labeled_questions.json", help="原始 JSON 文件")
    parser.add_argument("--output_file", type=str, default="paraphrased_labeled_questions.json", help="进行同义词替换后的 JSON 文件")
    args = parser.parse_args()

    # 在预训练模型基础上用自定义数据训练
    word2vec_model = train_word2vec_on_custom_data()

    # 重新加载训练后的模型
    # word2vec_model = Word2Vec.load("./word2vec/trained_word2vec.model")

    # 近义词替换
    do_paraphrase(word2vec_model)
    
