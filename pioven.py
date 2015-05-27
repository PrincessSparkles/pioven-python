#!/usr/bin/env python
#
# oven.py
#
# main code for driving the python oven
#
# 26-05-2015
#

import sys
import json
import serial
import RPi.GPIO as GPIO     # needed for GPIO.cleanup()

import LED as led
import MCP3008 as mcp3008

#-----------------------------------------------------------------------------

# load the JSON file with the configuaration
def load_config(config_file):
    with open(config_file, "r") as f:
        data = json.load(f)

    print json.dumps(data, indent=4, separators=(',', ': '))
    return data

#-----------------------------------------------------------------------------

def create_serial_port(config):
    port = config['port']
    baud = config['baud']
    timeout = config['timeout']
    xonxoff = config['xonxoff']
    rtscts = config['rtscts']
    dsrdtr = config['dsrdtr']

    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout, 
                            xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr)

    print ser

    return ser

#-----------------------------------------------------------------------------

def create_heater(config):
    heater = led.LED(config['led'])

    print heater

    return heater

#-----------------------------------------------------------------------------

def main(argv):
    print "PiOven v0.1.2.1"

    config_file = "pioven.json"
    if len(argv) > 1:
        config_file = argv[1]

    config = load_config(config_file)

    port = create_serial_port(config['serial'])
    heater = create_heater(config['heater'])

    


if __name__ == '__main__':
    main(sys.argv)
