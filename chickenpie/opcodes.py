EXIT = 0
CHICKEN = 1
ADD = 2
FOX = SUBTRACT = 3
ROOSTER = MULTIPLY = 4
COMPARE = 5
PICK = LOAD = 6
PECK = STORE = 7
FR = JUMP = 8
BBQ = CHAR = 9

names = {
    0: 'exit',
    1: 'chicken',
    2: 'add',
    3: 'fox',
    4: 'rooster',
    5: 'compare',
    6: 'pick',
    7: 'peck',
    8: 'fr',
    9: 'BBQ'
}


def get_name(opcode):
    return names[opcode] if opcode in names else 'push %d' % (opcode - 10)
