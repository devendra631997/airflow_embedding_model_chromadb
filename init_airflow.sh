#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:./"
# Initialize the Airflow database
echo "Initializing Airflow database..."
airflow db init

# Create the admin user (if it doesn't already exist)
echo "Creating admin user..."
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com || echo "Admin user already exists"

# Start the appropriate Airflow service (scheduler or webserver)
if [ "$1" == "webserver" ]; then
  echo "Starting Airflow webserver..."
  exec airflow webserver
elif [ "$1" == "scheduler" ]; then
  echo "Starting Airflow scheduler..."
  exec airflow scheduler
else
  echo "Invalid argument! Use 'webserver' or 'scheduler'."
  exit 1
fi
