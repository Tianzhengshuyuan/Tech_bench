import json

with open("json/output_phy.json", "r", encoding="utf-8") as file:
    data_phy = json.load(file)

filtered_items_phy = [item for item in data_phy if "exam" in item and "理综" in item["exam"] and not "物理" in item["exam"]]

with open("json/output_che.json", "r", encoding="utf-8") as file:
    data_che = json.load(file)

filtered_items_che = [item for item in data_che if "exam" in item and "理综" in item["exam"] and not "化学" in item["exam"]]

with open("json/output_bio.json", "r", encoding="utf-8") as file:
    data_bio = json.load(file)

filtered_items_bio = [item for item in data_bio if "exam" in item and "理综" in item["exam"] and not "生物" in item["exam"]]

# 合并从3个文件中提取出来的内容
all_items = filtered_items_phy + filtered_items_che + filtered_items_bio

# 去重逻辑
unique_entries = []
seen_questions = set()  # 用于存储唯一条目的标识

for entry in all_items:
    # 构造标识：仅比较 question, A, B, C, D
    identifier = (entry["question"], entry["A"], entry["B"], entry["C"], entry["D"])
    
    if identifier not in seen_questions:
        seen_questions.add(identifier)
        unique_entries.append(entry)
        
with open(f"json/conprehensive_questions.json", "w", encoding="utf-8") as file:
    json.dump(unique_entries, file, ensure_ascii=False, indent=4)