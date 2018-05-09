# Reference https://studio.dexterindustries.com/cwists/preview/432x

import time
from grove_rgb_lcd import *
import grovepi
import datetime
from time import strftime
import sys
import os

 
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

while True:
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

print "Bye"
restart_program()