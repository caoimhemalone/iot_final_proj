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
    global  clock_state, alarm_state, timer_state, temp_state, reply, clock_thread, alarm_thread, timer_thred, temp_thread

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
# show and temp
    temp_state = True
    if not publisher.is_alive():
      publisher = Thread(target=Temp_Method)
      publisher.start()
elif should_publish == "clock":
  # start the clock method thread
    clock_state = True
    if not clock.is_alive():
          clock = Thread(target=Clock_Method)
    clock.start()
elif should_publish == "alarm":
       # start the alarm method thread
    alarm_state = True
    if not alarm.is_alive():
            alarm = Thread(target=Alarm_Method)
    alarm.start()
elif should_publish == "timer":
      # start the timer method thread
    timer_state = True
    if not timer.is_alive():
        timer = Thread(target=Timer_Method)
    timer.start()


elif should_publish =="clock_off":
  clock_state = False;
elif should_publish =="alarm_off":
  alarm_state = False;
elif should_publish =="timer_off":
  timer_state = False;
elif should_publish == "temp_off":
  temp_state = False;

else:
    clock_state = False;
    alarm_state = False;
    timer_state = False;
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

dht_sensor_port = 7
buzzer = 4
button = 3

alarm_state = False;
timer_state = False;
temp_state = False;
thingName = "caoimhesiotfinal"
reply = ""
timeSleep = time.sleep(1)
setRGB(0,255,0)

              #Sensor Code 


#For Clock
def Clock_Method():
  while clock_state:
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

#For temp & hum
def Temp_Method():
  while temp_state:
      # try:
      #     [temp, hum] = dht(dht_sensor_port, 0)
      #     time.sleep(5)
      #     if math.isnan(temp):
      #         temp = 0
      #     result = myAWSIoTMQTTClient.publish("raspberryPI", temp, 1)
      # except (IOError, TypeError) as e:
      #     print "Error", e
      # print "Temp Ending"

try:
        # get the temperature and Humidity from the DHT sensor
    [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
    print("temp =", temp, "C\thumidity =", hum,"%")

    # check if we have nans
    # if so, then raise a type error exception
    if isnan(temp) is True or isnan(hum) is True:
      raise TypeError('nan error')

    t = str(temp)
    h = str(hum)

        # instead of inserting a bunch of whitespace, we can just insert a \n
        # we're ensuring that if we get some strange strings on one line, the 2nd one won't be affected
    setText_norefresh("Temp:" + t + "C\n" + "Humidity :" + h + "%")

  except (IOError, TypeError) as e:
    print(str(e))
    # and since we got a type error
    # then reset the LCD's text
    setText("")

  except KeyboardInterrupt as e:
    print(str(e))
    # since we're exiting the program
    # it's better to leave the LCD with a blank text
    setText("")
    break

  # wait some 




clock_thread = Thread(target=Clock_Method)
alarm_thread = Thread(target=Alarm_Method)
timer_thred = Thread(target=Timer_Method)
temp_thread = Thread(target=Temp_Method)


listener_thread = Thread(target=listener, args=(publisher_thread, temp_thread, clock_thread, alarm_thread, ))
listener_thread.start()

while True:
    time.sleep(1)
