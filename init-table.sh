# #!/bin/bash
# psql -U postgres -h localhost -c "CREATE DATABASE RATING;"
psql -U postgres -h localhost -d postgres -a -f "init-table.sql"

curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '
{
	"name": "rating-connector",
	"config": {
	    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "tasks.max": "1",
        "database.hostname": "postgres",
        "database.port": "5432",
        "database.user": "postgres",
        "database.password": "postgres",
        "database.dbname": "postgres",
        "database.server.name": "dbserver1",
        "schema.whitelist": "rating"
    }
	}
  }'

curl -X GET -H "Accept:application/json" localhost:8083/connectors/rating-connector

#=============================
# psql -U postgres -h localhost -c "CREATE DATABASE RATING_DB;"
# psql -U postgres -h localhost -d rating_db -a -f "init-table.sql"

# curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '
# {
# 	"name": "rating-data-connector",
# 	"config": {
# 	  "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
# 	  "tasks.max": "1",
# 	  "database.hostname": "pg-docker",
# 	  "database.port": "5432",
# 	  "database.user": "postgres",
# 	  "database.password": "postgres",
# 	  "database.dbname": "rating_db",
# 	  "database.server.name": "pg1",
# 	  "database.whitelist": "rating_db",
# 	  "database.history.kafka.bootstrap.servers": "kafka1:19092",
# 	  "database.history.kafka.topic": "schema-changes.rating"
# 	}
#   }'

# curl -X GET -H "Accept:application/json" localhost:8083/connectors/rating-data-connector
