from PIL import Image, ImageFont, ImageDraw
from collections import defaultdict
from bisect import bisect
import random as r

'''
    IMPROVEMENTS:
        USE SSIM FOR EACH GLYPH:
            STORE:
            LUMINANCE
            CONTRAST
            STRUCTURE

            FOR EACH CORRESPONDING LETTER
'''

def average(im, h, w):
    sum = 0
    for x in range(h - 1):
        for y in range(w - 1):
            mu = im.getpixel((x,y))
            sum += mu

    avg = sum/(h*w)
    return avg
    

def variance(im, h, w, avg):
    sumsq = 0
    for x in range(h - 1):
        for y in range(w - 1):
            mu = im.getpixel((x,y))
            sumsq += (mu**2)
                
    var = (sumsq/(h*w)) - (avg**2)
    return var

def process(font):
    font = ImageFont.truetype(font, 128)
    average_dict = defaultdict(list)
    variance_dict = defaultdict(list)
    average_dict[0].append(chr(32))
    variance_dict[0].append(chr(32))

    for i in range(33, 127):
        h,w = font.getsize(chr(i))
        im = Image.new("RGB", (h,w))
        draw = ImageDraw.Draw(im)
        draw.text((0,0), chr(i), font=font)
        im = im.convert('L')

        avg = average(im, h, w)
        var = variance(im, h, w, avg)

        average_dict[avg].append(chr(i))
        variance_dict[var].append(chr(i))

    for key in sorted(average_dict):
        print(average_dict[key])



def dprocess(font):

    # use a truetype font
    font = ImageFont.truetype(font, 128)

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
       
    for key in charDict:
        print(charDict[key])
    return charDict

    
def get_h_w(font, size):
    font = ImageFont.truetype(font, size)
    h,w = font.getsize(chr(64))
    
    return h,w

def select_symbol(val, charTable):
    lookup = sorted(charTable.keys())
    pos = bisect(lookup, val) - 1
    key = lookup[pos]
    vals = charTable[key]
    choose = r.randint(0, len(vals) - 1)
    
    return vals[choose]
    
