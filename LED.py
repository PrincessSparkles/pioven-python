#!/usr/bin/env python
#
# LED.py
#
# Class (and test code) for managing an LED plugged into a Raspberry Pi GPIO
# port.
#
# 25-05-2015
#

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class LED:
    # initialise
    # remember the pin number, and configure the pin to be an output pin
    def __init__(self, pin):
        self.pin = pin 
        GPIO.setup(pin, GPIO.OUT)

    # text representation for debugging
    def __repr__(self):
        return "LED(pin=%d)" % self.pin

    # switch the LED on
    def turn_on(self):
        GPIO.output(self.pin, True)

    # turn the LED off
    def turn_off(self):
        GPIO.output(self.pin, False)

##############################################################################

# test code

import sys
import time

def main(argv):
    pin = int(argv[1])
    led = LED(pin)

    print "[+] testing __repr__" 
    print "[+] should see indictation of LED and the selected pin"
    print led

    print "[+] the selected LED should now come on for two seconds"
    led.turn_on()
    time.sleep(2)
    led.turn_off()

if __name__ == '__main__':
    main(sys.argv)
    GPIO.cleanup()

