from sqlalchemy import Column, Integer, String, DateTime 
from base import Base 
class Stats(Base): 
    """ Processing Statistics """ 
 
    __tablename__ = "stats" 
 
    id = Column(Integer, primary_key=True) 
    num_w_PPH_readings = Column(Integer, nullable=False) 
    num_w_temp_readings = Column(Integer, nullable=False) 
    max_w_pres_reading = Column(Integer, nullable=True) 
    max_w_PH_reading = Column(Integer, nullable=True) 
    max_w_temp_reading = Column(Integer, nullable=True) 
    last_updated = Column(DateTime, nullable=False) 
 
    def __init__(self, num_w_PPH_readings, num_w_temp_readings, 
max_w_pres_reading, max_w_PH_reading, max_w_temp_reading, 
last_updated): 
        """ Initializes a processing statistics objet """ 
        self.num_w_PPH_readings = num_w_PPH_readings 
        self.num_w_temp_readings = num_w_temp_readings 
        self.max_w_pres_reading = max_w_pres_reading 
        self.max_w_PH_reading = max_w_PH_reading 
        self.max_w_temp_reading = max_w_temp_reading 
        self.last_updated = last_updated 
 
    def to_dict(self): 
        """ Dictionary Representation of a statistics """ 
        dict = {} 
        dict['num_w_PPH_readings'] = self.num_w_PPH_readings 
        dict['num_w_temp_readings'] = self.num_w_temp_readings 
        dict['max_w_pres_reading'] = self.max_w_pres_reading 
        dict['max_w_PH_reading'] = self.max_w_PH_reading 
        dict['max_w_temp_reading'] = self.max_w_temp_reading 
        dict['last_updated'] = self.last_updated.strftime('''%Y-
%m-%dT%H:%M:%S''') 
 
        return dict