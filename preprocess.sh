#!/bin/bash

# 从命令行获取参数
DIR_NAME=$1  # 第一个参数是文件夹名
OUTPUT_DIR_NAME=$2  # 第二个参数是文件夹名

# 删除所有名字中包含“A3”的文件夹
find "$DIR_NAME" -type d -name '*A3*' -exec rm -rf {} +

# 删除所有名字中包含“原卷”的文件
find "$DIR_NAME" -type f -name '*原卷*' -exec rm -f {} +

./doc_to_docx.sh "$DIR_NAME" "$OUTPUT_DIR_NAME"

