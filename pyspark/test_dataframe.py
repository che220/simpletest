import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator
from pyspark.ml.stat import Correlation
from pyspark.ml.linalg import Vectors
import test_env

pd.set_option('display.width', 1000)


spark = SparkSession.builder.master("spark://192.168.0.7:7077").appName('test_mac_dataframe').config("spark.cores.max","1").getOrCreate()

x= pd.read_csv('/Users/huiwang/dev/TY15_LACERTE_profile.csv')
print(x.head(10))
#x = x.drop('CAN', 1) # 0 for rows and 1 for columns

df = spark.createDataFrame(x)
df = df.drop('CAN')
print(df.take(4))
print(df.columns)
print(df.dtypes)
#print(df.toJSON().collect())

df1 = test_env.selectNumericColumns(df)
print(df1.take(10))
print(df1.dtypes)
test_env.correlationMatrix(df1)

nb = NaiveBayes(smoothing=1.0, modelType="bernoulli") #bernoulli or multunomial
evaluator = BinaryClassificationEvaluator()
#cv = CrossValidator(estimator=nb, evaluator=evaluator, numFolds=10)
#cvModel = cv.fit(df)
