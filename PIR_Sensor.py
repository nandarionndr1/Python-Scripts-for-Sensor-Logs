import RPi.GPIO as gpio
import time
import datetime
import sys
import scp_transfer_module
from pathlib import Path


gpio.setmode(gpio.BCM)
gpio.setup(3, gpio.IN)

sensor= "Collision Sensor" 
calibration = 5 #calibration time on sensor
remarks = "" #remarks on data
motion_detected = False # to record only when there are changes in motion in the sensor
remarks = ["active","inactive"] # list of possible remarks for a collision sensor

for x in range(0,calibration):
    time.sleep(.1)
    print("calibrating.. ")

print("calibration complete.")

my_file = Path("wew.text")

if my_file.is_file():
    fh = open("wew.txt","a")
else:
    fh = open("wew.txt","w")
    
try:
    while True:
        ts = time.time()
        st = str(datetime.datetime.now())
        
        input_value = gpio.input(3)
        if (input_value == True):
            if (motion_detected is False):
                
                value=1
                start = time.time()
                log = sensor+','+str(st)+','+ remarks[0]
                print(str(log))
                fh.write(log+"\n")
                #starts a thread everytime there is change to reflect change in network.
                try:
                    scp_transfer_module.transfer()
                except:
                    print ("error in thread start.")
                    
            motion_detected = True
        else:
            if (motion_detected):
                value=0
                end = time.time()
                log = sensor +"," +str(st) +","+remarks[1]
                print(log)
                fh.write(log+"\n")
                try:
                    scp_transfer_module.transfer()
                except:
                    print ("error in thread start.")
                
            motion_detected = False
        
except KeyboardInterrupt:
    print("program complete! ")

scp_transfer_module.scp_transfer()    
fh.close()
gpio.cleanup()

