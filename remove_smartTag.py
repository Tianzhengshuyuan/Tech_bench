import argparse
from lxml import etree
from docx import Document

# 定义 Word 的命名空间
NAMESPACE = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
}

def process_docx(file_path, output_path):
    # 加载 Word 文档
    doc = Document(file_path)
    
    # 遍历所有段落
    for paragraph in doc.paragraphs:
        # 获取段落的底层 XML 元素
        paragraph_xml = paragraph._element

        # 找到所有的 <w:smartTag> 元素
        smart_tags = paragraph_xml.findall('.//w:smartTag', namespaces=NAMESPACE)
        for smart_tag in smart_tags:
            # 查找 <w:t>（文本内容）和任何格式信息
            runs = smart_tag.findall('.//w:r', namespaces=NAMESPACE)
            
            # 将 <w:smartTag> 替换为其内部的 <w:r> 元素
            parent = smart_tag.getparent()
            for run in runs:
                parent.insert(parent.index(smart_tag), run)  # 插入 <w:r> 到 <w:smartTag> 的位置
            parent.remove(smart_tag)  # 移除原始的 <w:smartTag>
    
    # 保存处理后的文档
    doc.save(output_path)

# 命令行入口
if __name__ == "__main__":
    # 定义命令行参数
    parser = argparse.ArgumentParser(description="去除word文档中的smartTag，从而方便后续处理")
    parser.add_argument("--docx_name", type=str, help="Word文档名")
    args = parser.parse_args()
    
    docx_path = f"/root/tech_bench/docx/{args.docx_name}.docx"  
    
    # 处理文档
    process_docx(docx_path, docx_path)
    print(f"完成smartTag移除，文件已保存为 {docx_path}")