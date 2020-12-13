## PDB Big Data Project
#### Apache Kafka + Debezium 
----
This is a starter project for simulating CDC process using Apache Kafka and Debezium

link to frontend project is [here](https://github.com/Arnastria/pdb-kafka-frontend-django)

Prerequisite :
- Docker Compose. Get it from the [official instalation documentation](https://docs.docker.com/compose/install/)
- psql (postgresql client)
- Python

## How to Run
### Run the docker compose :
```
docker-compose -f docker-compose-pdb.yaml up
```
### Initiate the database using bash command :
* the default password is ```'postgres'```
```
./init-table.sh
```
### Check if the topics is created :
```
docker-compose -f docker-compose-pdb.yaml exec kafka /kafka/bin/kafka-topics.sh \          
    --bootstrap-server kafka:9092 \
    --list         
```
You should see topic ```dbserver1.rating.product_rating``` if the procedure are right.

### To listen the stream using command line :
```
docker-compose -f docker-compose-pdb.yaml exec kafka /kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server kafka:9092 \
    --from-beginning \
    --property print.key=true \
    --topic dbserver1.rating.product_rating
```
### Modify records in the database via Postgres client
```
docker-compose -f docker-compose-pdb.yaml exec postgres env PGOPTIONS="--search_path=rating" bash -c 'psql -U $POSTGRES_USER postgres'
```
### Modify records using bash command (WARNING : DUMMY):
```
./table-add-command.sh   
```
### Listen to the stream using python :
* make sure you've already installed kafka-python in pip
```
python consumer.py   
```
### Modify records using using python :
```
python queryinserter.py
```
### Shut down the cluster
```
docker-compose -f docker-compose-pdb.yaml down
```

## TODO
-------
- [x] Listen using python (kafka-python) 
- [ ] Simulate data stream every x seconds using airflow
- [ ] create proper DB. please look at ```init-table.sql``` to see that the table is still dummy. Adjust with the dataset.