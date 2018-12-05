import serial
serport=serial.Serial('/dev/ttyACM1')
def read_light():
        data=serport.readline()
        light_yagami=str(data)[2:5]
        if int(light_yagami) > 750:
                return 1
        return 0
