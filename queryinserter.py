import argparse
import requests
import yaml
from sqlalchemy import create_engine
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
        query = open(
            './backend-app/sql/insert_query_rating.sql', 'r')
        statement = query.read()
        query.close()
        statement = statement.format(
            clothing_id=data['clothing_id'], age=data['age'], title=data['title'], review=data['review'], rating=data['rating'], recommended=data['recommended'], positive_feedback=data['positive_feedback'], division=data['division'], department=data['department'], class_name=data['class_name'])
        return statement

    @staticmethod
    def get_update_query():
        UPDATE_QUERY = ''
        return UPDATE_QUERY


with open('./backend-app/variables.yaml') as var:
    variables = yaml.load(var, Loader=yaml.FullLoader)

    db = DatabaseConnector(variables)
    datas = [{"clothing_id": 1, "age": 35, "title": "haha", "review": "haha", "rating": 4, "recommended": 1,
              "positive_feedback": 0, "division": "General", "department": "Dresses", "class_name": "Dresses"}]
    db.insert_rating_data(datas)

print("--- data scrapping finished ---")
print("--- execution delta: %s seconds ---" % (time.time() - start_time))
