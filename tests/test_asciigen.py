# Trying to test brand new rewritten code
import os, sys
os.chdir('../')
sys.path.append(os.getcwd())
from asciigen import api
sys.path.pop()

font = 'UbuntuMono-R.ttf'

dictionary, size = api.select_dictionary(font=font)
print('Font Size: ', size)
api.generate(image='imgs/mona1.png', 
            font=font, fontsize=size, 
            gradient=dictionary)