# Trying to test brand new rewritten code
import os, sys
os.chdir('../')
sys.path.append(os.getcwd())
from asciigen import api
sys.path.pop()

dictionary, size = api.select_dictionary()
print('Font Size: ', size)
api.generate(font='fonts/FSEX300.ttf', fontsize=22, 
            image='imgs/clown.png', gradient=dictionary)