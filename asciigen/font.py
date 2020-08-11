from PIL import Image, ImageFont, ImageDraw
from collections import defaultdict
from bisect import bisect
import random as r

# TO-DO: add documentation
def find_dictionary(font, size):
        font = ImageFont.truetype(font, size)
        ascii_gradient = defaultdict(list)
        #creates map with a list of values
        table = defaultdict(list)
        table[0].append(chr(32))
        min = 0
        max = 0
        
        for i in range(33,127):
            # finds the characters height and width and creates an 
            # image where it pastes the character and processes it
            h,w = font.getsize(chr(i))
            image = Image.new("RGB", (h, w))
            draw = ImageDraw.Draw(image)
            draw.text((0,0), chr(i), font=font)
            image = image.convert('L')
            
            # finds the brightness value of the character and adds 
            # it to the table

            sum = 0
            for x in range(h - 1):
                for y in range(w - 1):
                    mu = image.getpixel((x,y))
                    sum += mu
                    
            val = int(sum/(h*w))
            
            table[val].append(chr(i))

            if (val > max):
                max = val

        for key in table:
            tmp = int((255 * (key - min)) / (max - min))
            ascii_gradient[tmp] = table[key]
        
        return ascii_gradient


def select_symbol(dictionary, sorted_keys, val):
    gradient_idx = bisect(sorted_keys, val) - 1
    key = sorted_keys[gradient_idx]
    symbols = dictionary[key]
    if (len(symbols) > 1):
        idx = r.randint(0, len(vals) - 1)
        return symbols[idx]
    else:
        return symbols[0]


def printdict(dictionary):
    for key in sorted(dictionary.keys()):
        print(key, dictionary[key])


def length(dictionary):
    return len(dictionary)