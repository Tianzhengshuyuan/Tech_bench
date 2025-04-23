import re
import json
import random
import argparse
from tqdm import tqdm
import openai
import os

os.environ["HTTP_PROXY"] = "http://localhost:7890"
os.environ["HTTPS_PROXY"] = "http://localhost:7890"

def call_gpt_api(question):
    """
    调用 gpt API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 gpt API 时出错: {e}")
        return "API 调用失败"

def process_questions(input_file, output_file):
    """
    调用 gpt API 获取答案，并统计结果。
    """
    try:
        # 读取输入文件
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        results = []

        count = 0
        correct_count = 0
        correct = False

        # 遍历数据并处理
        for i, item in tqdm(enumerate(data), desc="gpt 处理问题进度", total=len(data)):
            question = item.get("question", "").strip()
            options = {
                "A": item.get("A", "").strip(),
                "B": item.get("B", "").strip(),
                "C": item.get("C", "").strip(),
                "D": item.get("D", "").strip(),
            }

            correct_answer = item.get("answer", "").strip()
            if not correct_answer:
                continue
            
            count += 1

            # 拼接完整问题
            full_question = f"{question}\nA. {options['A']}\nB. {options['B']}\nC. {options['C']}\nD. {options['D']}\n"
            full_question += "上面的题目的答案是什么？答案可能不止一个，请回复“正确答案是”并给出正确答案，不用解释"
            
            # 调用 gpt API
            answer = call_gpt_api(full_question)
            print(answer)

            extracted_answer = re.findall(r'[A-D]', answer) 

            # 分割正确答案和模型的回答，确保模型的回答严格匹配正确答案
            correct_answer_set = set(correct_answer)  # 正确答案转为集合
            response_answer_set = set(extracted_answer)  # 模型的回答转为集合

            # 判断模型的回答是否完全等于正确答案
            if response_answer_set == correct_answer_set:
                correct_count += 1
                correct = True
            else:
                correct = False
                
            # 保存结果
            results.append({
                "full_question": full_question,
                "gpt_answer": answer,
                "true_answer": correct_answer,
                "correct": correct
            })


        # 将结果保存到输出文件
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
            
        print(f"处理完成，结果已保存到文件: {output_file}，共处理 {count} 个问题，正确率: {correct_count / count:.2%}")

    except Exception as e:
        print(f"处理问题时出错: {e}")


# 主函数
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获得 gpt 的答案并验证结果")
    parser.add_argument("--input_file", type=str, default="json/phy_no_picture.json", help="输入的 JSON 文件路径")
    parser.add_argument("--output_file", type=str, default="json/answers_from_gpt.json", help="输出的 JSON 文件路径")
    args = parser.parse_args()
    process_questions(args.input_file, args.output_file)