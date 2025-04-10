from transformers.models.bert.convert_bert_original_tf_checkpoint_to_pytorch import convert_tf_checkpoint_to_pytorch

path = "/root/tech_bench/wo_phy"
tf_checkpoint_path = path + "/wo_phy_model"
bert_config_file = path + "/bert_config.json"
pytorch_dump_path = "wo_phy_pytorch/pytorch_model.bin"

convert_tf_checkpoint_to_pytorch(tf_checkpoint_path, bert_config_file,
                                 pytorch_dump_path)

# from transformers.models.bert.convert_bert_original_tf_checkpoint_to_pytorch import convert_tf_checkpoint_to_pytorch

# path = "/root/tech_bench/chinese_wobert_L-12_H-768_A-12"
# tf_checkpoint_path = path + "/bert_model.ckpt"
# bert_config_file = path + "/bert_config.json"
# pytorch_dump_path = "wo_phy/pytorch_model.bin"

# convert_tf_checkpoint_to_pytorch(tf_checkpoint_path, bert_config_file,
#                                  pytorch_dump_path)

