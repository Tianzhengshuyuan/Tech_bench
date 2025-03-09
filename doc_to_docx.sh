#!/bin/bash

# 检查是否安装了LibreOffice
if ! command -v soffice &> /dev/null; then
    echo "LibreOffice (soffice) 未安装，请先安装 LibreOffice。"
    exit 1
fi

# 检查是否提供源和目标文件夹
if [ $# -ne 2 ]; then
    echo "用法: $0 <源文件夹> <目标文件夹>"
    echo "示例: $0 /path/to/source /path/to/target"
    exit 1
fi

# 获取源和目标文件夹
DOC_FOLDER=$1
DOCX_FOLDER=$2

# 检查源文件夹是否存在
if [ ! -d "$DOC_FOLDER" ]; then
    echo "源文件夹不存在: $DOC_FOLDER"
    exit 1
fi

# 如果目标文件夹不存在，则创建
if [ ! -d "$DOCX_FOLDER" ]; then
    mkdir -p "$DOCX_FOLDER"
fi

# 遍历源文件夹中的所有 .doc 和 .docx 文件
find "$DOC_FOLDER" -type f \( -name "*.doc" -o -name "*.docx" \) | while read -r FILE; do
    # 获取文件的路径和名称
    FILE_DIR=$(dirname "$FILE")
    FILE_BASENAME=$(basename "$FILE")
    FILE_EXTENSION="${FILE##*.}"
    FILE_NAME="${FILE_BASENAME%.*}"

    # 目标文件路径
    TARGET_FILE="$DOCX_FOLDER/$FILE_NAME.docx"

    if [ "$FILE_EXTENSION" == "doc" ]; then
        # 如果是 .doc 文件，转换为 .docx
        echo "正在转换: $FILE -> $TARGET_FILE"
        soffice --headless --convert-to docx --outdir "$DOCX_FOLDER" "$FILE"

        # 检查转换是否成功
        if [ $? -eq 0 ]; then
            echo "转换成功: $TARGET_FILE"
        else
            echo "转换失败: $FILE"
        fi
    elif [ "$FILE_EXTENSION" == "docx" ]; then
        # 如果是 .docx 文件，直接复制到目标文件夹
        echo "正在复制: $FILE -> $TARGET_FILE"
        cp "$FILE" "$TARGET_FILE"

        # 检查复制是否成功
        if [ $? -eq 0 ]; then
            echo "复制成功: $TARGET_FILE"
        else
            echo "复制失败: $FILE"
        fi
    fi
done

echo "批量处理完成！"