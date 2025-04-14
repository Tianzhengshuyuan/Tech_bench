import os
import json
import jieba
import spacy
import torch
import random
import stanza
import argparse
import numpy as np
from tqdm import tqdm
from spacy.lang.zh import Chinese
from spacy.tokenizer import Tokenizer
from wobert import WoBertTokenizer
from wobert_phy import WoBertPhyTokenizer
from transformers import AutoTokenizer, AutoModel, AutoModelForMaskedLM
from transformers import BertTokenizer, BertModel, BertForMaskedLM, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from sklearn.metrics.pairwise import cosine_similarity

# 加载 spacy 的中文模型
print("加载 spacy 的中文模型")
nlp = spacy.load("zh_core_web_sm")
# 自定义分词器（使用 Jieba）
def custom_tokenizer(nlp):
    def tokenizer(text):
        # 使用 Jieba 分词
        words = list(jieba.cut(text, cut_all=False))
        return spacy.tokens.Doc(nlp.vocab, words)
    return tokenizer

# 替换 spaCy 默认分词器
nlp.tokenizer = custom_tokenizer(nlp)
jieba.load_userdict("new_word.txt")

# # 加载 stanza 的中文模型
# print("加载 stanza 的中文模型")
# stanza.download("zh")
# nlp = stanza.Pipeline("zh")

# 全局变量，用于缓存词汇表和嵌入
bert_model_name = "bert-base-chinese"  # 使用中文 BERT 模型
tokenizer = BertTokenizer.from_pretrained(bert_model_name)
bert_model = None  # 模型将在程序启动时加载
vocab = None  # BERT 的词汇表
vocab_embeddings = None  # 将在程序启动时加载或生成

