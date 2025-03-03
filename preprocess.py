import re
import json
import pytesseract
from docx import Document
from PIL import Image
from io import BytesIO


def extract_text_or_image_from_run(run):
    """
    提取段落中每个 run 的文本或图片内容。如果是图片，使用 OCR 识别。
    """
    if run.text.strip():
        # 如果是文本，直接返回
        return run.text.strip()
    elif run.element.xpath(".//w:drawing"):
        # 如果是图片，提取图片并进行 OCR 识别
        for blip in run.element.xpath(".//a:blip"):
            rId = blip.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed']
            image = run.part.related_parts[rId]
            image_data = BytesIO(image.blob)
            img = Image.open(image_data)

            # 使用 pytesseract OCR 识别图片内容
            recognized_text = pytesseract.image_to_string(img, config='--psm 6')
            return f"$$ {recognized_text.strip()} $$"  # 返回 LaTeX 格式公式
    return ""


def parse_paragraph(paragraph):
    """
    解析段落内容，提取题目和选项（包括同一行的多个选项）。
    """
    # 将段落内容按文本和图片分离
    runs_content = [extract_text_or_image_from_run(run) for run in paragraph.runs]
    full_text = " ".join(runs_content).strip()

    # 定义正则表达式，匹配题目和选项
    question_and_options_pattern = re.compile(
        r"^(?P<question>\d+[．.。].*?)"  # 匹配题目编号和题目内容
        r"(?:A[．.。]\s*(?P<A>.*?))?"    # 匹配 A 选项
        r"(?:B[．.。]\s*(?P<B>.*?))?"    # 匹配 B 选项
        r"(?:C[．.。]\s*(?P<C>.*?))?"    # 匹配 C 选项
        r"(?:D[．.。]\s*(?P<D>.*?))?"    # 匹配 D 选项
    )

    match = question_and_options_pattern.match(full_text)
    if match:
        return match.groupdict()
    return None


def extract_questions_from_docx(docx_path, output_json_path):
    """
    从 Word 文档中提取选择题内容，并保存为 JSON 文件。
    """
    # 打开 Word 文档
    doc = Document(docx_path)

    # 初始化结果列表
    questions = []
    current_question = None
    number=1
    # 遍历文档中的每个段落
    for paragraph in doc.paragraphs:
        print(">>>>>>>")
        print(paragraph.text)
        parsed_content = parse_paragraph(paragraph)

    #     if parsed_content:
    #         # 如果解析到题目编号，开始一个新的问题
    #         if parsed_content["question"]:
    #             if current_question:
    #                 questions.append(current_question)  # 保存上一题
    #             current_question = {
    #                 "question": parsed_content["question"],
    #                 "A": parsed_content.get("A", "").strip(),
    #                 "B": parsed_content.get("B", "").strip(),
    #                 "C": parsed_content.get("C", "").strip(),
    #                 "D": parsed_content.get("D", "").strip()
    #             }
    #         else:
    #             # 如果当前段落补充了选项内容，则追加到当前选项
    #             for key in ["A", "B", "C", "D"]:
    #                 if parsed_content.get(key):
    #                     current_question[key] += " " + parsed_content[key].strip()

    # # 保存最后一个问题
    # if current_question:
    #     questions.append(current_question)

    # # 保存为 JSON 文件
    # with open(output_json_path, "w", encoding="utf-8") as f:
    #     json.dump(questions, f, ensure_ascii=False, indent=4)

    print(f"提取完成！选择题已保存到 {output_json_path}")


# 使用示例
docx_path = "/root/tech_bench/2001年陕西高考理综真题及答案.docx"  # 替换为你的 Word 文档路径
output_json_path = "questions.json"       # 输出 JSON 文件路径
extract_questions_from_docx(docx_path, output_json_path)