import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from water_pressure_PH import WaterPressurePH
from water_temperature import WaterTemperature
import datetime
import mysql.connector
import yaml
import pymysql
import logging
import yaml
import logging.config
import sys
import json
from pykafka import KafkaClient
from pykafka.common import  OffsetType
from threading import Thread

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

user = app_config['datastore']['user']
password = app_config['datastore']['password']
hostname = app_config['datastore']['hostname']
port = app_config['datastore']['port']
db = app_config['datastore']['db']

DB_ENGINE = create_engine (f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

def report_water_pressure_PH(body):
    """ Receives a blood pressure reading """

    session = DB_SESSION()
    logger.info(f'Connecting to DB. Hostname:{hostname}, Port:{port}')
    bp = WaterPressurePH(
                       body['device_id'],
                       body['timestamp'],
                       body['kPa'],
                       body['PH'],
                       body['trace_id'])
    logger.info(f'Stored event report_water_pressure_PH request with a trace id of {bp.trace_id}')
    session.add(bp)
    session.commit()
    session.close()
    #trace_id = WaterPressurePH(body['trace_id'])
    return NoContent, 201


def report_water_temperature(body):
    """ Receives a reading """

    session = DB_SESSION()

    hr = WaterTemperature(
                   body['device_id'],
                   body['timestamp'],
                   body['Celcius'],
                   body['trace_id'])
    logger.info(f'Stored event report_water_pressure_PH request with a trace id of {hr.trace_id}')
    session.add(hr)
    session.commit()
    session.close()
    # trace_id = WaterTemperature(body['trace_id'])
    return NoContent, 201

    return NoContent, 200

def get_water_pressure_PH_readings(timestamp): 
    """ Gets new blood pressure readings after the timestamp """ 
 
    session = DB_SESSION() 
 
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ") 
   
 
    readings = session.query(WaterPressurePH).filter(WaterPressurePH.date_created >=   
                                                  timestamp_datetime) 
 
    results_list = [] 
 
    for reading in readings: 
        results_list.append(reading.to_dict()) 
 
    session.close() 
    logger.info("Query for Blood Pressure readings after %s returns %d results" %  
                (timestamp, len(results_list))) 
 
    return results_list, 200

def get_water_temperature_readings(timestamp): 
    """ Gets new blood pressure readings after the timestamp """ 
 
    session = DB_SESSION() 
 
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ") 
   
 
    readings = session.query(WaterTemperature).filter(WaterTemperature.date_created >=   
                                                  timestamp_datetime) 
 
    results_list = [] 

    for reading in readings: 
        results_list.append(reading.to_dict()) 
    session.close() 
    logger.info("Query for Blood Pressure readings after %s returns %d results" %  
                (timestamp, len(results_list))) 
 
    return results_list, 200

def process_messages(): 
    """ Process event messages """ 
    hostname = "%s:%d" % (app_config["events"]["hostname"],   
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
     
    # Create a consume on a consumer group, that only reads new messages  
    # (uncommitted messages) when the service re-starts (i.e., it doesn't  
    # read all the old messages from the history in the message queue). 
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', 
                                         reset_offset_on_start=False, 
                                         auto_offset_reset=OffsetType.LATEST) 
 
    # This is blocking - it will wait for a new message 
    for msg in consumer: 
        msg_str = msg.value.decode('utf-8') 
        msg = json.loads(msg_str) 
        logger.info("Message: %s" % msg) 
 
        payload = msg["payload"] 
 
        if msg["type"] == "water_temperature":
            session = DB_SESSION()
            logger.info(f'Stored event report_water_temperature request with a trace id of {payload["trace_id"]}')
            session.add(WaterTemperature(payload["device_id"],payload["timestamp"],payload["Celcius"],payload["trace_id"]))
            session.commit()
            session.close() # Change this to your event type
            # Store the event1 (i.e., the payload) to the DB 
        elif msg["type"] == "water_pressure_PH":
            session = DB_SESSION()
            logger.info(f'Connecting to DB. Hostname:{hostname}, Port:{port}')
            logger.info(f'Stored event report_water_pressure_PH request with a trace id of {payload["trace_id"]}')
            session.add(WaterPressurePH(payload["device_id"],payload["timestamp"],payload["kPa"],payload["PH"],payload["trace_id"]))
            session.commit()
            session.close() # Change this to your event type 
            # Store the event2 (i.e., the payload) to the DB 
 
        # Commit the new message as being read 
        consumer.commit_offsets()
if __name__ == "__main__":
    t1 = Thread(target=process_messages) 
    t1.setDaemon(True) 
    t1.start()
app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8090)
