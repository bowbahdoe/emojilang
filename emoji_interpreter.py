from __future__ import print_function
from pyparsing import nestedExpr
from collections import namedtuple
from collections import defaultdict
from functools import partial
import random
import sys

Location = namedtuple('Location',['x', 'y'])

def set_value_one_char(board):
    board.value = ord(sys.stdin.read(1))

def set_value_number(board):
    board.value = int(input())

class HappyField(object):
    '''
    The happiness field keeps track of all the
    happiness values in the board
    '''
    def __init__(self):
        '''
        Initializes the field of happiness
        '''
        ############################################################
        # we use default dict so that all cells go to zero         #
        # by default and we do not have to handle explicit setting #
        # of those values                                          #
        # and we keep track of the current cell                    #
        # using a named tuple so that we can access with .x and .y #
        ############################################################

        self._cells = defaultdict(lambda: 0)
        self._current_cell = Location(0,0)

    def move_up(self, distance=1):
        self._current_cell = Location(self._current_cell.x,
                                      self._current_cell.y+distance)
    def move_down(self, distance=1):
        self._current_cell = Location(self._current_cell.x,
                                      self._current_cell.y-distance)
    def move_left(self, distance=1):
        self._current_cell = Location(self._current_cell.x-distance,
                                      self._current_cell.y)
    def move_right(self, distance=1):
        self._current_cell = Location(self._current_cell.x+distance,
                                      self._current_cell.y)
    def move_upleft(self):
        self.move_up()
        self.move_left()

    def move_upright(self):
        self.move_up()
        self.move_right()

    def move_downleft(self):
        self.move_down()
        self.move_left()

    def move_downright(self):
        self.move_down()
        self.move_right()

    def increment(self):
        self._cells[self._current_cell] += 1
    
    def decrement(self):
        self._cells[self._current_cell] -= 1
    
    def get_x(self):
        return self._current_cell.x

    def set_x(self, new_x):
        self._current_cell = Location(new_x,
                                      self._current_cell.y)

    def get_y(self):
        return self._current_cell.y

    def set_y(self, new_y):
        self._current_cell = Location(self._current_cell.x,
                                      new_y)
    def print_as_ASCII(self):
        print(chr(self.value), end='')

    def square(self):
        self._cells[self._current_cell] = self._cells[self._current_cell]**2
    
    def set_value_randomly(self, start=0, stop=2):
        self.value = random.randrange(start, stop)
    
    def print_value(self):
        print(self.value, end='')

    def get_value(self):
        return self._cells[self._current_cell]

    def set_value(self, new_value):
        self._cells[self._current_cell] = new_value
    
    def get_current_cell(self):
        return self._current_cell
    
    def set_current_cell(self, new_cell):
        self._current_cell = new_cell

    current_cell = property(get_current_cell, set_current_cell)

    value = property(get_value, set_value)

board = HappyField()

command_equivalance = {

#Happy emojis add one to the value at the location,
#sad emojis subtract

    '😃': board.increment,
    '😄': board.increment,
    '☹': board.decrement,

#the joy emoji squares the value at the point
    '😂': board.square,

#the scream emoji sets the x coordinate to zero
    '😱': partial(board.set_x, 0),

#right and left pointing move right and left
    '👉': board.move_right,
    '👈': board.move_left,

#middle finger moves up,
    '🖕': board.move_up,

#pointing finger up moves up
    '☝': board.move_up,
    '👆': board.move_up,
    '👍': board.move_up,

#pointing down goes down
    '👇': board.move_down,
    '👎': board.move_down,

#upleft arrow goes upleft
    '↖': board.move_upleft,

#upright arrow goes upright
    '↗': board.move_upright,

#downright goes downright
    '↘': board.move_downright,

#downleft goes downleft
    '↙': board.move_downleft,

#doubleup arrow goes two up
    '⏫': partial(board.move_up, 2),

#doubledown arrow goes down two
    '⏬': partial(board.move_down, 2),

#sleepy face waits for input then stores it in the cell
    '😪': partial(set_value_one_char, board),

#thinking face waits for a number
    '🤔': partial(set_value_number,board),

#kissy face prints out the value as ASCII
    '😘': board.print_as_ASCII,

#sun and full moon w/ face start and close loops 
#where it loops if the value at the end is not zero
#in this dictionary to simplify parsing
    '🌞': 'while(data[x][y]){\n',
    '☀': 'while(data[x][y]){\n',
    '🌝': '}',

#winky face prints a newline
    '😉': print,

#open mouth suprised face waits for one char of input
    '😮': partial(set_value_one_char, board),

#poop emoji dumps the entire stack, not pretty, dont use
    '💩': partial(print, board._cells),

#Die emoji puts a random value between 1 and 6 in the cell
    '🎲': partial(board.set_value_randomly, 1, 7),

#nerd face prints out the value in the cell as a number
#because nerds and numbers amiright
    '🤓': board.print_value
}

class Loop(object):
    def __init__(self, commands):
        self.commands = commands

    def run(self, board):
        print(self.commands)
        for i in self.commands:
            if type(i) == type(self):
                i.run()
                continue
            else:
                command_equivalance[i]()
        if board.value == 0:
            return
        else:
            self.run(board)

def extract_emoji(filename):
    data = ''
    with open(filename) as bffile:
        for line in bffile:
            data += line
    data = [char for char in data if char in command_equivalance.keys()]
    code=''
    for i in data:
        code+=i
    return code


def make_loops(code):
    sun_indexes = []
    moon_indexes = []
    code = list(code)
    suns = ['🌞', '☀']
    moons = ['🌝']
    final_code = []
    
    for command in code:
        if command in (suns+moons):
            break
    else:
        return code

    counter = 0
    for index, command in enumerate(code):
        if command in suns:
            sun_indexes.append(index)
            counter+=1
        elif command in moons:
            moon_indexes.append(index)
            counter-=1
        if counter == 0 and command not in (moons+suns):
            final_code.append(command)
            return final_code + make_loops(code[index+1:])

        elif counter == 0:
            return final_code + [Loop(code[sun_indexes[0]+1:moon_indexes[-1]])] + make_loops(code[moon_indexes[-1]+1:])
    
    print(final_code)
    
    if len(sun_indexes) != len(moon_indexes):
        raise Exception("Suns do not equal moons, life is out of balance")
    
    
    
    


if __name__ == '__main__':
    a = make_loops(extract_emoji('examples/add.emoj'))

    for i in a:
        if type(i) != Loop:
            command_equivalance[i]()
        else:
            i.run(board)
    pass

