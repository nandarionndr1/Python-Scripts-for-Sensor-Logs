import threading
import time
import datetime
import pexpect
import sys

class TransferThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      print ("Starting Transfer")
      scp_transfer()
      print ("Transfer End")
      sys.exit()


def scp_transfer():
    
    print("uploading in progress ... ")
    try:
        child = pexpect.spawn("scp /home/pi/Desktop/PyLab/wew.txt leebet-vm@192.168.0.29:/home/leebet-vm/dir")
        i = child.expect("assword:")

        print(i)
        
        if i==0: # send password                
            child.sendline("root")
            child.expect(pexpect.EOF)
            
            print("file transfer complete.")
            
        elif i==1: 
            print ("Got the key or connection timeout")
            pass

    except Exception as e:
            print ("Oops Something went wrong buddy")
            print (e)

def transfer():
    # Create new threads
    thread_transfer = TransferThread()
    # Start new Threads
    thread_transfer.start()

transfer()
