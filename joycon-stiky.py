#!/usr/bin/python3

import asyncio
import joycon
import stiky
from stiky import Stik, DoubleStik, QuadrantState, ButtonState

from evdev import list_devices, InputDevice, categorize, ecodes, eventio_async


directionToQuad = {
    joycon.centered : stiky.QC,
    joycon.up : stiky.Q1,
    joycon.right : stiky.Q2,
    joycon.down : stiky.Q3,
    joycon.left : stiky.Q4
}

directionToOct = {
    joycon.centered : stiky.OC,
    joycon.up : stiky.O1,
    joycon.up_right : stiky.O2,
    joycon.right : stiky.O3,
    joycon.down_right : stiky.O4,
    joycon.down : stiky.O5,
    joycon.down_left : stiky.O6,
    joycon.left : stiky.O7,
    joycon.up_left : stiky.O8
}


def directionToQuadrant(direction):
    return directionToQuad.get(direction)

def directionToOctant(direction):
    return directionToOctant.get(direction)

def toQuadrantState(hand, direction):
    if direction == None:
        print("direction is None!, hand is {}".format(hand))
    quad = directionToQuadrant(direction)
    return QuadrantState(hand, quad)

def toButtonState(hand, button):
    return ButtonState(hand, button)

def main():

    print(list_devices())
    dev = InputDevice( list_devices()[0] )
    print(list_devices()[0])

    leftJoycon = joycon.Joycon(joycon.hand_left)
    rightJoycon = joycon.Joycon(joycon.hand_right)

    joycons = joycon.Joycons(leftJoycon, rightJoycon)

    leftStik = Stik(joycon.hand_left, {})
    rightStik = Stik(joycon.hand_right, {})

    stik = DoubleStik(leftStik, rightStik)

    for event in dev.read_loop():
        # determine hand for event
        # handle event
        joycon_hand = joycons.handleEvent(event, debug = False)
        if joycon_hand == None:
            continue
        # create QuadrantState and ButtonState from event
        quadState = toQuadrantState(joycon_hand.hand, joycon_hand.getStickQuad() )
        buttonState = toButtonState(joycon_hand.hand, joycon_hand.getButton() )

        # send QuadrantState to stiky, which sends keypresses when it is ready
        stik.updateState(quadState, buttonState)



    return










if __name__ == "__main__":
    main()
    # asyncio.run(main())
