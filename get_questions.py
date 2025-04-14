import json
import random
import argparse

def load_json(file_path):
    """
    加载 JSON 文件。
    :param file_path: JSON 文件路径
    :return: 加载后的数据
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"加载文件 {file_path} 时出错: {e}")
        return []

def save_json(data, file_path):
    """
    保存数据到 JSON 文件。
    :param data: 要保存的数据
    :param file_path: 保存路径
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"数据已保存到文件: {file_path}")
    except Exception as e:
        print(f"保存文件 {file_path} 时出错: {e}")

def filter_questions(data):
    """
    筛选符合条件的问题。
    条件：A、B、C、D 键的值不为空，且存在 answer 键。
    :param data: 原始问题数据
    :return: 筛选后的问题列表
    """
    valid_questions = []
    for item in data:
        # 检查 A, B, C, D 是否为空
        if all(item.get(option, "").strip() for option in ["A", "B", "C", "D"]):
            # 检查是否存在 answer 键
            if "answer" in item and item["answer"].strip():
                valid_questions.append(item)
    return valid_questions

def main(input_file, output_file, use_random, num_questions):
    """
    主函数，执行筛选
    """
    # 加载输入文件
    data = load_json(input_file)
    if not data:
        print("输入数据为空或文件加载失败！")
        return

    # 筛选符合条件的问题
    valid_questions = filter_questions(data)
    
    if use_random:
        # 从筛选结果中随机选取 num_questions 条
        selected_questions = random.sample(valid_questions, min(num_questions, len(valid_questions)))
    else:
        # 如果不随机，则选取前 num_questions 条
        selected_questions = valid_questions[:num_questions]

    # 保存到输出文件
    save_json(selected_questions, output_file)


if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="从 JSON 文件中随机提取符合条件的题目")
    parser.add_argument("--input_file", type=str, default="json/phy_only.json", help="输入的 JSON 文件路径")
    parser.add_argument("--output_file", type=str, default="json/selected_questions.json", help="输出的 JSON 文件路径")
    parser.add_argument("--random", type=bool, default=True, help="是否随机提取题目")
    parser.add_argument("--num_questions", type=int, default=100, help="随机提取的题目数量")
    args = parser.parse_args()

    # 执行主函数
    main(args.input_file, args.output_file, args.random, args.num_questions)