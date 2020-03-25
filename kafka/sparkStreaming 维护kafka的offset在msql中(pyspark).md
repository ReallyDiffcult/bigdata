## sparkStreaming 维护kafka的offset在msql中(pyspark)

 

```python
# -*- coding: utf-8 -*-

import os.path
import sys
import pymysql
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


# 选择sparkStreaming数据库，连接MySQL
def query_partition():
    db = pymysql.connect(host="10.108.113.211", port=3306, user="root", password="000000",\
                         db="sparkStreaming", charset="utf8")
    cursor = db.cursor()
    sql='select * from test_offset'
    rows=cursor.execute(sql)
#     print(rows)
    info = cursor.fetchall()
#     print(info)  # 获得所有的记录

    cursor.close()
    db.close()
    return info
offsetRanges = []
def storeOffsetRanges(rdd):
    global offsetRanges
    offsetRanges = rdd.offsetRanges()
    return rdd

def printOffsetRanges(rdd):
    db = pymysql.connect(host="10.108.113.211", port=3306, user="root", password="000000",\
                         db="sparkStreaming", charset="utf8")
    cursor = db.cursor()    
    for o in offsetRanges:
        print "%s %s %s %s %s" % (o.topic, o.partition, o.fromOffset, o.untilOffset,o.untilOffset-o.fromOffset)
        sql_str = "update test_offset set fromoffset = " + str(o.fromOffset) + ",untiloffset = "+str(o.untilOffset) + " where partitions = "+ str(o.partition)+";"
#         print "I am update sql.............. :"+sql_str
        cursor.execute(sql_str)
        db.commit()
    cursor.close()
    db.close()
    
partition_info=query_partition()
print partition_info
fromOffsets = {}
for i in partition_info:
    partition = i[1]
    topicPartion = TopicAndPartition("test_first",partition)
    offset = i[3]
    fromOffsets[topicPartion] = long(offset)
    print partition
    print topicPartion
    print offset
print(fromOffsets)

# Create a spark context
sc = SparkContext(appName="SparkStreamingTest")
sc.setLogLevel("WARN")
ssc = StreamingContext(sc, 5)

kafkaParams={"metadata.broker.list":"hdp4.buptnsrc.com:6667"}
topic=["test_first"]
# lines=KafkaUtils.createDirectStream(ssc,topic,kafkaParams,fromOffsets={TopicAndPartition("test_first",0):long(2077644),TopicAndPartition("test_first",1):long(2075729),TopicAndPartition("test_first",2):long(1201194),TopicAndPartition("test_first",3):long(1200158)})

lines=KafkaUtils.createDirectStream(ssc,topic,kafkaParams,fromOffsets=fromOffsets)
# lines=KafkaUtils.createDirectStream(ssc,topic,kafkaParams)
lines.transform(storeOffsetRanges).foreachRDD(printOffsetRanges)
lines.pprint()
ssc.start()
ssc.awaitTermination()


# /usr/hdp/2.6.2.0-205/spark2/bin/spark-submit --master yarn --deploy-mode client --class sparkstreaming.KafkaStreaming --jars /usr/hdp/2.6.2.0-205/third-jars/spark-streaming-kafka-0-8-assembly_2.11-2.1.1.2.6.2.0-205.jar  --conf spark.pyspark.driver.python=/root/anaconda2/bin/python test.py
```

