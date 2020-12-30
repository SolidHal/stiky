#!/usr/bin/python3


from evdev import list_devices, InputDevice, categorize, ecodes, eventio_async
from math import sqrt, atan2, degrees
import asyncio


hand_left = "left"
hand_right = "right"
ecodes_left = {ecodes.ABS_X : "X", ecodes.ABS_Y: "Y", ecodes.BTN_THUMBL : "THUMB"}
ecodes_right = {ecodes.ABS_RX : "X" ,ecodes.ABS_RY : "Y", ecodes.BTN_THUMBR : "THUMB"}

centered = "CENTERED"
left = "LEFT"
right = "RIGHT"
up = "UP"
down = "DOWN"

cardinal_directions = [
    centered,
    left,
    right,
    up,
    down
]

up_left = "UP_LEFT"
up_right = "UP_RIGHT"
down_left = "DOWN_LEFT"
down_right = "DOWN_RIGHT"

angled_directions = [
    up_left,
    up_right,
    down_left,
    down_right
]

class joycon:

    X = 0
    Y = 0
    axis_map = {"X" : X, "Y": Y}

    thumb = 0
    button_map = {"THUMB" : thumb}

    syn_events = []
    hand = None
    hand_ecodes = None

    hyp = 0
    angle = 0

    # Time in seconds since epoch at which the last event occured
    stick_timestamp_sec = None
    # Microsecond portion of the timestamp.
    stick_timestamp_usec = None

    # Time in seconds since epoch at which the last event occured
    button_timestamp_sec = None
    # Microsecond portion of the timestamp.
    button_timestamp_usec = None

    center_tolerance = 7500

    four_direction = None
    eight_direction = None

    def _printif(self, debug, string):
        if debug:
            print("{} : {}".format(self.hand, string))

    def __init__(self, hand, center_tolerance = self.center_tolerance):
        self.hand = hand
        if hand == hand_left:
            self.hand_ecodes = ecodes_left
        elif hand == hand_right:
            self.hand_ecodes = ecodes_right
        else:
            raise KeyError
        self.center_tolerance = center_tolerance

    def _inDeadZone(self, value):
        value = abs(value)
        value = value - self.center_tolerance
        if value > 0:
            return False
        else:
            return True

    def _getFourDirection(self, angle):
        if (angle > 315 and angle <= 360) or ( angle >=0 and angle <= 45):
            direction = up
        if angle <= 135 and angle > 45:
            direction = left
        if angle > 135 and angle <= 225:
            direction = down
        if angle > 225 and angle <=315:
            direction = right

        return direction

    def _getEightDirection(self, angle):
        if (angle > 337.5 and angle <= 360) or ( angle >= 0 and angle <= 22.5):
            direction = up
        if angle <= 67.5 and angle > 22.5:
            direction = up_left
        if angle > 67.5 and angle <= 112.5:
            direction = left
        if angle > 112.5 and angle <= 157.5:
            direction = down_left
        if angle > 157.5 and angle <= 202.5:
            direction = down
        if angle > 202.5 and angle <= 247.5:
            direction = down_right
        if angle > 247.5 and angle <= 292.5:
            direction = right
        if angle > 292.5 and angle <= 337.5:
            direction = up_right

        return direction

    def _getAxisFromCode(self, code):
        axis_label = self.hand_ecodes.get(code)
        return self.axis_map.get(axis_label)

    def _getButtonFromCode(self, code):
        button_label = self.hand_ecodes.get(code)
        return self.button_map.get(button_label)

    def updateStick(self, event):
        code = event.code
        value = event.value
        if code not in self.hand_ecodes.keys():
            raise KeyError

        if self._inDeadZone(value):
            value = 0

        axis = self._getAxisFromCode(code)
        axis = value
        stick_timestamp_sec = event.sec
        stick_timestamp_usec = event.usec

    def decodeStick(self, debug = False):
        X = self.X
        Y = self.Y

        self.hyp = sqrt(pow(left_X, 2) + pow(left_Y, 2))

        if self.hyp == 0:
            self.angle = None
            self.four_direction = centered
            self.eight_direction = centered
        else:
            # 0 is vertical, goes counter clockwise from there
            self.angle = degrees(atan2(X, Y)) + 180.0
            angle = self.angle
            self.four_direction = self._getFourDirection(angle)
            self.eight_direction = self._getEightDirection(angle)


        self._printif(debug, "X: {} Y:{} HYP: {} ANGLE: {}".format(X, Y, self.hyp, self.angle))
        self._printif(debug, "four_direction: {} eight_direction".format(four_direction, eight_direction))

    def updateButtons(self, event):
        code = event.code
        value = event.value
        if code not in self.hand_ecodes.keys():
            raise KeyError

        button = self._getButtonFromCode(code)
        button = value
        button_timestamp_sec = event.sec
        button_timestamp_usec = event.usec

    def decodeButtons(self, debug = False):
        thumb = self.thumb
        if thumb:
            direction = PRESSED
        else:
            direction = RELEASED

        self._printif(debug, "thumb status: ".format(direction))




class Joycons:
    left = None
    right = None

    def __init__(self, left_joycon, right_joycon):
        self.left = left_joycon
        self.right = right_joycon

    def handleEvent(self, event):
        hand = None
        if event.code in self.left.hand_ecodes.keys():
            hand = self.left

        elif event.code in self.left.hand_ecodes.keys():
            hand = self.right

        if hand != None:
            if event.type == ecodes.EV_ABS:
                hand.updateStick(event)
                hand.decodeStick(debug = True)
            elif event.type == ecodes.EV_ABS:
                hand.updateButtons(event)
                hand.decodeButtons(debug = True)

        return




















if __name__ == "__main__":
    asyncio.run(main())
