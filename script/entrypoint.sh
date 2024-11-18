#!/bin/bash
set -e

# installs all requirements
if [ -e "/opt/airflow/requirements.txt" ]; then
  $(command python) pip install --upgrade pip
  $(command -v pip) install --user -r requirements.txt
fi

# check if db exists
if [ ! -f "/opt/airflow/airflow.db" ]; then
  # initiate db
  airflow db init && \
  # create admin user
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin
fi

# finds the db and upgrades it 
$(command -v airflow) db upgrade

# runs the Airflow web server 
exec airflow webserver