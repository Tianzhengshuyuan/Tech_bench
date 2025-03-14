#!/bin/bash

# 定义目标文件夹
TARGET_DIR="./物理_docx2"

# 遍历目标文件夹中的所有文件
find "$TARGET_DIR" -type f | while IFS= read -r FILE; do
  # 使用 ls -b 输出文件名的转义形式
  ESCAPED_NAME=$(ls -b "$FILE")
  
  # 检查文件名是否包含反斜杠和空格
  if [[ "$ESCAPED_NAME" =~ \\[[:space:]] ]]; then
    # 获取文件所在目录
    FILE_DIR=$(dirname "$FILE")
    
    # 获取原始文件名
    FILE_NAME=$(basename "$ESCAPED_NAME")
    
    # 修复文件名：移除反斜杠和多余空格
    FIXED_FILE_NAME=$(echo "$FILE_NAME" | sed 's/[[:space:]]*//g' | sed 's/\\//g')
    
    # 拼接新的完整文件路径
    NEW_FILE="$FILE_DIR/$FIXED_FILE_NAME"

    # 输出重命名操作日志
    echo "Renaming:"
    echo "  OLD: $FILE"
    echo "  NEW: $NEW_FILE"

    # 执行重命名
    mv "$FILE" "$NEW_FILE"
  fi
done

echo "File renaming completed."