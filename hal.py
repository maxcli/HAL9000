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
import pyaudio
import wave
import sys



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
# length of data to read.
chunk = 1024
RESPEAKER_INDEX = 1
INTROWAV="..\voice_dataset\wavs\lj0011.wav"
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

def play_wav(wavename):
    print(f"Hello, my name is {wavename}")
    # open the file for reading.
    wf = wave.open(wavename, 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True,
                    output_device_index = RESPEAKER_INDEX)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)
    # play stream (looping from beginning of file to the end)
    while data:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

    # cleanup stuff.
    stream.close()    
    p.terminate()

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

    play_wav(INTROWAV)
 

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
