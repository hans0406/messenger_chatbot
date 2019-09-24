#!/usr/bin/python

"""micro servo 9g: Tower Pro SG90"""

import RPi.GPIO as GPIO
import time

SERVO = 26
STEP = 9.5/8
SERVO_ANGLE = (2.5 + 12) / 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT)
SG90 = GPIO.PWM(SERVO, 50)
SG90.start(0)

def turn_left():
    global SERVO_ANGLE
    if SERVO_ANGLE < 12 - (STEP*2):
        SERVO_ANGLE += STEP
        SG90.ChangeDutyCycle(SERVO_ANGLE)
        print("turn left", SERVO_ANGLE)

def turn_right():
    global SERVO_ANGLE
    if SERVO_ANGLE > 2.5 + STEP:
        SERVO_ANGLE -= STEP
        SG90.ChangeDutyCycle(SERVO_ANGLE)
        print("turn right", SERVO_ANGLE)

