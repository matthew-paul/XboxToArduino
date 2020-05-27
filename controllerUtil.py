import copy
import threading
import time

import inputs

# Define some constants.
XBOX_CONTROLLER_NAME = 'Microsoft X-Box 360 pad'

names = {'BTN_NORTH': 'Y',
         'BTN_EAST': 'B',
         'BTN_SOUTH': 'A',
         'BTN_WEST': 'X',
         'BTN_SELECT': 'Select',
         'BTN_START': 'Start',
         'BTN_TL': 'LB',
         'BTN_TR': 'RB',
         'BTN_THUMBL': 'ThumbL',
         'BTN_THUMBR': 'ThumbR',
         'ABS_X': 'LJX',  # left joystick X
         'ABS_Y': 'LJY',
         'ABS_RX': 'RJX',
         'ABS_RY': 'RJY',
         'ABS_Z': 'LT',
         'ABS_RZ': 'RT',
         'ABS_HAT0X': 'HX',
         'ABS_HAT0Y': 'HY'}

JOYSTICK_MAX = 32768.0
TRIGGER_MAX = 256.0
DEADZONE = 0.15  # percent of total joystick motion


class ControllerStatus:
    def __init__(self, other_obj=None):
        self.joysticks = {'LJX': 0,
                          'LJY': 0,
                          'RJX': 0,
                          'RJY': 0,
                          'LT': 0,
                          'RT': 0}

        self.buttons = {'Y': 0,
                        'B': 0,
                        'A': 0,
                        'X': 0,
                        'LB': 0,
                        'RB': 0,
                        'Select': 0,
                        'Start': 0,
                        'ThumbL': 0,
                        'ThumbR': 0}

        self.hats = {'HX': 0,
                     'HY': 0}

        if other_obj:
            self.joysticks = copy.deepcopy(other_obj.joysticks)
            self.buttons = copy.deepcopy(other_obj.buttons)
            self.hats = copy.deepcopy(other_obj.hats)

    def update(self, event):
        if event.type == 'Joystick':
            self.joysticks[event.code] = round(event.state / JOYSTICK_MAX, 4)
        elif event.type == 'Trigger':
            self.joysticks[event.code] = round(event.state / TRIGGER_MAX, 4)
        elif event.type == 'Hat':
            self.hats[event.code] = event.state
        elif event.type == 'Button':
            self.buttons[event.code] = event.state

    def clear(self):
        for k in self.buttons:
            self.buttons[k] = 0
        for k in self.joysticks:
            self.joysticks[k] = 0
        for k in self.hats:
            self.hats[k] = 0

    def is_button_held(self):
        return 1 in self.buttons.values()

    def __str__(self):
        return f'{self.joysticks} {self.buttons} {self.hats}'

    def __eq__(self, other):
        if type(other) is not ControllerStatus:
            return False

        return self.joysticks == other.joysticks and self.buttons == other.buttons and self.hats == other.hats


class Event:
    def __init__(self, event):
        self.type = None
        self.code = None
        self.state = None

        if event.ev_type == 'Absolute':
            if 'Z' in event.code:
                self.type = 'Trigger'
            elif 'HAT' in event.code:
                self.type = 'Hat'
            else:
                self.type = 'Joystick'
        elif event.ev_type == 'Key':
            self.type = 'Button'

        self.code = names[event.code] if event.code in names else event.code

        # add in deadzones for joysticks
        if self.type == 'Joystick' and abs(event.state) <= JOYSTICK_MAX * DEADZONE:
            self.state = 0
        else:
            self.state = event.state

    def __bool__(self):
        return self.type is not None

    def __str__(self):
        return f'{self.type} {self.code} {self.state}'


class ControllerThread(threading.Thread):
    def __init__(self, thread_id, name, status):
        threading.Thread.__init__(self, args=status)
        self.status = status
        self.threadID = thread_id
        self.name = name
        self.stop = False
        self.xboxController = None
        self.controller_delay = 20  # milliseconds

    def get_xbox_controller(self):
        xboxController = None

        # Get devices and make sure xbox controller is connected
        while not xboxController:
            for device in inputs.devices.gamepads:
                if device.name == XBOX_CONTROLLER_NAME:
                    print(f'Controller Found: {device.name}')
                    xboxController = device
                    xboxController.set_vibration(0.1, 0.1, 50)
                    break
            if not xboxController:
                print('Searching for controller...')
                time.sleep(5)
                inputs.devices._post_init()  # search for controllers again

        return xboxController

    def run(self):
        self.xboxController = self.get_xbox_controller()

        print('Entering controller loop...')
        while not self.stop:
            events = []
            try:
                events = self.xboxController.read()
            except inputs.UnpluggedError:
                print('\nController disconnected')
                self.status.buttons['Select'] = 1
                time.sleep(5)  # gives main thread time to turn off led
                self.status.clear()
                inputs.devices.gamepads = []
                self.xboxController = self.get_xbox_controller()

            for event in events:
                # print(f'{event.ev_type} {event.code} {event.state}')
                e = Event(event)
                if e:
                    self.status.update(e)
                    if e.code == 'Select' and e.state == 1:
                        self.stop = True
                        print('Exiting controller loop')

            time.sleep(0.002)
