from transformers import BertConfig, BertForMaskedLM, load_tf_weights_in_bert
import torch

# 1. 配置文件路径
config_path = "./new_bert_config.json"
vocab_path = "./new_vocab.txt"
tf_checkpoint_path = "./bert_model.weights"  # 微调后保存的 TensorFlow 权重
output_dir = "./converted_model"  # 转换后 PyTorch 模型的保存路径

# 2. 加载配置文件
config = BertConfig.from_json_file(config_path)

# 3. 初始化 Hugging Face 的 Bert 模型
model = BertForMaskedLM(config)

# 4. 加载 TensorFlow 权重到 Hugging Face 的 PyTorch 模型
model = load_tf_weights_in_bert(model, config, tf_checkpoint_path)

# 5. 保存转换后的 PyTorch 模型
model.save_pretrained(output_dir)

# 6. 保存词表
with open(vocab_path, "r", encoding="utf-8") as f:
    vocab = f.read()
with open(f"{output_dir}/vocab.txt", "w", encoding="utf-8") as f:
    f.write(vocab)

print(f"转换成功！模型已保存到 {output_dir}")