import sys, os, math
import datetime as dt
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.linalg import DenseVector
from pyspark.ml.feature import StringIndexer
import pyspark.sql.functions as spark_func
import model.spark_util as spark_util
import pyspark.sql.types as spark_types
import pyspark.ml.classification as spark_classification

for path in sys.path:
    print(path)

os.environ['PYSPARK_PYTHON'] = '/usr/lib/anaconda3/bin/python3'
#os.environ['PYSPARK_PYTHON'] = 'C:/apps/Anaconda3/python.exe'
sc = SparkContext("spark://prodlsv1301:7077", "FirstTest")
sqlContext = SQLContext(sc)

dataFile = '/home/hwang7/workspace/cliff-diving/risk_data/TY2015/TY2015_LACERTE_risk_data_new.csv'
df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(dataFile)
df = df.drop('CAN')
print('number of samples: {}'.format(df.count()))
df.printSchema()

cols = len(df.columns)
inputData = df.rdd.map(lambda x: (x[cols-1], DenseVector(x[0:(cols-2)])))
modelData = sqlContext.sparkSession.createDataFrame(inputData, ["label", "features"])
modelData = modelData.withColumn('label', modelData['label'].cast(spark_types.StringType()))
indexer = StringIndexer(inputCol="label", outputCol="label_indexed")
modelData = indexer.fit(modelData).transform(modelData)
folds = 10
modelData = modelData.withColumn('random', math.floor(spark_func.rand()*folds))

for depth in range(2, 10):
    print("======================================")
    print('Depth: {}'.format(depth))

    print(dt.datetime.now())
    allPreds = None
    for i in range(folds):
        print('running cv {}/{} ...'.format(i, folds))
        trains = modelData.where(modelData['random'] != i)
        tests = modelData.where(modelData['random'] == i)
        # print('training/tests: {}/{}'.format(trains.count(), tests.count()))

        rf = spark_classification.RandomForestClassifier(numTrees=250, maxDepth=depth, labelCol="label_indexed", seed=42)
        model = rf.fit(trains)
        preds = model.transform(tests)
        if allPreds is None:
            allPreds = preds
        else:
            allPreds = allPreds.union(preds)
            # print(allPreds.count())
    print(dt.datetime.now())
    evaluator = spark_util.SparkEvaluator()
    evaluator.evaluate(allPreds)
    evaluator.prettyPrint()
