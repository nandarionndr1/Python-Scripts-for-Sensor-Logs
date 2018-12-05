import RPi.GPIO as gpio
import time
import datetime
import sys
from pathlib import Path
from LIGHT_LBY import read_light
from sensor_publish import publish

sensors=[]
#false value means unactivated.
sensor1={"name":"Mag Switch S1","sid":1,"pin":2,"value":-1,"av":0,"outpin":17}
sensor2={"name":"Mag Switch S2","sid":2,"pin":3,"value":-1,"av":0,"outpin":27}
sensor3={"name":"Light Sensor","sid":3,"pin":4,"value":-1,"av":1,"outpin":22}
sensor4={"name":"Collision Sensor","sid":4,"pin":5,"value":-1,"av":1,"outpin":6}

sensors.append(sensor1)
sensors.append(sensor2)
sensors.append(sensor3)
sensors.append(sensor4)
def light_led(outpin,val):
    if val == 1:
        gpio.output(outpin,gpio.HIGH)
    else:
        gpio.output(outpin,gpio.LOW)
    
def setup_pins(sensors):
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    for i in range(0, len(sensors)):
        cur_sensor = sensors[i]
        gpio.setup(cur_sensor["pin"], gpio.IN,pull_up_down=gpio.PUD_UP)
    gpio.setup(17, gpio.OUT)
    gpio.setup(27, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(6, gpio.OUT)
    
        
            
def check_status(sensors):
    for i in range(0, len(sensors)):
        av = 0
        ts = time.time()
        st = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cur_sensor = sensors[i]
        val_read = gpio.input(cur_sensor["pin"])
        
        if cur_sensor["sid"] == 3:
            val_read = read_light()
                
        if val_read is not cur_sensor["value"]:
            if val_read == cur_sensor["av"]:
                av = 1
            val = (str(cur_sensor["sid"]),str(st),str(av))
            log = str(cur_sensor["sid"]) +","+ str(st) +","+  str(av)
            sensors[i]["value"] = val_read
            print(log)
            publish("ccm/rpi_1",log)
            light_led(cur_sensor["outpin"],av)
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

