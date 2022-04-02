import sqlite3 
 
conn = sqlite3.connect('stats.sqlite') 
 
c = conn.cursor() 
c.execute(''' 
          CREATE TABLE stats 
          (id INTEGER PRIMARY KEY ASC,  
           num_w_PPH_readings INTEGER NOT NULL, 
           max_w_pres_reading INTEGER NOT NULL, 
           max_w_PH_reading INTEGER NOT NULL, 
           num_w_temp_readings INTEGER, 
           max_w_temp_reading INTEGER, 
           last_updated VARCHAR(100) NOT NULL) 
          ''') 

conn.commit() 
conn.close()