import json

with open("output_deduplicated.json", "r", encoding="utf-8") as file:
    data = json.load(file)

filtered_items = [item for item in data if "exam" in item and "理综" in item["exam"] and not "物理" in item["exam"]]
with open(f"conprehensive_questions.json", "w", encoding="utf-8") as file:
    json.dump(filtered_items, file, ensure_ascii=False, indent=4)