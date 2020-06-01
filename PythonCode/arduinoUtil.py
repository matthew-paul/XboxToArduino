import time

import serial
from serial.tools import list_ports

from PythonCode.util import eprint


def arduino_port():
    arduinoPorts = []

    print('Searching for arduino...')
    while len(arduinoPorts) != 1:
        ports = serial.tools.list_ports.comports()
        [print(port.description) for port in ports]
        arduinoPorts = [port for port in ports if 'Arduino Uno' in str(port) and 'bootloader' not in str(
            port)]  # when restarting, com port will temporarily show 'Arduino ___ bootloader'

        if len(arduinoPorts) != 1:
            time.sleep(1)

    arduinoPort = arduinoPorts[0]

    if arduinoPort:
        print('Arduino Found')

    return arduinoPort

def send_message(ser, message):
    if not ser.is_open:
        eprint('Port not open, exiting.')
        return -1

    try:
        ser.write(message.encode())
        # print(f'Sent message "{message}" on port {ser.port}')
    except Exception as e:
        ser.close()
        print(f'Error writing to port: {e}')
