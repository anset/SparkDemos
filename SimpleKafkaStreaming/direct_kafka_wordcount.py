from __future__ import print_function
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def PrintResult (time, rdd):
    cnt = rdd.count()
    result = rdd.takeOrdered(100, key = lambda x: -x[1])
    print ( "\n\n======================================")
    print ( "= Batch Result @ " + str(time) + " =")
    print ( "======================================")
    print ( "\nNumber of distinct words found = " + str(cnt) )
    print ( "\nTop 100 words counted list:\n")
    print ( result )
    print ( "\n======================================\n\n")


# Create the Spark Context
sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")

# Reduce the amount of logging once the stream is started makes the actual output easier to see.
logger = sc._jvm.org.apache.log4j
logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)

# Create the Spark Streaming Context with a 20 second interval
ssc = StreamingContext(sc, 20)

# Set up the Kafka Direct Stream using the command line arguments
brokers, topic = sys.argv[1:]
kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})

# Get the events form the Kafka Stream
lines = kvs.map(lambda x: x[1])

# Do the work count 
counts = lines.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a+b)

# Print the results
counts.foreachRDD( PrintResult )

# Actually start the stream processing
ssc.start()

ssc.awaitTermination()
