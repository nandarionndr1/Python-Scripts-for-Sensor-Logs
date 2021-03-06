import RPi.GPIO as gpio
import time
import datetime
import sys
import mysql.connector
from pathlib import Path
from sensor_publish import publish

sensors=[]
#false value means unactivated.
sensor1={"name":"Mag Switch S1","sid":1,"pin":2,"value":-1,"av":0}
sensor2={"name":"Mag Switch S2","sid":2,"pin":3,"value":-1,"av":0}
sensor3={"name":"Magswitch S3","sid":3,"pin":4,"value":-1,"av":0}
sensor4={"name":"Collision Sensor","sid":4,"pin":5,"value":-1,"av":1}

sensors.append(sensor1)
sensors.append(sensor2)
sensors.append(sensor3)
sensors.append(sensor4)

mydb = mysql.connector.connect(
        host="localhost",
        user="rootroot",
        passwd="root",
        database="sensorDB"
        )
curs = mydb.cursor()
sql ="INSERT INTO `sensorDB`.`sensor_log` (`log_id`,`sensor_id`, `timestamp`, `value`) VALUES (null, %s, %s, %s);"
def setup_pins(sensors):
    gpio.setmode(gpio.BCM)
    for i in range(0, len(sensors)):
        cur_sensor = sensors[i]
        gpio.setup(cur_sensor["pin"], gpio.IN,pull_up_down=gpio.PUD_UP)
            
def check_status(sensors):
    for i in range(0, len(sensors)):
        av = 0
        ts = time.time()
        st = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cur_sensor = sensors[i]
        val_read = gpio.input(cur_sensor["pin"])
        if val_read is not cur_sensor["value"]:
            if val_read == cur_sensor["av"]:
                av = 1
            val = (str(cur_sensor["sid"]),str(st),str(av))
            log = str(cur_sensor["sid"]) +","+ str(st) +","+  str(av)
            sensors[i]["value"] = val_read
            print(log)
            publish("ccm/rpi_1",log)
#            curs.execute(sql,val)
#            mydb.commit()
#            print(curs.rowcount," inserted done")
        time.sleep(0.1)

try:
    setup_pins(sensors)
    print("pins set up: all set to inactive.")
    while True:
        check_status(sensors)
        
except KeyboardInterrupt:
    print("program complete! ")

#fh.close()
gpio.cleanup()

