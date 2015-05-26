#!/usr/bin/env python
#
# MCP3008.py
#
# Provides an interface (and test code) to the MCP3008 chip
# This chip is an 8 channel, 10-bit ADC with SPI interface
#
# 25-05-2015
#

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class MCP3008:
    # initialise
    # remember the parameters, and configure the pins
    def __init__(self, clk, mosi, miso, cs):
        self.clk = clk
        self.mosi = mosi
        self.miso = miso
        self.cs = cs

        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.mosi, GPIO.OUT)
        GPIO.setup(self.miso, GPIO.IN)
        GPIO.setup(self.cs, GPIO.OUT)

    # string representation of the MCP3008 - used for debugging
    def __repr__(self):
        return "MCP3008(clk=%d, mosi=%d, miso=%d, cs=%d)" % \
                            (self.clk, self.mosi, self.miso, self.cs)

    # read the 10-bit value from specified ADC
    # use SPI to talk to the chip
    def read_adc(self, adc):
        if (adc < 0 or adc > 7):
            # invalid adc number
            return -1

        GPIO.output(self.cs, True)

        GPIO.output(self.clk, False)
        GPIO.output(self.cs, False)

        cmd = adc
        cmd |= 0x18     # start bit and single-ended bit
        cmd <<= 3       # we only need to send 5 bits

        for i in range(5):
            if cmd & 0x80:
                GPIO.output(self.mosi, True)
            else:
                GPIO.output(self.mosi, False)

            cmd <<= 1
            GPIO.output(self.clk, True)
            GPIO.output(self.clk, False)

        out = 0

        # read one empty bit, 10 data bits and 1 null bit
        for i in range(12):
            GPIO.output(self.clk, True)
            GPIO.output(self.clk, False)

            out <<= 1

            if GPIO.input(self.miso):
                out |= 0x01

        GPIO.output(self.cs, True)

        out >>= 1           # drop the last bit (null or empty)
        return out
        
##############################################################################

import time

test_clk = 22
test_mosi = 17
test_miso = 27
test_cs = 4
test_adc = 0

def main():
    mcp = MCP3008(test_clk, test_mosi, test_miso, test_cs)

    print "[+] outputting mcp"
    print mcp

    last_read = -100
    tolerance = 5

    print "[+] reading values from adc in a loop - please turn the knob"
    print "[+] pres Ctrl-C when done"
    while True:
        val = mcp.read_adc(test_adc)

        if abs(val - last_read) > tolerance:
            percent = val / 10.24
            print "val = {pc}%".format(pc = percent)

        last_read = val
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

