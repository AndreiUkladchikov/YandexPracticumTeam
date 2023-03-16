#!/bin/sh

start_etl_worker () {
  echo "Starting ETL worker for email messages rendering..."
  
  cd worker && python3 -m main.py
}

start_etl_worker

exec "$@"
