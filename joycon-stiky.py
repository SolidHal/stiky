#!/usr/bin/python3

from datetime import datetime, timedelta
import time
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

async def eventProducer(queue, dev, stik, joycons):
    async for event in dev.async_read_loop():
        # determine hand for event
        joycon_hand = joycons.handleEvent(event, debug = False)
        if joycon_hand == None:
            continue
        # create QuadrantState and ButtonState from event
        quadState = toQuadrantState(joycon_hand.hand, joycon_hand.getStickQuad() )
        buttonState = toButtonState(joycon_hand.hand, joycon_hand.getButton() )
        # send QuadrantState to stiky, which sends keypresses when it is ready
        await stik.updateState(quadState, buttonState, queue)

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

    #producer, fill queue with events
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    producer_coro = eventProducer(queue, dev, stik, joycons)
    consumer_coro = stik.combineState(queue)
    loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
    loop.close()

    #consumer, consume queue events

    return

if __name__ == "__main__":
    main()
