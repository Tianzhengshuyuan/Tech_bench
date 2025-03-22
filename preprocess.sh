#!/bin/bash

# 从命令行获取参数
DIR_NAME=$1  # 第一个参数是文件夹名
OUTPUT_DIR_NAME=$2  # 第二个参数是文件夹名

# 删除所有名字中包含“A3”的文件夹
find "$DIR_NAME" -type d -name '*A3*' -exec rm -rf {} +

# 删除所有名字中包含“原卷”的文件
find "$DIR_NAME" -type f -name '*原卷*' -exec rm -f {} +

# 删除名字中不包含“答案”且不包含“解析”的所有文件
find "$DIR_NAME" -type f ! -name '*答案*' ! -name '*解析*' -exec rm -f {} +

# ./doc_to_docx.sh "$DIR_NAME" "$OUTPUT_DIR_NAME"

# 将所有剩下的文件复制到目标文件夹（平铺，无目录结构）
find "$DIR_NAME" -type f -exec cp {} "$OUTPUT_DIR_NAME" \;

echo "文件处理完成，所有文件已复制到 $OUTPUT_DIR_NAME 中。"


