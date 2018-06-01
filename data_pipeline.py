from __future__ import absolute_import, division, print_function
import tensorflow as tf
import itertools

def generator1():
    for i in itertools.count(10, 3):
        yield (i, [i*i]*5) # [i]*10: list of 10 i

def generator2():
    for i in itertools.cycle(range(10)):
        yield (i, i + 5, i + 10)

# tf.TensorShape([]): shape of a primitive
# tf.TensorShape([None]): shape of a 1-D list
# tf.TensorShape(None): unknown dimensions and unknown sizes in all dimensions

a = zip([1,2,3], [4,5])
for i in a:
    print(i)

sess = tf.Session()
ds = tf.data.Dataset.from_generator(generator1, (tf.int64, tf.int64), (tf.TensorShape([]), tf.TensorShape([None])))
value = ds.make_one_shot_iterator().get_next()
cnt = 0
while cnt < 4:
    print(sess.run(value))
    cnt += 1
print('Done generating numbers')

ds = tf.data.Dataset.list_files('E:/Software/*.exe')
val = ds.make_one_shot_iterator().get_next()
while True:
    try:
        print(sess.run(val))
    except tf.errors.OutOfRangeError:
        break
print('Done listing files')

ds = tf.data.Dataset.list_files('E:/git-review/invest/data/*.csv')
file_handle = sess.run(ds.make_one_shot_iterator().string_handle())
val = tf.data.Iterator.from_string_handle(file_handle, ds.output_types).get_next()
files = {}
while True:
    try:
        file = sess.run(val).decode('utf-8')
        if file.find('GDXJ.d.csv') >= 0:
            files['GDXJ'] = file
        elif file.find('SPY.d.csv') >= 0:
            files['SPY'] = file
    except tf.errors.OutOfRangeError:
        break
print('Found file:', files)

filename_queue = tf.train.string_input_producer(list(files.values()))
reader = tf.TextLineReader()
key, value = reader.read(filename_queue)

coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(coord=coord, sess=sess)
firstKey = None
cnt = 0
while True:
    kv = sess.run([key, value])
    k = kv[0].decode('utf-8')
    if firstKey is None:
        firstKey = k
        print('First key:', firstKey)
    elif k == firstKey:
        break
    #if cnt < 10:
    print(kv)
    cnt += 1
coord.request_stop()
coord.join(threads)
print('read {} lines'.format(cnt))
print('All Done')
