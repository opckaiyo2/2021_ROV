import serial
import time
   
def main():
    con=serial.Serial('/dev/ttyUSB0', 115200)
    print (con.portstr)
    while 1:
        str=con.readline()
        print (len(str))
        print (str)
   
if __name__ == '__main__':
    main()
