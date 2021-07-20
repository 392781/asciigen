# Trying to test brand new rewritten code
import os, sys
os.chdir('../')
sys.path.append(os.getcwd())
from asciigen import ascii_art
sys.path.pop()

font = 'UbuntuMono-R.ttf'

# dictionary, size = api._gradient_selector(font=font)
# print('Font Size: ', size)
# api.generate(image='imgs/mona1.png', 
#             font=font, fontsize=size, 
#             gradient=dictionary)

print(ascii_art.generate(image='imgs/mona1.png', font=font))