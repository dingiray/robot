#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com
# Programm fuer das autonome Fahren des Roboter-Autos

import smbus, time, os, random
import RPi.GPIO as GPIO

# omxplayer Bibliothek importieren
from omxplayer import OMXPlayer

# Threads Bibliothek importieren.
from threading import Thread

# Das Programm L298NHBridge.py wird als Modul geladen.
import L298NHBridge as HBridge

# Sense HAT Bibliothek importieren.
from sense_hat import SenseHat

# Das Programm led_matrix.py wird als Modul geladen. 
import ledmatrix as matrix
   
# Setzen des SMBus Geraetes.
dev = smbus.SMBus(1)

# stopp Bedingung für die While Schleifen der Threads.
global stopp_turn
global time_stopp


# z Variable fuer das Gyroskop.
z = 0         

# GPIO-Ports Ultrasonic Sensor 1 (center)
gpioEcho1 = 23
gpioTrigger1 = 24
	
# GPIO-Ports Ultrasonic Sensor 2 (right)
gpioEcho2 = 23
gpioTrigger2 = 24   
      
 
def calc_distance(gpioEcho, gpioTrigger):
		
	calc_range = 0
		
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(gpioTrigger, GPIO.OUT)
	GPIO.setup(gpioEcho, GPIO.IN)
	GPIO.output(gpioTrigger, True)

	# set the trigger PIN on LOW after 0.01ms to stop the ultrasonic beam
	time.sleep(0.00001)
	GPIO.output(gpioTrigger, False)

	# define the start and time for our time distance measure
	startTime = time.time()
	stopTime = time.time()
 
	# save the start time (echo pin is low) in the local variable StartTime
	while GPIO.input(gpioEcho) == 0:
		startTime = time.time()
 
	# save the receive time of the echo signal (echo pin is high) in the local variable StopTime
	while GPIO.input(gpioEcho) == 1:
		stopTime = time.time()
 
	timeElapsed = stopTime - startTime
	# now we have to multiply the time with the speed of sound of 34300 cm/s
	# and we have to divide the time with 2 because the beam has two directions. 
	# Away from the sensor and back to the sensor
	calc_range = (timeElapsed * 34300) / 2

	return calc_range	


# Drehen um einen bestimmten Gradwert .
def turn_robot(value):
   global z
   global stopp_turn
   global time_stopp
   
   stopp_turn = 0
   turn_delta = 0
   turn = value
   speed = 1
   
   # Spiele mp3-File ab (Dateiname, Pause)
   omxplayer()
   
   sense = SenseHat()
   sense.set_imu_config(False, True, False)

   # So lange stopp = 0 arbeitet dieser Thread in der
   # Endlosschleife.
   while stopp_turn == 0:
      # z Wert aus dem Gyroskop auslesen.
      z = sense.get_orientation()['yaw']
      
      # Hier prueft das Programm in welche Richtung das 
      # Roboter-Auto sich drehen soll. Die Motoren werden 
      # entsprechend der ermittelten Drehrichtung angesteuert
	  # um das Roboter-Auto auszurichten.
      if turn <= 180:
         if turn - z > 0:
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)
         elif turn - z < 0:
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)      
      elif turn > 180:
         if z - turn > 0:
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)         
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)
         elif z - turn < 0:
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)         
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)   

      # Berechnung der aktuellen Abweichung zu der Ziel Grad Zahl.
      turn_delta = turn - z   

      # Wenn die Abweichung zum Ziel lediglich 
      # +-5 Grad betraegt verlangsamen die Motoren .
      if z - 5 < turn < z + 5:
         speed = 0.8      

      # Wenn die Abweichung zum Ziel lediglich 
      # +-2 Grad betraegt stoppen die Motoren .
      if z - 2 < turn < z + 2:
         stopp_turn = 1
         sense.set_imu_config(False, False, False)
         t_control = Thread(target=control)
         t_control.start()
      # Ausgabe der aktuellen Informationen ueber das Roboter-
      # Auto und die aktuelle Drehung.
      os.system('clear')      
      print "########### Drehen ###########"
      print "Aktuelle Gradzahl der Drehung:      %1.f" % z
      print "Verbleibende Gradzahl bis zum Ziel: %1.f" % turn_delta	 

      print "Programm Ende in %1.f" % (time_stopp - time.time()), "sec."
      print "Geschwindigkeit ", speed
      time.sleep(0.02)

      # Die Zeit wird berechnet die das Programm noch
      # aktiv sein darf bis das Roboter-Auto gestoppt wird.
      if time_stopp < time.time():
         # Zeigt auf der LED-Matrix das Programm Ende Symbol an .
         matrix.display_pixels("finish")
         # Motoren stoppen.
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)
         # Die Endlosschleife wird ebenfalls gestoppt.
         stopp_turn = 1

