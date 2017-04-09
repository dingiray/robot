#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com
# Programm liesst das Magentometer aus und dreht das Roboter-Auto
# in die vom Anwender eingegebene Himmelsrichtung

import time, smbus, os

# Threads Bibliothek importieren
from threading import Thread

# Sense HAT Bibliothek importieren
from sense_hat import SenseHat

# Das Programm L298NHBridge.py wird als Modul geladen.
import L298NHBridge as HBridge

# Es wird die Python Klasse ledmatrix importiert.
import ledmatrix as matrix

# initialisieren des SenseHat
sense = SenseHat()
   
# Variablen initialisieren
z = 0
turn= 0
degree = 0

# Motor Geschwindigkeit
speed = 0.7

# Delta Gradzahl die sich das Roboter Auto noch 
# drehen muss bis der eingegebene Wert erreicht ist
turn_delta = 0

# stopp Bedingung für die While Schleife
stopp = 0

# Auslesen der Position aus Magnetometer und Gyroskop
# des Raspberry Pi Sense-HAT 
def readposition(value):
   # Variablen als global definieren
   global degree
   degree_delta = 0
   global x
   global y
   global z
   global stopp
   pol = value

   # Maximal werden 60 Sekunden lang bzw. 60 mal der Wert
   # des Magnetometer ausgelesen um die genaue
   # Position zu erhalten.   
   for i in range(60):
      # Aktivieren des Magnetometers
      sense.set_imu_config(True, False, False)  
      # Es wird die Gradzahl Richtung Norden ausgelesen
      north = sense.get_compass()
      degree = float(north)
      
      os.system('clear')
      print "-----------------------------------------------"
      print "Aktueller Kompass Wert in Grad zu Nord: ",degree      
      print "Kompass Kalibrierung in ", 60 - i, "s beendet."
      print "-----------------------------------------------"
      
      # 10 Sekunden lang den Wert des Magnetometers ermitteln.
      # Wenn die Abweichung nach 10 Sekunden kleiner als 1 
      # ist gilt die Messung als gueltig.
      if i > 10 and degree_delta - degree < 1:
         os.system('clear')
         print "-------------------------------------------"
         print "Aktueller Kompass Wert in Grad:     ",degree      
         print "Kalibrierung erfolgreich und beendet."
         print "-------------------------------------------"      
         time.sleep(1)
         
         # Initialisieren des Threads turn_robot um das 
         # Roboter Auto zu drehen.
         t_turn_robot = Thread(target=turn_robot, args=(pol,))         
         # Starten des Threads turn_robot um das Roboter 
         # Auto in die vorgegebene Himmelsrichtung zu drehen.
         t_turn_robot.start()
         break
      else:
         degree_delta = degree

      time.sleep(1)
      
# Drehen um einen bestimmten Gradwert 
def turn_robot(value):
   global z
   global stopp
   global degree
   global turn
   global turn_delta
   global speed

   # Himmelsrichtung aus der Eingabe des Anwenders
   pol = value
   # initiale Drehgeschwindigkeit
   speed = 0.7
   
   # Festlegen der Gradzahl auf die sich das
   # Roboter Auto drehen muss um in die eingegebene
   # Himmelsrichtung zu zeigen.
   if pol == "N":
      turn = 0
   elif pol == "E":
      turn = 90
   elif pol == "S":
      turn = 180
   elif pol == "W":
      turn = 270
         
   # So lange stopp = 0 arbeitet dieser Thread in der
   # Endlosschleife
   while stopp == 0:
      # Gyroskop Sensor auswaehlen
      sense.set_imu_config(False, True, False)      
      # Get the z axis from the array
      z = sense.get_orientation()['yaw']      
   
      # Wenn das Auto nach rechts gedreht wird 
      # startet z bei 0 und zählt bis 360 hoch
      # Wenn das Auto nach links gedreht wird 
      # startet z bei 360 und zählt bis 0 herunter

      # Prüfen in welcher Richtung das Auto drehen soll
      # um am schnellsten den eingegebenen Wert zu erreichen.
      # direction uebergibt den Wert fuer das Symbol fuer die
      # LED Anzeige
      if turn == 0:
         if z > 345:
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)
         elif z <= 345:
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)   
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)
      elif turn <= 180:
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

      # Berechnung der aktuellen Abweichung
      turn_delta = turn - z   

      # Wenn die Abweichung zum Ziel lediglich 
      # +-8 Grad betraegt verlangsamen die Motoren 
      if z - 15 < turn < z + 15:
         speed = 0.5         

      # Wenn die Abweichung zum Ziel lediglich 
      # +-2 Grad betraegt stoppen die Motoren 
      if z - 0.5 < turn < z + 0.5:
         matrix.display_pixels("finish")      
         stopp = 1

      print_all(pol)
      
# Ausgabe der Messwerte auf der Konsole die pro
# Thread ermittelt werden. 
def print_all(value):
   global z 
   global turn   
   global turn_delta
   global speed
   global degree
   pol = value
   
   os.system('clear')

   print "############################################"
   print "############ Magnetometer ##################"
   print "##### Aktualisierung alle 0,04 Sekunden ####"   
   print "############################################"
   print "--------------------------------------------"
   print "Eingegebene Himmelsrichtung: ",pol
   print "Grad Zahl Drehen (yaw):      ",round(z,1)
   print "Start Kompass Wert in Grad:  ",round(degree,1)
   print "Abweichung in Grad:          ",round(turn_delta,1)
   print "Aktuelle Geschwindigkeit:    ",speed
   print "--------------------------------------------"
      
# Einlesen der Himmelsrichtung die der Anwender eingibt
pol=raw_input("Bitte die Himmelsrichtung N, E, S oder W eingeben: ")   

# Pruefen ob die eingegebene Grad Zahl Sinn macht. 
if pol=="N" or pol=="E" or pol=="S" or pol=="W":
   # initialisieren der Threads readposition mit Uebergabe
   # der Himmelsrichtung die der Anwender eingegeben hat.   
   t_readposition = Thread(target=readposition, args=(pol,))
   # starten des threads
   t_readposition.start()
else: 
   # Fehlerbehandlung falls nicht N, E, S und W eingeben wird
   print "-----------------------------------------------------"
   print "Bitte nur die Himmelsrichtung N, E, S und W eingeben:"
   print "-----------------------------------------------------"   
# Ende des Programmes