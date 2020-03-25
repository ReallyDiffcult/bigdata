# -*- coding:utf8 -*-
import findspark

findspark.init(spark_home="/usr/hdp/current/spark2-client/", python_path="/root/anaconda2/bin/python")

from pyspark.sql import SparkSession
import json
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark.streaming import StreamingContext


def get_spark(master="yarn", memory="1g", local_dir="/tmp", app_name="preporcess", queue="default", engine_id="asdf"):
    msg = "Please Note..... \n      spark up."
    '''
    创建spark content

    输入:
        master: spark 运行模式
        memory: spark 执行节点的内存
        local_dir: spark的本地目录位置 需要容量较大
    输出:
        spark content
    '''
    spark = SparkSession.builder.appName(app_name).master("yarn").config(
        "spark.shuffle.service.enabled", True
    ).config(
        "spark.executor.instances", 2
    ).config(
        "spark.executor.cores", 2
    ).config("spark.driver.memory", "1G"
             ).config(
        "spark.executor.memory", "1G"
    ).config(
        "spark.shuffle.memoryFraction", "0.6"
    ).config(
        "spark.default.parallelism", 400
    ).config(
        "spark.local.dir", "/tmp"
    ).config(
        "spark.driver.maxResultSize", "5G"
    ).config(
        "spark.yarn.queue", "http_project"
    ).config(
        "spark.streaming.kafka.maxRatePerPartition", 100
    ).getOrCreate()

    print("create spark session", spark.sparkContext.master)
    print(msg)
    return spark

def get_direct_kafka(ssc):
    # zookeeper="hdp2.buptnsrc.com:2181,hdp4.buptnsrc.com:2181,hdp1.buptnsrc.com:2181"
    # groupid="test-consumer-lwh-group"
    # topics={"test_kafka_flume_hbase_lwh":0,"test_kafka_flume_hbase_lwh":1}
    # lines=KafkaUtils.createStream(ssc=ssc,topics=topics,groupId=groupid,zkQuorum=zookeeper)
    # return lines
    kafkaParams = {"metadata.broker.list": "hdp2.buptnsrc.com:6667,hdp4.buptnsrc.com:6667,hdp5.buptnsrc.com:6667"}
    topic = ["test_first"]
    lines = KafkaUtils.createDirectStream(ssc, topic, kafkaParams)
    return lines


def process(row):
    return 0


if __name__ == '__main__':
    print("11122")
    # 获取到spark session
    spark = get_spark(master="yarn", app_name="kafka-test-yangkun1", queue="default")
    sc = spark.sparkContext
    # 处理时间间隔为2s
    ssc = StreamingContext(sc, 30)
    print("333")

    lines = get_direct_kafka(ssc)

    # lines=get_kafka(ssc)

    lines.foreachRDD(process)
    line = lines.flatMap(lambda x: x[1].split(' '))
    res = line.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)
    print(type(lines))
    print("------------------   start   ---------------")
    res.pprint()
    print("-------------------  finish  --------------------!!!")

    ssc.start()
    ssc.awaitTermination()