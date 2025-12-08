#!/usr/bin/env python

# Hal.py

import RPi.GPIO as GPIO
from gpiozero import LED 
from signal import signal,SIGTERM,SIGHUP,pause
import time
import threading
import json
import os
import os.path
import yaml
import argparse
from time import sleep

#definitions
BUTTON = 17
redled= LED(13)
blink_on=False
reading=True
statusString="unknown"  

#functions
def button_handler():
  
    
    global blink_on
    state = GPIO.input(BUTTON)
    print("button handler.  blink flag:"+str(blink_on) +" state:"  state) 
    
    if blink_on:
        redled.off()
    else:    
        redled.blink(0.5,0.5)

    blink_on=not blink_on

#main loop.  runs on schedule
def main_daemon():
    while reading:
        print('Wakeup  ' )
  
 
        #print('Distance: ' +  '{:1.2f}'.format( distancesensor.distance) + " m") #speech . replace print with voice messaged      
        sleep(5)


def get_settings():
    full_file_path = Path(__file__).parent.joinpath('settings.yaml')
    with open(full_file_path) as settings:
        settings_data = yaml.load(settings, Loader=yaml.Loader)
    return settings_data


#ctrl C to exit program, and reset gpio pins
def safe_exit(signum,frame):
    print("Goodbye, Safe exit signal")
    sleep(2)
    exit(1)

def startup():
    
    print("red on")
    redled.on()
    sleep(4)
   
 
    redled.off()
    sleep(4)
 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON, GPIO.IN)

try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    settingsDict =get_settings()
    SS_SUBSCRIPTION_KEY=settingsDict["ss_SUBSCRIPTION_KEY"]
    print("sub key"+ SS_SUBSCRIPTION_KEY)
    
    button.when_pressed=button_handler
    startup()


    reader=Thread(target=main_daemon,daemon=True)
    reader.start()
    pause()

 

finally:
    reading=False
    distancesensor.close()
    pass
