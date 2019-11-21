"""下面演示一个简单的seq2seq模型的代码
"""
import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt
import copy

# 假设词典的大小为256
vocab_size = 256
target_vocab_size = vocab_size

# learning rate
learnging_rate = 0.006

# 假设输入句子和输出句子一样长
in_size = 10
out_size = 10

buckets = [(in_size, out_size)]
batch_size = 1

# 输入数据和目标数据
input_data = np.arange(in_size)
target_data = copy.deepcopy(input_data)

np.random.shuffle(target_data)

target_weights = ([1.0]*in_size + [0.0]*0)

class Seq2Seq:
    def __init__(self, source_vocab_size, target_vocab_size, buckets, size):
        # 因为只有一个桶，所以索引为0
        self.encoder_size, self.decoder_size = buckets[0]
        self.source_vocab_size = source_vocab_size
        self.target_vocab_size = target_vocab_size
        
        cell = tf.contrib.rnn.BasicLSTMCell(size)
        cell = tf.contrib.rnn.MultiRNNCell([cell])
        
        def seq2seq_f(encoder_inputs, decoder_inputs, do_decode):
            return tf.contrib.legacy_seq2seq.embedding_attention_seq2seq(
                encoder_inputs,
                decoder_inputs,
                cell,
                num_encoder_symbols=source_vocab_size,
                num_decoder_symbols=target_vocab_size,
                embedding_size=size,
                feed_previous=do_decode
            )
            
        self.encoder_inputs = []
        self.decoder_inputs = []
        self.target_weights = []
        
        for i in range(self.encoder_size):
            self.encoder_inputs.append(tf.placeholder(tf.int32, shape=[None], name='encoder{0}'.format(i)))
            
        for i in range(self.decoder_size):
            self.decoder_inputs.append(tf.placeholder(tf.int32, shape=[None], name='decoder{}'.format(i)))
            self.target_weights.append(tf.placeholder(tf.float32, shape=[None], name='weights{0}'.format(i)))
        
        targets = [self.decoder_inputs[i] for i in range(len(self.decoder_inputs))]
        
        self.outputs,self.losses = tf.contrib.legacy_seq2seq.model_with_buckets(
            self.encoder_inputs,
            self.decoder_inputs,
            targets,
            self.target_weights,
            buckets,
            lambda x,y: seq2seq_f(x,y,False)
        )
        
        self.getPoints = tf.argmax(self.outputs[0], axis=2)
        self.trainOp = tf.train.AdamOptimizer(learnging_rate).minimize(self.losses[0])
        
    def step(self, session, encoder_inputs, decoder_inputs, target_weights):
        input_feed = {}
        for l in range(self.encoder_size):
            input_feed[self.encoder_inputs[l].name] = [encoder_inputs[l]]
            
        for l in range(self.decoder_size):
            input_feed[self.decoder_inputs[l].name] = [decoder_inputs[l]]
            input_feed[self.target_weights[l].name] = [target_weights[l]]
            
        output_feed = [self.losses[0], self.getPoints, self.trainOp]
        outputs = session.run(output_feed, input_feed)
        
        return outputs[0], outputs[1]
    
# 训练 LSTMRNN
if __name__ == '__main__':
    # 搭建 LSTMRNN 模型 
    model= Seq2Seq(vocab_size, target_vocab_size, buckets, size=5)
    sess = tf.Session()
    saver=tf.train.Saver(max_to_keep=3)
    sess.run(tf.global_variables_initializer())   
    # matplotlib可视化
    plt.ion()  # 设置连续 plot
    plt.show()  
    # 训练多次
    for i in range(100):
        losses, points= model.step(sess, input_data, target_data, target_weights)
        x = range(in_size)
        plt.clf()
        plt.plot(x, target_data, 'r', x, points, 'b--')#
        plt.draw()
        plt.pause(0.3)  # 每 0.3 s 刷新一次
        # 打印 cost 结果
        if i % 20 == 0:
            saver.save(sess, "model/lstem_text.ckpt",global_step=i)#
            print(losses)