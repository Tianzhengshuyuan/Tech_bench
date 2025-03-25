import json
import argparse

def remove_entries_with_keyword(input_file, output_file, keyword="图"):
    # 打开并读取 JSON 文件内容
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
        return
    except json.JSONDecodeError:
        print(f"错误：文件 {input_file} 不是有效的 JSON 格式")
        return

    # 过滤掉包含关键字的条目
    filtered_data = [
        item for item in data
        if not (
            keyword in item.get("question", "") or
            keyword in item.get("A", "") or
            keyword in item.get("B", "") or
            keyword in item.get("C", "") or
            keyword in item.get("D", "")
        )
    ]

    # 将过滤后的数据写入输出文件
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)
        print(f"处理完成，过滤后的数据已保存到 {output_file}")
    except Exception as e:
        print(f"错误：无法写入输出文件 {output_file}，错误信息：{e}")

if __name__ == "__main__":
    # 使用 argparse 模块处理命令行参数
    parser = argparse.ArgumentParser(description="过滤 JSON 文件中包含特定关键字的条目")
    parser.add_argument("--input_file", help="输入 JSON 文件路径")
    parser.add_argument("--output_file", help="输出 JSON 文件路径")
    parser.add_argument(
        "-k", "--keyword", default="图", help="要过滤的关键字（默认：图）"
    )

    args = parser.parse_args()

    # 调用函数处理输入和输出文件
    remove_entries_with_keyword(args.input_file, args.output_file, args.keyword)