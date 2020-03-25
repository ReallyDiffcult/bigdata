import os.path
import sys
from pyspark.sql import SparkSession
from pyspark.sql import Row
import json
import os
from io import BytesIO

import avro.schema
from avro.io import DatumReader, DatumWriter, BinaryDecoder, BinaryEncoder
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils




def decoder(binary_data):
    bio = BytesIO(binary_data)
    binary_decoder = BinaryDecoder(bio)
    # return "yangkun"
    schema = avro.schema.parse(open("user.avsc", "rb").read())
    return DatumReader(schema).read(binary_decoder)


def updateFunc(new_values, last_sum):
    return sum(new_values) + (last_sum or 0)


def stopStreaming(rdd):
    res1 = rdd.filter(lambda x: x[1] >= 100000)
    if res1.isEmpty() != True:
        print("---------------------      i want to stop ------------------------------------")
        sys.exit(0)



# Create a spark context
sc = SparkContext(appName="SparkStreamingTest")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 5)
ssc.checkpoint(r"C:\Users\yangkun\Desktop\checkpoint")
kafkaParams = {"metadata.broker.list": "hdp2.buptnsrc.com:6667,hdp4.buptnsrc.com:6667,hdp5.buptnsrc.com:6667"}
topic = ["test_first"]

# lines = KafkaUtils.createDirectStream(ssc, topic, kafkaParams,valueDecoder=decoder)
lines = KafkaUtils.createDirectStream(ssc, topic, kafkaParams)
# lines.pprint()

#
# #### 1.updateStateByKey
# initialStateRDD = sc.parallelize([(u'hello', 1), (u'world', 1)])
# res = lines.map(lambda x: (str(x), 1)).updateStateByKey(updateFunc, initialRDD=initialStateRDD)
# res.pprint()
#### 2.reduceByKey
res = lines.map(lambda x:(str(x),1)).reduceByKey(lambda a,b: a+b)
res.pprint()
#### 3. stop sparkstreaming

# res.foreachRDD(stopStreaming)

ssc.start()
ssc.awaitTermination()