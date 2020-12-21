import argparse
import requests
import yaml,csv
from sqlalchemy import create_engine
import time
from json import dumps
import pandas as pd
start_time = time.time()

# class RatingData:

#     def __init__(self, variables):
#         self.payload = requests.get(variables['endpoint']).json()['rating']

#     def get_rating_data(self):
#         rating_data = [{"clothing_id": i['clothing_id'],
#                           "age": i['age'],
#                           "title": i['title'],
#                           "review": i['review'],
#                           "rating": i['rating'],
#                           "recommended": i['recommended'],
#                           "positive_feedback": i['positive_feedback'],
#                           "division": i['division'],
#                           "department": i['department'],
#                           "class_name": i['class_name']} for i in self.payload]
#         return rating_data

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

# def yaml_dump(filepath,data):
#     with open(filepath,"w") as file_descriptor:
#         yaml.dump(data,file_descriptor)

# csvfile = open('./dummy.csv', 'r')
# datareader = csv.reader(csvfile, delimiter=';', quotechar='"')
# data_headings = []
# new_yaml = open('outfile.yaml', 'w')
# filepath = "rating.yaml"
# for row_index, row in enumerate(datareader):
#     print(row)
#     if row_index == 0:
#         data_headings = row
#     else:
#         yaml_text = "\n {"
#         for cell_index, cell in enumerate(row):
#             lineSeperator = ""
#             cell_heading = data_headings[cell_index].lower().replace(" ", "_").replace("-", "")
#             if (cell_heading == "id"):
#                 cell_text = ''
#             elif (cell_heading == "class_name"):
#                 cell_text = lineSeperator+cell_heading + ": " + cell.replace("\n", ", ") + "},"
#             else:
#                 cell_text = lineSeperator+cell_heading + ": " + cell.replace("\n", ", ") + ","
#             yaml_text += cell_text
#             print (yaml_text)
#         new_yaml.write(yaml_text)
            

#         # yaml_dump(filepath,new_yaml)
# csvfile.close()

with open('./backend-app/variables.yaml') as var:
    variables = yaml.load(var)
    

    # rating = RatingData(variables)

    # with open('./dummy.yaml') as product:
    #     product_rating = yaml.load(product, Loader=yaml.FullLoader)
    #     print(product_rating)
    # db = DatabaseConnector(variables)
    # db.insert_rating_data(product_rating)

    # with open('./outfile.yaml') as product:
    #     product_rating = yaml.load(product, Loader=yaml.FullLoader)
    #     print(product_rating)
    # db = DatabaseConnector(variables)
    # db.insert_rating_data(product_rating)

    db = DatabaseConnector(variables)
    print('test')

    data = pd.read_csv (r'./dummy.csv', delimiter=';')   
    
    ratings = []
    for row in zip(*data.to_dict("list").values()):
        print(row[0])
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
        # datas = {"clothing_id": row.clothing_id, 
        #             "age": row.age,
        #             "title": row.title, 
        #             "review": row.review, 
        #             "rating": row.rating, 
        #             "recommended": row.recommended, 
        #             "positive_feedback": row.positive_feedback, 
        #             "division": row.division, 
        #             "department": row.department, 
        #             "class_name": row.class_name}
    db.insert_rating_data(ratings)

    # openFile = open('./dummy.csv', 'r')
    # csvFile = csv.reader(openFile, delimiter=';')
    # header = next(csvFile)
    # headers = map((lambda x: '`'+x+'`'), header)
    # for row in csvFile:
    #     values = map((lambda x: '"'+x+'"'), row)
    #     coba = "("+ ", ".join(values) +");"
    #     db.insert_rating_data(coba)
    # openFile.close()

    # with open('./dummy.csv') as csvfile:
    #     myCSVReader = csv.DictReader(csvfile, delimiter=';', quotechar='"')

    #     for row in myCSVReader:
    #     # use row directly when csv headers match column names.
    #         print(row[0][0])
    # datas = [{"clothing_id": 10, "age": 20, "title": "future", "review": "haha", "rating": 4, "recommended": 1, "positive_feedback": 0, "division": "General", "department": "Dresses","class_name": "Dresses"}]
        # db.insert_rating_data(row)

print("--- data scrapping finished ---")
print("--- execution delta: %s seconds ---" % (time.time() - start_time))
