#!/usr/bin/python3
from __future__ import print_function
from collections import namedtuple
from collections import defaultdict
from functools import partial
import random
import sys


Location = namedtuple('Location',['x', 'y', 'z', 't'])

class MemoryState(object):
    '''
    Stores the state of the computation
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
        self._current_cell = Location(0,0,0,0)
        self._working_value = 0
        self.output = sys.stdout

    
    def get_x(self):
        return self._current_cell.x

    def set_x(self, new_x):
        self.current_cell = Location(new_x,
                                     self._current_cell.y,
                                     self._current_cell.z,
                                     self._current_cell.t)

    def get_y(self):
        return self.current_cell.y

    def set_y(self, new_y):
        self.current_cell = Location(self._current_cell.x,
                                     new_y,
                                     self._current_cell.z,
                                     self._current_cell.t)
    def get_z(self):
        return self.current_cell.z

    def set_z(self, new_z):
        self.current_cell = Location(self._current_cell.x,
                                     self._current_cell.y,
                                     new_z,
                                     self._current_cell.t)


    def get_time(self):
        return self.current_cell.t

    def set_time(self, new_time):
        self.current_cell = Location(self._current_cell.x,
                                     self._current_cell.y,
                                     self._current_cell.z,
                                     new_time)
        

    #sets up the dimensions as properties    
    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)
    t = property(get_time, set_time)

    def print_as_ASCII(self):
        print(chr(self.value), end='', file=self.output)

    def store_string_horizontally(self):
        string = input()
        length = len(string)
        for char in string:
            self.value = ord(char)
            self.current_cell = Location(self.current_cell.x+1,
                                         self.current_cell.y,
                                         self.current_cell.z,
                                         self.current_cell.t)
        self.value = 0

        self.current_cell = Location(self.current_cell.x-length,
                                     self.current_cell.y,
                                     self.current_cell.z,
                                     self.current_cell.t)

    def store_string_vertically(self):
        string = input()
        length = len(string)
        for char in string:
            self.value = ord(char)
            self.current_cell = Location(self.current_cell.x,
                                         self.current_cell.y+1,
                                         self.current_cell.z,
                                         self.current_cell.t)
        self.value = 0

        self.current_cell = Location(self.current_cell.x,
                                     self.current_cell.y-length,
                                     self.current_cell.z,
                                     self.current_cell.t)


    def print_value(self):
        print(self.value, end='', file=self.output)
    
    def set_value_number(self):
        self.value = int(input())

    def get_value(self):
        return self._cells[self._current_cell]

    def set_value(self, new_value):
        self._cells[self._current_cell] = new_value
    
    def get_current_cell(self):
        return self._current_cell
    
    def set_current_cell(self, new_cell):
        self._current_cell = new_cell

    def get_working_value(self):
        return self._working_value

    def set_working_value(self, new_value):
        self._working_value = new_value

    working_value = property(get_working_value, set_working_value)

    current_cell = property(get_current_cell, set_current_cell)

    value = property(get_value, set_value)

board = MemoryState()

command_equivalance = {

#Happy emojis add one to the value at the location,
#sad emojis subtract

    '😃': 'board.value += 1',
    '😄': 'board.value += 1',
    '☹': 'board.value -= 1',

#Fruits and veggies add one, unhealthy foods subtract
    '🍏': 'board.value += 1',
    '🍎': 'board.value += 1',
    '🍐': 'board.value += 1',
    '🍊': 'board.value += 1',
    '🍋': 'board.value += 1',
    '🍌': 'board.value += 1',
    '🍉': 'board.value += 1',
    '🍇': 'board.value += 1',
    '🍓': 'board.value += 1',
    '🍈': 'board.value += 1',
    '🍒': 'board.value += 1',
    '🍑': 'board.value += 1',
    '🍍': 'board.value += 1',
    '🍅': 'board.value += 1',
    '🍆': 'board.value += 1',
    '🌶': 'board.value += 1',
    '🌽': 'board.value += 1',


    '🍠': 'board.value -= 1',
    '🍯': 'board.value -= 1',
    '🍞': 'board.value -= 1',
    '🧀': 'board.value -= 1',
    '🍗': 'board.value -= 1',
    '🍖': 'board.value -= 1',
    '🍤': 'board.value -= 1',
    #we count the cooking emoji as unhealthy since it has a fried egg 
    '🍳': 'board.value -= 1',
    '🍔': 'board.value -= 1',
    '🍟': 'board.value -= 1',
    '🌭': 'board.value -= 1',
    '🍕': 'board.value -= 1',
    '🍝': 'board.value -= 1',
    '🌮': 'board.value -= 1',
    '🌯': 'board.value -= 1',
    '🍜': 'board.value -= 1',
    #Pot of food is unhealthy because it is a large serving size
    '🍲': 'board.value -= 1',
    '🍥': 'board.value -= 1',
    '🍣': 'board.value -= 1',
    '🍱': 'board.value -= 1',
    '🍛': 'board.value -= 1',
    '🍙': 'board.value -= 1',
    '🍚': 'board.value -= 1',
    '🍘': 'board.value -= 1',
    '🍢': 'board.value -= 1',
    '🍡': 'board.value -= 1',
    '🍧': 'board.value -= 1',
    '🍨': 'board.value -= 1',
    '🍦': 'board.value -= 1',
    '🍰': 'board.value -= 1',
    '🎂': 'board.value -= 1',
    '🍮': 'board.value -= 1',
    '🍬': 'board.value -= 1',
    '🍭': 'board.value -= 1',
    '🍫': 'board.value -= 1',
    '🍿': 'board.value -= 1',
    '🍩': 'board.value -= 1',
    '🍪': 'board.value -= 1',
    #alcohol is really bad for you, so it subtracts 10
    '🍺': 'board.value -= 10',
    '🍻': 'board.value -= 10',
    '🍷': 'board.value -= 10',
    '🍸': 'board.value -= 10',
    '🍹': 'board.value -= 10',
    '🍾': 'board.value -= 10',

#the joy emoji squares the value at the point
    '😂': 'board.value **= 2',

#the scream emoji sets the x coordinate to zero
    '😱': 'board.x = 0',

#right and left pointing move right and left
    '👉': 'board.x += 1',
    '👈': 'board.x -= 1',

#middle finger moves up,
    '🖕': 'board.y += 1',

#pointing finger up moves up
    '☝': 'board.y += 1',
    '👆': 'board.y += 1',
    '👍': 'board.y += 1',

#pointing down goes down
    '👇': 'board.y -= 1',
    '👎': 'board.y -= 1',

#upleft arrow goes upleft
    '↖': 'board.y += 1; board.x -= 1',

#upright arrow goes upright
    '↗': 'board.y += 1; board.x += 1',

#downright goes downright
    '↘': 'board.y -= 1; board.x += 1',

#downleft goes downleft
    '↙': 'board.y -= 1; board.x -= 1',

#doubleup arrow goes two up
    '⏫': 'board.y += 2',

#doubledown arrow goes down two
    '⏬': 'board.y -= 2',

#punching fist increases z by one
    '👊': 'board.z += 1',

#okay sign decreases z by one
    '👌': 'board.z -= 1',

#sleepy face waits for input then stores it vertically as a string
    '😪': 'board.store_string_vertically()',

#thinking face waits for a number
    '🤔': 'board.set_value_number()',

#kissy face prints out the value as ASCII
    '😘': 'board.print_as_ASCII()',

#sun and full moon w/ face start and close loops 
#where it loops if the value at the end is not zero
#in this dictionary to simplify parsing
    '🌞': 'while board.value != 0:',
    '☀': 'while board.value != 0:',
    '🌝': '',

#winky face prints a newline
    '😉': 'print(file=board.output)',

#open mouth suprised face waits for a string and stores it horizontally
#making sure that there is one zero at the end
    '😮': 'board.store_string_horizontally()',

#poop emoji dumps the entire stack, not pretty, dont use
    '💩': 'partial(print, board._cells)()',

#Die emoji puts a random value between 1 and 6 in the cell
    '🎲': 'board.value = random.randrange(1, 7)',

#nerd face prints out the value in the cell as a number
#because nerds and numbers amiright
    '🤓': 'board.print_value()',

#construction worker sets the working value as the value in the current cell
    '👷': 'board.working_value = board.value',

#two people holding hands adds the current cell to the working value and stores that in the cell
    '👫': 'board.value += board.working_value',
    '👬': 'board.value += board.working_value',
    '👭': 'board.value += board.working_value',

#two people kissing multiplies the current cell to the working value and stores that in the cell
    '💏': 'board.value *= board.working_value',

#hourglass and clocks go forwards in time
    '⌛': 'board.t += 1',
    '⏳': 'board.t += 1',
    '⏱': 'board.t += 1',
    '⏰': 'board.t += 1',
    '⌚': 'board.t += 1',
    '⏲': 'board.t += 1',
    '🕰': 'board.t += 1',

#The Man in buisness suit levitating goes back in time
    '🕴': 'board.t -= 1',

#four leafed clover puts a random value between the current value
#and zero
    '🍀': 'board.value = random.randrange(1, board.value)'


}

#we convert it to a default dict to deal with moons, since they are repetitive and all return nothing

command_equivalance = defaultdict(lambda: '', command_equivalance)

#Adds the moons to the dictionary
[command_equivalance[i] for i in ['🌝', '🌑', '🌒', '🌓', \
                                  '🌔', '🌕', '🌖', '🌗', \
                                  '🌘', '🌙', '🌛', '🌜']]

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

def make_py_code(code):
    '''
    alternative approach, generates and executes python code
    '''
    py_code = ''
    indentation_level = 0

    suns = ['🌞', '☀']
    moons = ['🌝', '🌑', '🌒', '🌓', \
             '🌔', '🌕', '🌖', '🌗', \
             '🌘', '🌙', '🌛', '🌜']

    used_flags = []
    possible_flags = []

    with open('flags.txt', 'r') as flags_file:
        for line in flags_file:
            possible_flags += line.split(' ')
    
    #for some reason split adds a newline to the last flag so we get rid of it here
    possible_flags[-1] = possible_flags[-1][:-1]
    
    for flag in possible_flags:
        if flag in code:
            code.replace(flag,ord(flag))

    for character in code:
        py_code += '    ' * indentation_level + command_equivalance[character] + '\n'
        if character in suns:
            indentation_level += 1
        if character in moons:
            indentation_level -= 1

    return py_code


if __name__ == '__main__':
    exec(make_py_code(extract_emoji(sys.argv[1])))
