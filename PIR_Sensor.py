import RPi.GPIO as gpio
import time
import datetime

gpio.setmode(gpio.BCM)
gpio.setup(3, gpio.IN)

calibration=15
lockLow = True
takeLowTime = False
inBetween = False



for x in range(0,calibration):
    time.sleep(.1)
    print("calibrating.. ")

print("calibration complete.")

try:
    while True:
        input_value = gpio.input(3)
        if (input_value == True):
            ts = time.time()
            st = str(datetime.datetime.utcnow())
            print('Motion detected at .. ', st)
	

except KeyboardInterrupt:
    print("program complete! ")

gpio.cleanup()

