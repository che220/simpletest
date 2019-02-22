import scipy.spatial as sc
import pandas as pd
import operator
import time, datetime as dt
import profile, cProfile

print(int('ABCD', base=16))

microsec_since_epoch = lambda: (dt.datetime.now() - dt.datetime(1970, 1, 1)).total_seconds()*1000000.0
millisec_since_epoch = lambda: (dt.datetime.now() - dt.datetime(1970, 1, 1)).total_seconds()*1000.0
print(microsec_since_epoch())
print(millisec_since_epoch())
#cProfile.run('microsec_since_epoch()')

a = {'a' : 1, 'b' : 1}
print(a)
a['a'] += 1
print(a)

t0 = microsec_since_epoch()
for i in range(10000):
    b = sorted(a.items(), key=lambda kv: kv[0], reverse=True)
t1 = microsec_since_epoch()
print(b, t1-t0)

t2 = microsec_since_epoch()
for i in range(1000):
    b = sorted(a.items(), key=lambda kv: kv[0], reverse=True)
t3 = microsec_since_epoch()
print(b, t3-t2, (t3-t2)*10)

t4 = microsec_since_epoch()
k = 0
for i in range(1000000):
    k += 1
t5 = microsec_since_epoch()
print(t5-t4, (t5-t4)/1000000)

x = list(a.items())
print(x)
df = pd.DataFrame(x, columns=['key', 'val'])
print(df)

def inc_weight(kv):
    return (kv[0], kv[1] + 0.001 * len(kv[0]))

# map with lambda is about 15% slower than list comprehension
# map with function is as fast as map with lambda
# list.sort() is about 17% faster than sorted(list)
def popular_value_map(weights):
    items = list(map(lambda kv: (kv[0], kv[1] + 0.001 * len(kv[0])), weights.items()))
    sort_weights = sorted(items, key=lambda kv: kv[1], reverse=True)
    return sort_weights[0][0]

def popular_value_map_func(weights):
    items = list(map(inc_weight, weights.items()))
    sort_weights = sorted(items, key=lambda kv: kv[1], reverse=True)
    return sort_weights[0][0]

def popular_value_list(weights):
    items = [(kv[0], kv[1] + 0.001 * len(kv[0])) for kv in weights.items()]
    sort_weights = sorted(items, key=lambda kv: kv[1], reverse=True)
    return sort_weights[0][0]

def popular_value_list_sort(weights):
    items = [(kv[0], kv[1] + 0.001 * len(kv[0])) for kv in weights.items()]
    items.sort(key=lambda kv: kv[1], reverse=True)
    return items[0][0]

def sort_on_value(weights):
    items = [(kv[0], kv[1] + 0.001 * len(kv[0])) for kv in weights.items()]
    items.sort(key=lambda kv: kv[1], reverse=True)
    return items

key_weights = {}
key_weights['value_1'] = 1
key_weights['value_2'] = 1
key_weights['value_3'] = 1

key_weights['value_1'] += 1
key_weights['value_2'] += 6
key_weights['value_3'] += 5
print(key_weights)

n = 500000
print('loops:', n)

t0 = microsec_since_epoch()
for i in range(n):
    x = popular_value_list(key_weights)
t1 = microsec_since_epoch()
print('list:', t1 - t0)
tt0 = t1 - t0

t0 = microsec_since_epoch()
for i in range(n):
    x = popular_value_map(key_weights)
t1 = microsec_since_epoch()
print('map-lambda:', t1 - t0)
tt1 = t1 - t0

t0 = microsec_since_epoch()
for i in range(n):
    x = popular_value_map_func(key_weights)
t1 = microsec_since_epoch()
print('map-func:', t1 - t0)
tt2 = t1 - t0

t0 = microsec_since_epoch()
for i in range(n):
    x = popular_value_list_sort(key_weights)
t1 = microsec_since_epoch()
print('list-sort:', t1 - t0)
tt3 = t1 - t0

print('=========================')
ts = {'list-sort' : tt3, 'list' : tt0, 'map-lambda' : tt1, 'map-func' : tt2}
ts = sort_on_value(ts)
max_t = ts[0][1]
for k in ts:
    print('{name}:\t{time}\t{pct:.2f}%'.format(name=k[0], time=k[1], pct=k[1]/max_t*100.0))

#
table1 = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5}
table2 = {'e' : 1, 'f' : 2, 'x' : 3, 'a' : 4, 'c' : 5}
ks1 = set(table1.keys())
ks2 = set(table2.keys())
ks = ks1.intersection(ks2)
print(ks)

rs = []
for k in ks:
    rs.append((k, table1[k], table2[k]))
rs.sort(key=lambda kvv: kvv[0], reverse=False)
print('Col1, Col2, Col3')
for r in rs:
    print(r)

