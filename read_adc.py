#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 2

# read SPI data from MCP3001 chip, 8 possible ADCs (0-7)
def read_adc(adc_num, clock_pin, mosi_pin, miso_pin, cs_pin):
    if ((adc_num < 0) or (adc_num > 7)):
        return -1

    GPIO.output(cs_pin, True)

    GPIO.output(clock_pin, False)   # clock starts low
    GPIO.output(cs_pin, False)      # bring CS low

    command_out = adc_num
    command_out |= 0x18             # start bit + single-ended bit
    command_out <<= 3               # only need to send 5 bits

    for i in range(5):
        if command_out & 0x80:
            GPIO.output(mosi_pin, True)
        else:
            GPIO.output(mosi_pin, False)

        command_out <<= 1
        GPIO.output(clock_pin, True)
        GPIO.output(clock_pin, False)

    adc_out = 0
    # read one empty bit, 10 ADC bits and 1 'null' bit
    for i in range(12):
        GPIO.output(clock_pin, True)
        GPIO.output(clock_pin, False)

        adc_out <<= 1

        if GPIO.input(miso_pin):
            if DEBUG > 1:
                print "{i} MISO=1".format(i = i)
            adc_out |= 0x01
        else:
            if DEBUG > 1:
                print "{i} MISO=0".format(i = i)

    GPIO.output(cs_pin, True)

    adc_out >>= 1                   # first bit is 'null' so drop it
    return adc_out

SPI_CLK = 22
SPI_MISO = 27
SPI_MOSI = 17
SPI_CS = 4

GPIO.setup(SPI_MOSI, GPIO.OUT);
GPIO.setup(SPI_MISO, GPIO.IN);
GPIO.setup(SPI_CLK, GPIO.OUT);
GPIO.setup(SPI_CS, GPIO.OUT);

potentiometer_adc = 0

def main():
    last_read = 0
    tolerance = 5

    while True:
        # read the analogue pin
        pot_value = read_adc(potentiometer_adc, SPI_CLK, SPI_MOSI, SPI_MISO, SPI_CS)

        pot_adjust = abs(pot_value - last_read)

        if DEBUG:
            print "pot : ", pot_value
            print "last: ", last_read
            print "adj:  ", pot_adjust

        if pot_adjust > tolerance:
            percent = pot_value / 10.24
            print "value = {pc}%".format(pc = percent)

        last_read = pot_value

        time.sleep(0.5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
