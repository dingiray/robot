#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com
# Dieses Programm ist das Steuerprogramm fuer das 
# Roboter-Auto ueber ein Web-Interface. So ist die Steuerung mit 
# jedem Web-Browser moeglich.

import sys
# Mit diesem Aufruf sucht Python im angegebenen Ordner nach 
# weiteren Modulen die importiert werden koennen.
sys.path.append("/home/pi/robot")

# Das Programm L298NHBridge.py wird als Modul geladen. Es stellt
# die Funktionen fuer die Steuerung der H-Bruecke zur Verfuegung.
import L298NHBridge as HBridge

# WebIOPI wird importiert damit die Funktionen der Web-Steuerung
# von WebIOPI verwendet werden koennen.
import webiopi

# Die Variable "step" legt die Schrittweite der Beschleunigung 
# fest. Mit jedem Aufruf ueber die Web-Steuerung wird die 
# Geschwindigkeit im Wert der Variable step veraendert 
step = 0

# Initialisieren der Variablen und Definition dieser als global so dass
# sie allen anderen Programmteilen zur Verfügung stehen.
def initiate():
   global speedleft
   global speedright
   global step

   # Variablen Definition der Geschwindigkeit der linken und rechten 
   # Motoren des Roboter-Autos.
   speedleft = 0
   speedright = 0
   # Definition der Schrittweite fuer die Beschleunigung. 
   step = 0.3

# Die Entgegennahme von Befehlen aufgerufen auf der Web-Oberflaeche
# wird ueber Macros @webiopi.macro durch WebIOPI realisiert. Diese 
# Macros benötigt WebIOPi für die weitere Verarbeitung der auf der
# Web-Oberfläche eingegebenen Befehle.
   
# Die Funktion "ButtonForward()" legt fest, dass das Roboter
# Auto vorwaerts faehrt.
@webiopi.macro
def ButtonForward():
   global speedleft
   global speedright
   
   # Das Roboter-Auto wird beschleunigt bzw. es faehrt vorwaerts.
   speedleft = speedleft + step
   speedright = speedright + step
   
   # Die Geschwindigkeit darf nicht groesser als +1 werden. 
   # Der Bereich der Geschwindigkeit liegt zwischen -1 und +1.
   if speedleft > 1:
      speedleft = 1
   if speedright > 1:
      speedright = 1

   # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke
   HBridge.setMotorLeft(speedleft)
   HBridge.setMotorRight(speedright)
      
# Die Funktion "ButtonReverse()" legt fest, dass das Roboter  
# Auto rueckwaerts faehrt.
@webiopi.macro
def ButtonReverse():   
   global speedleft
   global speedright
   
   # Das Roboter-Auto wird abgebremst bzw. es faehrt rueckwaerts.
   # Der Bereich der Geschwindigkeit liegt zwischen +1 fuer die vorwaerts
   # Fahrt und -1 für die rueckwaerts Fahrt des Roboter-Autos.   
   speedleft = speedleft - step
   speedright = speedright - step

   # Die Geschwindigkeit darf nicht kleiner als -1 werden.
   if speedleft < -1:
      speedleft = -1
   if speedright < -1:
      speedright = -1

   # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke   
   HBridge.setMotorLeft(speedleft)
   HBridge.setMotorRight(speedright)
   
# Die Funktion "ButtonTurnLeft()" legt fest, dass das Roboter  
# Auto nach links faehrt.
@webiopi.macro
def ButtonTurnLeft():
   global speedleft
   global speedright

   speedleft = speedleft - step
   speedright = speedright + step

   # Die Geschwindigkeit darf nicht kleiner als -1 werden oder 
   # groesser als +1 werden da sonst jeweils die 100% 
   # ueberschritten waren.   
   if speedleft < -1:
      speedleft = -1
   if speedright > 1:
      speedright = 1

   # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke   
   HBridge.setMotorLeft(speedleft)
   HBridge.setMotorRight(speedright)

# Die Funktion "ButtonTurnRight()" legt fest, dass das Roboter  
# Auto nach rechts faehrt.
@webiopi.macro
def ButtonTurnRight():   
   global speedleft
   global speedright
      
   speedright = speedright - step
   speedleft = speedleft + step

   # Die Geschwindigkeit darf nicht kleiner als -1 werden oder 
   # groesser als +1 werden.   
   if speedright < -1:
      speedright = -1
   if speedleft > 1:
      speedleft = 1

   # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke      
   HBridge.setMotorLeft(speedleft)
   HBridge.setMotorRight(speedright)
   
# Die Funktion "ButtonStop()" legt fest, dass das Roboter
# Auto anhaelt.
@webiopi.macro
def ButtonStop():   
   global speedleft
   global speedright

   # Die Geschwindigkeit wird auf 0 gesetzt damit die Motoren 
   # stoppen
   speedleft = 0
   speedright = 0
   
   # Uebergabe der Geschwindigkeit an die Funktion der H-Bruecke
   HBridge.setMotorLeft(speedleft)
   HBridge.setMotorRight(speedright)

initiate()   
   
# Es wird der WebIOPi Web-Service des  WebIOPI Web-Servers 
# auf dem Port 8000 gestartet. Ein Passwort wird nicht vergeben.
server = webiopi.Server(port=8001, coap_port=8081, configfile=None)

# Es muessen noch die Buttons die auf der Web-Oberflaeche 
# verwendet werden definiert werden. Dies geschieht im folgenden 
# Abschnitt. Diese hier definierten Button-Funktionen werden von
# der Web-Oberflaeche und dem dort hinterlegten Java-Skript
# aufgerufen und ermöglichen so die Fernsteuerung des Roboter-Autos.
server.addMacro(ButtonForward)
server.addMacro(ButtonStop)
server.addMacro(ButtonReverse)
server.addMacro(ButtonTurnRight)
server.addMacro(ButtonTurnLeft)

# WebIOPi wird in einer Endlos-Schleife gestartet damit die 
# Befehle jederzeit entgegengenommen werden koennen.
webiopi.runLoop()
server.stop()
   
# Ende des Programms
