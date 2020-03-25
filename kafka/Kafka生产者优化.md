### Kafka优化

#### 1、并发优化

 **（1）利用消费者组，可以开启多个消费者进行消费**

  		利用producer生产10条数据（生产到两个分区），利用消费者组开启2个消费者可以进行不重复消费

```
package com.bupt.comsumer;

import org.apache.kafka.clients.consumer.*;

import java.util.Arrays;

import java.util.Properties;

public class MyConsumer {
    public static void main(String[] args) {
        //1 创建消费者配置信息
        Properties properties = new Properties();
        //2 给配置信息复制
            //连接集群
        properties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,"hadoop101:9092");
            //消费者组
        properties.put(ConsumerConfig.GROUP_ID_CONFIG,"test");
            //开启自动提交
        properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true");
       // properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
            //自动提交的延时
        properties.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000");
            //key value的反序列化
        properties.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG,"earliest");
        properties.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringDeserializer");
        properties.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringDeserializer");
        //3 创建消费者
        KafkaConsumer<String, String> consumer = new KafkaConsumer<String, String>(properties);
        //4 订阅主题
        consumer.subscribe(Arrays.asList("first","second"));

        while(true){
            //获取数据
            ConsumerRecords<String, String> consumerRecords = consumer.poll(100);
            //解析并打印
            for(ConsumerRecord<String, String> Records:consumerRecords){
                System.out.println(Records.offset()+"--------"+Records.key()+"------"+Records.value());
            }
           // consumer.commitSync();
        }

    }
}
```

consumer1控制台

![consumeryouhua1](C:\Users\yangkun\Desktop\bigdata\kafka\笔记截图\consumeryouhua1.png)

consumer2控制台

![consumeryouhua2](C:\Users\yangkun\Desktop\bigdata\kafka\笔记截图\consumeryouhua2.png)

   **(2) 利用多线程，开启多线程进行消费**

​		利用多线程开启不同的消费者进行消费

```
package com.bupt.comsumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;

import java.util.Arrays;
import java.util.Properties;
public class MyTestThread {

    public static void main(String[] args) {
        new Thread(new MyConsumerThread(),"a").start();

        new Thread(new MyConsumerThread(),"b").start();
    }
}

class MyConsumerThread implements Runnable {
    KafkaConsumer<String, String> consumer;
    public  MyConsumerThread(){
        Properties properties = new Properties();
        properties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,"hadoop101:9092");
        //消费者组
        properties.put(ConsumerConfig.GROUP_ID_CONFIG,"test");
        //开启自动提交
        properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true");
        // properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        //自动提交的延时
        properties.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000");
        //key value的反序列化
        //properties.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG,"earliest");
        properties.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringDeserializer");
        properties.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringDeserializer");
        //3 创建消费者
        consumer = new KafkaConsumer<String, String>(properties);
    }
    @Override
    public void run() {
        consumer.subscribe(Arrays.asList("first"));
        while(true){
            ConsumerRecords<String,String> records = consumer.poll(1000);
            for (ConsumerRecord<String, String> record : records) {
                System.out.println(Thread.currentThread().getName()+"进行了消费"+record.value()+"分区是"+record.partition()+"偏移量是"+record.offset());
            }

        }

    }
}
```

测试结果：

![duoxianchengceshijieguo](C:\Users\yangkun\Desktop\bigdata\kafka\笔记截图\duoxianchengceshijieguo.png)

**消费的阻塞队列**

```
 消费和处理解耦 
一个或多个消费者线程来做所有的数据消费，把ConsumerRecords实例存到一个被多个处理线程或线程池
消费的阻塞队列
	好处：不限制消费和处理的线程，让一个消费者来满足多个处理线程，避免了线程数被分区数所限制
    理解 ：(因为 不解耦的情况下，消费和处理在一起，offset提交的原因，消费线程被分区数限制，多的线程都是空转。而解耦了，处理线程完全不受限制，消费线程仍然限制) 
    坏处 : 顺序是一个问题， 多个处理线程顺序无法保证，先从阻塞队列获得的数据 可能比后面获得的数据处理时间晚
    坏处 ： 手动提交offset变得很难，可能数据丢失和重复消费
```

