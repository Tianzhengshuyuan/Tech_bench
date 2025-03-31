import json
import spacy
from gensim.models import KeyedVectors

# 加载 spaCy 的中文模型
nlp = spacy.blank("zh")

# 加载 Word2Vec 模型（假设有一个预训练的中文 Word2Vec 模型文件）
# 替换 model_path 为实际的 Word2Vec 模型路径
model_path = "path_to_your_chinese_word2vec_model.bin"
word2vec_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

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

# 使用 Word2Vec 找相似词的函数
def find_similar_word(word):
    try:
        similar_words = word2vec_model.most_similar(word, topn=1)
        if similar_words:
            return similar_words[0][0]
    except KeyError:
        # 如果词不在词汇表中，返回原词
        return word
    return word

# 替换主语和谓语的函数
def replace_with_similar(sentence):
    subject, predicate, obj = extract_svo(sentence)
    if subject:
        subject_similar = find_similar_word(subject)
        sentence = sentence.replace(subject, subject_similar, 1)
    if predicate:
        predicate_similar = find_similar_word(predicate)
        sentence = sentence.replace(predicate, predicate_similar, 1)
    return sentence

# 读取 JSON 文件
input_file = "input.json"
output_file = "output.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 遍历数据并替换内容
for item in data:
    item["question"] = replace_with_similar(item["question"])
    for option in ["A", "B", "C", "D"]:
        item[option] = replace_with_similar(item[option])

# 将修改后的数据写入新的 JSON 文件
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"替换后的 JSON 文件已保存为 {output_file}")