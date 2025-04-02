import os
import json
import spacy
import torch
import argparse
import numpy as np
from tqdm import tqdm
from transformers import BertTokenizer, BertModel, BertForMaskedLM, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from sklearn.metrics.pairwise import cosine_similarity
import pickle  # 用于缓存词汇表嵌入

# 加载 spacy 的中文模型
print("加载 spacy 的中文模型")
nlp = spacy.load("zh_core_web_sm")

# 全局变量，用于缓存词汇表和嵌入
bert_model_name = "bert-base-chinese"  # 使用中文 BERT 模型
tokenizer = BertTokenizer.from_pretrained(bert_model_name)
bert_model = None  # 模型将在程序启动时加载
vocab = None  # BERT 的词汇表
vocab_embeddings = None  # 将在程序启动时加载或生成

def get_token_embedding(token):
    # 将 token 转换为模型输入的 ID
    token_id = tokenizer.convert_tokens_to_ids(token)
    if token_id is None:
        raise ValueError(f"Token '{token}' not found in the tokenizer vocabulary.")
    token_tensor = torch.tensor([[token_id]])
    with torch.no_grad():
        outputs = bert_model(input_ids=token_tensor)

    # 获取最后一层的输出，取该 token 的 embedding
    embedding = outputs.last_hidden_state.squeeze(0).squeeze(0).numpy()
    return embedding

def get_word_embeddings(word):
    # 对输入的单词进行分词并生成对应的张量
    tokens = tokenizer(word, return_tensors="pt", padding=True, truncation=True)
    input_ids = tokens["input_ids"].squeeze(0).tolist()  # 获取 token IDs
    token_strings = tokenizer.convert_ids_to_tokens(input_ids)  # 将 token IDs 转为字符串
    print(f"Tokens for '{word}': {token_strings}")  # 打印 token 字符串
    with torch.no_grad():
        # 使用 BERT 模型进行前向传播
        outputs = bert_model(**tokens)
    # 获取最后一层的输出，每个 token 的 embedding
    embeddings = outputs.last_hidden_state.squeeze(0).numpy()
    # 返回一个列表，其中每个元素是一个 token 的 embedding
    return embeddings.tolist()

# 预计算并缓存词汇表嵌入
def generate_vocab_embeddings(cache_file="vocab_embeddings.pkl"):
    global vocab_embeddings, vocab

    if os.path.exists(cache_file):
        print(f"从缓存文件 {cache_file} 加载词汇表嵌入...")
        with open(cache_file, "rb") as f:
            vocab_embeddings = pickle.load(f)
    else:
        print("计算 BERT 词汇表的嵌入向量...")
        vocab = list(tokenizer.vocab.keys())
        
        vocab_embeddings = []
        for vocab_word in tqdm(vocab, desc="Processing vocab embeddings"):
            vocab_embedding = get_token_embedding(vocab_word)
            vocab_embeddings.append(vocab_embedding)
        vocab_embeddings = np.array(vocab_embeddings)  # 转为 NumPy 数组

        # 缓存到文件中
        print(f"保存词汇表嵌入到缓存文件 {cache_file}...")
        with open(cache_file, "wb") as f:
            pickle.dump(vocab_embeddings, f)
    print(list(tokenizer.vocab.keys()))

# 使用 BERT 找相似词的函数（从缓存的词汇表嵌入中寻找）
def find_similar_word_bert(word, topn=1):
    try:
        # 获取目标词的嵌入列表（每个 token 的 embedding）
        word_embeddings = get_word_embeddings(word)  # 确保调用的是返回 embedding 列表的函数
        print(len(word_embeddings))
        similar_words = []  # 用于存储每个 token 的最相似词

        # 遍历每个 token 的 embedding
        for i, token_embedding in enumerate(word_embeddings):
            if i == 0 or i == len(word_embeddings)-1:
                continue
            # 计算当前 token 与词汇表中所有词的余弦相似度
            similarities = cosine_similarity([token_embedding], vocab_embeddings)[0]
            # 找到相似度最高的词
            top_indices = np.argsort(similarities)[::-1]  # 按相似度从高到低排序
            
            for idx in top_indices:
                similar_word = vocab[idx]
                if similar_word != word:  # 确保返回的词与输入词不同
                    similar_words.append(similar_word)  # 添加到相似词列表
                    print(similar_word)
                    break  # 找到第一个不同的相似词后跳出循环

        # 将所有相似词拼接成一个字符串
        result = "".join(similar_words)
        return result

    except Exception as e:
        print(f"Error finding similar word for '{word}': {e}")
        return word  # 如果出错，返回原词


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

