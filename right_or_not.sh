#!/bin/bash

# 设置默认值
NUM_QUESTIONS=100
USE_RANDOM=false
ALL_NEW=false
RATIO_NOUNS=1.0  # 默认 ratio 为 1.0，即替换所有名词

# 解析命令行参数
for arg in "$@"; do
    if [[ $arg =~ ^NUM_QUESTIONS= ]]; then
        NUM_QUESTIONS=${arg#*=}  # 提取 NUM_QUESTIONS 的值
    elif [[ $arg =~ ^USE_RANDOM= ]]; then
        USE_RANDOM=${arg#*=}  # 提取 USE_RANDOM 的值
    elif [[ $arg =~ ^ALL_NEW= ]]; then
        ALL_NEW=${arg#*=}  # 提取 ALL_NEW 的值
    elif [[ $arg =~ ^RATIO_NOUNS= ]]; then
        RATIO_NOUNS=${arg#*=}  # 提取 RATIO_NOUNS 的值
    fi
done

# 构造 get_questions.py 的命令
if [[ $USE_RANDOM == true ]]; then
    GET_QUESTIONS_CMD="python get_questions.py --num_questions=$NUM_QUESTIONS --random=True"
else
    GET_QUESTIONS_CMD="python get_questions.py --num_questions=$NUM_QUESTIONS"
fi

# 执行生成问题的命令
eval $GET_QUESTIONS_CMD

# 执行 bert_paraphrase.py，传递 RATIO_NOUNS 参数
python bert_paraphrase.py --input_file=selected_questions.json --ratio=$RATIO_NOUNS --wo_phy > wo_phy.log

# 构造 get_deepseek_answer.py 的命令
if [[ $ALL_NEW == true ]]; then
    GET_DEEPSEEK_ANSWER_CMD="python get_deepseek_answer.py --all_new"
else
    GET_DEEPSEEK_ANSWER_CMD="python get_deepseek_answer.py"
fi

# 执行获取答案的命令
eval $GET_DEEPSEEK_ANSWER_CMD