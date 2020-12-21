import argparse
import requests
import yaml,csv
from sqlalchemy import create_engine
import time
from json import dumps
import pandas as pd
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
        
        starttime = time.time()
        while True:
            start = 0
            end = 5
            for i in range(end):
                self.engine.execute(QueryList.get_rating_insert_query(rating_data[i]))
                if i == end:
                    i = 0
            print("tick")
            time.sleep(5.0 - ((time.time() - starttime) % 5.0))

            

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
    variables = yaml.load(var)
    db = DatabaseConnector(variables)

    raw_data = pd.read_csv (r'./dummy.csv', delimiter=';')
    data = raw_data.dropna().astype({'clothing_id':int,'age':int,'rating':int,'recommended':int,'positive_feedback':int}) 

    ratings = []
    
    for row in zip(*data.to_dict("list").values()):
        ratings.append({"clothing_id": row[1], 
                    "age": row[2], 
                    "title": row[3], 
                    "review": row[4],  
                    "rating": row[5],  
                    "recommended": row[6], 
                    "positive_feedback": row[7],
                    "division": row[8],  
                    "department": row[9], 
                    "class_name": row[10]})
    db.insert_rating_data(ratings)

print("--- data scrapping finished ---")
print("--- execution delta: %s seconds ---" % (time.time() - start_time))
