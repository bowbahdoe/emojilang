#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import namedtuple
from collections import defaultdict
from functools import partial
import argparse
import random
import sys
import io


Location = namedtuple('Location', ['x', 'y', 'z', 't'])

class MemoryState(object):
    '''
    Stores the state of the computation
    '''
    def __init__(self):
        '''
        Initializes the Memory State
        '''
        ############################################################
        # we use default dict so that all cells go to zero         #
        # by default and we do not have to handle explicit setting #
        # of those values                                          #
        # and we keep track of the current cell                    #
        # using a named tuple so that we can access with .x and .y #
        ############################################################

        self._cells = defaultdict(lambda: 0)
        self.current_cell = Location(0,0,0,0)
        self.working_value = 0
        self.output = sys.stdout

    
    def get_x(self):
        return self.current_cell.x

    def set_x(self, new_x):
        self.current_cell = Location(new_x,
                                     self.current_cell.y,
                                     self.current_cell.z,
                                     self.current_cell.t)

    def get_y(self):
        return self.current_cell.y

    def set_y(self, new_y):
        self.current_cell = Location(self.current_cell.x,
                                     new_y,
                                     self.current_cell.z,
                                     self.current_cell.t)
    def get_z(self):
        return self.current_cell.z

    def set_z(self, new_z):
        self.current_cell = Location(self.current_cell.x,
                                     self.current_cell.y,
                                     new_z,
                                     self.current_cell.t)


    def get_time(self):
        return self.current_cell.t

    def set_time(self, new_time):
        self.current_cell = Location(self.current_cell.x,
                                     self.current_cell.y,
                                     self.current_cell.z,
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
        starting_x = self.x
        for char in string:
            self.value = ord(char)
            self.x += 1
        self.value = 0
        self.x = starting_x

    def store_string_vertically(self):
        string = input()
        starting_y = self.y
        for char in string:
            self.value = ord(char)
            self.y += 1
        self.value = 0
        self.y = starting_y
    
    def set_value_number(self):
        self.value = int(input())

    def _get_value(self):
        return self._cells[self.current_cell]

    def _set_value(self, new_value):
        self._cells[self.current_cell] = new_value

    value = property(_get_value, _set_value)

class Interpreter(MemoryState):
    def __init__(self):
        '''
        Initializes the interpreter
        
        also builds the list of commands
        '''
        
        super(Interpreter, self).__init__()

        self.equivalents = {}
        self.block_starters = set()
        self.block_enders = set()
        
        ######################################################
        # Happy emojis add one to the value at the location, #
        # sad emojis subtract                                #
        ######################################################
        self.add_commands('self.value += 1', u'😃', u'😄')
        self.add_commands('self.value -= 1', u'☹')

        ########################################################
        # Fruits and veggies add one, unhealthy foods subtract #
        ########################################################
        self.add_commands('self.value += 1', u'🍏', u'🍎', u'🍐', u'🍊',
                                             u'🍋', u'🍌', u'🍉', u'🍇',
                                             u'🍓', u'🍈', u'🍒', u'🍑',
                                             u'🍍', u'🍅', u'🍆', u'🌶',
                                             u'🌽')

        self.add_commands('self.value -= 1', u'🍠', u'🍯', u'🍞', u'🧀',
                                             u'🍗', u'🍖', u'🍤', u'🍳',
                                             u'🍔', u'🍟', u'🌭', u'🍕',
                                             u'🍝', u'🌮', u'🌯', u'🍜',
                                             u'🍲', u'🍥', u'🍣', u'🍱',
                                             u'🍛', u'🍙', u'🍚', u'🍘',
                                             u'🍢', u'🍡', u'🍧', u'🍨',
                                             u'🍦', u'🍰', u'🎂', u'🍮',
                                             u'🍬', u'🍭', u'🍫', u'🍿',
                                             u'🍩', u'🍪')

        #####################################################
        # alcohol is really bad for you, so it subtracts 10 #
        #####################################################

        self.add_commands('self.value -= 10', u'🍺', u'🍻', u'🍷', u'🍸',
                                              u'🍹', u'🍾')

        ################################################
        # the joy emoji squares the value at the point #
        ################################################

        self.add_commands('self.value **= 2', u'😂')
        
        #########################################
        # weeping face zeroes the current value #
        #########################################
        
        self.add_commands('self.value = 0', u'😭')
        
        ##############################################    
        # construction worker sets the working value #
        # as the value in the current cell           #
        ##############################################

        self.add_commands('self.working_value = self.value', u'👷')

        ##################################################
        # the scream emoji sets the x coordinate to zero #
        ##################################################
        self.add_commands('self.x = 0', u'😱')

        ###############################################
        # right and left pointing move right and left #
        ###############################################
        self.add_commands('self.x += 1', u'👉')
        self.add_commands('self.x -= 1', u'👈')

        ################################################
        # pointing up goes up, pointing down goes down #
        ################################################

        self.add_commands('self.y += 1', u'🖕', u'☝', u'👆', u'👍')
        self.add_commands('self.y -= 1', u'👇', u'👎')

        ######################################
        # upleft arrow goes upleft and so on #
        ######################################
        self.add_commands('self.y += 1; self.x -= 1', u'↖')
        self.add_commands('self.y += 1; self.x += 1', u'↗')
        self.add_commands('self.y += 1; self.x += 1', u'↗')
        self.add_commands('self.y -= 1; self.x += 1', u'↘')
        self.add_commands('self.y -= 1; self.x -= 1', u'↙')

        ######################################################
        # double arrows move two in the direction they point #
        ######################################################

        self.add_commands('self.y += 2', u'⏫')
        self.add_commands('self.y -= 2', u'⏬')


        ####################################
        # punching fist increases z by one #
        # okay sign decreases z by one     #
        ####################################

        self.add_commands('self.z += 1', u'👊')
        self.add_commands('self.z -= 1', u'👌')

        #########################################################
        # hourglass and clocks go forwards in time              #
        # The Man in buisness suit levitating goes back in time #
        #########################################################
        
        self.add_commands('self.t += 1', u'⌛', u'⏳', u'⏱', u'⏰', 
                                         u'⌚', u'⏲', u'🕰')
        self.add_commands('self.t -= 1', u'🕴')

        ######################################################
        # sleepy face and open mouth surprised face store    #
        # strings vertically and horizontally respectively   #
        #                                                    #
        # when strings are stored the cell immediately after #
        # the string is zeroed (Just like a null terminated  #
        # string)                                            #
        ######################################################
        
        self.add_commands('self.store_string_vertically()', u'😪')
        self.add_commands('self.store_string_horizontally()', u'😮')

        #########################################################
        # thinking face waits for a number and stores it in the #
        # current cell                                          #
        #########################################################

        self.add_commands('self.set_value_number()', u'🤔')

        ##################################################
        # four leafed clover puts a random value between #
        # the current value and zero (inclusive)         #
        #                                                #
        # The die emoji puts a random number between 1   #
        # and 6 in the cell                              #
        ##################################################

        self.add_commands('self.value = random.randrange(0, self.value + 1)', u'🍀')
        self.add_commands('self.value = random.randrange(1, 7)', u'🎲')

        ##############################################
        # construction worker sets the working value #
        # as the value in the current cell           #
        ##############################################

        self.add_commands('self.working_value = self.value', u'👷')

        ####################################################
        # two people holding hands adds the current cell   #
        # to the working value and stores that in the cell #
        ####################################################
        
        self.add_commands('self.value += self.working_value', u'👫', u'👬', u'👭')

        ####################################################
        # two people kissing multiplies the current cell   #
        # to the working value and stores that in the cell #
        ####################################################

        self.add_commands('self.value *= self.working_value', u'💏')
        
        ################################################################
        # unicorn and horse set working value to the remainder         #
        # of the division between that cell and the working value      #
        ################################################################
        
        self.add_commands('self.working_value = self.working_value % self.value',
                                                             u'🦄', u'🐴', u'🐎')


        ######################################################
        # sun and full moon  start and close loops           # 
        # where it loops if the value at the end is not zero #
        #                                                    #
        # The earth functions as a start to an if block and  #
        # is closed by a moon                                #
        #                                                    #  
        # The angel tests if the value is greater than the   #
        # working value and the devil tests if it is less    #
        # than the working value                             #
        #                                                    #
        # The eyes off to the side is an else block, and     #
        # must come after an if block                        #
        #                                                    #
        # moons end blocks with no side effects              #
        ######################################################

        self.add_commands('while self.value != 0:', u'🌞', u'☀', block_starter = True)
        self.add_commands('if self.value != 0:', u'🌍', u'🌏', u'🌎', block_starter = True)
        self.add_commands('if self.value > self.working_value:', u'😇', block_starter = True)
        self.add_commands('if self.value < self.working_value:', u'😈', block_starter = True)
        self.add_commands('else:', u'😒', block_starter = True, block_ender = True)
        self.add_commands('', u'🌝', u'🌑', u'🌒', u'🌓', 
                              u'🌔', u'🌕', u'🌖', u'🌗',
                              u'🌘', u'🌙', u'🌛', u'🌜', block_ender = True)
        ##########################################################
        # Kissy face prints out the value as ASCII               #
        # Winky face prints a newline                            #
        # Nerd face prints out the value in the cell as a number #
        # because nerds and numbers amiright                     #
        ##########################################################

        self.add_commands('self.print_as_ASCII()', u'😘')
        self.add_commands('print(file=self.output)', u'😉')
        self.add_commands('print(self.value, end=\'\', file=self.output)', u'🤓')

        ###########################################################
        # poop emoji dumps the entire stack, not pretty, dont use #
        ###########################################################
        self.add_commands('partial(print, self._cells)()', u'💩')


    def add_commands(self, code, *commands, block_starter = False, block_ender = False):
        '''
        Takes the code that each command should represent
        and at least one command
        '''

        if not commands:
            return

        for command in commands:
            self.equivalents[command] = code
            if block_starter:
                self.block_starters.add(command)
            if block_ender:
                self.block_enders.add(command)

    def extract_emoji(self, filename):
        '''
        parses the source file, taking only the emoji that
        have defined behaviour into memory
        '''
        data = ''
        with io.open(filename, encoding="utf-8") as emojfile:
            for line in emojfile:
                data += line

        code = [char for char in data if char in self.equivalents.keys()]
        return code

    def make_py_code(self, code):
        '''
        generates python code equivalent to the emoji fed to it 
        '''
        py_code = ''
        indentation_level = 0

        for character in code:
            if character in self.block_enders:
                indentation_level -= 1

            #This line is snuggled in here to make else clauses work right
            py_code += '    ' * indentation_level + self.equivalents[character] + '\n'
            
            if character in self.block_starters:
                indentation_level += 1
                py_code += '    ' * indentation_level + 'pass\n'

        return py_code


    def compress_optimize(self, commands_list):
        
        ######################################################
        # We go through the dictionary of commands and keep  #
        # track of what has the same behaviour of smiles and #
        # frowns                                             #
        ######################################################

        incrementers = []
        decrementers = []
        
        for key in self.equivalents:
            if self.equivalents[key] == self.equivalents[u'😃']:
                incrementers.append(key)
            elif self.equivalents[key] == self.equivalents[u'☹']:
                decrementers.append(key)

        #####################################################
        # Then we replace everything that increments with a #
        # positive 1 and everything that decrements with a  #
        # negative 1                                        #
        #####################################################

        for index, command in enumerate(commands_list):
            if command in incrementers:
                commands_list[index] = 1
            elif command in decrementers:
                commands_list[index] = -1

        #################################################################
        # goes through the list of commands and compresses every string #
        # of increments and decrements with the equivalent sum of those #
        #                                                               #
        # in python2 str is not the same as a unicode string and in     #
        # python3 unicode is not defined, so we just look for something #
        # that is NOT an int, which matches both cases                  #
        #################################################################

        optimized_commands = []
        current_total = 0
        for command in commands_list:
            if type(command) != int and abs(current_total) > 0:
                optimized_commands.append(current_total)
                optimized_commands.append(command)
                current_total = 0
            elif type(command) == int:
                current_total += command
            else:
                optimized_commands.append(command)
        if abs(current_total) > 0:
            optimized_commands.append(current_total)

        ###############################################################
        # To simplify matters, we add the simplified integer value to #
        # the dictionary with a corresponding command to change value #
        ###############################################################
        for command in set(optimized_commands):
            if type(command) == int:
                self.add_commands('self.value += {0}'.format(command), command)

        return optimized_commands

        
    def interpret_code(self, filename, should_optimize = False,
                                       should_print_code = False):
        '''
        starting point for code optimization
        '''
        commands_list = self.extract_emoji(filename)

        if should_optimize:
            commands_list = self.compress_optimize(commands_list)

        python_code = self.make_py_code(commands_list)
        
        if should_print_code:
            print(python_code)

        exec(python_code)

def main():
    '''
    start of execution
    '''
    
    #############################################################
    # builds an argument parser to get the filename and whether #
    # optimizations are wanted                                  #
    #############################################################

    parser = argparse.ArgumentParser(description='emoji based programming language')
    parser.add_argument('-o', dest='should_optimize', action='store_const',
                         const=True, default=False,
                         help='should the code be optimized')
    parser.add_argument('-d', dest='should_print_code', action='store_const',
                         const=True, default=False,
                         help='should the code be printed once generated')
    parser.add_argument('filename', metavar='filename', type=str,
                        help='name of the file to be parsed')
    args = parser.parse_args()
    
    code_interpreter = Interpreter()

    code_interpreter.interpret_code(filename = args.filename,
                                    should_optimize = args.should_optimize,
                                    should_print_code = args.should_print_code)
    
if __name__ == '__main__':
    main()

