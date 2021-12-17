import serial
import time

def main():
    con=serial.Serial('/dev/ttyUSB0', 115200)
    print('connected.')
    while 1:
        str=con.readline() # byte code
        print (str.strip().decode('utf-8')) # decoded string

if __name__ == '__main__':
    main()
