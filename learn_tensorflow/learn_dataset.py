import os, sys, re, pandas as pd, numpy as np
import tensorflow as tf

rs = tf.random_uniform([4,10])
print(rs)

ds1 = tf.data.Dataset.from_tensor_slices(rs)
print(ds1.output_types)
print(ds1.output_shapes)

iterator = ds1.make_initializable_iterator()
nextElem = iterator.get_next()

with tf.Session() as sess:
    sess.run(iterator.initializer)
    a = sess.run(rs)
    print(a)

    print('------------------------')
    cnt = 0
    while True:
        try:
            a = sess.run(nextElem) # this will re-init variable "rs"
            cnt += 1
            print(cnt, a)
        except tf.errors.OutOfRangeError:
            break

    print('------------------------')
    cnt = 0
    while True:
        try:
            a = sess.run(nextElem) # this will re-init variable "rs"
            cnt += 1
            print(cnt, a)
        except tf.errors.OutOfRangeError:
            break
sess.close()