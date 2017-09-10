from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("test_mac_pyspark").setMaster("spark://192.168.0.7:7077")
#sc = SparkContext(conf=conf)
sc = SparkContext.getOrCreate(conf=conf)

rawData = [1,2,3,4,5,6,7,4,4,4,4,6,6,9,0,7,41,5,4]
a = sc.parallelize(rawData)
print(a.collect())

b = a.map(lambda x: (x,1))
c = a.reduce(lambda x,y: x+y)
print(c)

c1 = b.reduceByKey(lambda v1, v2: v1+v2)
print(c1.collect())
