import RPi.GPIO as gpio
import time
import datetime
import sys
import mysql.connector
from pathlib import Path

sensors=[]
#false value means unactivated.
sensor1={"name":"Mag Switch S1","pin":2,"value":1}
sensor2={"name":"Mag Switch S2","pin":3,"value":1}

sensors.append(sensor1)
sensors.append(sensor2)

mydb = mysql.connector.connect(
        host="localhost",
        user="rootroot",
        passwd="root",
        database="sensorDB"
        )
curs = mysql.cursor()
sql ="INSERT INTO `sensorDB`.`logs` (`sensor_name`, `timestamp`, `value`) VALUES (%s, %s, %s);"
def setup_pins(sensors):
    gpio.setmode(gpio.BCM)
    for i in range(0, len(sensors)):
        cur_sensor = sensors[i]
        gpio.setup(cur_sensor["pin"], gpio.IN)
    
        
def check_status(sensors):
    for i in range(0, len(sensors)):
        ts = time.time()
        st = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cur_sensor = sensors[i]
        val_read = gpio.input(cur_sensor["pin"])
        if val_read is not cur_sensor["value"]:
            val = (str(cur_sensor["name"],str(st),str(val_read))
            #log = str(cur_sensor["name"]) +","+ str(st) +","+  str(val_read)
            sensors[i]["value"] = val_read
            curs.execute(sql,val)
            mydb.commit()
	    print(curs.rowcount," inserted done")
        time.sleep(0.1)


remarks = ["active","inactive"] # list of possible remarks for a collision sensor


try:
    setup_pins(sensors)
    print("pins set up: all set to inactive.")
    while True:
        check_status(sensors)
        
except KeyboardInterrupt:
    print("program complete! ")
    #transfer()


fh.close()
gpio.cleanup()

