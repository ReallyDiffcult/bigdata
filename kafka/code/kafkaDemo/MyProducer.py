from kafka import KafkaProducer
from kafka.errors import KafkaError
producer = KafkaProducer(bootstrap_servers='hdp4.buptnsrc.com:6667')

# Asynchronous by default
for i in range(100):
    value = "hello yangkun" + str(i)
    future = producer.send("test_first", bytes(value,encoding="utf-8"))

producer.flush()
producer.close()

