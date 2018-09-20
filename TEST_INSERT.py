import time
import datetime
import sys
import mysql.connector
from pathlib import Path


mydb = mysql.connector.connect(
        host="localhost",
        user="rootroot",
        passwd="root",
        database="sensorDB"
        )
curs = mydb.cursor()
sql ="INSERT INTO `sensorDB`.`logs` (`sensor_name`, `timestamp`, `value`) VALUES (%s, %s, %s);"

prompt = input("Value: ")
st = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
val = ("hello",str(st),str(prompt))

curs.execute(sql,val)
mydb.commit()
print(curs.rowcount," inserted done")


