library(RJDBC)
if (nchar(Sys.getenv("SPARK_HOME")) < 1) {
  #Sys.setenv(SPARK_HOME='/home/hui/spark-1.6.0-bin-hadoop2.6') #Ubuntu
  Sys.setenv(SPARK_HOME='C:/apps/spark-1.6.0-bin-hadoop2.6')
}
library(SparkR, lib.loc = c(file.path(Sys.getenv("SPARK_HOME"), "R", "lib")))
#.libPaths(c(file.path(Sys.getenv("SPARK_HOME"), "R", "lib"), .libPaths()))
#sc <- sparkR.init(master = "local[*]", sparkEnvir = list(spark.driver.memory="2g"))

#setwd("/home/hui/spark-1.6.0-bin-hadoop2.6") # Ubuntu
setwd("C:/apps/spark-1.6.0-bin-hadoop2.6")

initSpark = function()
{
  jars = list.files(path="C:/apps/java_lib", pattern='*.jar', full.names=TRUE)
  extraCP <<- paste0(jars, collapse=';')
  verticaDriver <<- JDBC(driverClass="com.vertica.jdbc.Driver", classPath=extraCP)
  sc <<- sparkR.init(master="spark://172.20.122.177:7077", sparkEnvir = list(spark.driver.memory="1g", spark.driver.extraClassPath=extraCP))
  sqlContext <<- sparkRSQL.init(sc)
}

stopSpark = function()
{
  # Stop the SparkContext now
  sparkR.stop()
}

verticaJDBC = function()
{
  url = "jdbc:vertica://pprddaavt-vip.ie.intuit.net:5433/Analytics"
  conn = dbConnect(verticaDriver, url, 'hwang7', 'Heaven9938')
  return (conn)
}

tryJDBC = function()
{
  vertica = verticaJDBC()
  sql = "select * from PTG_DWH.PTG_CAN_PRODUCT"
  print(sql)
  dd=dbGetQuery(vertica, sql)
  print(sprintf("%d rows", nrow(dd)))
  
  # to speed up
  write.csv(dd, row.names=FALSE, file="1.csv")
  x=read.df(sqlContext, '1.csv', source='com.databricks.spark.csv', header='true', inferSchema='true')
  # TODO: need to find dataBrick jar
  
  sparkDF = createDataFrame(sqlContext, dd) # VERY VERY SLOW!!!!!
  print("created spark DataFrame")
  head(sparkDF)
  registerTempTable(sparkDF, "PTG_CAN_PRODUCT")
  print("created spark temp table")
  
  #url = "jdbc:vertica://pprddaavt-vip.ie.intuit.net:5433/Analytics"
  #props = list(url=url, user='hwang7', password='')
  #read.df
  #loadDF(sqlContext, "PTG_WS.US_STATE", "jdbc")
  #reader = sqlContext.read()
  #reader = reader.format("jdbc")
  #reader = reader.option("url", url)
  #reader = reader.option("user", 'hwang7')
  #reader = reader.option("password", 'Heaven9938')
  #reader = option("dbtable", 'PTG_WS.US_STATE')
  #df = reade.load()
  #df.printSchema()
}

tests = function()
{
  faiths = createDataFrame(sqlContext, faithful)
  head(faiths)
  
  localDF <- data.frame(name=c("John", "Smith", "Sarah"), age=c(19, 23, 18))
  df <- createDataFrame(sqlContext, localDF)
  printSchema(df)
  
  
  # Create a DataFrame from a JSON file
  path <- file.path(Sys.getenv("SPARK_HOME"), "examples/src/main/resources/people.json")
  peopleDF <- jsonFile(sqlContext, path)
  printSchema(peopleDF)
  
  # Register this DataFrame as a table.
  registerTempTable(peopleDF, "people")
  
  # SQL statements can be run by using the sql methods provided by sqlContext
  teenagers <- sql(sqlContext, "SELECT name FROM people WHERE age >= 13 AND age <= 19")
  
  # Call collect to get a local data.frame
  teenagersLocalDF <- collect(teenagers)
  
  # Print the teenagers in our dataset 
  print(teenagersLocalDF)
}
