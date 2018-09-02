import tensorflow as tf, numpy as np

a = '123-abc-WEH'
alist = ['12', '34', '56', 'xr', 'th', 'as', 'op', 'asd']
mat = np.array(alist).reshape(-1, 2)
print('np mat:\n', mat, '\n')
tf_mat = tf.convert_to_tensor(mat, dtype=tf.string)
print('tensor shape:', tf_mat.shape, '\n')
y = tf.strings.join(alist, separator=",")

n_elements = tf_mat.shape[0]
n = tf.slice(tf_mat, [0, 0], [n_elements, 1])# start at location (1,0) get 2 rows and 1 columns - if 2d tensor
y1 = tf.strings.join(tf.split(n, n.shape[0]), separator=",")

alist = ['12', '34', '56', '124', '234', '3463', '343', '34']
mat = np.array(alist).reshape(-1, 2)
print('number mat:\n', mat, '\n')
tf_num_mat = tf.convert_to_tensor(mat, dtype=tf.string)

with tf.Session() as sess:
    print('libs:\n', tf.sysconfig.get_lib(), '\n')
    print('incs:\n', tf.sysconfig.get_include(), '\n')
    print('compile flags:\n', tf.sysconfig.get_compile_flags(), '\n')
    print('link flags:\n', tf.sysconfig.get_link_flags(), '\n')
    print('GPU:\n', tf.test.is_gpu_available(cuda_only=False), '\n')
    print('CUDA GPU:\n', tf.test.is_gpu_available(cuda_only=True), '\n')

    print('sliced:\n', sess.run(n), '\n')
    print('row split:\n', sess.run(tf.split(tf_mat, tf_mat.shape[0], axis=0)), '\n')
    print('column split:\n', sess.run(tf.split(tf_mat, tf_mat.shape[1], axis=1)), '\n')

    print('---------y-------', '\n')
    print(sess.run(y), '\n')
    print('---------y1-------', '\n')
    print(sess.run(y1), '\n')

    print('---------regex_replace-------', '\n')
    print('regex replace:\n', sess.run(tf.regex_replace(tf_mat, 'a', 'A')), '\n')
    print('---------string split-------', '\n')
    x = sess.run(tf.strings.split(tf.convert_to_tensor([a, a, a]), sep='-'))
    print('string split:\n', x, '\n')
    print('string split:\n', x[0][1], '\n')

    print('---------string to number-------', '\n')
    print(sess.run(tf.string_to_number(tf_num_mat, out_type=tf.int64)), '\n')
