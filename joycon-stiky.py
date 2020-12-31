#!/usr/bin/python3

import asyncio
from joycon import Joycon, Joycons, eventHand, hand_left, hand_right
from stiky import Stik, QuadrantState, ButtonState

from evdev import list_devices, InputDevice, categorize, ecodes, eventio_async


directionToQuad = {
    Joycon.centered : Stik.QC,
    Joycon.up : Stik.Q1,
    Joycon.right : Stik.Q2,
    Joycon.down : Stik.Q3,
    Joycon.left : Stik.Q4
}

directionToOct = {
    Joycon.centered : Stik.OC,
    Joycon.up : Stik.O1,
    Joycon.up_right : Stik.O2,
    Joycon.right : Stik.O3,
    Joycon.down_right : Stik.O4,
    Joycon.down : Stik.O5,
    Joycon.down_left : Stik.O6,
    Joycon.left : Stik.O7,
    Joycon.up_left : Stik.O8
}


def directionToQuadrant(direction):
    return directionToQuad.get(direction)

def directionToOctant(direction):
    return directionToOctant.get(direction)

def toQuadrantState(hand, direction):
    quad = directionToQuadrant(direction)
    return QuadrantState(hand, quad)

def toButtonState(hand, button):
    return ButtonState(hand, button)

async def main():

    print(list_devices())
    dev = InputDevice( list_devices()[0] )

    leftJoycon = Joycon(hand_left)
    rightJoycon = Joycon(hand_right)

    joycons = Joycons(leftJoycon, rightJoycon)

    leftStik = Stik(hand_left, {})
    rightStik = Stik(hand_right, {})

    stik = DoubleStik(leftStik, rightStik)

    async for event in dev.async_read_loop():
        # determine hand for event
        # handle event
        joycon_hand = joycons.handleEvent(event)
        # create QuadrantState and ButtonState from event
        quadState = toQuadrantState(joycon_hand.hand, joycon_hand.getStickQuad() )
        buttonState = toButtonState(joycon_hand.hand, joycon_hand.getButton() )

        # send QuadrantState to stiky, which sends keypresses when it is ready
        stik.updateStik(quadState, buttonState)



    return










if __name__ == "__main__":
    asyncio.run(main())
