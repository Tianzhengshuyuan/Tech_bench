import json
from tqdm import tqdm
from openai import OpenAI

# 配置 DeepSeek API 客户端
client = OpenAI(api_key="sk-09da13b2c97948628523d042d6a02f06", base_url="https://api.deepseek.com")

# 输入和输出文件路径
INPUT_FILE = "paraphrased_labeled_questions.json"  # 输入的 JSON 文件
OUTPUT_FILE = "answers.json"  # 输出的 JSON 文件

def call_deepseek_api(question):
    """
    调用 DeepSeek API 并获取答案。
    :param question: 需要发送到 API 的完整问题
    :return: API 返回的答案
    """
    try:
        # 调用 deepseek-chat 模型
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
            stream=False  # 设置为 True 可启用流式输出
        )
        # 返回模型的回答内容
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return "API 调用失败"

def process_questions(input_file, output_file):
    """
    处理 JSON 文件中的问题，调用 DeepSeek API 获取答案，并保存结果到新的文件。
    :param input_file: 输入的 JSON 文件路径
    :param output_file: 输出的 JSON 文件路径
    """
    try:
        # 读取 JSON 文件
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        results = []
        for item in tqdm(data, desc="处理问题进度"):
            # 获取问题内容和选项
            question = item.get("question", "").strip()
            options = {
                "A": item.get("A", "").strip(),
                "B": item.get("B", "").strip(),
                "C": item.get("C", "").strip(),
                "D": item.get("D", "").strip(),
            }
            
            # 拼接完整问题，包括选项
            full_question = f"{question}\nA. {options['A']}\nB. {options['B']}\nC. {options['C']}\nD. {options['D']}\n"
            full_question += "上面的题目有什么问题吗？有的话请指出，没有的话给我正确答案。"
            
            # 调用 DeepSeek API 获取答案
            answer = call_deepseek_api(full_question)
            
            # 保存问题和答案
            results.append({
                "question": question,
                "full_question": full_question,
                "answer": answer
            })

        # 将结果保存到输出文件
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        print(f"处理完成，结果已保存到文件: {output_file}")

    except Exception as e:
        print(f"处理问题时出错: {e}")

# 主函数
if __name__ == "__main__":
    process_questions(INPUT_FILE, OUTPUT_FILE)