#!/bin/bash

# 删除之前的output.json
rm output.json
rm log.txt

# 将所有输出重定向到 run.log
exec >run.log 2>&1

# 从命令行获取参数
DIR_NAME=$1  # 第一个参数是文件夹名
LATEX_OPTION=$2  # 第二个参数是 latex 的选项

# 检查参数是否提供
if [ -z "$DIR_NAME" ] || [ -z "$LATEX_OPTION" ]; then
  echo "Usage: ./run_all.sh <dir_name> <latex_option>"
  echo "Example: ./run_all.sh GAOKAO off"
  exit 1
fi

# 遍历 DIR_NAME 中的所有 .docx 文件并执行命令
find "$DIR_NAME" -type f -name '*.docx' | while read -r DOCX_FILE; do
  echo "Processing file: $DOCX_FILE"
  FILE_NAME="${DOCX_FILE%.docx}"

  # 执行 remove_smartTag.py
  python remove_smartTag.py --docx_name="$FILE_NAME"

  # 执行 docx_to_json.py，json_name 统一设置为 "output"
  # python docx_to_json.py --docx_name="$FILE_NAME" --json_name="output" --new="off" --latex="$LATEX_OPTION" >> log.txt
  # 执行 docx_to_json.py，json_name 统一设置为 "output"
  CMD="python docx_to_json.py --docx_name=\"$FILE_NAME\" --json_name=\"output\" --new=\"off\" --latex=\"$LATEX_OPTION\""
  eval $CMD >> log.txt 2>&1
  if [ $? -ne 0 ]; then
    echo "Error occurred while executing: $CMD"
    echo "Skipping file: $DOCX_FILE"
    continue
  fi

done