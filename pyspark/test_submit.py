# submit command:
#    spark-submit --master spark://nuc5vm:7077 --deploy-mode client test_submit.py
#
from pyspark import SparkContext, SparkConf

sc = SparkContext.getOrCreate()

rawData = [1,2,3,4,5,6,7,4,4,4,4,6,6,9,0,7,4]
a = sc.parallelize(rawData)
print(a.collect())

b = a.map(lambda x: (x,1))
c = a.reduce(lambda x,y: x+y)
print(c)

c1 = b.reduceByKey(lambda v1, v2: v1+v2)
print(c1.collect())
