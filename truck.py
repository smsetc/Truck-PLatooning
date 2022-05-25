import paho.mqtt.client as mqtt
import datetime
import time
import flask
from flask import jsonify
from flask_cors import CORS
import json
import threading
import sys
import os
import random

if len(sys.argv)>1:
    truck_id = sys.argv[1]
else:
    truck_id=str(random.randint(5,5000))

print("Truck ID:",truck_id)
trucks = []
speed = 0
accel = 0 code: "+str(rc))
    if rc==0:
        print("Connected Successfully")
    else:
        return
    global truck_id
    client.subscribe("register")
    client.subscribe("unregister")
    client.subscribe(truck_id+"/set/#")
    client.subscribe(truck_id+"/feedback")
    
brakes = True

def on_connect(client, userdata, flags, rc):
    print("Result 

def on_message(client, userdata, msg):
    #print("Message "+str(msg.payload)+" Received at topic "+msg.topic)
    data=msg.payload.decode("utf-8")

    global trucks
    global truck_id
    global speed
    global accel
    global brakes

    if "register" == msg.topic:
        new_truck_id = data
        if new_truck_id not in trucks:
            trucks.append(new_truck_id)
            trucks.sort()
    elif "unregister" == msg.topic:
        print("Unregistering ",data)
        rem_truck_id = data
        if rem_truck_id == truck_id:
            print("Exiting this truck")
            os._exit(1)
        time.sleep(2)
        trucks.remove(rem_truck_id)
    elif truck_id+"/set/speed" in msg.topic:
        accel = 0
        speed = data
        if float(speed) > 0:
            brakes = False
        else:
            brakes = True
            
        next_truck_index=trucks.index(truck_id)+1
        prev_truck_index=trucks.index(truck_id)-1
        if prev_truck_index>=0:
            client.publish(trucks[prev_truck_index]+'/feedback',truck_id)
        if next_truck_index!=len(trucks):
            client.publish(trucks[next_truck_index]+'/set/speed',str(speed))
    elif truck_id+"/set/accel" in msg.topic:
        accel = data
        brakes=False
        next_truck_index=trucks.index(truck_id)+1
        prev_truck_index=trucks.index(truck_id)-1
        if prev_truck_index>=0:
            client.publish(trucks[prev_truck_index]+'/feedback',truck_id)
        if next_truck_index!=len(trucks):
            client.publish(trucks[next_truck_index]+'/set/accel',str(accel))
    elif truck_id+"/set/brakes" in msg.topic:
        speed = 0
        accel = 0
        brakes = True
        if "True" in data:
            brakes = True
        else:
            brakes=False
        next_truck_index=trucks.index(truck_id)+1
        prev_truck_index=trucks.index(truck_id)-1
        if prev_truck_index>=0:
            client.publish(trucks[prev_truck_index]+'/feedback',truck_id)
        if next_truck_index!=len(trucks):
            if brakes:
                client.publish(trucks[next_truck_index]+'/set/brakes',"True")
            else:
                client.publish(trucks[next_truck_index]+'/set/brakes',"False")
    elif truck_id+"/feedback" in msg.topic:
        next_truck_index=trucks.index(truck_id)+1
        print("feedback received from truck",data)

def logs():
    global speed
    global accel
    global brakes
    while True:
        client.publish("register",truck_id)
        print("Trucks:",trucks,"\n")
        speed=float(speed)+(float(accel)*0.01667)
        print("Speed:",str(speed),", Acceleration:",str(accel),", Brakes:",str(brakes))
        time.sleep(1)

app = flask.Flask(__name__)
CORS(app)
@app.route('/')
def index():
    global speed
    global accel
    global brakes
    data={
        "speed":speed,
        "accel":accel,
        "brakes":brakes
        }
    return jsonify(data)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.connect("host.docker.internal", 1883, 60)
client.connect("localhost", 1883, 60)
client.loop_start()
thread = threading.Thread(target=logs)
thread.start()

app.run(host='0.0.0.0',port=5000)
