from kafka import KafkaConsumer
import json
import avro
from kafka.consumer.fetcher import ConsumerRecord

consumer = KafkaConsumer("test_first",bootstrap_servers="hdp4.buptnsrc.com:6667")
for message in consumer:
    # print(message)
    #json读取kafka的消息
    # content = json.loads(message.value)
    # print(content)
    print(message.value)