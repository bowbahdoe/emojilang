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
            self.x += 1
        self.value = 0
        self.x -= length

    def store_string_vertically(self):
        string = input()
        length = len(string)
        for char in string:
            self.value = ord(char)
            self.y += 1
        self.value = 0
        self.y -= length
    
    def set_value_number(self):
        self.value = int(input())

    def _get_value(self):
        return self._cells[self._current_cell]

    def _set_value(self, new_value):
        self._cells[self._current_cell] = new_value
    
    def _get_current_cell(self):
        return self._current_cell
    
    def _set_current_cell(self, new_cell):
        self._current_cell = new_cell

    def _get_working_value(self):
        return self._working_value

    def _set_working_value(self, new_value):
        self._working_value = new_value

    working_value = property(_get_working_value, _set_working_value)

    current_cell = property(_get_current_cell, _set_current_cell)

    value = property(_get_value, _set_value)

class Interpreter(MemoryState):
    def __init__(self):
        '''
        Initializes the interpreter
        
        also builds the list of commands
        '''
        
        super().__init__()

        self.equivalents = {}
        
        ######################################################
        # Happy emojis add one to the value at the location, #
        # sad emojis subtract                                #
        ######################################################
        self.add_commands('self.value += 1', '😃', '😄')
        self.add_commands('self.value -= 1', '☹')

        ########################################################
        # Fruits and veggies add one, unhealthy foods subtract #
        ########################################################
        self.add_commands('self.value += 1', '🍏', '🍎', '🍐', '🍊',
                                             '🍋', '🍌', '🍉', '🍇',
                                             '🍓', '🍈', '🍒', '🍑',
                                             '🍍', '🍅', '🍆', '🌶',
                                             '🌽')

        self.add_commands('self.value -= 1', '🍠', '🍯', '🍞', '🧀',
                                             '🍗', '🍖', '🍤', '🍳',
                                             '🍔', '🍟', '🌭', '🍕',
                                             '🍝', '🌮', '🌯', '🍜',
                                             '🍲', '🍥', '🍣', '🍱',
                                             '🍛', '🍙', '🍚', '🍘',
                                             '🍢', '🍡', '🍧', '🍨',
                                             '🍦', '🍰', '🎂', '🍮',
                                             '🍬', '🍭', '🍫', '🍿',
                                             '🍩', '🍪')

        #####################################################
        # alcohol is really bad for you, so it subtracts 10 #
        #####################################################

        self.add_commands('self.value -= 10', '🍺','🍻','🍷','🍸',
                                              '🍹','🍾')

        ################################################
        # the joy emoji squares the value at the point #
        ################################################

        self.add_commands('self.value **= 2', '😂')

        ##############################################    
        # construction worker sets the working value #
        # as the value in the current cell           #
        ##############################################

        self.add_commands('self.working_value = self.value', '👷')

        ##################################################
        # the scream emoji sets the x coordinate to zero #
        ##################################################
        self.add_commands('self.x = 0', '😱')

        ###############################################
        # right and left pointing move right and left #
        ###############################################
        self.add_commands('self.x += 1', '👉')
        self.add_commands('self.x -= 1', '👈')

        ################################################
        # pointing up goes up, pointing down goes down #
        ################################################

        self.add_commands('self.y += 1', '🖕', '☝', '👆', '👍')
        self.add_commands('self.y -= 1', '👇', '👎')

        ######################################
        # upleft arrow goes upleft and so on #
        ######################################
        self.add_commands('self.y += 1; self.x -= 1', '↖')
        self.add_commands('self.y += 1; self.x += 1', '↗')
        self.add_commands('self.y += 1; self.x += 1', '↗')
        self.add_commands('self.y -= 1; self.x += 1', '↘')
        self.add_commands('self.y -= 1; self.x -= 1', '↙')

        ######################################################
        # double arrows move two in the direction they point #
        ######################################################

        self.add_commands('self.y += 2', '⏫')
        self.add_commands('self.y -= 2', '⏬')

        ####################################
        # punching fist increases z by one #
        # okay sign decreases z by one     #
        ####################################

        self.add_commands('self.z += 1', '👊')
        self.add_commands('self.z -= 1', '👌')

        #########################################################
        # hourglass and clocks go forwards in time              #
        # The Man in buisness suit levitating goes back in time #
        #########################################################
        
        self.add_commands('self.t += 1', '⌛', '⏳', '⏱', '⏰', 
                                          '⌚', '⏲', '🕰')
        self.add_commands('self.t -= 1', '🕴')

        ######################################################
        # sleepy face and open mouth surprised face store    #
        # strings vertically and horizontally respectively   #
        #                                                    #
        # when strings are stored the cell immediately after #
        # the string is zeroed (Just like a null terminated  #
        # string)                                            #
        ######################################################
        
        self.add_commands('self.store_string_vertically()', '😪')
        self.add_commands('self.store_string_horizontally()', '😮')

        #########################################################
        # thinking face waits for a number and stores it in the #
        # current cell                                          #
        #########################################################

        self.add_commands('self.set_value_number()', '🤔')

        ##################################################
        # four leafed clover puts a random value between #
        # the current value and zero (inclusive)         #
        #                                                #
        # The die emoji puts a random number between 1   #
        # and 6 in the cell                              #
        ##################################################

        self.add_commands('self.value = random.randrange(0, self.value + 1)', '🍀')
        self.add_commands('self.value = random.randrange(1, 7)','🎲')

        ##############################################
        # construction worker sets the working value #
        # as the value in the current cell           #
        ##############################################

        self.add_commands('self.working_value = self.value','👷')

        ####################################################
        # two people holding hands adds the current cell   #
        # to the working value and stores that in the cell #
        ####################################################
        
        self.add_commands('self.value += self.working_value',
                          '👫', '👬', '👭')

        ####################################################
        # two people kissing multiplies the current cell   #
        # to the working value and stores that in the cell #
        ####################################################

        self.add_commands('self.value *= self.working_value', '💏')


        ######################################################
        # sun and full moon w/ face start and close loops    # 
        # where it loops if the value at the end is not zero #
        #                                                    #
        # logic of moons is dealt with with decrementing     #
        # indents so we dont worry about it here and just    #
        # add it to the list of commands                     #
        #                                                    #
        ######################################################

        self.add_commands('while self.value != 0:', '🌞', '☀')
        self.add_commands('', '🌝', '🌑', '🌒', '🌓', 
                              '🌔', '🌕', '🌖', '🌗',
                              '🌘', '🌙', '🌛', '🌜')
        ##########################################################
        # Kissy face prints out the value as ASCII               #
        # Winky face prints a newline                            #
        # Nerd face prints out the value in the cell as a number #
        # because nerds and numbers amiright                     #
        ##########################################################

        self.add_commands('self.print_as_ASCII()', '😘')
        self.add_commands('print(file=self.output)', '😉')
        self.add_commands('print(self.value, end=\'\', file=self.output)', '🤓')

        ###########################################################
        # poop emoji dumps the entire stack, not pretty, dont use #
        ###########################################################
        self.add_commands('partial(print, self._cells)()', '💩')


    def add_commands(self, code, *commands):
        '''
        Takes the code that each command should represent
        and at least one command
        '''
        if not commands:
            return

        for command in commands:
            self.equivalents[command] = code

    def extract_emoji(self, filename):
        '''
        parses the source file, taking only the emoji that
        have defined behaviour into memory
        '''
        data = ''
        with open(filename) as emojfile:
            for line in emojfile:
                data += line
        data = [char for char in data if char in self.equivalents.keys()]
        code=''
        for i in data:
            code+=i
        return list(code)

    def make_py_code(self, code):
        '''
        alternative approach, generates and executes python code
        '''
        py_code = ''
        indentation_level = 0

        suns = ['🌞', '☀']
        moons = ['🌝', '🌑', '🌒', '🌓', \
                 '🌔', '🌕', '🌖', '🌗', \
                 '🌘', '🌙', '🌛', '🌜']
    

        for character in code:
            py_code += '    ' * indentation_level + self.equivalents[character] + '\n'
            if character in suns:
                indentation_level += 1
            if character in moons:
                indentation_level -= 1
    
        return py_code

    def interpret_code(self, filename):
        exec(self.make_py_code(self.extract_emoji(filename)))
if __name__ == '__main__':
    code_interpreter = Interpreter()
    code_interpreter.interpret_code(sys.argv[1])
