import json
import random
import argparse
from tqdm import tqdm


def load_replace_rules(file_path):
    """加载替换规则"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def replace_with_synonym(text, rules):
    """
    使用替换规则对文本进行同义词替换
    """
    replace_list = []
    for rule in rules:
        origin = rule["origin"]
        replace_options = rule["replace"].split("、")
        no_before = rule.get("no_before", "")  # 如果不存在，则默认为空字符串
        no_after = rule.get("no_after", "")   # 如果不存在，则默认为空字符串

        if origin in replace_list:
            continue
        
        # 查找所有匹配的 origin
        start = 0
        while start < len(text):
            index = text.find(origin, start)
            if index == -1:
                break

            # 检查 no_before
            before = text[index - len(no_before):index] if no_before and index >= len(no_before) else ""

            # 检查 no_after，并确保不越界
            after_index_end = index + len(origin) + len(no_after)
            after = text[index + len(origin):after_index_end] if no_after and after_index_end <= len(text) else ""

            # 如果前后有禁用词，则跳过替换
            if (no_before and before == no_before) or (no_after and after == no_after):
                start = index + len(origin)
                continue

            # 随机选择一个替换词并替换
            replacement = random.choice(replace_options)
            print(f"替换 '{origin}' 为 '{replacement}'")
            replace_list.append(replacement)
            text = text[:index] + replacement + text[index + len(origin):]
            start = index + len(replacement)

    return text


def do_paraphrase(input_file, replace_file, output_file):
    """
    主函数：读取输入文件，进行替换，并保存到输出文件
    """
    # 加载替换规则
    replace_rules = load_replace_rules(replace_file)

    # 读取输入文件
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 遍历数据并替换内容
    for item in tqdm(data, desc="对问题和选项进行同义词替换"):
        item["question"] = replace_with_synonym(item["question"], replace_rules)
        for option in ["A", "B", "C", "D"]:
            item[option] = replace_with_synonym(item[option], replace_rules)

    # 保存到输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="将题目中的关键词进行同义词替换")
    parser.add_argument("--input_file", type=str, default="json/phy_no_picture.json", help="原始 JSON 文件路径")
    parser.add_argument("--replace_file", type=str, default="json/replace.json", help="替换规则 JSON 文件路径")
    parser.add_argument("--output_file", type=str, default="json/paraphrase_questions.json", help="替换后的 JSON 文件路径")
    args = parser.parse_args()

    # 执行同义词替换
    do_paraphrase(args.input_file, args.replace_file, args.output_file)