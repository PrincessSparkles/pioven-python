#!/usr/bin/env python
"""
oven.py

main code for driving the python oven

26-05-2015
"""

import sys
import json
import serial
import RPi.GPIO as GPIO     # needed for GPIO.cleanup()

import LED as led
import MCP3008 as mcp3008

#-----------------------------------------------------------------------------

__LOG_NONE = 0
__LOG_INFO = 1
__LOG_DEBUG = 2

__LOG_LEVEL = __LOG_INFO

#-----------------------------------------------------------------------------

def log(level, message):
    """
    conditionally output a message to the screen
    
    Parameters
    level   - the level of the message
    message - the message
    
    if the __LOG_LEVEL variable is equal or greater than the level
    parameter, the message is printed
    """
    if level <= __LOG_LEVEL:
        print message

#-----------------------------------------------------------------------------

def log_info(message):
    """ log message at __LOG_INFO level """
    log(__LOG_INFO, message)    

#-----------------------------------------------------------------------------

def log_debug(message):
    """ log message at __LOG_DEBUG level """
    log(__LOG_DEBUG, message)    

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

def load_config(config_file_name):
    """ 
    load the JSON file with the configuaration
    Parameters
    config_file_name - the file to load the configuration from

    An example configuration file is given below
    {
        "heater": {
            "pin": 18
        },
        "temperature_sensor": {
            "channel": 0
        },
        "serial": {
            "port": "/dev/ttyAMA0",
            "baud": 115200,
            "timeout": 1,
            "xonxoff": true,
            "rtscts": false,
            "dsrdtr": false
        }
    }

    See the create_xxx methods for more details on the configuration parameters
    """
    with open(config_file_name, "r") as config_file:
        data = json.load(config_file)

    log_info("--[Config loaded]--")
    log_info(json.dumps(data, indent=4, separators=(',', ': ')))
    
    return data

#-----------------------------------------------------------------------------

def create_serial_port(config):
    """ 
    creates the serial port
    Parameters
    config - the configuration parameters
    
    The configuration parameters are
    port: (string) the name of the port to open
    baud: (int) the baudrate
    timeout: (float) the default timeout when reading from the port
    xonxoff: (bool) use software flow control
    rtscts: (bool) use hardware flow control
    dstdtr: (bool) use hardware flow control
    """
    port = config['port']
    baud = config['baud']
    timeout = config['timeout']
    xonxoff = config['xonxoff']
    rtscts = config['rtscts']
    dsrdtr = config['dsrdtr']

    ser = serial.Serial(port=port, baudrate=baud, timeout=timeout, 
                            xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr)

    log_debug("--[Serial port]--")
    log_debug(ser)

    return ser

#-----------------------------------------------------------------------------

def create_heater(config):
    """ 
    creates the heater from the specified configuration
    Parameters
    config - the configuration parameters
    
    The configuration parameters are
    pin: (int) the GPIO pin to use
    """
    heater = led.LED(config['pin'])

    log_debug("--[Heater]--")
    log_debug(heater)

    return heater

#-----------------------------------------------------------------------------

def create_temperature_sensor(config):
    """ 
    creates the temperature sensor from the specified configuration
    Parameters
    config - the configuration parameters
    
    The configuration parameters are
    channel: (int) the MCP3008 channel to use
    """
    channel = config['channel']

    temp = mcp3008.MCP3008()
    temp.set_default_channel(channel)

    log_debug("--[Temperature Sensor]--")
    log_debug(temp)

    return temp

#-----------------------------------------------------------------------------

def read_char(port):
    """ 
    read a single character from the serial port 
    Do not return until the character is read
    """
    while True:
        cmd = port.read()

        if len(cmd) == 1:
            return cmd[0]


#-----------------------------------------------------------------------------

def main(argv):
    """
    the main loop of the pioven project
    """
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

        log_info("--[Main loop]--")

        while True:
            cmd = read_char(port)

            if cmd == 'h':
                # make it hot
                log_info("[+] Heater on")
                heater.turn_on()
            elif cmd == 'c':
                # make it cold
                log_info("[+] Heater off")
                heater.turn_off()
            elif cmd == '?':
                # query what the current temperature is
                log_info("[+] Query temperature")
                temp = temp_sensor.read_channel()
                log_info("[+] Temperature={:03x}".format(temp))
                port.write("{:03x}\n".format(temp))
            elif cmd == 'v':
                # get version
                log_info("[+] Version {}".format(version))
                port.write("{}\n".format(version))

    except KeyboardInterrupt:
        pass
    finally:
        print ""        # tidy-up the output
        port.close()
        GPIO.cleanup()
    

if __name__ == '__main__':
    main(sys.argv)
