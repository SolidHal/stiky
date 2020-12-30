#!/usr/bin/python3

from evdev import list_devices, InputDevice, categorize, ecodes
from math import sqrt, atan2, degrees

CENTER_TOLERANCE = 10000
STICK_MAX = 32767

print(list_devices())

dev = InputDevice( list_devices()[0] )
axis = {
    ecodes.ABS_X: 'ls_x', # 0 - 65,536   the middle is 32768
    ecodes.ABS_Y: 'ls_y',
    ecodes.ABS_Z: 'rs_x',
    ecodes.ABS_RZ: 'rs_y',
    ecodes.ABS_BRAKE: 'lt', # 0 - 1023
    ecodes.ABS_GAS: 'rt',

    ecodes.ABS_HAT0X: 'dpad_x', # -1 - 1
    ecodes.ABS_HAT0Y: 'dpad_y'
}

center = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

last = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

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
            left_angle = degrees(atan2(left_X, left_Y)) + 180.0

            #right
            if left_X > abs(left_Y):
                print("hand: {} direction: right ".format(hand))
            #left
            elif abs(left_X) > left_Y:
                print("hand: {} direction: left ".format(hand))
            #up
            elif abs(left_Y) > left_X:
                print("hand: {} direction: up ".format(hand))
            #down
            elif left_Y > abs(left_X):
                print("hand: {} direction: up ".format(hand))

        elif hand == "right":
            right = sqrt(pow(right_X, 2) + pow(right_Y, 2))
            right_angle = degrees(atan2(right_X, right_Y)) + 180.0

            # 0 is vertical

            print("hand: {} angle: {}".format(hand, right_angle))
            #TODO: correct these ranges to account to 0 being the top
            # make deadzone events set the axis value to 0 to clean up behavior

            # if (right_angle > 315 and right_angle <= 360) or ( right_angle >=0 and right_angle <= 45):
            #     print("hand: {} direction: right ".format(hand))
            # if right_angle <= 135 and right_angle > 45:
            #     print("hand: {} direction: up ".format(hand))
            # if right_angle > 135 and right_angle <= 225:
            #     print("hand: {} direction: left ".format(hand))

            # if right_angle > 225 and right_angle <=315:
            #     print("hand: {} direction: down ".format(hand))

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
            #TODO: move this to the processing portion, so we can set the X/Y values
            # to 0 when we are in the deadzone
            if not inDeadZone(event.value):
                joycons.syn_events.append(event)


        # if axis[ event.code ] in [ 'ls_x', 'ls_y', 'rs_x', 'rs_y' ]:
        #     last[ axis[ event.code ] ] = event.value

        #     value = event.value - center[ axis[ event.code ] ]

        #     if abs( value ) <= CENTER_TOLERANCE:
        #         value = 0

        #     if axis[ event.code ] == 'rs_x':
        #         if value < 0:
        #             print('left')
        #         else:
        #             print('right')
        #         print( value )

        #     elif axis[ event.code ] == 'ls_y':
        #         if value < 0:
        #             print('foreward')
        #         else:
        #             print('backward')
        #         print( value )


if __name__ == "__main__":
    main()
