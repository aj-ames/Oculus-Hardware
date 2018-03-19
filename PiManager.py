import serial
import time
import xlwt
import numpy
import os
import paho.mqtt.client as mqtt
addr  = '/dev/ttyACM0' #bitchy line. Always run /dev to find it.
baud  = 9600
x = 'z'
brokerAddress = "192.168.0.9"
port = 1883

def mqttPub(msg):
        CLIENT = mqtt.Client("RPi")
        CLIENT.connect(brokerAddress)
        CLIENT.loop_start()
        CLIENT.publish("oculus", msg)
        time.sleep(3)
        CLIENT.loop_stop()

def clicker():
    os.system("raspistill -o image.jpg")

def looper(i):
    if i == '1':
        os.system("sudo motion")
        time.sleep(1)
        mqttPub("object")
    if i == '2':
        clicker()
        mqttPub("money")
    if i == '3':
        clicker()
        mqttPub("faces")
    if i == '4':
        mqttPub("lightOn")
    if i == '5':
        mqttPub("lightOff")
    if i == '6':
        mqttPub("kitchen")
    if i == '7':
        mqttPub("security")
    if i == '8':
        mqttPub("maa ****")
    if i == '*':
        os.system("sudo service motion stop")

while x != '#':
    with serial.Serial(addr,baud) as port:
        temp = (port.readline())
        x = str(temp)[0]
        print(x)
        looper(x)
