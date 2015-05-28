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

__verbose = 1

#-----------------------------------------------------------------------------

# load the JSON file with the configuaration
def load_config(config_file):
    with open(config_file, "r") as f:
        data = json.load(f)

    if __verbose > 0:
        print "--[Config loaded]--"
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

    if __verbose > 1:
        print "--[Serial port]--"
        print ser

    return ser

#-----------------------------------------------------------------------------

def create_heater(config):
    heater = led.LED(config['led'])

    if __verbose > 1:
        print "--[Heater]--"
        print heater

    return heater

#-----------------------------------------------------------------------------

def create_temperature_sensor(config):
    channel = config['channel']

    temp = mcp3008.MCP3008()
    temp.set_default_channel(channel)

    if __verbose > 1:
        print "--[Temperature Sensor]--"
        print temp

    return temp

#-----------------------------------------------------------------------------

def main(argv):
    version = "PiOven v0.4.2.0"
    print version

    config_file = "pioven.json"
    if len(argv) > 1:
        config_file = argv[1]

    config = load_config(config_file)

    port = create_serial_port(config['serial'])
    try:
        heater = create_heater(config['heater'])
        temp_sensor = create_temperature_sensor(config['temperature_sensor'])

        if __verbose > 0:
            print "--[Main loop]--"

        while True:
            cmd = port.read()

            if len(cmd) == 1:
                if cmd[0] == 'h':
                    # make it hot
                    if __verbose > 0:
                        print "[+] Heater on"
                    heater.on()
                elif cmd[0] == 'c':
                    # make it cold
                    if __verbose > 0:
                        print "[+] Heater off"
                    heater.off()
                elif cmd[0] == '?':
                    # query what the current temperature is
                    if __verbose > 0:
                        print "[+] Query temperature"
                    temp = temp_sensor.read_channel()
                    if __verbose > 0:
                        print "[+] Temperature={:03x}".format(temp)
                    port.write("{:03x}\n".format(temp))
                elif cmd[0] == 'v':
                    # get version
                    if __verbose > 0:
                        print "[+] Version {}".format(version)
                    port.write("{}\n".format(version))

    except KeyboardInterrupt:
        pass
    finally:
        print ""        # tidy-up the output
        port.close()
        GPIO.cleanup()
    


if __name__ == '__main__':
    main(sys.argv)