def find_similar_word_bert(word, sentence, topn=1):
    """
    使用 BERT 模型根据上下文找到指定单词的同义词。
    """
    # 将句子标记化
    inputs = tokenizer(sentence, return_tensors="pt")
    input_ids = inputs["input_ids"] # token的 ID
    token_type_ids = inputs["token_type_ids"] # 用于区分属于句子对里的哪一个句子
    attention_mask = inputs["attention_mask"] # 标记有效的token

    # 获取分词后的 token 列表
    tokenized_words = tokenizer.convert_ids_to_tokens(input_ids[0])
    print(f"分词后的句子：{tokenized_words} ")
    if args.wobert or args.wo_phy: # 使用词粒度 bert 模型
        word_start_idx = None
        for i in range(len(tokenized_words)):
            token = tokenized_words[i]
            if token == word:
                word_start_idx = i
                break
        if word_start_idx is None:
            print(f"在分词后的句子中没有找到'{word}'")
            return word  # 如果找不到，返回原单词
        
        masked_input_ids = input_ids.clone()
        # masked_input_ids 中第 0 个句子的第 idx 位置的 token ID 替换为 mask的ID
        masked_input_ids[0, word_start_idx] = tokenizer.mask_token_id

        # 通过模型计算 [MASK] 的预测分布
        with torch.no_grad():
            outputs = bert_model(masked_input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
            # outputs.logits的形状为(batch_size, sequence_length, vocab_size)
            # batch_size是输入的批大小，sequence_length是每个输入序列的长度，vocab_size是模型词汇表大小
            predictions = outputs.logits

        # 找到 [MASK] 的预测向量
        mask_logits = predictions[0, word_start_idx]
        probs = torch.softmax(mask_logits, dim=-1)

        # 获取概率最高的词
        topk_indices = torch.topk(probs, 2).indices # 概率最高的 topn 个词在词汇表中的索引
        similar_word = tokenizer.convert_ids_to_tokens(topk_indices[1].item()) # 如果是获取概率第二高则使用topk_indices[1].item()
    else:
        # 在 tokenized_words 中找到 word 的起始索引和长度
        word_start_idx = None
        word_length = 0
        # print("word is: "+word)
        for i in range(len(tokenized_words)):
            reconstructed_word = ""
            word_length = 0
            for j in range(i, len(tokenized_words)):
                token = tokenized_words[j]
                if token.startswith("##"):
                    reconstructed_word += token[2:]
                else:
                    reconstructed_word += token
                word_length += 1
                if reconstructed_word == word:
                    word_start_idx = i
                    break
            if word_start_idx is not None:
                break

        if word_start_idx is None:
            print(f"Word '{word}' not found in tokenized sentence.")
            return word  # 如果找不到，返回原单词

        # 替换 word 的每个 token 为 [MASK]，逐个预测
        predicted_tokens = []
        for idx in range(word_start_idx, word_start_idx + word_length):
            masked_input_ids = input_ids.clone()
            # masked_input_ids 中第 0 个句子的第 idx 位置的 token ID 替换为 mask的ID
            masked_input_ids[0, idx] = tokenizer.mask_token_id

            # 通过模型计算 [MASK] 的预测分布
            with torch.no_grad():
                outputs = bert_model(masked_input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
                # outputs.logits的形状为(batch_size, sequence_length, vocab_size)
                # batch_size是输入的批大小，sequence_length是每个输入序列的长度，vocab_size是模型词汇表大小
                predictions = outputs.logits

            # 找到 [MASK] 的预测向量
            mask_logits = predictions[0, idx]
            probs = torch.softmax(mask_logits, dim=-1)

            # 获取概率最高的词
            topk_indices = torch.topk(probs, 2).indices # 概率最高的 topn 个词在词汇表中的索引
            similar_token = tokenizer.convert_ids_to_tokens(topk_indices[1].item()) # 如果是获取概率第二高则使用topk_indices[1].item()
            predicted_tokens.append(similar_token)

        # 拼接预测的 token，生成替换后的完整词语
        similar_word = "".join([t if not t.startswith("##") else t[2:] for t in predicted_tokens])
    # 返回拼接后的相似词
    # print("word is: "+word+", sim word is: "+similar_word)
    return similar_word

# 使用 spacy 提取主语、谓语、宾语的函数
def extract_svo_spacy(text):
    doc = nlp(text)  # 使用 spaCy 对文本进行分析
    all_svo = []  # 用于存储所有 SVO

    for sent in doc.sents:  # 自动分割句子
        sub, pred, obj = None, None, None
        print("sent is: "+str(sent))
        # 遍历句子中的每个词
        for token in sent:
            # 主语：依存关系中包含 nsubj
            if "nsubj" in token.dep_:
                sub = token.text
            # 谓语：依存关系是句子的 ROOT
            if "ROOT" in token.dep_:
                pred = token.text
            # 宾语：依存关系中包含 obj
            if "obj" in token.dep_:
                obj = token.text

        all_svo.append((sub, pred, obj))
        print("SVO is: ", end="")
        print(sub, pred, obj)

    return all_svo

# 使用 stanza 提取主语、谓语和宾语的函数
def extract_svo_stanza(text):
    doc = nlp(text)  # 使用 Stanza 对文本进行分析
    all_svo = []  # 用于存储所有 SVO

    for sentence in doc.sentences:  # 遍历每个句子
        sub, pred, obj = None, None, None
        print("Sentence: ", sentence.text)
        
        for word in sentence.words:  # 遍历句子中的每个词
            # 主语：依存关系是 nsubj
            if word.deprel == "nsubj":
                sub = word.text
            # 谓语：依存关系是 ROOT
            if word.head == 0:  # Stanza 的 ROOT 的 head 是 0
                pred = word.text
            # 宾语：依存关系是 obj
            if "obj" in word.deprel:
                obj = word.text
        
        all_svo.append((sub, pred, obj))
        print("SVO: ", sub, pred, obj)

    return all_svo
# 提取名词的函数
def extract_nouns(sentence):
    doc = nlp(sentence)
    nouns = []

    for token in doc:
        # 判断 token 是否为普通名词 (NOUN) 或专有名词 (PROPN)
        if token.pos_ in ["NOUN", "PROPN"]:
            nouns.append(token.text)
    print(nouns)
    return nouns

# 替换主语和谓语的函数
def replace_with_similar(sentence):
    # all_svo = extract_svo_spacy(sentence)
    # if not all_svo:
    #     print(f"No SVO found in sentence {sentence}")
    #     return sentence 
    # for sub, pred, obj in all_svo:   
    #     if sub:
    #         sub_similar = find_similar_word_bert(sub, sentence, topn=1)
    #         print("subject is: "+sub)
    #         print("subject_similar is: "+sub_similar)
    #         sentence = sentence.replace(sub, sub_similar, 1)
    #     if obj:
    #         obj_similar = find_similar_word_bert(obj, sentence, topn=1)
    #         print("object is: "+obj)
    #         print("object_similar is: "+obj_similar)
    #         sentence = sentence.replace(obj, obj_similar, 1)
    # return sentence  

    nouns = extract_nouns(sentence)
    print(sentence)
    if not nouns:
        return sentence  # 如果没有名词，直接返回原句
    # 根据指定的比例随机选择名词进行替换
    num_to_replace = max(1, int(len(nouns) * args.ratio))
    nouns_to_replace = random.sample(nouns, num_to_replace)
    for noun in nouns_to_replace:
        noun_similar = find_similar_word_bert(noun, sentence, topn=1)
        print("noun is: "+noun+" similar is: "+noun_similar)
        sentence = sentence.replace(noun, noun_similar, 1)
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
    count=0
    for item in tqdm(data, desc="使用 BERT 进行同义词替换进度"):
        item["question"] = replace_with_similar(item["question"])
        for option in ["A", "B", "C", "D"]:
            item[option] = replace_with_similar(item[option])

    # 将修改后的数据写入新的 JSON 文件
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="将题目中的关键词进行同义词替换")
    parser.add_argument("--input_file", type=str, default="json/labeled_questions.json", help="原始 JSON 文件")
    parser.add_argument("--output_file", type=str, default="json/paraphrased_labeled_questions.json", help="进行同义词替换后的 JSON 文件")
    parser.add_argument("--cache_file", type=str, default="vocab_embeddings.pkl", help="词汇表嵌入的缓存文件")
    parser.add_argument("--fine_tune", action="store_true", help="是否对 BERT 模型进行微调")
    parser.add_argument("--physbert", action="store_true", help="是否使用针对物理领域的 bert 模型")
    parser.add_argument("--wobert", action="store_true", help="是否使用词粒度的 bert 模型")
    parser.add_argument("--wo_phy", action="store_true", help="是否使用物理领域词粒度的 bert 模型")
    parser.add_argument("--fine_tune_data", type=str, default="json/phy_only.json", help="用于微调的数据文件")
    parser.add_argument("--fine_tune_output", type=str, default="./fine_tuned_bert", help="微调后模型的保存路径")
    parser.add_argument("--ratio", type=float, default=1.0, help="替换名词的比例，范围为 0 到 1")
    args = parser.parse_args()

    # 加载或微调模型
    if args.fine_tune:
        print("使用微调 bert 模型")
        bert_model = BertForMaskedLM.from_pretrained(bert_model_name)
        fine_tune_bert(args.fine_tune_data, args.fine_tune_output)
        bert_model = BertForMaskedLM.from_pretrained(args.fine_tune_output)
        tokenizer = BertTokenizer.from_pretrained(args.fine_tune_output)
    elif args.physbert:
        print("使用物理领域 bert 模型")
        bert_model = AutoModelForMaskedLM.from_pretrained("thellert/physbert_cased") 
        tokenizer = AutoTokenizer.from_pretrained("thellert/physbert_cased")
    elif args.wobert:
        print("使用词粒度 bert 模型")
        # bert_model = BertForMaskedLM.from_pretrained("junnyu/wobert_chinese_base")        
        # tokenizer = WoBertTokenizer.from_pretrained("junnyu/wobert_chinese_base")
        bert_model = BertForMaskedLM.from_pretrained("junnyu/wobert_chinese_plus_base")        
        tokenizer = WoBertTokenizer.from_pretrained("junnyu/wobert_chinese_plus_base")
    elif args.wo_phy:
        print("使用物理领域词粒度 bert 模型")
        bert_model = BertForMaskedLM.from_pretrained("./wo_phy_pytorch")        
        tokenizer = WoBertPhyTokenizer.from_pretrained("./wo_phy_pytorch", custom_word_dict="new_word.txt")        
    else:
        print("使用预训练 bert 模型")
        bert_model = BertForMaskedLM.from_pretrained(bert_model_name)
        tokenizer = BertTokenizer.from_pretrained(bert_model_name)

    # 加载词汇表
    vocab = list(tokenizer.vocab.keys())

    # 使用 BERT 进行近义词替换
    do_paraphrase()