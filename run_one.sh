#!/bin/bash

# 从命令行获取参数
DOCX_NAME=$1  # 第一个参数是 docx 文件名
LATEX_OPTION=$2  # 第二个参数是 latex 的选项

# 检查参数是否提供
if [ -z "$DOCX_NAME" ] || [ -z "$LATEX_OPTION" ]; then
  echo "Usage: ./run_one.sh <docx_name> <latex_option>"
  echo "Example: ./run_one.sh 2004年云南高考理科综合真题及答案 off"
  exit 1
fi

# 执行命令
python remove_smartTag.py --docx_name="docx/$DOCX_NAME"
python docx_to_json.py --docx_name="docx/$DOCX_NAME" --json_name="json/$DOCX_NAME" --new="on" --latex="$LATEX_OPTION"