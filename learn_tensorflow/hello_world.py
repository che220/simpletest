import tensorflow as tf
import pandas as pd, numpy as np

def selu(z,
         scale=1.0507009873554804934193349852946,
         alpha=1.6732632423543772848170429916717):
    return scale * tf.where(z >= 0.0, z, alpha * tf.nn.elu(z))

x = tf.Variable(3.0, name='x')
y = tf.Variable(4.0, name='y')
f = x*x + y*y + 2
init = tf.global_variables_initializer()

# in notebook, use sess = tf.InteractiveSession(). Then close it at the end
for tensor in tf.get_default_graph().get_all_collection_keys():
    print(tensor.name)

with tf.Session() as sess:
    init.run()
    z = 1.0
    a = sess.run(selu(z))
    print(a)
