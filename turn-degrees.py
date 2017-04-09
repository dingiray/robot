#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com
# Das Programm dreht das Roboter-Auto um einen vom Anwender 
# eingegeben Winkel.

import time, smbus, os

# Threads Bibliothek importieren
from threading import Thread

# Sense HAT Bibliothek importieren
from sense_hat import SenseHat

# Das Programm L298NHBridge.py wird als Modul geladen.
import L298NHBridge as HBridge

# Es wird die Python Klasse ledmatrix importiert.
import ledmatrix as matrix

# Variablen initialisieren fuer das Gyroskop
z = 0
turn= 0

# Motor Grund-Geschwindigkeit
speed = 0.7

# Delta Gradzahl die sich das Roboter Auto noch 
# drehen muss bis der eingegebene Wert erreicht ist
turn_delta = 0

# stopp Bedingung für die While Schleifen der Threads
stopp = 0

# Auslesen des Gyroskopes des Sense HAT 
def gyroscope():
# Variablen als global definieren
   global z
   global stopp

   # initialisieren des SenseHat
   sense = SenseHat()
   sense.set_imu_config(False, True, False)

   # So lange stopp = 0 arbeitet dieser Thread in der
   # Endlosschleife
   while stopp == 0:   
      # Hier wird die z Achse ausgelesen
      z = sense.get_orientation()['yaw']
      time.sleep(0.03)

      
# Drehen um einen bestimmten Gradwert 
def turn_robot(value):
   global z
   global stopp
   global turn
   global turn_delta
   global speed

   # uebergebener Wert aus der Eingabe des Anwenders
   turn = value
   # initiale Drehgeschwindigkeit
   speed = 0.7
   
   # So lange stopp = 0 arbeitet dieser Thread in der
   # Endlosschleife
   while stopp == 0:
      # Wenn das Auto nach rechts gedreht wird 
      # startet z bei 0 und zählt bis 360 hoch
      # Wenn das Auto nach links gedreht wird 
      # startet z bei 360 und zählt bis 0 herunter

      # Prüfen in welcher Richtung das Auto drehen soll
      # um am schnellsten den eingegebenen Wert zu erreichen
      if turn <= 180:
         if turn - z > 0:
            # Anzeige des gruenen Pfeils 
            # um 180° gedreht
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)
            # Ist speed postiv drehen sich die Motoren vorwaerts.
            # Ist speed negativ drehen sich die Motoren rueckwaerts.
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)
         elif turn - z < 0:
            # Anzeige des gruenen Pfeils 
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)      
      elif turn > 180:
         if z - turn > 0:
            # Anzeige des gruenen Pfeils 
            matrix.display_pixels("arrow")
            matrix.display_rotate(0)         
            HBridge.setMotorLeft(-speed)
            HBridge.setMotorRight(speed)
         elif z - turn < 0:
            # Anzeige des gruenen Pfeils 
            # um 180° gedreht
            matrix.display_pixels("arrow")
            matrix.display_rotate(180)         
            HBridge.setMotorLeft(speed)
            HBridge.setMotorRight(-speed)         
      # Berechnung der aktuellen Abweichung.
      turn_delta = turn - z   

      # Wenn die Abweichung zum Ziel lediglich 
      # +-15 Grad betraegt verlangsamen die Motoren.
      if z - 15 < turn < z + 15:
         speed = 0.5         

      # Wenn die Abweichung zum Ziel lediglich +-2 Grad betraegt
      # stoppen die Motoren und das Programm wird beendet.
      if z - 2 < turn < z + 2:
         # Anzeige des roten Stopp Symbols
         matrix.display_pixels("finish")
         stopp = 1
         
      print_all()
      time.sleep(0.04)
      
# Ausgabe der Messwerte auf der Konsole die pro
# Thread ermittelt werden. 
def print_all():
   global z 
   global turn   
   global turn_delta
   global speed
   os.system('clear')

   print "############################################"
   print "############ Thread drehen #################"
   print "##### Aktualisierung alle 0,05 Sekunden ####"   
   print "############################################"
   print "--------------------------------------------"
   print "Aktuelle Gradzahl (z):    ",round(z,1)
   print "Eingegebene Gradzahl:    ",turn
   print "Aktuelle Gradzahl:       ",round(turn_delta,1)
   print "Aktuelle Geschwindigkeit: ",speed
   print "--------------------------------------------"

# Einlesen der Gradzahl die der Anwender eingibt
gradzahl=input("Grad Zahl fuer die Drehung des Roboter-Autos: ")   

# Pruefen ob die eingegebene Grad Zahl Sinn macht. 
if gradzahl <= 0 or gradzahl >= 360:
   print "--------------------------------------------"
   print "Bitte eine Gradzahl zwischen >0 und <360 eingeben."
   print "--------------------------------------------"   
else: 
   # initialisieren der Threads gyroscope und compass.   
   t_gyroscope = Thread(target=gyroscope)
   t_turn_robot = Thread(target=turn_robot, args=(gradzahl,))
   # Starten der Threads gyroscope und compass.
   t_gyroscope.start()
   t_turn_robot.start()

   t_gyroscope.join()
   t_turn_robot.join()
# Ende des Programmes
