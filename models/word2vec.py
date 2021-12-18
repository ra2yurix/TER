# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# from random import choice
# import collections
# import math
# import random
# import numpy as np
# from six.moves import xrange
# import tensorflow as tf


if __name__ == "__main__":
    keywords = []
    all_keywords = set()
    for line in open("../data/movie_keywords_preprocessed.txt", "r", encoding="utf-8"):
        line = line.replace("\n", "").split(" ")
        # line  =line.strip('\n')
        # line = line.split(' ')
        keywords.append(line)
        all_keywords = all_keywords | set(line)
        print(all_keywords)

    batch_size = 128
    embedding_size = 128
    skip_window = 1
    num_skips = 2
    valid_size = 4
    valid_window = 100
    num_sampled = 64

    # data = []
    # all_word = []
    # for line in open('cilin.txt', 'r', encoding='utf8'):
    #     line =  line.replace('\n','').split(' ')[1:]
    #     # line  =line.strip('\n')
    #     # line = line.split(' ')
    #     data.append(line)
    #     for element in line:
    #         if element not in all_word:
    #             all_word.append(element)
    # dictionary = [i for i in range(len(all_word))]
    # reverse_dictionary_ = dict(zip(dictionary, all_word))
    # reverse_dictionary = dict(zip(all_word, dictionary))
    # print(reverse_dictionary)
    #
    # batch_size = 128
    # embedding_size = 128
    # skip_window = 1
    # num_skips = 2
    # valid_size = 4
    # valid_window = 100
    # num_sampled = 64
    # vocabulary_size  =len(all_word)
    # #验证集
    # valid_word = ['专家','住户','祖父','家乡']
    # valid_examples =[reverse_dictionary[li] for li in valid_word]
    # def generate_batch(data,batch_size):
    # data_input = np.ndarray(shape=(batch_size), dtype=np.int32)
    # data_label = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    # for i in range(batch_size):
    #     slice = random.sample( choice(data), 2)
    #     data_input[i ] = reverse_dictionary[slice[0]]
    #     data_label[i , 0] = reverse_dictionary[slice[1]]
    # return data_input, data_label
    #
    # graph = tf.Graph()
    # with graph.as_default():
    # # Input data.
    # train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
    # train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
    # valid_dataset = tf.constant(valid_examples, dtype=tf.int32)
    # # Ops and variables pinned to the CPU because of missing GPU implementation
    # with tf.device('/cpu:0'):
    #     # Look up embeddings for inputs.
    #     embeddings = tf.Variable(
    #         tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
    #     embed = tf.nn.embedding_lookup(embeddings, train_inputs)
    #     # Construct the variables for the NCE loss
    #     nce_weights = tf.Variable(
    #         tf.truncated_normal([vocabulary_size, embedding_size],
    #                             stddev=1.0 / math.sqrt(embedding_size)))
    #     nce_biases = tf.Variable(tf.zeros([vocabulary_size]),dtype=tf.float32)
    # # Compute the average NCE loss for the batch.
    # # tf.nce_loss automatically draws a new sample of the negative labels each
    # # time we evaluate the loss.
    # loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weights,
    #                                      biases=nce_biases,
    #                                      inputs=embed,
    #                                      labels=train_labels,
    #                                      num_sampled=num_sampled,
    #                                      num_classes=vocabulary_size))
    # # Construct the SGD optimizer using a learning rate of 1.0.
    # optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)
    # # Compute the cosine similarity between minibatch examples and all embeddings.
    # norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
    # normalized_embeddings = embeddings / norm
    # valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings, valid_dataset)
    # similarity = tf.matmul(valid_embeddings, normalized_embeddings, transpose_b=True)
    # # Add variable initializer.
    # init = tf.global_variables_initializer()
