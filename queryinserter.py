import argparse
import yaml,csv
from sqlalchemy import create_engine,text
import time
from json import dumps
import random
import linecache
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
        for i in range(int(len(rating_data))):
            self.engine.execute(QueryList.get_rating_insert_query(rating_data[i]))
        
    def simulate_rating_data(self, rating_data):  
        start = 0
        end = int(len(rating_data))
        while True:    
            self.engine.execute(QueryList.get_rating_insert_query(rating_data[start]))
            print(start)
            start +=1
            if start == end:
                start = 0
            time.sleep(5)

class QueryList:
    @staticmethod
    def get_rating_insert_query(data):
        query = open(
            './backend-app/sql/insert_query_rating.sql', 'r')
        statement = query.read()
        query.close()
        statement = statement.format(
            clothing_id=data['clothing_id'], age=data['age'], title=data['title'], review=data['review'], rating=data['rating'], recommended=data['recommended'], positive_feedback=data['positive_feedback'], division=data['division'], department=data['department'], class_name=data['class_name'])
        final = text(statement)
        return final

    @staticmethod
    def get_update_query():
        UPDATE_QUERY = ''
        return UPDATE_QUERY

with open('./backend-app/variables.yaml') as var:
    variables = yaml.load(var)
    db = DatabaseConnector(variables)

    raw_data = pd.read_csv (r'./review.csv', delimiter=',')
    data = raw_data.dropna()

    datas = data.astype({'clothing_id':int,'age':int,'rating':int,'recommended':int,'positive_feedback':int})
    # print(datas)

    ratings = []
    for row in zip(*datas.to_dict("list").values()):
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
    db.simulate_rating_data(ratings)

print("--- data scrapping finished ---")
print("--- execution delta: %s seconds ---" % (time.time() - start_time))