# Abspielen von mp3 oder mp4-Files
def omxplayer():

	# mp4 oder mp3
	file_path_or_url = '/home/pi/Music/r2d2/R2D2-yeah.mp3'
	print file_path_or_url

	# This will start an `omxplayer` process, this might
	# fail the first time you run it, currently in the
	# process of fixing this though.
	player = OMXPlayer(file_path_or_url)

	# The player will initially be paused

	player.play()
	time.sleep(1.5)
	player.pause()

	# Kill the `omxplayer` process gracefully.
	player.quit()
         
# Hauptprogramm fuer die Steuerung.
def control():
   global stopp_control
   global z
   global time_stopp
   
   stopp_control = 0
   turn_degree = 0

   ############################ Start ###########################   
   ##### Hier koennen Sie bei Bedarf die Parameter anpassen #####
 
   # Mindestabstand bis zum Hindernis.
   min_dist = 40
   # Die Geschwindigkeit wird auf 0 gesetzt damit sich das
   # Robter-Auto in einem definierten Zustand befindet.
   speed = 0
   ############################ ENDE ############################
   
   while stopp_control == 0:   
      # startet die Messung für den Sensor 1.
      dist = calc_distance(gpioEcho1, gpioTrigger1)
      
      # startet die Messung für den Sensor 1.
      #dist2 = calc_distance(gpioEcho2, gpioTrigger2)

      if min_dist + 20 <= dist <= min_dist + 35:
         speed = 0.5
      elif min_dist + 15 <= dist <= min_dist + 20:
         speed = 0.4
      elif min_dist <= dist <= min_dist + 15:
         speed = 0.3
      elif 0 <= dist <= min_dist:
         speed = 0
         turn_degree = random.randint(90,270)
         # Stoppen der Motoren.
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)
         # Auruf des Threads der das Roboter-Auto drehen 
         # laest um dem Hindernis auszuweichen.
         t_turn_robot = Thread(target=turn_robot, args=(turn_degree,))
         t_turn_robot.start()
         # Die Endlosschleife wird ebenfalls gestoppt.
         stopp_control = 1
      else:
         # Damit das Auto bei einer Entfernung groesser
         # 35 + min_dist losfaehrt wird diese Abfrage
         # gebraucht die speed von 0 auf 0.8 setzt.
         speed = 0.6
         
      # Die Geschwindigkeit der Motoren wird gesetzt.
      HBridge.setMotorLeft(speed)
      HBridge.setMotorRight(speed)      

      # Auf der LED-Matrix wird der gruene Pfeil nach vorne
      # gezeichnet.
      matrix.display_pixels("arrow")
      matrix.display_rotate(90)   

      # Ausgabe der aktuellen Informationen  wie Abstand, der 
	  # Geschwindigkeit und verbleibenden Programmlaufzeit.
      os.system('clear')
      print "########### Fahren ###########"
      print "Abstand:            %1.f" % dist,"cm"
      print "Geschwindigkeit:  ", speed
      print "Programmlaufzeit: ",round(time_stopp - time.time(),1),"s"
      
      time.sleep(0.04)

      # Die Zeit wird berechnet die das Programm noch
      # aktiv sein darf bis das Roboter-Auto gestoppt wird.
      if time_stopp < time.time():
         # Zeigt das Programm Ende Symbol an auf der LED-Matrix.
         matrix.display_pixels("finish")
         # Motoren stoppen
         HBridge.setMotorLeft(0)
         HBridge.setMotorRight(0)
         # Die Endlosschleife wird ebenfalls gestopped.
         stopp_control = 1

laufzeit=input("Bitte die Zeit in Minuten eingeben die das Roboter-Auto fahren soll: ")      
time_stopp = laufzeit*60 + time.time()

t_control = Thread(target=control)
t_control.start()

# End des Programmes
