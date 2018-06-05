import RPi.GPIO as gpio
import time
import datetime
import sys
#import scp_transfer_module
from pathlib import Path

sensors=[]
#false value means unactivated.
sensor1={"name":"Mag Switch S1","pin":2,"value":1}
sensor2={"name":"Mag Switch S2","pin":3,"value":1}

sensors.append(sensor1)
sensors.append(sensor2)


def setup_pins(sensors):
    gpio.setmode(gpio.BCM)
    for i in range(0, len(sensors)):
        cur_sensor = sensors[i]
        gpio.setup(cur_sensor["pin"], gpio.IN)
        
def check_status(sensors):
    for i in range(0, len(sensors)):
        ts = time.time()
        st = str(datetime.datetime.now())
        
        cur_sensor = sensors[i]
        val_read = gpio.input(cur_sensor["pin"])
        if val_read is not cur_sensor["value"]:
            print("current value: ",cur_sensor["value"])
            print ("value read: ", val_read)
            
            log = str(cur_sensor["name"]) +","+ str(st) +","+  str(val_read)
            sensors[i]["value"] = val_read
            print(log)
            fh.write(log+"\n")


remarks = ["active","inactive"] # list of possible remarks for a collision sensor


my_file = Path("wew.text")

if my_file.is_file():
    fh = open("wew.txt","a")
else:
    fh = open("wew.txt","w")
    
try:
    setup_pins(sensors)
    print("pins set up: all set to inactive.")
    while True:
        
        check_status(sensors)
        
except KeyboardInterrupt:
    print("program complete! ")



fh.close()
gpio.cleanup()

