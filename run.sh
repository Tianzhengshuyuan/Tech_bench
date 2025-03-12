#!/bin/bash

# 删除所有名字中包含“A3”的文件夹
find . -type d -name '*A3*' -exec rm -rf {} +

# 删除所有名字中包含“原卷”的文件
find . -type f -name '*原卷*' -exec rm -f {} +

# 从命令行获取参数
DOCX_NAME=$1  # 第一个参数是 docx 文件名
LATEX_OPTION=$2  # 第二个参数是 latex 的选项

# 检查参数是否提供
if [ -z "$DOCX_NAME" ] || [ -z "$LATEX_OPTION" ]; then
  echo "Usage: ./run.sh <docx_name> <latex_option>"
  echo "Example: ./run.sh '2004年云南高考理科综合真题及答案' off"
  exit 1
fi

# 执行命令
python remove_smartTag.py --docx_name="$DOCX_NAME"
python docx_to_json.py --docx_name="$DOCX_NAME" --latex="$LATEX_OPTION"