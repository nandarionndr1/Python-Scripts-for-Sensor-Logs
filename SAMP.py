import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(3, gpio.IN)

calibration=30

for x in range(0,calibration):
    time.sleep(.75)
    print("calibrating.. ")
print("calibration complete.")

try:
    while True:
        input_value = gpio.input(3)
        if input_value == False:
            print('Motion detected...')
            while input_value == False:
                input_value = gpio.input(3)
except KeyboardInterrupt:
    print("program complete! ")

gpio.cleanup()

