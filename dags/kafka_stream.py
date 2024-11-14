from datetime import datetime 
from airflow import DAG 
from airflow.operators.python import PythonOperator
import json 
import requests 
import uuid

default_args = {
    'owener': 'Dominic Siew', 
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

    print(json.dumps(formatted_info, indent=3))

stream_data()