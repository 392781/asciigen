from PIL import Image, ImageFont, ImageDraw
from collections import defaultdict
from bisect import bisect
from tqdm import tqdm
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

class FontProcessor:
    def __init__(self, font = 'asciigen/FSEX300.ttf', size=None, optimal = False):
        self.chrdict = defaultdict(list)
        self.font = font
        self.size = size

        if (size == None and optimal == True):
            length = 0
            for i in tqdm(range(8, 131), ascii=True, desc='Finding table'):
                tmp = self.finddict(i)
                if (len(tmp) > length):
                    self.chrdict = tmp
                    length = len(tmp)
                    self.size = i
        elif (size == None and optimal == False):
            self.chrdict = self.finddict(64)
        else:
            self.chrdict = self.finddict(size)



    def finddict(self, size):
        font = ImageFont.truetype(self.font, size)
        chrdict = defaultdict(list)
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
            chrdict[tmp] = table[key]
        
        return chrdict



    def select_symbol(self, val):
        lookup = sorted(self.chrdict.keys())
        pos = bisect(lookup, val) - 1
        key = lookup[pos]
        vals = self.chrdict[key]
        choose = r.randint(0, len(vals) - 1)
        
        return vals[choose]



    def printdict(self):
        for key in sorted(self.chrdict.keys()):
            print(key, self.chrdict[key])



    def length(self):
        return len(self.chrdict)
