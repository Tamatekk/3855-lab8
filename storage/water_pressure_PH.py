from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime
import sys
sys.path.append('C:\\Users\\rpi_n\\Downloads\\lab3885\\new')

class WaterPressurePH(Base):
    """ Water Pressure PH"""

    __tablename__ = "water_pressure_PH"

    id = Column(Integer, primary_key=True)
    device_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    kPa = Column(Integer, nullable=False)
    PH = Column(Integer, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, device_id, timestamp, kPa, PH, trace_id):
        """ Initializes a blood pressure reading """
        self.device_id = device_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.kPa = kPa
        self.PH = PH
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['device_id'] = self.device_id
        dict['kPa'] = self.kPa
        dict['PH'] = self.PH
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict
