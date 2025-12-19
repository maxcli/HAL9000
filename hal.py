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
TESTWAV = r"/home/pi/test.wav"
INTROWAV = r"voice_dataset/wavs/LJ0011.wav"

PIXELS_N = 3
strip= apa102.APA102(num_led=PIXELS_N)
# 1. Force ALSA to use the plug interface before initializing PyAudio
os.environ['PA_ALSA_PLUGHW'] = '1'

DEVICE_INDEX=1
#DEVICE_NAME = "plughw:3,0"   #  this works :  aplay -D "plughw:3,0" test.wav

#functions

def set_strip_color(r, g, b, brightness=31):
    """Sets the entire strip to one color. Brightness is 0-31."""
    for i in range(PIXELS_N ):
        strip.set_pixel(i, r, g, b, brightness)
    strip.show()

def clear_strip():
    """Turns all LEDs off."""
    set_strip_color(0, 0, 0, 0)

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

def showAudioDevice():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    
    
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        # Check if the device has output channels
        
        if (device_info.get('maxOutputChannels')) > 0:
            print(f"Index {i}: {device_info.get('name')}")
            print(f"  Max Output Channels: {device_info.get('maxOutputChannels')}")
            print(f"  Sample Rates: {device_info.get('defaultSampleRate')}")

def play_wav(wavename):

    chunk = 1024  # Define the buffer size
    print(f"Playing wav file  :  {wavename}")
    try:
        wf = wave.open(str(wavename), 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                            channels = wf.getnchannels(),
                            rate = wf.getframerate(),
                            output = True,
                            output_device_index = DEVICE_INDEX)  # Matches your 'card 3'
                    
        print(f"Playing to Index {DEVICE_INDEX}...")
        # read data (based on the chunk size)
        data = wf.readframes(chunk)
        # play stream (looping from beginning of file to the end)
        while len(data)>0:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)

        # cleanup  
        stream.stop_stream()
        stream.close()    
        p.terminate()

    except FileNotFoundError:
        print(f"Error: The file {wavename} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


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
