import copy
import time

import serial

import arduinoUtil
import controllerUtil
from arduinoUtil import send_message as send
from util import eprint

PRESS_THRESHOLD = 0.1

ON = 'I'
OFF = 'O'
RESET = 'R'
TOGGLE = 'T'


def get_arduino_port():
    arduinoPort = arduinoUtil.arduino_port()

    return arduinoPort


def main():
    status = controllerUtil.ControllerStatus()
    thread1 = controllerUtil.ControllerThread(1, 'Controller Thread', status=status)
    thread1.start()

    ser = serial.Serial()
    ser.baudrate = 115200

    def reset_port():
        if ser.is_open:
            ser.close()
            time.sleep(0.1)
        port = get_arduino_port()
        ser.port = port.device
        print(f'Connecting to port {ser.port}...')

        # Connect to arduino
        errorPrinted = False
        while not ser.is_open:
            try:
                ser.open()
            except Exception as e:
                if not errorPrinted:
                    eprint('Port is busy...')
                    errorPrinted = True
                time.sleep(2)
        print(f'Connected to port {ser.port}')

    reset_port()

    lastStatus = controllerUtil.ControllerStatus(status)

    while True:
        if not thread1.is_alive():  # Controller unplugged/disconnected - Turn off LED; Allows for uploading Arduino code
            send(ser, OFF)
            time.sleep(0.1)
            ser.close()
            eprint(f'Resetting controller thread')
            time.sleep(10)
            reset_port()

            print(f'Starting controller thread')
            status = controllerUtil.ControllerStatus()
            thread1 = controllerUtil.ControllerThread(1, 'Controller Thread', status=status)
            thread1.start()
            continue

        if not ser.is_open:
            eprint('Port error. Resetting...')
            reset_port()
            continue

        if status != lastStatus:

            if status.hats['HY'] == -1 and status.buttons['LB'] == 1 and status.buttons['RB'] == 1:
                send(ser, OFF)
                print('Exiting program.')
                thread1.stop = True
                break

            if status.joysticks['LJY'] != lastStatus.joysticks['LJY']:  # left joysick is moved in y direction
                direction = 'F' if status.joysticks['LJY'] > 0 else 'B'
                speed = chr(abs(round(status.joysticks['LJY'] * 254)))
                message = f"{direction}{speed}"
                print(f'Sending {ord(speed)}')
                send(ser, message)

            '''if status.hats['HY'] == -1 and status.buttons['LB'] == 1 and status.buttons['RB'] == 1:
                send(ser, OFF)
                print('Exiting program.')
                thread1.stop = True
                break
                
            if status.buttons['Start'] == 1:  # Reset Arduino
                print('Resetting Arduino...')
                send(ser, RESET)
                time.sleep(5)
                # reset serial connection
                reset_port()
                continue
            elif status.joysticks['RT'] > PRESS_THRESHOLD or status.joysticks['LT'] > PRESS_THRESHOLD:  # Trigger pressed
                send(ser, ON)
            elif ((lastStatus.joysticks['RT'] > PRESS_THRESHOLD >= status.joysticks['RT']) or
                  (lastStatus.joysticks['LT'] > PRESS_THRESHOLD >= status.joysticks['LT'])) and \
                    not lastStatus.is_button_held():  # Trigger released
                send(ser, OFF)
            elif not lastStatus.is_button_held() and status.is_button_held(): # Button pressed
                send(ser, TOGGLE)'''

            lastStatus = copy.deepcopy(status)

        time.sleep(0.003)

    ser.close()


if __name__ == '__main__':
    main()
