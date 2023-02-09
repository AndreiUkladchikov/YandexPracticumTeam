#!/bin/sh

start_etl_process () {
  echo "Starting ETL process from Kafka to ClickHouse..."
  
  ./main.py
}

start_etl_process 

exec "$@"
