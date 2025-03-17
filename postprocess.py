import json

# 加载 JSON 文件
with open("output.json", "r", encoding="utf-8") as file:
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

# 将去重后的数据保存到新文件
with open("output_deduplicated.json", "w", encoding="utf-8") as file:
    json.dump(unique_entries, file, ensure_ascii=False, indent=4)
        
        
# 初始化计数器
total_entries = 0
empty_value_count = 0
empty_ABCD_count = 0
empty_answer_count = 0
empty_ABCD = []
empty_answer = []
        
# 要检查的键
key_to_check1 = ["A", "B", "C", "D"]
key_to_check2 = ["answer"]

# 遍历每个条目
for entry in unique_entries:
    total_entries += 1
    already_count = 0
    
    # 检查是否有ABCD选项对应的值为空
    for key in key_to_check1:
        if entry[key] == "" or entry[key].strip() == "":
            empty_ABCD_count += 1
            empty_value_count += 1
            empty_ABCD.append(entry)
            already_count = 1
            break  # 只计一次，跳出当前条目的检查
 
    # 检查是否有answer对应的值为空
    if "answer" not in entry:        
        empty_answer_count += 1
        empty_answer.append(entry)
        if already_count == 0:
            empty_value_count += 1
 

# 输出统计结果
rate_value = round(empty_value_count/total_entries*100, 2)
rate_ABCD = round(empty_ABCD_count/total_entries*100, 2)
rate_answer = round(empty_answer_count/total_entries*100, 2)
print(f"总条目数：{total_entries}")
print(f"不完整条目数：{empty_value_count}"+" 比例为："+str(rate_value)+"%")
print(f"选项不完整条目数：{empty_ABCD_count}"+" 比例为："+str(rate_ABCD)+"%")
print(f"答案不完整条目数：{empty_answer_count}"+" 比例为："+str(rate_answer)+"%")
    
with open("empty_ABCD.json", "w", encoding="utf-8") as output_file:
    json.dump(empty_ABCD, output_file, ensure_ascii=False, indent=4)
    
with open("empty_answer.json", "w", encoding="utf-8") as output_file:
    json.dump(empty_answer, output_file, ensure_ascii=False, indent=4)
    
