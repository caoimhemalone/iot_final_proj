import dweepy, time, random, math, 
# picamera
import json
from grovepi import *
from time import sleep, gmtime, strftime
from grove_rgb_lcd import *
import grovepi
import datetime
import sys
import os

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
    global  clock_state,  temp_state, reply, clock_thread,  temp_thread

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




elif should_publish =="clock_off":
  clock_state = False;
elif should_publish == "temp_off":
  temp_state = False;

else:
    clock_state = False;
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

sensor = 1
button = 3
buzzer = 2
dht_sensor = 4
led = 6
grovepi.pinMode(sensor,"INPUT")
grovepi.pinMode(button,"INPUT")
grovepi.pinMode(buzzer,"OUTPUT")
grovepi.pinMode(led,"OUTPUT")

filesalarm = open('/home/pi/Desktop/iot-final/python_files/alarms.txt','r')
onoffalarm = open('/home/pi/Desktop/iot-final/python_files/onoff.txt','r')
settingalarm = str(filesalarm.readline())
settingonoff = str(onoffalarm.readline())
filesalarm.close()
onoffalarm.close()

grovepi.digitalWrite(buzzer,0)


print settingalarm
print settingonoff

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

last_sound = 0

alarm_state = False;
clock_state = False;
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
    [temp,humidity] = grovepi.dht(dht_sensor,0)
    temp = str(temp)
    humidity = str(humidity)
    date = strftime("%d-%m-%Y")
    hourmintime = strftime("%H:%M")
    if settingonoff == "1":
      grovepi.analogWrite(led,1)
    else:
      grovepi.analogWrite(led,0)
        setRGB(0,0,255)
        setText(str(date + " " + temp + "C\n" + settingonoff + "  *" + hourmintime + "* " + humidity + "%"))
        print date + hourmintime
        if hourmintime == settingalarm and settingonoff == "1":
      alarmrange = range(0,5)
          for count in alarmrange:
        grovepi.digitalWrite(buzzer,0)
        setRGB(200,5,5)
        setText(" W A K E   U P \n   IT'S  " + settingalarm)
        #Alarm goes off unless button held
        grovepi.digitalWrite(buzzer,1)
        time.sleep(.1)
        setRGB(0,5,5)
        grovepi.digitalWrite(buzzer,0)
        time.sleep(.1)
        setRGB(200,5,5)
        grovepi.digitalWrite(buzzer,1)
        time.sleep(.3)
        setRGB(0,5,5)
        grovepi.digitalWrite(buzzer,0)
        #If the button is pressed snooze starts 60 seconds later
        if grovepi.digitalRead(button):
          hourmintime = strftime("%H:%M")
          setRGB(0,0,255)
                      setText(str(date + " " + temp + "C\n" + settingonoff + "  *" + hourmintime + "* " + humidity + "%"))
                                  time.sleep(60) # snooze time
          snoozerange = range(0,3)
          for count in snoozerange:
            alarmrange = range(0,10)
            for count in alarmrange:
                                      setRGB(200,5,5)
                                      setText("  ARE YOU STILL\n   IN BED?")
                                      grovepi.digitalWrite(buzzer,1)
              time.sleep(.1)
              setRGB(0,5,5)
              grovepi.digitalWrite(buzzer,0)
                                                        time.sleep(.1)
              setRGB(200,5,5)
              grovepi.digitalWrite(buzzer,1)
              time.sleep(.2)
              setRGB(0,5,5)
              grovepi.digitalWrite(buzzer,0)
              if grovepi.digitalRead(button):
                restart_program()
                                      time.sleep(.5)
          restart_program()           
        grovepi.digitalWrite(buzzer,0)
        time.sleep(.5)
        time.sleep(5)
        if grovepi.digitalRead(button):
      time.sleep(1)
      break

        except (IOError,TypeError) as e:
              print "Error"
    restart_program()
        
#while True:
menu = range(0,10)
for count in menu:
  try:
    sensor_value = grovepi.analogRead(sensor)
    setRGB(20,20,255)
    setText(" < OFF     ON > ")
    time.sleep(0.5)
    onoff = str(int(sensor_value / 512))
    if onoff == "0" and grovepi.digitalRead(button):
      setText("ALERT OFF")
      onoffalarm = open('/home/pi/Desktop/iot-final/python_files/onoff.txt','w')
      onoffalarm.write("0")
      onoffalarm.close()
      time.sleep(1)
                        restart_program()
      
    if onoff == "1" and grovepi.digitalRead(button):
                        setText("ALERT ON")
      onoffalarm = open('/home/pi/Desktop/iot-final/python_files/onoff.txt','w')
                        onoffalarm.write("1")
                        onoffalarm.close()
      time.sleep(1)
      while True:
        try:
          sensor_value = grovepi.analogRead(sensor) 
          setRGB(200,20,255)
          setText(" < SET TIME\n ALREADY DONE > ")
          time.sleep(.5)
          onoff = str(int(sensor_value / 512))
          if onoff == "0" and grovepi.digitalRead(button):
            setRGB(200,20,255)
            setText("    SET HOUR")
            time.sleep(1)
            while True:
                  try:
                if grovepi.digitalRead(button):
                  time.sleep(1)
                  sethour = str(" HOUR SET:\n      " + whour)
                  setRGB(0,255,255)
                  setText(sethour)
                  time.sleep(1)
                  setRGB(200,20,255)
                  setText("   SET MINUTE")
                  time.sleep(1)
                  while True:
                    try:
  
                      if grovepi.digitalRead(button):
                        time.sleep(1)
                        alarm = str("  WAKE UP AT\n    " + whour + ":" + wmin)
                        print alarm
                        setRGB(0,255,255)
                        setText(" MINUTE SET:\n    " + wmin)
                        time.sleep(1)
                        setText(alarm)
                        time.sleep(1)
                        filesalarm = open('/home/pi/Desktop/iot-final/python_files/alarms.txt','w')
                        filesalarm.write(whour + ":" + wmin)
                        filesalarm.close()
                        time.sleep(1)
                        restart_program()
                      sensor_value = grovepi.analogRead(sensor)
                      setRGB(255,0,255)
                      minutes = int(sensor_value / 17.1)
                      wmin = str("%02d"%minutes)
                      setText(wmin)
                      time.sleep(.1)
                    except IOError:
                      print "Error"
                sensor_value = grovepi.analogRead(sensor)
                setRGB(0,0,255)
                ora = int(sensor_value / 44.478)
                whour = str("%02d"%ora)
                setText(whour) 
                time.sleep(.3)

                  except IOError:
                      print "Error"

          if onoff >= "1" and grovepi.digitalRead(button):
            setRGB(100,20,255)
            setText("    WAKE UP AT:\n    " + settingalarm)
            time.sleep(2)
            restart_program()
        except IOError:
                      print "Error"
    time.sleep(1)   
  except (IOError,TypeError) as e:
                print "Error"
                restart_program()

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
temp_thread = Thread(target=Temp_Method)


listener_thread = Thread(target=listener, args=(publisher_thread, temp_thread, clock_thread, ))
listener_thread.start()

while True:
    time.sleep(1)
