import connexion
from connexion import NoContent
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
import datetime
import yaml
import requests
import logging
import yaml
import logging.config
from stats import Stats
from apscheduler.schedulers.background import BackgroundScheduler
from uuid import uuid1
from datetime import datetime
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

DB_ENGINE = create_engine("sqlite:///%s" % 
app_config["datastore"]["filename"]) 
Base.metadata.bind = DB_ENGINE 
DB_SESSION = sessionmaker(bind=DB_ENGINE) 

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config) 
logger = logging.getLogger('basicLogger')

def get_stats():
    logger.info("Request has started.")

    session = DB_SESSION() 

    try:
        readings = session.query(Stats).order_by(Stats.last_updated.desc()).first()

        results = readings.to_dict()
    except:
        logger.error("Statistics do not exist.")

    session.close()

    logger.debug(f"Python Dictionary Contents: {results}.")
    logger.info(f"Request has completed.")

    return results, 200

def populate_stats():
    logger.info(f"Periodic Request Process Has Started")

    session = DB_SESSION() 
 
    try:
        readings = session.query(Stats).order_by(Stats.last_updated.desc()).all()

        results = [] 

        for reading in readings: 
            results.append(reading.to_dict()) 
    except:
        results = [{'num_w_PPH_readings': 0, 'max_w_pres_reading': 0, 'max_w_PH_reading': 0, 'num_w_temp_readings': 0, 'max_w_temp_reading': 0, 'last_updated': '2022-02-17T10%3A31%3A41Z'}]
    
    response1 = requests.get(f"http://localhost:8090/readings/water_pressure_PH/stats?timestamp=2022-02-17T10%3A31%3A41Z")
    response2 = requests.get(f"http://localhost:8090/readings/water_temperature/stats?timestamp=2022-02-17T10%3A31%3A41Z")

    pressurePH = response1.json()
    temp = response2.json()

    responses = pressurePH + temp

    if response1.ok and response2.ok:
        logger.info(f"Total responses received: {len(responses)}")
    else:
        logger.error("GET request failed.")

    trace_id = str(uuid1())

    total_pres = sum([x['kPa'] for x in pressurePH])
    total_ph = sum([x['PH'] for x in pressurePH])
    total_temp = sum([x['Celcius'] for x in temp])


    logger.debug(f"Total PH: {total_ph}. TraceID: {trace_id}")
    logger.debug(f"Total pressure {total_pres}. TraceID: {trace_id}")
    logger.debug(f"Total temparature {total_temp}. TraceID: {trace_id}")
    logger.debug(f"Total number of PPH requests {len(pressurePH)}. TraceID: {trace_id}")
    logger.debug(f"Total number of temp updates {len(temp)}. TraceID: {trace_id}")

    stats = Stats(
              len(pressurePH), 
              len(temp), 
              total_pres, 
              total_ph, 
              total_temp, 
              datetime.now())

    session.add(stats) 
 
    logger.debug(f"New Stat entry. TraceID: {trace_id}")

    session.commit()
    session.close()

    logger.info(f"Periodic Request Process has ended.")

def init_scheduler(): 
    sched = BackgroundScheduler(daemon=True) 
    sched.add_job(populate_stats,    
                  'interval', 
                  seconds=app_config['scheduler']['period_sec']) 
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8101, use_reloader=False)