# !/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com

# Dieses Programm greift auf die Sensoren Luftdruck, Temperatur
# und Luftfeuchtigkeit des Raspberry Pi Sense-HAT zu und zeigt
# die Werte auf der LED-Matrix des Raspberry Pi Sense-HAT an.

import sys, tty, termios, os, time

# Es wird die Python Klasse SenseHat importiert.
from sense_hat import SenseHat

# Es wird die Python Klasse led-matrix importiert.
import ledmatrix as matrix

# Ein Objekt sense wird von der Klasse SenseHat() erzeugt
# um auf die Sensoren des Sense-HAT zugreifen zu koennen.
sense = SenseHat()

try:
   while True:
      # Es werden die Werte fuer die Temperatur, Luftdruck 
      # und Luftfeuchtigkeit aus dem Sensor ausgelesen.
      temp = sense.get_temperature()
      pres = sense.get_pressure()
      humi = sense.get_humidity()

      # Die ausgelesenen Werte werden auf eine Stelle nach 
      # dem Komma gerundet.
      temp = round(temp, 1)
      pres = round(pres, 1)
      humi = round(humi, 1)

      # Die LED-Matrix faerbt sich gruen oder rot je nach 
      # dem ob die gemessene Temperatur im definierten  
      # gueltigen Intervall liegt.
      if temp > 20 and temp < 27:
         bg = [0, 100, 0]  # Gruen
      else:
         bg = [100, 0, 0]  # Rot

      # Hier wird der Text in der Variable msg zusammen
      # gesetzt, der auf der LED-Matrix ausgegeben 
      # werden soll.
      msg = "Temp=%s, Press=%s, Humi=%s"%(temp, pres, humi)

      # Es wird in der Form einer Laufschrift die einzelnen
      # gemessenen Werte Temperatur, Luftdruck und
      # Luftfeuchtigkeit der LED-Matrix ausgegeben.
      matrix.display_message(msg,[250,250,50],bg,0.06)
      
# Tippt der Anwender im Terminal-Fenster Strg+c wird das Programm
# beendet und auch wieder der Sensor des Magnetometer freigegeben.
except KeyboardInterrupt:
    sense.set_imu_config(False, False, False)
# Ende des Programmes
