#!/usr/bin/python

"""micro servo 9g: Tower Pro SG90"""

import RPi.GPIO as GPIO
import time

SERVO = 26
ANGLE = 2.5
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT)
SG90 = GPIO.PWM(SERVO, 50)
SG90.start(ANGLE)

def turn_left():
    global ANGLE
    if ANGLE < 6:
        ANGLE += 0.5
        SG90.ChangeDutyCycle(ANGLE)
        time.spleep(0.02)
        SG90.ChangeDutyCycle(0)

def turn_right():
    global ANGLE
    if ANGLE > 3:
        ANGLE -= 0.5
        SG90.ChangeDutyCycle(ANGLE)
        time.spleep(0.02)
        SG90.ChangeDutyCycle(0)

