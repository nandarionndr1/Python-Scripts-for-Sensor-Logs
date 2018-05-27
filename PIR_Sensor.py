import RPi.GPIO as gpio
import time
import datetime
import pexpect
import sys

gpio.setmode(gpio.BCM)
gpio.setup(3, gpio.IN)

sensor= "Collision Sensor"
calibration = 5
remarks = ""
value = ""
motion_detected = False
remarks = ["active","inactive"]

fh = open("wew.txt","a")
for x in range(0,calibration):
    time.sleep(.1)
    print("calibrating.. ")

print("calibration complete.")

def scp_transfer():
    
    print("uploading in progress ... ")
    try:
        child = pexpect.spawn("scp /home/pi/Desktop/PyLab/wew.txt server-PC@192.168.0.1:/Users/Leebet-PC/Desktop/dir")
        i = child.expect("assword:")

        print(i)
        
        if i==0: # send password                
            child.sendline("password")
            child.expect(pexpect.EOF)
            
            print("file transfer complete.")
            
        elif i==1: 
            print ("Got the key or connection timeout")
            pass

    except Exception as e:
            print ("Oops Something went wrong buddy")
            print (e)
        
try:
    while True:
        ts = time.time()
        st = str(datetime.datetime.now())
        
        input_value = gpio.input(3)
        if (input_value == True):
            if (motion_detected is False):
                value=1
                start = time.time()
                log = sensor+','+str(st)+','+ remarks[0]+','+str(value)
                print(str(log))
                fh.write(log+"\n")
            motion_detected = True
        else:
            if (motion_detected):
                value=0
                end = time.time()
                log = sensor +"," +str(st) +","+remarks[1] + ","+ str(value) + "--elapsed: "+str( end - start )
                print(log)
                fh.write(log+"\n")
                
            motion_detected = False
        
except KeyboardInterrupt:
    print("program complete! ")

scp_transfer()    
fh.close()
gpio.cleanup()

