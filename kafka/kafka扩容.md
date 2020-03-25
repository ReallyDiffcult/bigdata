### kafka扩容

[参考博客](https://www.iteblog.com/archives/1611.html)

#### 1. 在broker0 和 broker1 的节点上创建分区为3，副本数为2的的主题

```
[atguigu@hadoop101 kafka]$ bin/kafka-topics.sh --zookeeper hadoop101:2181 --create --topic six --replica-assignment "0:1,0:1,0:1"
Created topic "six".
[atguigu@hadoop101 kafka]$ bin/kafka-topics.sh --zookeeper hadoop102:2181 --describe --topic six
Topic:six	PartitionCount:3	ReplicationFactor:2	Configs:
	Topic: six	Partition: 0	Leader: 0	Replicas: 0,1	Isr: 0,1
	Topic: six	Partition: 1	Leader: 0	Replicas: 0,1	Isr: 0,1
	Topic: six	Partition: 2	Leader: 0	Replicas: 0,1	Isr: 0,1

```

#### 2. 借助kafka-reassign-partitions.sh工具生成reassign plan，不过我们先得按照要求定义一个文件，里面说明哪些topic需要重新分区，文件内容如下：

```
[atguigu@hadoop101 kafka]$ vim topics-to-move.json

{ "topics": [{"topic": "six"}],
  "version" : 1
}
```

#### 3. 使用`kafka-reassign-partitions.sh`工具生成reassign plan

````
 bin/kafka-reassign-partitions.sh --zookeeper hadoop101:2181 --topics-to-move-json-file topics-to-move.json --broker-list "0,1,2" --generate
 ########################################################################
Current partition replica assignment
{"version":1,"partitions":[{"topic":"six","partition":0,"replicas":[0,1]},{"topic":"six","partition":1,"replicas":[0,1]},{"topic":"six","partition":2,"replicas":[0,1]}]}

Proposed partition reassignment configuration
{"version":1,"partitions":[{"topic":"six","partition":0,"replicas":[1,0]},{"topic":"six","partition":1,"replicas":[2,1]},{"topic":"six","partition":2,"replicas":[0,2]}]}

````

#### 4. Proposed partition reassignment configuration下面生成的就是将分区重新分布到broker 0-2上的结果。我们将这些内容保存到名为result.json文件里面（文件名不重要，文件格式也不一定要以json为结尾，只要保证内容是json即可），然后执行这些reassign plan：

```
[atguigu@hadoop101 kafka]$ bin/kafka-reassign-partitions.sh --zookeeper hadoop101:2181 --reassignment-json-file result.json --execute
Current partition replica assignment

{"version":1,"partitions":[{"topic":"six","partition":0,"replicas":[0,1]},{"topic":"six","partition":1,"replicas":[0,1]},{"topic":"six","partition":2,"replicas":[0,1]}]}

Save this to use as the --reassignment-json-file option during rollback
Successfully started reassignment of partitions.

```



#### 5. 这样Kafka就在执行reassign plan，我们可以校验reassign plan是否执行完成

```
[atguigu@hadoop101 kafka]$ bin/kafka-reassign-partitions.sh --zookeeper hadoop101:2181 --reassignment-json-file result.json --verify
Status of partition reassignment: 
Reassignment of partition [six,0] completed successfully
Reassignment of partition [six,1] completed successfully
Reassignment of partition [six,2] completed successfully
```

#### 6. 检验分区效果

```
[atguigu@hadoop101 kafka]$ ./bin/kafka-topics.sh --topic six --describe --zookeeper hadoop101:2181
Topic:six	PartitionCount:3	ReplicationFactor:2	Configs:
	Topic: six	Partition: 0	Leader: 0	Replicas: 1,0	Isr: 0,1
	Topic: six	Partition: 1	Leader: 2	Replicas: 2,1	Isr: 1,2
	Topic: six	Partition: 2	Leader: 0	Replicas: 0,2	Isr: 0,2

```

#### 注：`kafka-reassign-partitions.sh`工具生成的reassign plan只是一个建议，方便大家而已。其实我们自己完全可以编辑一个reassign plan，然后执行它，如下：

```
{
    "version": 1, 
    "partitions": [
        {
            "topic": "six", 
            "partition": 0, 
            "replicas": [
                0, 
                1
            ]
        }, 
        {
            "topic": "six", 
            "partition": 1, 
            "replicas": [
                1, 
                2
            ]
        }, 
        {
            "topic": "six", 
            "partition": 2, 
            "replicas": [
                2, 
                0
            ]
        }
    ]
}
```

```
[atguigu@hadoop101 kafka]$ ./bin/kafka-topics.sh --topic six --describe --zookeeper hadoop101:2181
Topic:six	PartitionCount:3	ReplicationFactor:2	Configs:
	Topic: six	Partition: 0	Leader: 0	Replicas: 0,1	Isr: 0,1
	Topic: six	Partition: 1	Leader: 2	Replicas: 1,2	Isr: 1,2
	Topic: six	Partition: 2	Leader: 0	Replicas: 2,0	Isr: 0,2

```



