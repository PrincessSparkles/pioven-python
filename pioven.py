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
import RPi.GPIO as GPIO     # needed for GPIO.cleanup()

import LED
import MCP3008

# load the JSON file with the configuaration
def load_config(config_file):
    with open(config_file, "r") as f:
        data = json.load(f)

    print json.dumps(data, indent=4, separators=(',', ': '))
    return data

def main(argv):
    print "PiOven v0.0.1.1"

    config_file = "pioven.json"
    if len(argv) > 1:
        config_file = argv[1]

    config = load_config(config_file)


if __name__ == '__main__':
    main(sys.argv)
