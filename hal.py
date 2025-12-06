
from gpiozero import LED 
from pathlib import Path
from time import sleep
from signal import signal,SIGTERM,SIGHUP,pause
import json
import os
import os.path
import yaml
from threading import Thread
from __future__ import print_function
import argparse
import google.auth.transport.requests
import google.oauth2.credentials
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from pixels import pixels
import RPi.GPIO as GPIO
import time

#definitions
BUTTON = 17
redled= LED(13)
blink_on=False
reading=True
statusString="unknown"  # make string list
DEVICE_API_URL = 'https://embeddedassistant.googleapis.com/v1alpha2'

#functions


#main loop.  runs on schedule
def main_daemon():
    while reading:
        print('Wakeup  ' )
        state = GPIO.input(BUTTON)
        if state:
            print("off")
        else:
            print("on")
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
   
    startup()


    reader=Thread(target=main_daemon,daemon=True)
    reader.start()
    pause()

 

finally:
    reading=False
    distancesensor.close()
    pass
