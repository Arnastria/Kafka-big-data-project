import argparse
import requests
import yaml
from sqlalchemy import create_engine
from kafka import KafkaProducer
import time
from json import dumps


start_time = time.time()

class DatabaseConnector:

    def __init__(self, variables):
        self.settings = {
            'user': variables['database']['username'],
            'pass': variables['database']['password'],
            'host': variables['database']['host'],
            'db': variables['database']['db'],
            'port': variables['database']['port']
        }
        url_db = 'postgresql+psycopg2://{user}:{pass}@{host}:{port}/{db}'.format(
            **self.settings)
        self.engine = create_engine(url_db, client_encoding='utf8')

    def insert_rating_data(self, rating_data):
        for i in rating_data:
            self.engine.execute(QueryList.get_rating_insert_query(i))

class QueryList:

    @staticmethod
    def get_rating_insert_query(data):
        query = open('/usr/local/airflow/dags/sql/insert_query_rating.sql', 'r')
        statement = query.read()
        query.close()
        statement = statement.format(product_name= data['product_name'], score= data['score'])
        return statement

    @staticmethod
    def get_update_query():
        UPDATE_QUERY = ''
        return UPDATE_QUERY


with open('/usr/local/airflow/dags/variables.yaml') as var:
    variables = yaml.load(var)

    db = DatabaseConnector(variables)
    datas = [{"product_name":"Brother","score":12},{"product_name":"Sister","score":23}]
    db.insert_rating_data(datas)

print("--- data scrapping finished ---")
print("--- execution delta: %s seconds ---" % (time.time() - start_time))