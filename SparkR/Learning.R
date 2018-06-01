if (nchar(Sys.getenv("SPARK_HOME")) < 1) {
  Sys.setenv(SPARK_HOME='/home/hui/spark-1.6.0-bin-hadoop2.6')
}
library(SparkR, lib.loc = c(file.path(Sys.getenv("SPARK_HOME"), "R", "lib")))
#.libPaths(c(file.path(Sys.getenv("SPARK_HOME"), "R", "lib"), .libPaths()))
#sc <- sparkR.init(master = "local[*]", sparkEnvir = list(spark.driver.memory="2g"))
setwd("/home/hui/spark-1.6.0-bin-hadoop2.6")

tests = function()
{
  sc = sparkR.init(master="spark://192.168.0.3:7077", sparkEnvir = list(spark.driver.memory="1g"))
  sqlContext = sparkRSQL.init(sc)

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
  
  # Stop the SparkContext now
  sparkR.stop()
}
