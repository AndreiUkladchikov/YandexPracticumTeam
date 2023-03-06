#!/bin/sh

start_etl_worker () {
  echo "Starting ETL worker for email messages rendering..."
  
  ./worker/main.py
}

start_etl_worker

exec "$@"
