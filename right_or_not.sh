#!/bin/bash

# 默认题目数量为 100
NUM_QUESTIONS=100
USE_RANDOM=false

# 解析命令行参数
for arg in "$@"; do
    if [[ $arg == "random" ]]; then
        USE_RANDOM=true
    elif [[ $arg =~ ^[0-9]+$ ]]; then
        NUM_QUESTIONS=$arg
    fi
done

# 根据是否指定 random 构造命令
if [[ $USE_RANDOM == true ]]; then
    GET_QUESTIONS_CMD="python get_questions.py --num_questions=$NUM_QUESTIONS --random"
else
    GET_QUESTIONS_CMD="python get_questions.py --num_questions=$NUM_QUESTIONS"
fi

# 打印执行的命令（可选，用于调试）
echo "执行命令: $GET_QUESTIONS_CMD"

# 执行生成问题的命令
eval $GET_QUESTIONS_CMD

# 执行后续命令
python bert_paraphrase.py --input_file=selected_questions.json --wo_phy > wo_phy.log
python get_deepseek_answer.py