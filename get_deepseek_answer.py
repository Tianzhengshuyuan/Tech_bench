import json
import random
import argparse
from tqdm import tqdm
from openai import OpenAI

# 配置 DeepSeek API 客户端
client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")

def call_deepseek_api(question):
    """
    调用 DeepSeek API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return "API 调用失败"


def process_questions(input_file_1, input_file_2, output_file, all_new=False):
    """
    随机从两个 JSON 文件中选题，或者全部从 input_file_2 中选题，调用 DeepSeek API 获取答案，并统计结果。
    """
    try:
        # 读取两个输入文件
        with open(input_file_1, "r", encoding="utf-8") as f1, open(input_file_2, "r", encoding="utf-8") as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

        # 确保两个文件的题目数量一致
        if not all_new and len(data1) != len(data2):
            print("两个文件的题目数量不一致，请检查输入文件！")
            return

        results = []
        wrong_results = []
        new_but_meiyou = []
        
        file1_meiyou_ratio = 0
        file1_correct_answer_ratio = 0
        file2_you_ratio = 0

        file1_count = 0
        file1_correct_count = 0
        file1_meiyou_count = 0
        file2_count = 0
        file2_you_count = 0

        # 确定处理的数据源
        data_source = data2 if all_new else zip(data1, data2)

        # 遍历数据并处理
        for i, item in tqdm(enumerate(data_source), desc="Deepseek 处理问题进度", total=len(data2), dynamic_ncols=True, mininterval=0.1):
            if all_new or (not all_new and random.choice([True, False])):
                # 从更改后的题目中选择
                if not all_new:
                    item = item[1]  # 如果不是 all_new，从 data2 中取题目
                question = item.get("question", "").strip()
                options = {
                    "A": item.get("A", "").strip(),
                    "B": item.get("B", "").strip(),
                    "C": item.get("C", "").strip(),
                    "D": item.get("D", "").strip(),
                }
                correct_answer = item.get("answer", "").strip()
                
                # 拼接完整问题
                full_question = f"{question}\nA. {options['A']}\nB. {options['B']}\nC. {options['C']}\nD. {options['D']}\n"
                full_question += "上面的题目逻辑和表述有什么问题吗？有的话请回复“有问题”并分析存在的问题，没问题的话请回复“没问题，正确答案是”并给出正确答案，不用解释"

                # 调用 DeepSeek API
                answer = call_deepseek_api(full_question)

                # 统计 metrics
                file2_count += 1
                if "有问题" in answer:
                    file2_you_count += 1
                else:
                    new_but_meiyou.append({
                        "source": "新题",
                        "full_question": full_question,
                        "deepseek_answer": answer,
                        "true_answer": correct_answer,
                        "回复是否包含“有问题”": "有问题" in answer,
                    })

                # 保存结果
                results.append({
                    "source": "新题",
                    "full_question": full_question,
                    "deepseek_answer": answer,
                    "true_answer": correct_answer,
                    "回复是否包含“有问题”": "有问题" in answer,
                })
            else:
                # 从原题中选择
                item = item[0]  # 从 data1 中取题目
                question = item.get("question", "").strip()
                options = {
                    "A": item.get("A", "").strip(),
                    "B": item.get("B", "").strip(),
                    "C": item.get("C", "").strip(),
                    "D": item.get("D", "").strip(),
                }
                correct_answer = item.get("answer", "").strip()

                # 拼接完整问题
                full_question = f"{question}\nA. {options['A']}\nB. {options['B']}\nC. {options['C']}\nD. {options['D']}\n"
                full_question += "上面的题目逻辑和表述有什么问题吗？有的话请回复“有问题”并分析存在的问题，没问题的话请回复“没问题，正确答案是”并给出正确答案，不用解释"

                # 调用 DeepSeek API
                answer = call_deepseek_api(full_question)

                # 统计 metrics
                file1_count += 1
                if "没问题" in answer:
                    file1_meiyou_count += 1

                    extracted_answer = answer.split("没问题，正确答案是")[-1].strip()  # 提取“没问题，正确答案是”后面的部分

                    # 分割正确答案和模型的回答，确保模型的回答严格匹配正确答案
                    correct_answer_set = set(correct_answer)  # 正确答案转为集合
                    response_answer_set = set(extracted_answer)  # 模型的回答转为集合

                    # 判断模型的回答是否完全等于正确答案
                    if response_answer_set == correct_answer_set:
                        file1_correct_count += 1
                    else:
                        wrong_results.append({
                            "source": "原题",
                            "full_question": full_question,
                            "deepseek_answer": answer,
                            "true_answer": correct_answer,
                            "回复是否包含“没问题”": "没问题" in answer,
                            "大模型回复是否正确": correct_answer in answer,
                        })


                # 保存结果
                results.append({
                    "source": "原题",
                    "full_question": full_question,
                    "deepseek_answer": answer,
                    "true_answer": correct_answer,
                    "回复是否包含“没问题”": "没问题" in answer,
                    "大模型回复是否正确": correct_answer in answer,
                })

        # 计算比例
        file1_meiyou_ratio = (
            file1_meiyou_count / file1_count if file1_count > 0 else 0
        )
        file1_correct_answer_ratio = (
            file1_correct_count / file1_meiyou_count if file1_meiyou_count > 0 else 0
        )
        file2_you_ratio = (
            file2_you_count / file2_count if file2_count > 0 else 0
        )

        # 输出统计结果
        print("统计结果：")
        print(f"从 原题 中选择的题目里，DeepSeek 回复中包含“没问题，正确答案是”的比例: {file1_meiyou_ratio:.2f}")
        print(f"从 原题 中选择的题目里，DeepSeek 回复的正确答案确实是正确答案的比例: {file1_correct_answer_ratio:.2f}")
        print(f"从 改题 中选择的题目里，DeepSeek 回复中包含“有问题”的比例: {file2_you_ratio:.2f}")

        # 将结果保存到输出文件
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        with open("json/wrong_results.json", "w", encoding="utf-8") as f:
            json.dump(wrong_results, f, ensure_ascii=False, indent=4)
        with open("json/new_but_meiyou.json", "w", encoding="utf-8") as f:
            json.dump(new_but_meiyou, f, ensure_ascii=False, indent=4)
            
        print(f"处理完成，结果已保存到文件: {output_file}")

    except Exception as e:
        print(f"处理问题时出错: {e}")


# 主函数
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获得 DeepSeek 的答案并验证结果")
    parser.add_argument("--input_file1", type=str, default="json/selected_questions.json", help="输入的 JSON 文件路径")
    parser.add_argument("--input_file2", type=str, default="json/paraphrased_labeled_questions.json", help="输入的 JSON 文件路径")
    parser.add_argument("--output_file", type=str, default="json/answers_with_validation.json", help="输出的 JSON 文件路径")
    parser.add_argument("--all_new", action="store_true", help="是否全部从 input_file2 中选择题目")
    args = parser.parse_args()
    process_questions(args.input_file1, args.input_file2, args.output_file, args.all_new)