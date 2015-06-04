#!/usr/bin/env python
"""
MCP3008.py

Provides an interface (and test code) to the MCP3008 chip
This chip is an 8 channel, 10-bit ADC with SPI interface

25-05-2015
"""

import spidev

class MCP3008:
    """ Provides an interface to read analogue data from an MCP3008 chip """

    def __init__(self):
        """ initialise """
        self.default_channel = 0
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)

    def __repr__(self):
        """ string representation of the MCP3008 - used for debugging """
        return "MCP3008()"

    def set_default_channel(self, channel):
        """ 
        setup a default channel to read from 
        Parameters
        channel - the new default channel (ignored if < 0 or > 7)
        """
        if (channel >= 0 and channel <= 7):
            self.default_channel = channel

    # code taken from http://www.raspberrypi-spy.co.uk/2013/10/
    #               analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/
    def read_channel(self, channel=-1):
        """ 
        read the 10-bit value from specified channel
        Parameters
        channel=-1 - the channel to read from. If -1, the default is used
        """
        if channel == -1:
            channel = self.default_channel

        adc = self.spi.xfer2([1, (0x08 + channel) << 4, 0])
        data = ((adc[1] & 0x03) << 8) + adc[2]

        return data

##############################################################################

import time

def main():
    """ test code """
    mcp = MCP3008()

    print "[+] outputting mcp"
    print mcp

    last_read = -100
    tolerance = 5
    test_channel = 0

    print "[+] reading values from channel in a loop - please turn the knob"
    print "[+] pres Ctrl-C when done"
    while True:
        val = mcp.read_channel(test_channel)

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
        pass
