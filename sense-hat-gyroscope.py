# !/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com

# Dieses Programm greift auf das Gyroskop des Raspberry Pi
# Sense-HAT zu und zeigt die Lage in Grad an.

import sys, tty, termios, os, time

# Es wird die Python Klasse SenseHat importiert.
from sense_hat import SenseHat

# Hier werden die Variablen der drei Achsen des Gyroskop gesetzt.
# So wird ein eventueller Fehler bei der Ausgabe vermieden 
# falls die Variable leer sein sollten.
x = 0
y = 0
z = 0

# Ein Objekt sense wird von der Klasse SenseHat() erzeugt
# um auf die Sensoren des Sense-HAT zugreifen zu koennen.
sense = SenseHat()

# Es wird der Sensor Gyroskop aktiviert.
sense.set_imu_config(False, True, False) 

try:
   while True:
      # Es werden die Werte der drei x y z Achsen 
      # ausgelesen.
      x, y, z = sense.get_orientation().values()

      # Der Bildschirminhalt wird pro Schleifendurchlauf 
      # geloescht.
      os.system('clear')

      # Die Anzeige wird im Terminal-Fenster ausgegeben.
	  # Die Werte werden auf eine Nachkommastelle genau gerundet.
      print "Orientierung mit dem Gyroskop:"
      print "Kippen x (pitch): ",round(x,1)
      print "Rollen y (roll):  ",round(y,1)
      print "Drehen z (yaw):   ",round(z,1)
      
      # Damit die Schleife geregelt laeuft wird eine sleep 
      # Phase von 0.1 Sekunden eingelegt.
      time.sleep(0.1)
      
# Tippt der Anwender im Terminal-Fenster Strg+C wird das Programm
# beendet und auch wieder der Sensor des Gyroskop freigegeben.
except KeyboardInterrupt:
   sense.set_imu_config(False, False, False)
# Ende des Programmes
