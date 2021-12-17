import serial
import time

def main():
# USB:ttyUSB0
# GPIO:ttyAMA0
    con=serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#    con=serial.Serial('/dev/ttyAMA0', 19200, timeout=10)
    print (con.portstr)
    while 1:
        str=con.readline()
        print (str)
        con.write(str)

if __name__ == '__main__':
    main()
