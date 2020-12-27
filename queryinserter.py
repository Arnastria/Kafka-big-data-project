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
        half = int(len(rating_data)/2)
        for i in range(200):
            self.engine.execute(QueryList.get_rating_insert_query(rating_data[i]))
        
        starttime = time.time()
        while True:
            for i in range(1):
                self.engine.execute(QueryList.get_rating_insert_query(rating_data[i]))
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

    # out = []
    # with open('test5.csv') as csv_file:
    #     reader = csv.reader(csv_file, delimiter=',')
    #     header = next(reader)
    #     for row in reader:
    #         if (len(row) == len(header)):
    #             out.append(row)

    # df = pd.DataFrame(out, columns=header)
    # data = df[df.positive_feedback.apply(lambda x: x.isnumeric())]
    # print(len(data))
    # data.to_csv(r'./test6.csv', index = False)

    raw_data = pd.read_csv (r'./review.csv', delimiter=',')
    data = raw_data.dropna()

    datas = data.astype({'clothing_id':int,'age':int,'rating':int,'recommended':int,'positive_feedback':int})
    print(datas)

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

print("--- data scrapping finished ---")
print("--- execution delta: %s seconds ---" % (time.time() - start_time))
