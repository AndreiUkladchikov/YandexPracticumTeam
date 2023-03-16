#!/bin/sh

start_etl_worker () {
  echo "Starting ETL worker for email messages rendering..."
  
  python main.py
}

start_etl_worker

exec "$@"
