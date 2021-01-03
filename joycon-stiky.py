#!/usr/bin/python3

from datetime import datetime, timedelta
import time
import asyncio
import joycon
import stiky
from stiky import Stik, DoubleStik, QuadrantState, ButtonState
import stikymap

from evdev import list_devices, InputDevice, categorize, ecodes, eventio_async


directionToQuad = {
    joycon.centered : stikymap.QC,
    joycon.up : stikymap.Q1,
    joycon.right : stikymap.Q2,
    joycon.down : stikymap.Q3,
    joycon.left : stikymap.Q4
}

directionToOct = {
    joycon.centered : stikymap.OC,
    joycon.up : stikymap.O1,
    joycon.up_right : stikymap.O2,
    joycon.right : stikymap.O3,
    joycon.down_right : stikymap.O4,
    joycon.down : stikymap.O5,
    joycon.down_left : stikymap.O6,
    joycon.left : stikymap.O7,
    joycon.up_left : stikymap.O8
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
    print (dev.name)
    if dev.name != "Nintendo Switch Combined Joy-Cons":
        print("ERROR! COMBINED JOYCONS ARE NOT AVAILABLE")
        return

    leftJoycon = joycon.Joycon(joycon.hand_left)
    rightJoycon = joycon.Joycon(joycon.hand_right)

    joycons = joycon.Joycons(leftJoycon, rightJoycon)

    leftStik = Stik(joycon.hand_left, stikymap.hand1map)
    rightStik = Stik(joycon.hand_right, stikymap.hand2map)

    stik = DoubleStik(leftStik, rightStik)

    #producer, fill queue with events
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    producer_coro = eventProducer(queue, dev, stik, joycons)
    consumer_coro = stik.translateState(queue)
    loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
    loop.close()

    #consumer, consume queue events

    return

if __name__ == "__main__":
    main()
