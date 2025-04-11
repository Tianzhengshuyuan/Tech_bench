import json
import jieba
from tqdm import tqdm

jieba.load_userdict("jieba_user_dict.txt")
# 读取 JSON 文件
with open("phy_only.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 初始化存储分词结果的列表
jieba_cut_results = []

# 遍历数据并替换内容
for item in tqdm(data, desc="Processing items"):
    # 对 question 进行分词
    question_cut = " ".join(jieba.cut(item["question"]))
    
    # 对每个选项（A, B, C, D）进行分词
    options_cut = {}
    for option_key in ["A", "B", "C", "D"]:
        options_cut[option_key] = " ".join(jieba.cut(item[option_key]))
    
    # 构造分词后的结果
    jieba_cut_results.append({
        "question": question_cut,
        "options": options_cut
    })

# 将修改后的数据写入新的 JSON 文件
with open("jieba_cut_old.json", "w", encoding="utf-8") as f:
    json.dump(jieba_cut_results, f, ensure_ascii=False, indent=4)