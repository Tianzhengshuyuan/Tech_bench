import json

# 加载 JSON 文件
with open("output_phy.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 去重逻辑
unique_entries = []
seen_questions = set()  # 用于存储唯一条目的标识

for entry in data:
    # 构造标识：仅比较 question, A, B, C, D
    identifier = (entry["question"], entry["A"], entry["B"], entry["C"], entry["D"])
    
    if identifier not in seen_questions:
        seen_questions.add(identifier)
        unique_entries.append(entry)
        
filtered_items = [item for item in unique_entries if "exam" in item and not "理综" in item["exam"] and "物理" in item["exam"]]

# 将去重且仅物理学科的数据保存到新文件
with open("phy_only.json", "w", encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False, indent=4)
    
# 加载 JSON 文件
with open("output_che.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 去重逻辑
unique_entries = []
seen_questions = set()  # 用于存储唯一条目的标识

for entry in data:
    # 构造标识：仅比较 question, A, B, C, D
    identifier = (entry["question"], entry["A"], entry["B"], entry["C"], entry["D"])
    
    if identifier not in seen_questions:
        seen_questions.add(identifier)
        unique_entries.append(entry)
        
filtered_items = [item for item in unique_entries if "exam" in item and not "理综" in item["exam"] and "化学" in item["exam"]]

# 将去重且仅化学学科的数据保存到新文件
with open("che_only.json", "w", encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False, indent=4)
    
# 加载 JSON 文件
with open("output_bio.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 去重逻辑
unique_entries = []
seen_questions = set()  # 用于存储唯一条目的标识

for entry in data:
    # 构造标识：仅比较 question, A, B, C, D
    identifier = (entry["question"], entry["A"], entry["B"], entry["C"], entry["D"])
    
    if identifier not in seen_questions:
        seen_questions.add(identifier)
        unique_entries.append(entry)
        
filtered_items = [item for item in unique_entries if "exam" in item and not "理综" in item["exam"] and "生物" in item["exam"]]

# 将去重且仅生物学科的数据保存到新文件
with open("bio_only.json", "w", encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False, indent=4)