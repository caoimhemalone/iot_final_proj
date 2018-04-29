import dweepy, time, random, math, 
# picamera
import json
from grovepi import *
from time import sleep, gmtime, strftime

from threading import Thread

'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt

# Custom MQTT message callback
def customCallback(client, userdata, message):
    global  led1_state, led2_state, led3_state, cam_state, temp_state, reply, led1_thread, led2_thread, led3_thred, cam_thread, temp_thread

    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    reply = message.payload
    message = json.loads(reply)
    should_publish = message.get("publish", "")
    sleep_time = message.get("time", "")
    if sleep_time < 0:
        sleep_time = 2        
    print should_publish
if should_publish == "true":
# show hum and temp
    temp_state = True
    if not publisher.is_alive():
      publisher = Thread(target=Temp_Method)
      publisher.start()
elif should_publish == "led1":
  # start the blue method thread
    led1_state = True
    if not led1.is_alive():
          led1 = Thread(target=Blue_Method)
    led1.start()
elif should_publish == "led2":
       # start the green method thread
    led2_state = True
    if not led2.is_alive():
            led2 = Thread(target=Green_Method)
    led2.start()
elif should_publish == "led3":
      # start the red method thread
    led3_state = True
    if not led3.is_alive():
        led3 = Thread(target=Red_Method)
    led3.start()
elif should_publish == "cam":
  # start the camera thread
  # cam_state = True
  # if not cam.is_alive():
  #   cam = Thread(target=Camera_Method)
  # cam.start()
elif should_publish == "temp":
  # start the temp method thread
  temp_state = True
  if not temp.is_alive():
    temp = Thread(target=Temp_Method)
  temp.start()

elif should_publish =="led1_off":
  led1_state = False;
elif should_publish =="led2_off":
  led2_state = False;
elif should_publish =="led3_off":
  led3_state = False;
# elif should_publish =="cam_off":
#   cam_state == False;
elif should_publish == "temp_off":
  temp_state = False;

else:
    led1_state = False;
    led2_state = False;
    led3_state = False;
    # cam_state = False;
    temp_state = False;

    print "Wasn't true"




# Usage
usageInfo = """Usage:

Use certificate based mutual authentication:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>

Use MQTT over WebSocket:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -w

Type "python basicPubSub.py -h" for available options.
"""
# Help info
helpInfo = """-e, --endpoint
    Your AWS IoT custom endpoint
-r, --rootCA
    Root CA file path
-c, --cert
    Certificate file path
-k, --key
    Private key file path
-w, --websocket
    Use MQTT over WebSocket
-h, --help
    Help information


"""

# Read in command-line parameters
useWebsocket = False
host = "a17y717e4a92so.iot.us-east-1.amazonaws.com"
rootCAPath = "root.pem"
certificatePath = "cert.pem.crt"
privateKeyPath = "private.pem.key"

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("iot-final", 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0

sleep_time = 1

led1sensor = 2

dht_sensor_port = 8
buzzer = 4
button = 3

alarm_state = False;
timer_state = False;
temp_state = False;
thingName = "caoimhesiotfinal"
reply = ""
timeSleep = time.sleep(1)


              #Sensor Code 


#For Blue LED
def Blue_Method():
  while led1_state:
      try:
          digitalWrite(buzzer, 1)
          time.sleep(.5)
          digitalWrite(buzzer, 0)
          digitalWrite(led1sensor, 1)
          time.sleep(1)
          result = myAWSIoTMQTTClient.publish('raspberryPI', "Blue LED On", 1, "Temperature" , +temp)
          print result
            

          digitalWrite(led1sensor, 0)
          digitalWrite(buzzer, 0)
          result = myAWSIoTMQTTClient.publish('raspberryPI', "Blue LED Off" , 0)
          print result
            

      except KeyboardInterrupt:
              digitalWrite(led1sensor,0)
              digitalWrite(buzzer, 0)
              break

      except (IOError, TypeError) as e:
          print "Error", e
          
      print "Blue LED ending"

#For timer
      # buzzer on countdown, button to turn it off

#For alarm
# buzzer on countdown, button to turn it off

#For temp
def Temp_Method():
  while temp_state:
      try:
          [temp, hum] = dht(dht_sensor_port, 0)
          time.sleep(5)
          if math.isnan(temp):
              temp = 0
          result = myAWSIoTMQTTClient.publish("raspberryPI", temp, 1)
      except (IOError, TypeError) as e:
          print "Error", e
      print "Temp Ending"





led1_thread = Thread(target=Blue_Method)
led2_thread = Thread(target=Green_Method)
led3_thred = Thread(target=Red_Method)
cam_thread = Thread(target=Camera_Method)
temp_thread = Thread(target=Temp_Method)


listener_thread = Thread(target=listener, args=(publisher_thread, temp_thread, hum_thread, led_thread, buzz_thread, every_thread, led_and_buzz_thread,))
listener_thread.start()

while True:
    time.sleep(1)
