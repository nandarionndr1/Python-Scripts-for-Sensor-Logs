import RPi.GPIO as gpio
import time
import datetime
import sys
import mysql.connector
from pathlib import Path

sensors=[]
#false value means unactivated.

sensors.append({"pin":1,"sensor_id":1})
sensors.append({"pin":2,"sensor_id":2})
sensors.append({"pin":3,"sensor_id":3})

mydb = mysql.connector.connect(
        host="localhost",
        user="rootroot",
        passwd="root",
        database="sensorDB"
        )
curs = mydb.cursor()
sql ="INSERT INTO `sensorDB`.`sensor_log` ( `timestamp`,`sensor_id`,`value`) VALUES (%s, %s, %s);"
def setup_pins(sensors):
    gpio.setmode(gpio.BCM)
    for i in range(0, len(sensors)):
        cur_sensor = sensors[i]
        gpio.setup(cur_sensor["pin"], gpio.IN)

def check_status(sensors):
    print(sensors)
    ts = time.time()
    st = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for pn in range(0, len(sensors)):
        pin = sensors[pn]
        print("pin: ",pin["pin"],"|","sensor id:",pin["sensor_id"])
    read_sensor_id = input("what sensor id?: ")
    val_read = input("value read:")
    val = (str(st),str(read_sensor_id),str(val_read))
    curs.execute(sql,val)
    mydb.commit()
try:
    setup_pins(sensors)
    print("pins set up: all set to inactive.")
    while True:
        check_status(sensors)
except KeyboardInterrupt:
    print("program complete! ")

gpio.cleanup()