# 替换主语和谓语的函数
def replace_with_similar(sentence):
    subject, predicate, obj = extract_svo(sentence)
    if subject:
        subject_similar = find_similar_word_bert(subject, topn=1)
        print("subject is: "+subject)
        print("subject_similar is: "+subject_similar)
        sentence = sentence.replace(subject, subject_similar, 1)
    if obj:
        obj_similar = find_similar_word_bert(obj, topn=1)
        print("object is: "+obj)
        print("object_similar is: "+obj_similar)
        sentence = sentence.replace(obj, obj_similar, 1)
    return sentence

# 微调 BERT 模型
def fine_tune_bert(data_file, output_dir, num_train_epochs=3, batch_size=8):
    global bert_model, tokenizer, vocab

    # 加载训练数据
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    questions = [item["question"] for item in data if "question" in item]

    # 将数据转换为 Dataset 格式
    def preprocess_data(questions):
        def tokenize_function(examples):
            return tokenizer(
                examples["text"],
                max_length=128,
                padding="max_length",
                truncation=True,
                return_special_tokens_mask=True,
            )
        from datasets import Dataset
        dataset = Dataset.from_dict({"text": questions})
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        return tokenized_dataset

    tokenized_dataset = preprocess_data(questions)

    # 数据整理器（用于掩码语言模型任务）
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=True, mlm_probability=0.15
    )

    # 训练参数
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir=f"{output_dir}/logs",
        logging_steps=500,
        evaluation_strategy="no",
    )

    # Trainer
    trainer = Trainer(
        model=bert_model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    # 开始微调
    print("开始微调 BERT 模型...")
    trainer.train()

    # 保存微调后的模型
    print(f"保存微调后的模型到 {output_dir}...")
    bert_model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)


def do_paraphrase():
    # 读取 JSON 文件
    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 遍历数据并替换内容
    for item in tqdm(data, desc="Processing items"):
        item["question"] = replace_with_similar(item["question"])
        for option in ["A", "B", "C", "D"]:
            item[option] = replace_with_similar(item[option])

    # 将修改后的数据写入新的 JSON 文件
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="将题目中的关键词进行同义词替换")
    parser.add_argument("--input_file", type=str, default="labeled_questions.json", help="原始 JSON 文件")
    parser.add_argument("--output_file", type=str, default="paraphrased_labeled_questions.json", help="进行同义词替换后的 JSON 文件")
    parser.add_argument("--cache_file", type=str, default="vocab_embeddings.pkl", help="词汇表嵌入的缓存文件")
    parser.add_argument("--fine_tune", action="store_true", help="是否对 BERT 模型进行微调")
    parser.add_argument("--fine_tune_data", type=str, default="phy_only.json", help="用于微调的数据文件")
    parser.add_argument("--fine_tune_output", type=str, default="./fine_tuned_bert", help="微调后模型的保存路径")
    args = parser.parse_args()

    # 加载或微调模型
    if args.fine_tune:
        print("使用微调 bert 模型")
        bert_model = BertForMaskedLM.from_pretrained(bert_model_name)
        fine_tune_bert(args.fine_tune_data, args.fine_tune_output)
        bert_model = BertModel.from_pretrained(args.fine_tune_output)
    else:
        print("使用预训练 bert 模型")
        bert_model = BertModel.from_pretrained(bert_model_name)

    # 加载分词器和词汇表
    tokenizer = BertTokenizer.from_pretrained(args.fine_tune_output if args.fine_tune else bert_model_name)
    vocab = list(tokenizer.vocab.keys())

    # 预计算或加载词汇表嵌入
    generate_vocab_embeddings(args.cache_file)

    # 使用 BERT 进行近义词替换
    do_paraphrase()