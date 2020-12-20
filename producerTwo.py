from time import sleep
from json import dumps
from kafka import KafkaProducer
import random

producer = KafkaProducer(
    bootstrap_servers=[
        'localhost:9093'], value_serializer=lambda x: dumps(x).encode('utf-8'))

# The data is still dummy
x = ['sentinel', 'havoc', 'charai', 'G7 Scout', 'Volt SMG', 'Prowler SMG',
     'R-99', 'R-301 Carbine', 'Hemlock Burst AR', 'Flatline', 'Masstiff']

for i in range(1000):
    data = {'id': i, 'name': random.choice(x)}
    producer.send('most-sales-product', value=data)
    print("sending message... "+str(data))
    sleep(5)
