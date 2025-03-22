import json

with open("output_phy.json", "r", encoding="utf-8") as file:
    data_phy = json.load(file)

filtered_items_phy = [item for item in data_phy if "exam" in item and "理综" in item["exam"] and not "物理" in item["exam"]]

with open("output_che.json", "r", encoding="utf-8") as file:
    data_che = json.load(file)

filtered_items_che = [item for item in data_che if "exam" in item and "理综" in item["exam"] and not "化学" in item["exam"]]

with open("output_bio.json", "r", encoding="utf-8") as file:
    data_bio = json.load(file)

filtered_items_bio = [item for item in data_bio if "exam" in item and "理综" in item["exam"] and not "生物" in item["exam"]]

all_items = filtered_items_phy + filtered_items_che + filtered_items_bio

with open(f"conprehensive_questions.json", "w", encoding="utf-8") as file:
    json.dump(all_items, file, ensure_ascii=False, indent=4)