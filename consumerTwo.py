from kafka import KafkaConsumer
from json import loads
from time import sleep


consumer = KafkaConsumer(
    'sales.most-sales-product',
    bootstrap_servers=['localhost:9093'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

consumer.poll()

for event in consumer:
    event_data = event.value

    print("====================================")
    print(event_data)
    print()
    sleep(2)
