#!/usr/bin/python

# code grabbed from
# http://recolog.blogspot.ca/2012/10/serial-line-internet-protocol-slip.html -
# by Asanka P. Sayakkara
#
# some hacks by me for testing purposes in the very end of this file.

import ProtoSLIP
import termios
import serial
import mapper

#-------------------------------------------------------------------------------
# This function connect and configure the serial port. Then returns the file discripter
def connectToSerialPort():
     serialFD = serial.Serial(port='/dev/ttyACM0', baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, rtscts=False)
     # port='/dev/ttyUSB0'- port to open
     # baudrate=115200  - baud rate to communicate with the port
     # bytesize=8           - size of a byte
     # parity='N'           - no parity
     # stopbits=1           - 1 stop bit
     # xonxoff=False           - no software handshakes
     # rtscts=False           - no hardware handshakes
     if serialFD < 0:
          print("Couldn't open serial port")
          return -1
     else:
          print("Opened serial port")
          return serialFD
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# This function accept a byte array and write it to the serial port
def writeToSerialPort(serialFD, byteArray):
     encodedSLIPBytes = ProtoSLIP.encodeToSLIP(byteArray)
     byteString = ''.join(chr(b) for b in encodedSLIPBytes) #convert byte list to a string
     serialFD.write(byteString)
     return
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# This function reads from the serial port and return a byte array
def readFromSerialPort(serialFD):
     i = 1
     byteArray = None
     byteArray = ProtoSLIP.decodeFromSLIP(serialFD)
     if byteArray is None:
          print "readFromSerialPort(serialFD): Error"
          return -1
     else:
          return byteArray
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# This function reads from the serial port and return a byte array
def disconnectFromSerialPort(serialFD):
     serialFD.close()
     return
#-------------------------------------------------------------------------------

c = connectToSerialPort()

distance = mapper.device("distance")
light = mapper.device("light")

di = distance.add_output("/vcnl4000/distance", 1, 'i', None, 0, 65536)
li = light.add_output("/vcnl4000/light", 1, 'i', None, 0, 65536)

while 1:
    l = [bin(i)[2:].zfill(8) for i in readFromSerialPort(c)]
    print int(l[0]+l[1], 2), int(l[2]+l[3], 2)

    di.update(int(l[0]+l[1], 2))
    li.update(int(l[2]+l[3], 2))

    distance.poll()
    light.poll()
