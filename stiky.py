#!/usr/bin/python3

from datetime import datetime, timedelta
import time
import asyncio
import joycon
from threading import Timer

hand1map = {

}

hand2map = {
    
}

    # need to handle 3 types of input
    # 1) rotation around quadrants, aka figures
    #    - note starting, ending quadrants
    #    - defined as movement from center, to quadrant A
    #      through 0-3 quadrants
    #      stopping in quadrant B
    #      and finally back to center
    #      quadrant B is allowed to be equal to A if 3 quadrants are moved through,
    #          EX:
    #           Q3 -> Q0 -> Q1 -> Q2 -> Q3 is legal
    #          but
    #           Q3 -> Q0 -> Q3 is *not* legal


    #  \  Q0   /
    #   \     /
    #    \   /
    #     \ /
    # Q3   O   Q1
    #     / \
    #    /   \
    #   /     \
    #  /  Q2   \

    # 2) single quadrant inputs, flicks and holds
    #     - defined as a movement from center, to quadrant A, and back to center with no other quadrants in between
    #     - these movements can have different behaviors when the time spend in quadrant A is short (a flick) or long (a hold)

    # 3) center button press
    #    - the center of the "joystick" is a button
    #    - different behaviors can be mapped for pressing or holding the button


    # We can break these types of input into the following events:
    #   Exited center
    #   Entered center
    #   Entered quadrant A
    #   Exited quadrant A
    #   Pressed Center
    #   Released Center

    #   And if we treat center as a special "quadrant" we can further simplify it to
    #   Entered quadrant A
    #   Exited quadrant A
    #   Pressed Center
    #   Released Center


    #   Finally, if we want to expand the number of buttons we can further abstract it to
    #   Entered quadrant A
    #   Exited quadrant A
    #   Pressed Button
    #   Released Button

    #   To then turn those events back into inputs we can do the following:
    #   When the special center quadrant is observed, that indicates the end of a "figure"
    #     - this handles flicks, and full figures
    #   When quadrant A is observed for longer than <some small time> this is considered a hold
    #   When a button press is observed for longer than <some small time> this is considered a hold
    #   When a button release is observed, but no button hold is observed this is considered a press


class QuadrantState:
    quadrant = None
    timestamp = None
    hand = None
    keepAlive = None
    def __init__(self, hand, quadrant, timestamp = None, keepAlive = False):
        self.hand = hand
        self.quadrant = quadrant
        self.keepAlive = keepAlive
        if timestamp == None:
                 self.timestamp = time.time()
        else:
                 self.timestamp = timestamp


    def __str__(self):
        return "hand: {}, quadrant: {}".format(self.hand, self.quadrant)

    def __repr__(self):
        return "hand: {}, quadrant: {}".format(self.hand, self.quadrant)

class ButtonState:
    button = None
    timestamp = None
    hand = None
    keepAlive = None
    def __init__(self, hand, button, timestamp = None, keepAlive = False):
        self.hand = hand
        self.button = button
        self.keepAlive = keepAlive
        if timestamp == None:
                 self.timestamp = time.time()
        else:
                 self.timestamp = timestamp


QC = 0
Q1 = 1
Q2 = 2
Q3 = 3
Q4 = 4

OC = 0
O1 = 0.5
O2 = 1
O3 = 1.5
O4 = 2
O5 = 2.5
O6 = 3
O7 = 3.5
O8 = 4

Quadrants = [
    QC,
    Q1,
    Q2,
    Q3,
    Q4
]

Octants = [
    OC,
    O1,
    O2,
    O3,
    O4,
    O5,
    O6,
    O7,
    O8
]

figureQuadrants = [
    QC,
    Q1,
    Q2,
    Q3,
    Q4
]

