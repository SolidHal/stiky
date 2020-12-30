#!/usr/bin/python3

from evdev import list_devices, InputDevice, categorize, ecodes
from math import sqrt, atan2, degrees

CENTER_TOLERANCE = 7500
STICK_MAX = 32767

print(list_devices())

dev = InputDevice( list_devices()[0] )

# Left hand
# code 0 = horizontal = ecodes.ABS_X
#  - right is positive
#  - left is negative
# code 1 = vertical = ecodes.ABS_Y
#  - up is negative
#  - down is positive
# code 317 = thumb btn = ecodes.BTN_THUMBL, EV_KEY event

# Right hand
# code 3 = horizontal = ecodes.ABS_RX
#  - right is positive
#  - left is negative
# code 4 = vertical = ecodes.ABS_RY
#  - up is negative
#   - down is positive
# code 318 = thumb btn = ecodes.BTN_THUMBR, EV_KEY event

def inDeadZone(value):
    value = abs(value)
    value = value - CENTER_TOLERANCE
    if value > 0:
        return False
    else:
        return True

class Sticks:
    left_X = 0
    left_Y = 0
    right_X = 0
    right_Y = 0

    syn_events = []

    def updateStick(self, code, value):
        if code == ecodes.ABS_X:
            self.left_X = value
        elif code == ecodes.ABS_Y:
            self.left_Y = value
        elif code == ecodes.ABS_RX:
            self.right_X = value
        elif code == ecodes.ABS_RY:
            self.right_Y = value

        return

    def decodeStick(self, hand):
        left_X = self.left_X
        left_Y = self.left_Y
        right_X = self.right_X
        right_Y = self.right_Y

        if hand == "left":
            left = sqrt(pow(left_X, 2) + pow(left_Y, 2))
            print("hand: {} X: {} Y:{}".format(hand, left_X, left_Y))

            #handle when we are at 0,0
            if (left_X == 0) and (left_Y == 0):
                print("hand: {} direction: centered ".format(hand))
                return

            # 0 is vertical, goes counter clockwise from there
            left_angle = degrees(atan2(left_X, left_Y)) + 180.0
            # print("hand: {} angle: {}".format(hand, right_angle))
            if (left_angle > 315 and left_angle <= 360) or ( left_angle >=0 and left_angle <= 45):
                print("hand: {} direction: up ".format(hand))
            if left_angle <= 135 and left_angle > 45:
                print("hand: {} direction: left ".format(hand))
            if left_angle > 135 and left_angle <= 225:
                print("hand: {} direction: down ".format(hand))
            if left_angle > 225 and left_angle <=315:
                print("hand: {} direction: right ".format(hand))

        elif hand == "right":
            right = sqrt(pow(right_X, 2) + pow(right_Y, 2))
            print("hand: {} X: {} Y:{}".format(hand, right_X, right_Y))

            #handle when we are at 0,0
            if (right_X == 0) and (right_Y == 0):
                print("hand: {} direction: centered ".format(hand))
                return

            # 0 is vertical, goes counter clockwise from there
            right_angle = degrees(atan2(right_X, right_Y)) + 180.0
            # print("hand: {} angle: {}".format(hand, right_angle))
            if (right_angle > 315 and right_angle <= 360) or ( right_angle >=0 and right_angle <= 45):
                print("hand: {} direction: up ".format(hand))
            if right_angle <= 135 and right_angle > 45:
                print("hand: {} direction: left ".format(hand))
            if right_angle > 135 and right_angle <= 225:
                print("hand: {} direction: down ".format(hand))
            if right_angle > 225 and right_angle <=315:
                print("hand: {} direction: right ".format(hand))

            return


def main():

    joycons = Sticks()

    for event in dev.read_loop():

        # combine all events between syn events

        if event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_THUMBL:
                if event.value == 1:
                    print("LEFT THUMB PRESSED")
                elif event.value == 0:
                    print("LEFT THUMB LIFTED")

            elif event.code == ecodes.BTN_THUMBR:
                if event.value == 1:
                    print("RIGHT THUMB PRESSED")
                elif event.value == 0:
                    print("RIGHT THUMB LIFTED")


        elif event.type == ecodes.EV_SYN:
            if len(joycons.syn_events) > 0:
                # combine all events between syn events
                print("------- SYN -------")
                for e in joycons.syn_events:
                    # print("code = {}, value = {}".format(e.code, e.value))
                    joycons.updateStick(e.code, e.value)
                    # print("{}, {}, {}, {}".format(left_X, left_Y, right_X, right_Y))
                joycons.decodeStick("left")
                joycons.decodeStick("right")
                print("----- END SYN -----")
                joycons.syn_events = []

        #read stick axis movement
        elif event.type == ecodes.EV_ABS:
            if not inDeadZone(event.value):
                joycons.syn_events.append(event)
            else:
                event.value = 0
                joycons.syn_events.append(event)

if __name__ == "__main__":
    main()
