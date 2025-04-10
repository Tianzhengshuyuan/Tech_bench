#! -*- coding: utf-8 -*-
# 词级别的中文BERT预训练
# MLM任务

import glob
import jieba
import shutil
import os, json
import numpy as np
import tensorflow as tf
from bert4keras.backend import keras, K
from bert4keras.layers import Loss
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer, load_vocab
from bert4keras.optimizers import Adam
from bert4keras.optimizers import extend_with_weight_decay
from bert4keras.optimizers import extend_with_gradient_accumulation
from bert4keras.snippets import sequence_padding, open
from bert4keras.snippets import DataGenerator
from bert4keras.snippets import text_segmentate
from tensorflow.python.client import device_lib

print(device_lib.list_local_devices())
jieba.initialize()
# os.environ["TF_KERAS"] = "1"  # 强制 bert4keras 使用 tf.keras

# 基本参数
maxlen = 512
batch_size = 16
epochs = 1
num_words = 20000

# bert配置
config_path = './chinese_wobert_L-12_H-768_A-12/bert_config.json'
checkpoint_path = './chinese_wobert_L-12_H-768_A-12/bert_model.ckpt'
dict_path = './chinese_wobert_L-12_H-768_A-12/vocab.txt'

def corpus():
    """
    语料生成器
    """
    while True:
        with open('./phy_only.json', 'r', encoding='utf-8') as f:
            data = json.load(f)  # 解析整个 JSON 数组
            for l in data:
                for text in text_process(l['question']):
                    yield text

def text_process(text):
    """
    分割文本
    """
    texts = text_segmentate(text, 32, u'\n。')
    result, length = '', 0
    for text in texts:
        if result and len(result) + len(text) > maxlen * 1.3:
            yield result
            result, length = '', 0
        result += text
    if result:
        yield result

# 词汇表是chinese_roberta_wwm_ext精简版 加上 jieba词汇表中出现频率最高的2万个中文词汇
# 加载并精简词表
token_dict = load_vocab(
    dict_path=dict_path,
    simplified=False
)
keep_tokens = list(token_dict.values())

pure_tokenizer = Tokenizer(token_dict.copy(), do_lower_case=True)

# 从 new_word.txt 加载物理专业词汇
with open('new_word.txt', 'r', encoding='utf-8') as f:
    new_words = set(f.read().strip().splitlines())

# 将物理专业词汇添加到词汇表
new_words_added = []
for w in new_words:
    if w not in token_dict:
        token_dict[w] = len(token_dict)
        new_words_added.append(w)

# 创建 compound_tokens，用于初始化新词的 embedding
compound_tokens = [pure_tokenizer.encode(w)[0][1:-1] for w in new_words_added]

# 将原始词汇表和新增词汇写入 new_vocab.txt
with open('new_vocab.txt', 'w', encoding='utf-8') as f:
    for token in token_dict.keys():
        f.write(token + '\n')

tokenizer = Tokenizer(
    token_dict,
    do_lower_case=True,
    pre_tokenize=lambda s: jieba.cut(s, HMM=False)
)

def random_masking(token_ids):
    """
    对输入进行随机mask
    """
    rands = np.random.random(len(token_ids))
    source, target = [], []
    for r, t in zip(rands, token_ids):
        if r < 0.15 * 0.8:
            source.append(tokenizer._token_mask_id)
            target.append(t)
        elif r < 0.15 * 0.9:
            source.append(t)
            target.append(t)
        elif r < 0.15:
            source.append(np.random.choice(tokenizer._vocab_size - 1) + 1)
            target.append(t)
        else:
            source.append(t)
            target.append(0)
    return source, target


class data_generator(DataGenerator):
    """
    数据生成器
    """
    def __iter__(self, random=False):
        batch_token_ids, batch_segment_ids, batch_output_ids = [], [], []
        for is_end, text in self.sample(random):
            token_ids, segment_ids = tokenizer.encode(text, maxlen=maxlen)
            # source是mask后的输入，target是被mask的位置的原始输入
            source, target = random_masking(token_ids)
            batch_token_ids.append(source)
            batch_segment_ids.append(segment_ids)
            batch_output_ids.append(target)
            if len(batch_token_ids) == self.batch_size or is_end:
                batch_token_ids = sequence_padding(batch_token_ids)
                batch_segment_ids = sequence_padding(batch_segment_ids)
                batch_output_ids = sequence_padding(batch_output_ids)
                yield [
                    batch_token_ids, batch_segment_ids, batch_output_ids
                ], None
                batch_token_ids, batch_segment_ids, batch_output_ids = [], [], []


