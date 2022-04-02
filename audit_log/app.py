import connexion
from connexion import NoContent

from sqlalchemy import create_engine

import yaml

import logging
import yaml
import logging.config

import json
from pykafka import KafkaClient


with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

def get_water_pressure_PH(index): 
    """ Get BP Reading in History """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],  
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
 
    # Here we reset the offset on start so that we retrieve 
    # messages at the beginning of the message queue.  
    # To prevent the for loop from blocking, we set the timeout to 
    # 100ms. There is a risk that this loop never stops if the 
    # index is large and messages are constantly being received! 
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,  
                                         consumer_timeout_ms=1000) 
 
    logger.info("Retrieving BP at index %d" % index) 
    list = []
    try: 
        for msg in consumer: 
            msg_str = msg.value.decode('utf-8') 
            msg = json.loads(msg_str) 
            if msg["type"] == "water_pressure_PH":
                list.append(msg)
        return list[index], 200
        # logger.info(list[index], 200)
            # Find the event at the index you want and  
            # return code 200  
    except: 
        logger.error("No more messages found") 
     
    logger.error("Could not find PPH at index %d" % index) 
    return { "message": "Not Found"}, 404

def get_water_temperature(index): 
    """ Get BP Reading in History """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],  
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
 
    # Here we reset the offset on start so that we retrieve 
    # messages at the beginning of the message queue.  
    # To prevent the for loop from blocking, we set the timeout to 
    # 100ms. There is a risk that this loop never stops if the 
    # index is large and messages are constantly being received! 
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,  
                                         consumer_timeout_ms=1000) 
 
    logger.info("Retrieving BP at index %d" % index)
    list = []
    try: 
        for msg in consumer: 
            msg_str = msg.value.decode('utf-8') 
            msg = json.loads(msg_str) 
            if msg["type"] == "water_temperature":
                list.append(msg)
        return list[index], 200
        # logger.info(list[index], 200) 
    except: 
        logger.error("No more messages found") 
     
    logger.error("Could not find temp at index %d" % index) 
    return { "message": "Not Found"}, 404
app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8100, use_reloader=False)