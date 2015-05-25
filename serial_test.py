
import serial


def main():
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.25, xonxoff=True, rtscts=False, dsrdtr=False)
    print ser

    try:
        while True:
            c = ser.read()

            if len(c) != 0:
                print c
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()

if __name__ == '__main__':
    main()
