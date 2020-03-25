from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":

    sc = SparkContext(appName="PythonStreamingKafkaWordCount")
    ssc = StreamingContext(sc, 5)
    sc.setLogLevel("ERROR")
    kafkaParams = {"metadata.broker.list": "hdp2.buptnsrc.com:6667,hdp4.buptnsrc.com:6667,hdp5.buptnsrc.com:6667"}
    topic = ["test_first"]
    lines = KafkaUtils.createDirectStream(ssc, topic, kafkaParams)
    res = lines.map(lambda x: (str(x), 1)).reduceByKey(lambda a, b: a + b)
    res.pprint()
    # lines = kvs.map(lambda x: x[1])
    # counts = lines.flatMap(lambda line: line.split(" ")) \
    #     .map(lambda word: (word, 1)) \
    #     .reduceByKey(lambda a, b: a + b)
    # counts.pprint()

    ssc.start()
    ssc.awaitTermination()