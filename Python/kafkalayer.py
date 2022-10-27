from kafka import KafkaConsumer, KafkaClient

def Producer():
    from kafka import KafkaProducer

    producer = KafkaProducer(bootstrap_servers='433-14.csse.rose-hulman.edu:9092')

    future = producer.send('foobar', b'another_message')
    result = future.get(timeout=60)
    print(result)
    producer.flush()
    producer.close()
def Consumer():
    consumer = KafkaConsumer('input_recommend_product', group_id='test-consumer-group',bootstrap_servers=['433-14.csse.rose-hulman.edu:9092'], auto_offset_reset='earliest')
    print(consumer.topics())
    consumer.poll()
    #consumer.seek_to_beginning()
    for msg in consumer:
        print(msg.value)
    consumer.close()

if __name__ == '__main__':
    #Producer()
    Consumer()