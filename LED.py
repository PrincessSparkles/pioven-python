#!/usr/bin/env python
"""
LED.py

Class (and test code) for managing an LED plugged into a Raspberry Pi GPIO
pin

25-05-2015
"""

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class LED:
    """
    Class representing an LED connected to a GPIO pin of a Raspberry Pi
    Provides methods to turn the LED on, and off
    """

    def __init__(self, pin):
        """
        initialise
        remember the pin number, and configure the pin to be an output pin

        Parameters:
        pin - the GPIO pin to use
        """
        self.pin = pin 
        GPIO.setup(pin, GPIO.OUT)

    def __repr__(self):
        """ text representation for debugging """
        return "LED(pin=%d)" % self.pin

    def turn_on(self):
        """ switch the LED on """
        GPIO.output(self.pin, True)

    def turn_off(self):
        """ turn the LED off """
        GPIO.output(self.pin, False)

##############################################################################

# test code

import sys
import time

def main(argv):
    """ Test code """
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

