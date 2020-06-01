import time

import inputs

xboxController = None
# Get devices and make sure xbox controller is connected
while not xboxController:
    for device in inputs.devices.gamepads:
        if device.name == 'Microsoft X-Box 360 pad':
            print('Controller Found')
            xboxController = device
            break
    if not xboxController:
        print('Searching for controller...')
        time.sleep(5)
        inputs.devices._post_init()  # search for controllers again

DELAY = 20  # milliseconds

done = False
while not done:
    for event in inputs.get_gamepad():  # xboxController.read():
        if event.ev_type == 'Absolute':
            if event.code == 'ABS_X':
                print(f'Left joystick x: {event.state}')
            elif event.code == 'ABS_Y':
                print(f'Left joystick y: {event.state}')
            elif event.code == 'ABS_RX':
                print(f'Right joystick x: {event.state}')
            elif event.code == 'ABS_RY':
                print(f'Right joystick y: {event.state}')
            elif event.code == 'ABS_Z':
                print(f'Left trigger: {event.state}')
            elif event.code == 'ABS_RZ':
                print(f'Right trigger: {event.state}')
        elif event.ev_type == 'Key':
            if event.code == 'BTN_SELECT':
                print(f'Exiting controller loop')
                done = True
                break
            else:
                print(f'Button {event.code} {event.state} pressed')
    time.sleep(DELAY / 1000.0)
