import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE water_pressure_PH
          (id INTEGER PRIMARY KEY ASC,
           device_id VARCHAR(250) NOT NULL,
           kPa INTEGER NOT NULL,
           PH INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE water_temperature
          (id INTEGER PRIMARY KEY ASC, 
           device_id VARCHAR(250) NOT NULL,
           celcius INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
