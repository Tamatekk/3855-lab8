import mysql.connector

mydb = mysql.connector.connect(
  host="lab63885.westus3.cloudapp.azure.com",
  user="root",
  password="sqlpw",
  database="3885"
)

mycursor = mydb.cursor()

mycursor.execute('''
CREATE TABLE water_pressure_PH
          (id INTEGER PRIMARY KEY AUTO_INCREMENT,
           device_id VARCHAR(250) NOT NULL,
           kPa INTEGER NOT NULL,
           PH INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL); 
           ''')

mycursor.execute('''
CREATE TABLE water_temperature
          (id INTEGER PRIMARY KEY AUTO_INCREMENT, 
           device_id VARCHAR(250) NOT NULL,
           celcius INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL);
''')