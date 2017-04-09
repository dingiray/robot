#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com
# Programm fuer die Einfuehrung in die Programmierung
# mit mehreren Threads. Es werden unterschiedliche Sensoren
# des Raspberry Pi Sense-HAT mit zwei Threads ausgelesen.

import time, smbus, os
from threading import Thread
from sense_hat import SenseHat

# Variablen initialisieren
x = 0
y = 0
z = 0
pressure = 0
temp = 0
humidity = 0

# Stopp Zeit nach der das Programm sich beenden soll.
global time_stopp

# Diese Funktion liest  die x, y, und z Werte des Gyroskops
# des Sense-HAT und uebergibt die gemessenen Werte an die
# gleichnamigen globalen Variablen x, y und z.
def gyroscope():
# Definition der Variablen x, y und z als globale Variablen.
# Dabei stehen die Variablen x, y und z fuer die jeweilige 
# Drehachse des Sense-HAT. 
   global x
   global y
   global z

   sense = SenseHat()
   # Aktivieren des Gyroskop-Sensors des Sense-HAT.
   sense.set_imu_config(False, True, False)

# diese Endlosschleife liest  alle 0,05 Sekunden
# die x, y, und z Werte aus. Da diese Funktion
# als Thread gestartet wird stehen so in den globalen
# Variablen x, y und z immer die neuen Messwerte.
   while time_stopp > time.time():	
      # Hier werden die Werte für x, y und Z ausgelesen. Die
	  # Sense-HAT API stellt die werte in der Liste 
	  # get_orientation() zur Verfügung.
      x = sense.get_orientation()['pitch']
      y = sense.get_orientation()['roll']
      z = sense.get_orientation()['yaw']
      # kurze Pause von 0,05 Sekunden
      time.sleep(0.05)
      # Aufruf der Funktion print_all() die
      # die Anzeige der Werte aktualisiert.
      print_all()

# Auslesen der Umgebungssensoren des Sense-HAT.
def environment():
# Definition der Variablen pressure, temp und humidity
# als global Variablen.
   global pressure
   global temp
   global humidity

   sense = SenseHat()

# diese Endlosschleife liest  alle 0,5 Sekunden
# die pressure, temp und humidity Werte aus. 
# Da diese Funktion als Thread gestartet wird,
# stehen so in den globalen Variablen pressure,
# temp und humidity immer die neuen Messwerte.
   while time_stopp > time.time():	
      humidity = sense.get_humidity()
      temp = sense.get_temperature()
      pressure = sense.get_pressure()
      # kurze Pause von 0,5 Sekunden
      time.sleep(0.5)
      # Aufruf der Funktion print_all() die
      # die Anzeige der Werte aktualisiert.
      print_all()

# Ausgabe der Werte im Terminal-Fenster mit der Funktion 
# print_all() die pro Thread alle 0,05 Sekunden oder 0,5 
# Sekunden aufgerufen wird.
# So ist an der Anzeige deutlich die unterschiedliche 
# Laufzeit der Threads zu erkennen und das diese parallel
# ausgefuehrt werden. 
def print_all():
   global x
   global y
   global z  
   global pressure
   global temp
   global humidity
   global time_stopp
   os.system('clear')
   print "############################################"
   print "############# Thread 1 #####################"
   print "##### Aktualisierung alle 0,5 Sekunden #####"      
   print "############################################"   
   print "--------------------------------------------"
   print("Temperatur:       %s C" % round(temp,2))      
   print("Luftdruck:        %s Millibar" % round(pressure,2))
   print("Luftfeuchtigkeit: %s %%rH" % round(humidity,2))
   print "--------------------------------------------"
   print "############################################"
   print "############# Thread 2 #####################"
   print "##### Aktualisierung alle 0,05 Sekunden ####"   
   print "############################################"
   print "--------------------------------------------"
   print "Kippen (pitch): ",x
   print "Rollen (roll):  ",y
   print "Drehen (yaw):   ",z
   print "--------------------------------------------"
   print "############################################"
   print "########### Verbleibende Laufzeit ##########"   
   print "############################################"
   print "--------------------------------------------"
   print "Programmlaufzeit: ",round(time_stopp - time.time(),1)," s"
   print "--------------------------------------------"

# Abfrage der Programmlaufzeit beim Anwender.
# Die vom Anwender eingegebene Laufzeit begrenzt
# die Lebensdauert der beiden Threads bis diese 
# beendet werden.
laufzeit=input("Programmlaufzeit in Minuten eingeben: ")		
time_stopp = laufzeit*60 + time.time()  
   
# initialisieren der Threads gyroscope und environment. 
# Mit z. B. target=gyroscope wird durch den Thread t_ gyroscope
# die Funktion gyroscope ausgefuehrt.
t_gyroscope = Thread(target=gyroscope)
t_environment = Thread(target=environment)

# Starten der beiden Threads gyroscope und environment. 
# Der Aufruf der Methode start ruft wiederum die 
# Methode run() auf.
t_gyroscope.start()
t_environment.start()

# Mit der Methode join() wartet das Hauptprogramm bis alle beiden
# Threads beendet sind. 
t_gyroscope.join()
t_environment.join()
# Ende des Programmes
