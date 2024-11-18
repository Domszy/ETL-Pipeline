from datetime import datetime 
from airflow import DAG 
from airflow.operators.python import PythonOperator
import json 
import requests 
import uuid
from kafka import KafkaProducer
import time 
import logging

default_args = {
    'owner': 'Dominic Siew', 
    'start_date': datetime(2024, 8, 3, 10, 00) 
}

def get_data(): 
    respond = requests.get('https://randomuser.me/api/')
    json_data = respond.json()['results'][0]

    return json_data

def format_data(res): 
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
        f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data

def stream_data(): 
    response_from_api = get_data() 
    formatted_info = format_data(response_from_api)

    # print(json.dumps(formatted_info, indent=3))

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    current_time = time.time()

    # stimulate the streaming of data
    while True: 
        if time.time() > current_time + 60: 
            break

        try: 
            result = get_data()
            formatted_result = format_data(result)

            producer.send('user_created', json.dumps(result).encode('utf-8'))
        except Exception as e: 
            logging.error(f'An error Occured: {e}')
            continue

def send_alert():
    # Placeholder for sending an alert after streaming is done
    logging.info("Sending alert...")

with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )

    send_alert_task = PythonOperator(
        task_id='send_alert',
        python_callable=send_alert
    )

    streaming_task >> send_alert_task