```
package com.bupt.comsumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import sun.applet.Main;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.Properties;
import java.util.concurrent.LinkedBlockingQueue;

public class MyTestThread2 {
    public static void main(String[] args) throws InterruptedException {
        KafkaConsumer<String, String> consumer;
        Properties properties = new Properties();
        properties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,"hadoop101:9092");
        //消费者组
        properties.put(ConsumerConfig.GROUP_ID_CONFIG,"test");
        //开启自动提交
        properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true");
        // properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        //自动提交的延时
        properties.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000");
        //key value的反序列化
        //properties.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG,"earliest");
        properties.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringDeserializer");
        properties.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,"org.apache.kafka.common.serialization.StringDeserializer");
        consumer = new KafkaConsumer<String, String>(properties);
        consumer.subscribe(Arrays.asList("first"));
        ConsumerRecords<String, String> records ;
 
        /*
        线程安全，获取如果没有 阻塞，添加如果多了 阻塞 ，多线程数据共享，类似消息队列
         */
        LinkedBlockingQueue<ConsumerRecords<String, String>> list = new LinkedBlockingQueue();


        new Thread(new MyThread4(list),"bb").start();

        new Thread(new MyThread4(list),"aa").start();

        while (true){

            records = consumer.poll(1000);

            list.put(records);

            //建议打开来主动提交
            // 默认的自动提交会造成offset的提交不及时，关闭再启动的时候会重复消费
            //避免不了数据丢失
            // consumer.commitAsync();
        }



    }
}
/**
 * 消费和处理解耦
 * 一个或多个消费者线程来做所有的数据消费，把ConsumerRecords实例存到一个被多个处理线程或线程池
 * 消费的阻塞队列
 * 好处：不限制消费和处理的线程，让 一个消费者来满足多个处理线程，避免了线程数被分区数所限制
 *      理解 ：(因为 不解耦的情况下，消费和处理在一起，offset提交的原因，消费线程被分区数限制，多的线程都是空转。
 *          而解耦了，处理线程完全不受限制，消费线程仍然限制
 *      )
 * 坏处 : 顺序是一个问题， 多个处理线程顺序无法保证，先从阻塞队列获得的数据 可能比后面获得的数据处理时间晚
 *  坏处 ： 手动提交offset变得很难，可能数据丢失和重复消费
 *
 * 2. Decouple Consumption and Processing
 * Another alternative is to have one or more consumer threads that do all data consumption and hands off ConsumerRecords instances to a blocking queue consumed by a pool of processor threads that actually handle the record processing.
 * This option likewise has pros and cons:
 * PRO: This option allows independently scaling the number of consumers and processors.
 *      This makes it possible to have a single consumer that feeds many processor threads, avoiding any limitation on partitions.
 * CON: Guaranteeing order across the processors requires particular care as the threads will execute independently an earlier chunk of data may actually be processed after a later chunk of data just due to the luck of thread execution timing.
 *      For processing that has no ordering requirements this is not a problem.
 * CON: Manually committing the position becomes harder as it requires that all threads co-ordinate to ensure that processing is complete for that partition.
 *      There are many possible variations on this approach. For example each processor thread can have its own queue,
 *      and the consumer threads can hash into these queues using the TopicPartition to ensure in-order consumption and simplify commit.
 */

class MyThread4 implements Runnable {

    LinkedBlockingQueue<ConsumerRecords<String, String>> list ;

    public MyThread4 (LinkedBlockingQueue<ConsumerRecords<String, String>> list){
        this.list = list;
    }

    @Override
    public void run() {
        System.out.println(Thread.currentThread().getName()+"I come in!!");
        while (true) {
            ConsumerRecords<String, String> consumerRecords;
            try {
                consumerRecords = list.take();
                for (ConsumerRecord<String, String> consumerRecord : consumerRecords) {
                    System.out.println(Thread.currentThread().getName()
                            +"消费了:" + consumerRecord.value()
                            +"  分区："+consumerRecord.partition()
                            +"偏移量是:" + consumerRecord.offset()
                    );
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }


        }
    }
}

```

