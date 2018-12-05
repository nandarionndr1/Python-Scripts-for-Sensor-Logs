import paho.mqtt.client as paho
broker="localhost"
port=1883
def on_publish(client,userdata,result):
    print("data published \n")
    pass
def publish(topic,data):
    client1= paho.Client("ctrl")                           #create client object
    client1.on_publish = on_publish                          #assign function to callback
    client1.connect(broker,port)                                 #establish connection
    ret= client1.publish(topic,data)
    
