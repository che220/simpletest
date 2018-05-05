import tensorflow as tf
import pandas as pd, numpy as np

x = tf.Variable(3.0, name='x')
y = tf.Variable(4.0, name='y')
f = x*x + y*y + 2
init = tf.global_variables_initializer()

# in notebook, use sess = tf.InteractiveSession(). Then close it at the end

with tf.Session() as sess:
    init.run()
    a = f.eval()
    print(a)
