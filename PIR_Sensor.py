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
remarks = ["active","inactive"]

fh = open("wew.txt","a")
fh_read = open("wew.txt","r")
print(fh_read.readline())
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
                value=1
                start = time.time()
                
                log = sensor,',', st,',', remarks[0],',',value
                print(str(log))
                fh.write(str(log))
            
            motion_detected = True

        else:
            if (motion_detected):
                value=0
                end = time.time()
                log = "motion ended at ", st,',',remarks[1],',', value,"-- ", end - start, "elapsed"
                print(log)
                fh.write(str(log))
                
            motion_detected = False
            
	

except KeyboardInterrupt:
    print("program complete! ")
fh.close()
gpio.cleanup()

