import RPi.GPIO as gpio
import time
import datetime

gpio.setmode(gpio.BCM)
gpio.setup(3, gpio.IN)

sensor= "Collision Sensor"
calibration = 10
remarks = ""
value = ""
motion_detected = False

for x in range(0,calibration):
    time.sleep(.1)
    print("calibrating.. ")

print("calibration complete.")

try:
    while True:
        ts = time.time()
        st = str(datetime.datetime.now())
        
        input_value = gpio.input(3)
        if (input_value == True):
            if (motion_detected is False):
                start = time.time()
                print(sensor,',', st,',', remarks,',',value)
            
            motion_detected = True

        else:
            if (motion_detected):
                end = time.time()
                print("motion ended at ", st, "-- ", end - start, "elapsed")
                
            motion_detected = False
            
	

except KeyboardInterrupt:
    print("program complete! ")

gpio.cleanup()

