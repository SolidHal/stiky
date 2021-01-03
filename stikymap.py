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

#BUTTON STATE DICT KEYS
# QUADRANT INPUT BLOCKING:
block = "block"
# BUTTONS:
buttons = "buttons"
THUMB = "thumb"
# BUTTON STATES:
RELEASED = "released"
PRESSED = "pressed"
HELD = "held"


#GENERAL DICT KEYS
HAND = "hand"

#QUADRANT STATE DICT KEYS
FIGURE = "figure"
# for continaing holds/flicks
FLICK_HOLD = "flick_hold"
# then uses the BUTTON STATES above but, FLICKED == PRESSED

# maps dict keys
PRESSES = "presses"
HOLDS = "holds"
CLOCK = "clockwise"
COUNTERCLOCK = "counterclockwise"
# layer dict keys
SYMBOLS = "SYMBOLS"

hand1map = {
    PRESSES : {THUMB : ["space"], Q1 : ["esc"], Q2 : ["backspace"], Q3 : ["enter"], Q4: SYMBOLS},
    HOLDS   : {THUMB : ["shift", "cmd"], Q1 : ["cmd"], Q2 : ["ctrl", "shift"], Q3 : ["ctrl"], Q4: SYMBOLS},
    FIGURE :
    {
        Q1 :
        {
            CLOCK        : [["y"], ["b"], ["p"], ["q"]],
            COUNTERCLOCK : [["s"], ["d"], ["g"], ["'"]]
        },
        Q2 :
        {
            CLOCK        : [["n"], ["m"], ["f"], ["!"]],
            COUNTERCLOCK : [["a"], ["r"], ["x"], ["?"]]
        },
        Q3 :
        {
            CLOCK        : [["e"], ["l"], ["k"], ["@"]],
            COUNTERCLOCK : [["o"], ["u"], ["v"], ["w"]]
        },
        Q4 :
        {
            CLOCK        : [["t"], ["c"], ["z"], ["."]],
            COUNTERCLOCK : [["i"], ["h"], ["j"], [","]]
        }
    }

}

hand2map = {
    PRESSES : {THUMB : ["tab"], Q1 : ["up"], Q2 : ["right"], Q3 : ["down"], Q4: ["left"]},
    HOLDS   : {THUMB : ["shift"], Q1 : ["up"], Q2 : ["right"], Q3 : ["down"], Q4: ["left"]},
    FIGURE :
    {
        Q1 :
        {
            CLOCK        : [[], [], [], []],
            COUNTERCLOCK : [[], [], [], []]
        },
        Q2 :
        {
            CLOCK        : [[], [], [], []],
            COUNTERCLOCK : [[], [], [], []]
        },
        Q3 :
        {
            CLOCK        : [[], [], [], []],
            COUNTERCLOCK : [[], [], [], []]
        },
        Q4 :
        {
            CLOCK        : [[], [], [], []],
            COUNTERCLOCK : [[], [], [], []]
        }
    }
}

emptyhandmap = {
    PRESSES : {THUMB : [], Q1 : [], Q2 : [], Q3 : [], Q4: []},
    HOLDS   : {THUMB : [], Q1 : [], Q2 : [], Q3 : [], Q4: []},
    FIGURE :
    {
        Q1 :
        {
            CLOCK        : [[], [], [], []],
            COUNTERCLOCK : [[], [], [], []]
        },
        Q2 :
        {
            CLOCK        : [[], [], [], []],
            COUNTERCLOCK : [[], [], [], []]
        },
        Q3 :
        {
            CLOCK        : [[], [], [], []],
            COUNTERCLOCK : [[], [], [], []]
        },
        Q4 :
        {
            CLOCK        : [[], [], [], []],
            COUNTERCLOCK : [[], [], [], []]
        }
    }
}
