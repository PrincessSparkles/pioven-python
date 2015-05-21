#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

RED_LED = 18

GPIO.setup(RED_LED, GPIO.OUT)

def light_on():
	GPIO.output(RED_LED, True)

def light_off():
	GPIO.output(RED_LED, False)


if __name__ == '__main__':
	light_on()
	time.sleep(2)
	light_off()
