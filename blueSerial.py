#! /home/juan/anaconda3/bin/python3.7
import serial
bluetoothSerial0 = serial.Serial("/dev/rfcomm0", baudrate=115200)
bluetoothSerial1 = serial.Serial("/dev/rfcomm1", baudrate=115200)
print("BT connected")

try:
    while 1:
        data = bluetoothSerial0.readline()
        print("data:{}".format(data))
        data = bluetoothSerial1.readline()
        print("data:{}".format(data))
except KeyboardInterrupt:
    print("Quit")
