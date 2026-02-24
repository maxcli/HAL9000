#!/usr/bin/env python

# Hal.py
#  
# 
#setup venv
# python3 -m venv hal_env
# source hal_env/bin/activate
# run program
#    ./runhal.sh#
#
#
import RPi.GPIO as GPIO  
from gpiozero import LED 
from signal import signal,SIGTERM,SIGHUP,pause
import json
import os
import os.path
import yaml
import argparse
import sys



from time import sleep
from pathlib import Path
from threading import Thread

#definitions
BUTTON = 17
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(BUTTON, GPIO.IN)
redled= LED(13)
blink_on=False
reading=True
statusString="unknown"  

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
    showAudioDevice()
    #play_wav(INTROWAV )  # DOES NOT WORK. Match Device’s Native Sample Rate
    play_wav(TESTWAV)   

    print("Strip blue ")
    set_strip_color(0, 0, 255, 5)
    sleep(4)

    print("Strip Green ")
    set_strip_color(0, 255, 0, 10)
    sleep(4)

    clear_strip()

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
