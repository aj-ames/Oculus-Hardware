"""Python script for Oculus RPi."""
import os
import paho.mqtt.client as mqtt
import argparse
import sys

# RPi.GPIO configuration
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
MATRIX = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9],
          ['*', 0, '#']]
ROW = [7, 11, 13, 15]
COL = [12, 16, 18]

register = 'z'

brokerAddress = "192.168.0.7"
port = 1883


def mqttSetup():
    """Method to initialize MQTT."""
    client = mqtt.Client("Oculus-Hardware")
    # set username and password
    client.username_pw_set(user, password=password)
    client.connect(broker_address, port)  # connect to broker
    return client


def clicker():
    """Click a picture in RPi."""
    os.system("raspistill -o ~/image/image.jpg")


def execute(option, client):
    """Execute commands based on the input."""
    if option == '1':
        os.system("mst")
        client.publish("Oculus", "object", qos=0, retain=False)
    elif option == '2':
        os.system("msp")
        clicker()
        client.publish("Oculus", "face", qos=0, retain=False)
    elif option == '3':
        os.system("msp")
        clicker()
        client.publish("Oculus", "currency", qos=0, retain=False)
    elif option == '4':
        os.system("msp")
        clicker()
        client.publish("Oculus", "predcition", qos=0, retain=False)
    elif option == '5':
        os.system("msp")
        clicker()
        client.publish("Oculus", "ocr", qos=0, retain=False)
    elif option == '6':
        pass
    elif option == '7':
        pass
    elif option == '8':
        pass
    elif option == '*':
        os.system("msp")
    elif option == '#':
        client.publish("Oculus", "terminate", qos=1, retain=True)
    else:
        pass


def keypadInit():
    """Keypad Initializer."""
    for j in range(3):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j], j)

    for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN,
                   pull_up_down=GPIO.PUD_UP)


def get_args_values(args=None):
    """Method to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Arguments supported..")
    parser.add_argument('-H', '--host',
                        help='Broker IP',
                        default='localhost')
    parser.add_argument('-p', '--port',
                        help='port of the Broker',
                        default='1883')
    parser.add_argument('-u', '--user',
                        help='user name',
                        default='astr1x')
    parser.add_argument('-P', '--password',
                        help="password",
                        default="astr1x2096")

    info = parser.parse_args(args)
    return (info.host,
            info.port,
            info.user,
            info.password)


"""
Get Broker address, port, username and password.
The default value has already been provided.
"""
if __name__ == '__main__':
    broker_address, port, user, password = get_args_values(sys.argv[1:])
    port = int(port)

client = mqttSetup()

try:
    keypadInit()
    while(True):
            for j in range(3):
                GPIO.output(COL[j], 0)

                for i in range(4):
                    if GPIO.input(ROW[i]) == 0:
                        if not register == MATRIX[i][j]:
                            register = MATRIX[i][j]
                            print(MATRIX[i][j])
                            execute(register, client)
                            while(GPIO.input(ROW[i]) == 0):
                                pass
                GPIO.output(COL[j], i)

except KeyboardInterrupt:
    GPIO.cleanup()
