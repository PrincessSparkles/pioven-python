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
    def __init__(self, pin):
        self.pin = pin 
        GPIO.setup(pin, GPIO.OUT)

    def __repr__(self):
        return "LED(pin=%d)" % self.pin

    def on(self):
        GPIO.output(self.pin, True)

    def off(self):
        GPIO.output(self.pin, False)

import sys
import time

def main(argv):
    pin = int(argv[1])
    led = LED(pin)

    print "[+] testing __repr__" 
    print "[+] should see indictation of LED and the selected pin"
    print led

    print "[+] the selected LED should now come on for two seconds"
    led.on()
    time.sleep(2)
    led.off()

if __name__ == '__main__':
    main(sys.argv)
    GPIO.cleanup()