class CrossEntropy(Loss):
    """
    交叉熵作为loss，并mask掉输入部分
    """
    def compute_loss(self, inputs, mask=None):
        y_true, y_pred = inputs
        y_mask = K.cast(K.not_equal(y_true, 0), K.floatx())
        accuracy = keras.metrics.sparse_categorical_accuracy(y_true, y_pred)
        accuracy = K.sum(accuracy * y_mask) / K.sum(y_mask)
        self.add_metric(accuracy, name='accuracy')
        loss = K.sparse_categorical_crossentropy(
            y_true, y_pred, from_logits=True
        )
        loss = K.sum(loss * y_mask) / K.sum(y_mask)
        return loss


model = build_transformer_model(
    config_path,
    checkpoint_path,
    model='bert',
    with_mlm='linear',
    keep_tokens=keep_tokens,  # 只保留keep_tokens中的字，精简原字表
    compound_tokens=compound_tokens,  # 增加词，用字平均来初始化
    return_keras_model=False 
)
# model.name = "bert"
print(type(model))
# for var in model.trainable_variables:
#     print(var.name)
# model.summary()
# 训练用模型
y_in = keras.layers.Input(shape=(None,))
outputs = CrossEntropy(1)([y_in, model.output]) # y_in是真实标签，model.output是模型预测的结果

train_model = keras.models.Model(model.inputs + [y_in], outputs)

AdamW = extend_with_weight_decay(Adam, name='AdamW')
AdamWG = extend_with_gradient_accumulation(AdamW, name='AdamWG')
optimizer = AdamWG(
    learning_rate=5e-6,
    weight_decay_rate=0.01,
    exclude_from_weight_decay=['Norm', 'bias'],
    grad_accum_steps=16,
)
train_model.compile(optimizer=optimizer) # 配置模型的训练过程，指定优化器、损失函数和评估指标
train_model.summary() # 打印模型结构

class Evaluator(keras.callbacks.Callback):
    """
    训练回调：在每个 epoch 结束时保存模型，并删除旧的 checkpoint 文件
    """
    def __init__(self, model, checkpoint_dir='./tf_checkpoints'):
        super().__init__()
        self.model = model  # 需要保存的基础模型
        self.checkpoint_dir = checkpoint_dir  # 保存路径
        self.last_checkpoint = None  # 记录上一个 checkpoint 的路径

    def delete_old_checkpoints(self):
        """
        删除旧的 checkpoint 文件
        """
        if self.last_checkpoint:
            # 获取所有与上一个 checkpoint 相关的文件
            for file in glob.glob(f"{self.last_checkpoint}*"):
                if os.path.exists(file):
                    os.remove(file)
            print(f"已删除旧的 checkpoint 文件：{self.last_checkpoint}")

    def on_epoch_end(self, epoch, logs=None):
        """
        每个 epoch 结束时保存模型
        """
        # 创建保存目录
        if not os.path.exists(self.checkpoint_dir):
            os.makedirs(self.checkpoint_dir)

        # 保存 checkpoint 的路径
        save_path = os.path.join(self.checkpoint_dir, f'bert_model_epoch_{epoch}.ckpt')

        # 删除旧的 checkpoint 文件
        self.delete_old_checkpoints()

        # 保存模型权重（仅保存基础模型）
        saver = tf.compat.v1.train.Saver(var_list=self.model.weights)
        sess = K.get_session()
        saver.save(sess, save_path)
        print(f"模型已保存至 {save_path}")

        # 更新 last_checkpoint 路径
        self.last_checkpoint = save_path
        
if __name__ == '__main__':
    # 启动训练
    evaluator = Evaluator(model=model, checkpoint_dir='./tf_checkpoints')
    train_generator = data_generator(corpus(), batch_size, 10**5)

    # fit_generator 是 Keras 中用于训练模型的方法，适合处理通过生成器动态生成的数据
    train_model.fit_generator(
        train_generator.forfit(),
        steps_per_epoch=120,
        epochs=epochs,
        callbacks=[evaluator]
    )

