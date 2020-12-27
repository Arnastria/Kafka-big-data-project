from time import sleep
from json import dumps
from kafka import KafkaProducer
import random
import linecache

producer = KafkaProducer(
    bootstrap_servers=[
        'localhost:9093'], value_serializer=lambda x: dumps(x).encode('utf-8'))

with open('women_westernwear.csv') as data_csv:
    lines = sum(1 for line in data_csv)
    for i in range(1000):
        try:
            line_number = random.randrange(1, lines)
            time_random = random.randrange(8, 15)
        except ValueError as e:
            line_number = 1
            time_random = 10

        line = linecache.getline('women_westernwear.csv', line_number)
        data = {"id": line_number, "productName": line.split(',')[0]}

        print("[sending data...] "+str(data))
        producer.send('sales.most-sales-product', value=data)
        sleep(time_random)
