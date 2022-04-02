import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sqlpw",
  database="api"
)

mycursor = mydb.cursor()

mycursor.execute('''drop table water_pressure_PH''')
mycursor.execute('''drop table water_temperature''')
