"""light: control power relay"""

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

def on():
    GPIO.setup(17, GPIO.HIGH)

def off():
    GPIO.setup(17, GPIO.LOW)

