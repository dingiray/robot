#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com
# Modul welches die Anzeige von Informationen auf der 
# LED-Matrix des Raspberry Pi Sense-HAT umsetzt.

import time, os

# Sense HAT Bibliothek importieren.
from sense_hat import SenseHat

# initialisieren des SenseHat.
sense = SenseHat()

# Farben festlegen für die Symbole für die LED Anzeige.
g = [0, 255, 0]
r = [255, 0, 0]
e = [0, 0, 0]   

# Ende Symbol fuer das LED-Matrix.
icon_finish = [
e,e,e,r,r,e,e,e,
e,e,r,e,e,r,e,e,
e,r,e,e,e,e,r,e,
r,e,e,r,r,e,e,r,
r,e,e,r,r,e,e,r,
e,r,e,e,e,e,r,e,
e,e,r,e,e,r,e,e,
e,e,e,r,r,e,e,e
]

# Pfeil als Symbol fuer die LED-Matrix.
icon_arrow = [
e,e,e,g,g,e,e,e,
e,e,g,g,g,g,e,e,
e,g,e,g,g,e,g,e,
g,e,e,g,g,e,e,g,
e,e,e,g,g,e,e,e,
e,e,e,g,g,e,e,e,
e,e,e,g,g,e,e,e,
e,e,e,g,g,e,e,e
]   

def display_letter(text,txt_colour,bg_color):
   if bg_color =="":
      bg_color = [255,255,255]
   if txt_colour =="":
      txt_colour = [0,0,0]
   # Der Inhalt der Variable text wird explizit in einen String
   # umgewandelt damit Fehler vermieden werden bei der Anzeige.
   text = str(text)
   # Anzeige des Textes auf der LED-Matrix.
   sense.show_letter(text,text_colour=txt_colour,\
   back_colour=bg_color)
   return -1
   
def display_message(text,txt_colour,bg_color, speed):
   if bg_color =="":
      bg_color = [255,255,255]
   if txt_colour =="":
      txt_colour = [0,0,0]
   # Der Inhalt der Variable text wird explizit in einen String
   # umgewandelt damit Fehler vermieden werden bei der Anzeige.
   text = str(text)
   # Anzeige der Laufschrift auf der LED-Matrix.
   sense.show_message(text,scroll_speed=speed,\
   text_colour=txt_colour,back_colour=bg_color)
   return -1
   
def display_pixels(icon):
   if icon == "arrow":
      sense.set_pixels(icon_arrow)   
   elif icon == "finish":
      sense.set_pixels(icon_finish)
   return -1
   
def display_rotate(value):
   # Die Sense-HAT API akzeptiert nur Winkel von 0, 90, 180 
   # und 270 um die die Anzeige gedreht werden kann. 
   if value == 0:
      sense.set_rotation(value)      
   elif value == 90:
      sense.set_rotation(value)      
   elif value == 180:
      sense.set_rotation(value)   
   elif value == 270:
      sense.set_rotation(value)   
   return -1
   
def display_image(file_path):
   # Pruefen ob es die Datei ueberhaupt gibt.
   if os.path.isfile(file_path)== True:
      sense.load_image(file_path,redraw=True)      
   return -1
   
def display_clear():
   # Loescht die aktuelle Anzeige auf der LED-Matrix.
   sense.clear(255, 255, 255)
   return -1
   
def display_flip(flip):
   # Spiegelt die aktuelle Anzeige auf der LED-Matrix vertikal.
   if flip == "v":
      sense.flip_v()
   # Spiegelt die aktuelle Anzeige auf der LED-Matrix horizontal.
   elif flip =="h":
      sense.flip_h()
   return -1       
# Ende des Programmes
