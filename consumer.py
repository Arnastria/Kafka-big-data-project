from kafka import KafkaConsumer
from json import loads
from time import sleep


consumer = KafkaConsumer(
    'dbserver1.rating.product_rating',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

for event in consumer:
    event_data = event.value

    print("====================================")
    print(event_data)
    print()
    sleep(2)
