#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
'''
compiler for emojilang
'''

filename = sys.argv[1]
output_name = 'emoji'

c_code = ''

with open('c_template.c') as c:
    for line in c:
        c_code+=line+'\n'

#small superset of bf also supported
code_equivalance = {
    '+': '(data[x][y])++;\n',
    '-': '(data[x][y])--;\n',
    '>': 'x++;\n',
    '<': 'x--;\n',
    ',': 'data[x][y] = getchar();\n',
    '.': 'putchar(data[x][y]);\n',
    '*': 'printf(\"%d\", (int) data[x][y] );\n',
    '!': 'printf("\\n");\n',
    '[': 'while(data[x][y]){\n',
    ']': '}\n',


#Happy emojis add one to the value at the location,
#sad emojis subtract

    '😃': '(data[x][y])++;\n',
    '😄': '(data[x][y])++;\n',
    '☹': '(data[x][y])--;\n',

#the joy emoji squares the value at the point
    '😂': 'data[x][y] = (data[x][y]*data[x][y]);\n',

#the scream emoji sets the x coordinate to zero
    '😱': 'x=origin;\n',

#right and left pointing move right and left
    '👉': 'x++;\n',
    '👈': 'x--;\n',

#middle finger moves up,
    '🖕': 'y++;\n',

#pointing finger up moves up
    '☝': 'y++;\n',
    '👆': 'y++;\n',
    '👍': 'y++;\n',

#pointing down goes down
    '👇': 'y--;\n',
    '👎': 'y--;\n',

#upleft arrow goes upleft
    '↖': 'y++;x--;\n',

#upright arrow goes upright
    '↗': 'y++;x++;\n',

#downright goes downright
    '↘': 'y--;x++;\n',

#downleft goes downleft
    '↙': 'y--;x--;\n',

#doubleup arrow goes two up
    '⏫': 'y+=2;\n',

#doubledown arrow goes down two
    '⏬': 'y-=2;\n',
#sleepy face waits for input then stores it in the cell
    '😪': 'data[x][y] = getchar();\n',

#thinking face waits for a number
    '🤔': 'scanf("%d",(int*)(&data[x][y]));\n',

#kissy face prints out the value as ASCII
    '😘': 'putchar(data[x][y]);\n',

#sun and full moon w/ face start and close loops 
#where it loops if the value at the end is not zero
    '🌞': 'while(data[x][y]){\n',
    '☀': 'while(data[x][y]){\n',
    '🌝': '}',

#winky face prints a newline
    '😉': 'printf("\\n");\n',

#open mouth suprised face waits for one char of input
    '😮': 'scanf("%c", (char*)(&data[x][y]));\n',

#poop emoji dumps the entire stack, not pretty, dont use
    '💩': 'for (int i = 0; i<cell_size;i++){\n \
              for(int e = 0; e<cell_size;e++){\n \
                  printf("%d",(int) data[i][e]);\
              }\
              printf("\\n");\
           }',

#Die emoji puts a random value between 1 and 6 in the cell
    '🎲': 'data[x][y] = (char)(rand() % 6) + 1;',

#nerd face prints out the value in the cell as a number
#because nerds and numbers amiright
    '🤓': 'printf(\"%d\",  data[x][y] );\n'
}

def loademoji(filename):
    data = ''
    with open(filename) as bffile:
        for line in bffile:
            data += line
    data = [char for char in data if char in code_equivalance.keys()]
    code=''
    for i in data:
        code+=i
    return code

symbols = loademoji(filename)

code = ''


for symbol in symbols:
    code += code_equivalance[symbol]

c_code = c_code % code

with open("c_code.c", "w") as code_file:
    code_file.write(c_code)
	
os.system("gcc -std=c99 c_code.c -o {0}".format(output_name))
os.system("rm c_code.c")
