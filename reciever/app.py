from inspect import trace
import connexion 
from connexion import NoContent 
import json 
from datetime import datetime
from os import path
import requests
import yaml
import logging
import logging.config
import uuid
from pykafka import KafkaClient

EVENTS_LIMIT = 10
EVENTS_FILE = "test.json"

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

headers = {'Content-type': 'application/json'}

def report_water_pressure_PH(body):
    # new_json = json.dumps(body, indent = 2)
    # events = []
    # if path.exists(EVENTS_FILE):
    #     with open(EVENTS_FILE, "r") as json_file:
    #         print(json_file)
    #         events = json.load(json_file)
    #     while len(events) >= 10:
    #         events.pop(0)            

    # now = {"now":str(datetime.now())}
    # new_entry=[]
    # new_entry.append(now)
    # new_entry.append(new_json)
    # events.append(new_entry)
    # with open(EVENTS_FILE,"w") as file:
    #     json.dump(events, file)
    trace_id = new_trace_id()
    body["trace_id"] = trace_id
    # logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)
    logger.info(f'Received event report_water_pressure_PH request with a trace id of {trace_id}')
    # requests.post(app_config["eventstore1"]["url"],json=body, headers=headers)

    client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}') 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
    producer = topic.get_sync_producer() 
    
    msg = { "type": "water_pressure_PH",  
            "datetime" :    
            datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f'Returned event report_water_pressure_PH response (Id: {trace_id}) with status 201 ')
    return NoContent, 201

def report_water_temperature(body):
    # new_json = json.dumps(body, indent = 2)
    # events = []
    # if path.exists(EVENTS_FILE):
    #     with open(EVENTS_FILE, "r") as json_file:
    #         print(json_file)
    #         events = json.load(json_file)
    #     while len(events) >= 10:
    #         events.pop(0)            

    # now = {"now":str(datetime.now())}
    # new_entry=[]
    # new_entry.append(now)
    # new_entry.append(new_json)
    # events.append(new_entry)
    # with open(EVENTS_FILE,"w") as file:
    #     json.dump(events, file)

    # logger.debug('Received event <event name> request with a trace id of <trace_id> ')
    # requests.post(app_config["eventstore2"]["url"],json=body,headers=headers)
    # logger.debug('Returned event <event name> response (Id: <trace_id>) with status <status code> ')  

    # logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)
    trace_id = new_trace_id()
    body["trace_id"] = trace_id
    logger.info(f'Received event report_water_temperature request with a trace id of {trace_id}')
    # requests.post(app_config["eventstore2"]["url"],json=body, headers=headers)

    client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}') 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
    producer = topic.get_sync_producer() 
    
    msg = { "type": "water_temperature",  
            "datetime" :    
            datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f'Returned event report_water_pressure_PH response (Id: {trace_id}) with status 201 ')  
    return NoContent, 201
# ids=[]
def new_trace_id():
    return str(uuid.uuid4())
    # trace_id = uuid.uuid4()
    # ids.append(trace_id)

app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yml", strict_validation= True, validate_responses=False) 




if __name__ == "__main__":
    app.run(port=8080)