class Stik:
    # QC = "Center Quadrant"
    # Q1 = "Top Quadrant"
    # Q2 = "Right Quadrant"
    # Q3 = "Bottom Quadrant"
    # Q4 = "Left Quadrant"
    # statics


    PRINTED = False

    # number of ms until a hold is triggered
    HOLD_TIME = None
    HOLD_TIME_DELTA = None

    # a flick is detected when the quadrant is entered for less than FLICK_TIME ms
    FLICK_TIME = None
    FLICK_TIME_DELTA = None

    # QC -> Q1 -> Q2 ->Q3 -> Q4 -> Q1 -> QC longest valid figure
    # possible future expansion: do a full loop, then a valid pattern to get the shifted version of the valid pattern
    MAX_FIGURE_LENGTH = 7

    # QC -> QX -> QY -> QC where QX/QY cannot be QC is the shortest figure length
    MIN_FIGURE_LENGTH = 4

    # store configuration
    stikHardware = None
    stikMap = None

    # track the quadrants and buttons observed
    # store a list of QuadrantEvents
    quadrantsObserved = []
    buttonsObserved = []

    # stores the quadrant held until a release event
    current_hold = None
    quadrant_hold_thread = None

    def __init__(self, hand, stikMap, hold_time = 400, flick_time = 200):
        self.hand = hand
        self.stikMap = stikMap
        self.HOLD_TIME = hold_time
        self.HOLD_TIME_DELTA = self.HOLD_TIME/1000.0
        self.FLICK_TIME = flick_time
        self.FLICK_TIME_DELTA = self.FLICK_TIME/1000.0


    # pass in some degree motion from the analog stick
    # returns what quadrant the stick is in
    def parseAnalogStick():
        return

    # pass in current button states
    # returns state information for updateState
    def parseButton():
        return

    def resetQuadrantsObserved(self):
        self.quadrantsObserved = []

    def resetButtonsObserved(self):
        self.buttonsObserved = []

    def previousQuadrantState(self):
        if len(self.quadrantsObserved) == 0:
            return None
        return self.quadrantsObserved[-1]

    def previousButtonState(self):
        if len(self.buttonsObserved) == 0:
            return None
        return self.buttonsObserved[-1]


    def _printif(self, debug, string):
        if debug:
            print("{} : {}".format(self.hand, string))

    def legalFigure(self, debug = False):

        # need both incrementing and decrementing checks to avoid 4,1,4 and 1,4,1 issues
        def isIncrementing(stateA, stateB):
            # handle the special wrap around case
            if (stateA.quadrant == Q4 and stateB.quadrant == Q1):
                return True
            elif (stateA.quadrant - stateB.quadrant) == -1:
                return True
            return False

        def isDecrementing(stateA, stateB):
            # handle the special wrap around case
            if (stateA.quadrant == Q1 and stateB.quadrant == Q4):
                return True
            elif (stateA.quadrant - stateB.quadrant) == 1:
                return True
            return False


        incrementing = None
        decrementing = None
        quadrantsObserved = self.quadrantsObserved
        figureLength = len(quadrantsObserved)

        # check figure length
        if (( figureLength < self.MIN_FIGURE_LENGTH ) and ( figureLength > self.MAX_FIGURE_LENGTH )):
            self._printif(debug, "ERROR: FIGURE TOO LONG")
            return False

        # check completion case, last quadrant should be QC
        if not quadrantsObserved[-1].quadrant == QC:
            self._printif(debug, "ERROR: FIGURE DOESN'T COMPLETE WITH QC; ends with {}".format(quadrantsObserved[-1].quadrant))
            return False

        # check base case, 0 ->1 should be QC -> QX
        if not quadrantsObserved[0].quadrant == QC:
            self._printif(debug, "ERROR: FIGURE DOESN'T HAVE PROPER BASE CASE")
            return False

        # ensure we didn't allow the same quadrant twice
        # this combined with the checks above for QC at the start and end ensure the start and end transitions are QC -> QX, QY -> QC
        for n in range(len(quadrantsObserved) - 1):
            if quadrantsObserved[n].quadrant == quadrantsObserved[n+1].quadrant:
                self._printif(debug, "ERROR: FIGURE HAS DUPLICATE QUADRANTS")
                return False

        # determine incrementing or decrementing by looking at first non-starting transition, aka 1 -> 2
        incrementing = isIncrementing(quadrantsObserved[1], quadrantsObserved[2])
        decrementing = isDecrementing(quadrantsObserved[1], quadrantsObserved[2])
        if incrementing:
                self._printif(debug, "FIGURE IS INCREMENTING")
        elif decrementing:
                self._printif(debug, "FIGURE IS DECREMENTING")


        # for ordering, once we being incrementing quadrants or decrementing quadrants we must continue incrementing or decrementing until QC is seen
        # check ordering for 2 -> 3, etc, up to before the last. We checked the last was QC above.
        orderQuadrants = quadrantsObserved[1:-1]
        for i, j in zip(orderQuadrants, orderQuadrants[1:]):
            if (incrementing and incrementing == isIncrementing(i, j)) or (decrementing and decrementing == isDecrementing(i,j)):
                continue
            else:
                self._printif(debug, "ERROR: FIGURE IS INCREMENTING AND DECREMENTING; First offending pair: {} to {} ".format(i.quadrant, j.quadrant))
                return False

        return True

    def _holdQuadrant(self, quadrantState):
        print("HOLD TO {} OBSERVED".format(quadrantState.quadrant))
        self.current_hold = quadrantState.quadrant



    # pass in current Analog Stick and Button information from parse functions
    # takes a QuadrantState and a ButtonState object
    def updateState(self, quadrantState, buttonState):
    # need to turn quadrantsObsereved and buttonsObseved from each hand into valid movements

        #Need to be able to differentiate short and long entries, and only care about changes in quadrant or long holds in non-QC
        #Add the current quadrant to quadrant observed if it is not the most recent quadrant, and not QC
        # Holds only "count" if we transitions from QC with no previous transitions


        figureLength = len(self.quadrantsObserved)
        #TODO: update button state for stik
        self.buttonsObserved.append(buttonState)

        #initial state, nothing observed yet.
        # *should* only ever add QC, as ending and starting occurs at QC
        if figureLength == 0:
            self.quadrantsObserved.append(quadrantState)
            return

        previousQuadrant = self.previousQuadrantState().quadrant
        previousTimestamp = self.previousQuadrantState().timestamp


        print("figure length = {}, previousQuadrant = {}, previousTimestamp = {},  currentQuadrant = {}, currentTimestamp = {} ".format(figureLength, previousQuadrant, previousTimestamp, quadrantState.quadrant, quadrantState.timestamp))


        # detect a hold release. All other movements on this Stik are invalid until the hold is released.
        if quadrantState.quadrant == QC and previousQuadrant != None and self.current_hold != None:
            print("HOLD TO {} RELEASED".format(self.current_hold))
            self.quadrant_hold_thread = None
            self.current_hold = None
            self.resetQuadrantsObserved()
            self.quadrantsObserved.append(quadrantState)
            #TODO, pass this information along in a reasonable format
            return

        # create a timer on possible hold start
        # after HOLD_TIME_DELTA, trigger hold state
        # cancel timer thread when:
        #   any other state detected
        if self.quadrant_hold_thread != None and previousQuadrant != quadrantState.quadrant:
            print("kill thread")
            self.quadrant_hold_thread.cancel()
            self.quadrant_hold_thread = None

        #idle state, only QC observed, no change in state, existing in QC has no "hold"
        #must update observed states with most recent so we have accurate flick timestamp comparisons
        if ( previousQuadrant == QC) and ( figureLength == 1 ) and quadrantState.quadrant == QC:
            self.resetQuadrantsObserved()
            self.quadrantsObserved.append(quadrantState)
            return

        # hold state, only QC -> QX observed, kick off thread
        if previousQuadrant == QC and quadrantState.quadrant != QC and (figureLength == 1) and quadrantState.quadrant != self.current_hold and self.quadrant_hold_thread == None:
            self.quadrant_hold_thread = Timer(self.HOLD_TIME_DELTA, self._holdQuadrant, args = [quadrantState])
            self.quadrantsObserved.append(quadrantState)
            print("start thread")
            self.quadrant_hold_thread.start()
            return


        # flick state, only QC -> QX -> QC observed, and for < FLICK_TIME_DELTA
        delta_s = time.time() - previousTimestamp
        if previousQuadrant != QC and quadrantState.quadrant == QC and ( figureLength == 2 ) and (delta_s < self.FLICK_TIME_DELTA) :
            print("FLICK TO {} OBSERVED".format(previousQuadrant))
            #TODO, pass this information along in a reasonable format
            self.resetQuadrantsObserved()
            self.quadrantsObserved.append(quadrantState)
            return


        # figure end condition:
        # we are in QC
        # we have seen at least QC -> QX -> QY -> QC where QX/QY cannot be QC
        # we have to check figure "legality" here
        #  - min/max length
        #  - ordering
        # if we check at time of add, can we end up with nonsense movements adding up into a valid figure?
        # We would like to enforce that anything after an invalid movement is invalid, and ignore the figure when it tries to "complete" so I think enforcement should be done
        # here instead of add
        # for ordering, once we being incrementing quadrants or decrementing quadrants we must continue incrementing or decrementing until QC is seen
        if previousQuadrant != QC and quadrantState.quadrant == QC:
            self.quadrantsObserved.append(quadrantState)
            if self.legalFigure(debug=True):
                print("FIGURE OBSERVED: {}".format(self.quadrantsObserved))
                #TODO, pass this information along in a reasonable format
            else:
                print("IGNORING ILLEGAL FIGURE OBSERVED: {}".format(self.quadrantsObserved))

            self.resetQuadrantsObserved()
            self.quadrantsObserved.append(quadrantState)
            return

        # new state, QX -> QY observed. need to confirm it is a valid transition
        # valid quadrants for figures are QC through Q4
        # QC can transition to any quadrant besides itself
        # all other quadrants can only transition to the adjacent ones
        if quadrantState.quadrant != QC and quadrantState.quadrant != previousQuadrant:
            # add and check legality later, the user made the input so don't just ignore it here
            self.quadrantsObserved.append(quadrantState)
            return


        return


# pass in the stik states, and generate keypresses
class DoubleStik:


    left = None
    right = None

    left_state = None
    right_state = None

    def __init__(self, left_stik, right_stik):
        self.left = left_stik
        self.right = right_stik

    def updateState(self, analogState, buttonState):
        if analogState.hand == "left":
            self.left.updateState(analogState, buttonState)
        elif analogState.hand == "right":
            self.right.updateState(analogState, buttonState)

        #TODO: take the states from both hands and combine them, then create a keypress when in a valid state
        # not every update state will generate a keypress
        return

    def keepAlive(self):
        self.left.keepAlive()
        self.right.keepAlive()

    def sendKeypress():
        #TODO: pick method to send keypress events to the OS
        return

    # poll the stiks and manage state
def main():

    hand1 = Stik()
    hand2 = Stik()

    while(true):
        analogState = hand1.parseAnalogStick()
        buttonState = hand1.parseButton()
        hand1.updateState(analogState, buttonState)
        analogState = parseAnalogStick()
        buttonState = parseButton()
        hand2.updateState(analogState, buttonState)
        keypress = doubleStik(hand1, hand2)
        sendKeypress(keypress)


    return

