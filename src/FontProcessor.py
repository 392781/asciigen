from PIL import Image, ImageFont, ImageDraw
from collections import defaultdict
from bisect import bisect
import random as r

def process(font, size):

    # use a truetype font
    font = ImageFont.truetype(font, size)

    #creates map with a list of values
    table = defaultdict(list)
    table[0].append(chr(32))
    min = 0
    max = 0
    
    for i in range(33,127):
        # finds the characters height and width and creates an 
        # image where it pastes the character and processes it
        h,w = font.getsize(chr(i))
        im = Image.new("RGB", (h,w))
        draw = ImageDraw.Draw(im)
        draw.text((0,0), chr(i), font=font)
        im = im.convert('L')
        
        # finds the brightness value of the character and adds 
        # it to the table
        sum = 0
        for x in range(h - 1):
            for y in range(w - 1):
                mu = im.getpixel((x,y))
                sum += mu
                
        val = int(sum/(h*w))
        
        table[val].append(chr(i))

        if (val > max):
            max = val
            
    charDict = defaultdict(list)
    for key in table:
        tmp = int((255 * (key - min)) / (max - min))
        charDict[tmp] = table[key]
        
    return charDict
'''
    print(len(table))

    for key in sorted(table.keys()):
        print("%s: %s" % (key, table[key]))

    print()

    print(len(charDict))
    for key in sorted(charDict.keys()):
        print("%s: %s" % (key, charDict[key]))
'''
    
def get_h_w(font, size):
    font = ImageFont.truetype(font, size)
    h,w = font.getsize(chr(120))
    
    return h,w

def select_symbol(val, charTable):
    lookup = sorted(charTable.keys())
    pos = bisect(lookup, val) - 1
    key = lookup[pos]
    vals = charTable[key]
    
    return vals[0]
    

