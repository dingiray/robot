# !/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com

# Dieses Programm greift auf das Magnetometer des Raspberry Pi
# Sense-HAT zu und zeigt die Abweichung nach Norden an in Grad.

import sys, tty, termios, os, time

# Es wird die Python Klasse SenseHat importiert.
from sense_hat import SenseHat

# Hier wir die Variable degree initial gesetzt damit ein Fehler
# bei der Ausgabe der Variable vermieden wird wenn diese leer ist.
degree = 0

# Ein Objekt sense wird von der Klasse SenseHat() erzeugt
# um auf die Sensoren des Sense-HAT zugreifen zu koennen.
sense = SenseHat()

# Es wird der Sensor Magnetometer aktiviert.
sense.set_imu_config(True, False, False)  

# Die Endlosschleife liest solange das Magenetometer aus bis der
# Anwender Strg+c im Terminal-Fenster tippt.

try:
   while True:
      # Es wird die Gradzahl Richtung Norden ausgelesen.
      north = sense.get_compass()

      # Die Gradzahl soll als Float Wert angezeigt werden.
      degree = float(north)       
      difference2north = 360 - degree

      # Der Bildschirminhalt wird pro Schleifendurchlauf 
      # geloescht.
      os.system('clear')

      # Die Anzeige wird im Terminal-Fenster ausgegeben.
      print "Orientierung mit dem Kompass:"      
      print("Nordrichtung: %s" % round(degree,1))
      print("Abweichung Nord: %s" % round(difference2north,1))
      # Damit die Schleife geregelt laeuft wird eine sleep 
      # Phase von 0.1 Sekunden eingelegt.
      time.sleep(0.1)

# Tippt der Anwender im Terminal-Fenster Strg+c wird das Programm
# beendet und auch wieder der Sensor des Magnetometer freigegeben.
except KeyboardInterrupt:
   sense.set_imu_config(False, False, False)
# Ende des Programmes
