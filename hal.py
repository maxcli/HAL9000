#!/usr/bin/env python

# Hal.py
#  
# run program
#    ./runhal.sh
#
import apa102
import RPi.GPIO as GPIO  
from gpiozero import LED 
from signal import signal,SIGTERM,SIGHUP,pause
import json
import os
import os.path
import yaml
import argparse
from time import sleep
from pathlib import Path
from threading import Thread

#definitions
BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)
redled= LED(13)
blink_on=False
reading=True
statusString="unknown"  

#functions


#main loop.  runs on schedule
def main_daemon():
    while reading:
        #print('Wakeup')

        state = GPIO.input(BUTTON)

        if state:
            print("button off")
        else:
            print("button on")

        sleep(2)


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
   
    print("red blink")
    redled.blink(0.5,0.5)
    sleep(4)
 
    redled.off()
 

try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    settingsDict =get_settings()
    SS_SUBSCRIPTION_KEY=settingsDict["ss_key"]
    print("sub key"+ SS_SUBSCRIPTION_KEY)
    
    #BUTTON.when_pressed=button_handler
    startup()


    reader=Thread(target=main_daemon,daemon=True)
    reader.start()
    pause()

 

finally:
    reading=False
    pass
