from PIL import Image, ImageEnhance, ImageFont, ImageDraw
from collections import defaultdict
from tqdm import tqdm
from bisect import bisect
from math import gcd
import random as r

'''
asciigen class tree

asciigen - param : font
    gradient - param : type, gradient, size
    generate - param : image, original_size, generate_size, color
'''

class asciigen:
    '''
    Parameters
    ----------
    font : str
    '''

    def __init__(self, font='./fonts/FSEX300.ttf'):
        self.font_name = font


    '''
    if you choose a 'custom_gradient' 
    '''
    def gradient(self, gradient_type = None, custom_gradient = None, custom_size = None):
        if (type(gradient_type) not in (str, type(None))):
            raise TypeError('Only str and None type supported')
        elif (gradient_type not in ('ssim', 'naive_optimal')):
            raise ValueError('Choose \'ssim\' or \'naive_optimal\'')
        elif (gradient_type == None):
            pass

        self.chrdict = defaultdict(list)
        if (gradient_type == 'naive_optimal'):
            length = 0
            for i in tqdm(range(8, 131), ascii=True, desc='Finding table'):
                tmp = self._find_naive_optimal(i)
                if (len(tmp) > length):
                    self.chrdict = tmp
                    length = len(tmp)
                    self.size = i

    def _find_naive_optimal(self, size):
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
        

class _FontProcessor:
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



class Generator:
    def __init__(self, address, scale = None, fp = FontProcessor(optimal = True)):
        self.ascii_table = fp
        self.img = Image.open(address)
        self.img = self.img.convert('L')
        enh = ImageEnhance.Contrast(self.img)
        self.img = enh.enhance(1)
        if (scale != None):
            self.img = self.img.resize((
                self.img.size[0]//scale, 
                self.img.size[1]//scale)
            )
    
    def generate(self):
        self.ascii_table.printdict()
        #w,h = fp.get_h_w(font, fontsize)
        w,h = self.img.size[0], self.img.size[1]
        x = gcd(h, w)
        h //= x
        w //= x
        h, w = 12, 7
        print(h,w)
        left_px = 0
        xp = 0
        yp = 0
        brightness = 0
        string = ""
        while (h + yp < self.img.size[1]):
            while (w + xp < self.img.size[0]):    
                for y in range(yp, h + yp):
                    for x in range(xp, w + xp):
                        brightness += self.img.getpixel((x, y))
                xp += w 
                brightness  = brightness // (h*w)
                char        = self.ascii_table.select_symbol(brightness)
                string      = string + char      
            xp = 0
            yp += h
            string = string + "\n"
                    
        size = 10000
        canvas = Image.new("RGB", (size,size))
        layer = ImageDraw.Draw(canvas)
        layer.text((0,0), string, font = ImageFont.truetype(self.ascii_table.font, self.ascii_table.size))
        
        canvas = canvas.crop(canvas.getbbox())
        canvas = canvas.convert('1')
        canvas = canvas.resize((canvas.size[0]//4, canvas.size[1]//4))
        return canvas




# def generate(font, fontsize, image):
#     """
#     Creates an ASCII image using a predefined lookup table
    
#     Uses predefined 'ascii' string and 'breakpoints' list to then test
#     the brightness of each pixel in the image and uses the breakpoints 
#     to determine which value to choose from the ascii string.  The 
#     chosen character is then appended to the string with linebreaks 
#     between each subsequent line of pixels
    
#     Parameters:
#         image (image):    Image to be processed and generated
    
#     Returns:
#         image (image):    Image representing the original input as ascii
#     """
#     ascii_table = fp()
#     ascii_table.printdict()
#     #w,h = fp.get_h_w(font, fontsize)
#     w,h = image.size[0], image.size[1]
#     x = gcd(h, w)
#     h //= x
#     w //= x
#     h, w = 12, 7
#     print(h,w)
#     left_px = 0
#     xp = 0
#     yp = 0
#     brightness = 0
#     string = ""
#     while (h + yp < image.size[1]):
#         while (w + xp < image.size[0]):    
#             for y in range(yp, h + yp):
#                 for x in range(xp, w + xp):
#                     brightness += image.getpixel((x, y))
#             xp += w 
#             brightness  = brightness // (h*w)
#             char        = ascii_table.select_symbol(brightness)
#             string      = string + char      
#         xp = 0
#         yp += h
#         string = string + "\n"
                
#     size = 10000
#     im = Image.new("RGB", (size,size))
#     img = ImageDraw.Draw(im)
#     font = ImageFont.truetype(font, fontsize)
#     img.text((0,0), string, font = font)
    
#     im=im.crop(im.getbbox())
#     im = im.convert('1')
#     im = im.resize((im.size[0]//8, im.size[1]//8))
#     im.show()
#     return im

# #~~~~~~~~~~~~RUNNER~~~~~~~~~~~~~#
# address = "../imgs/mona1.png"

# image     = preprocess(address, 1)
# ASCII     = generate("FSEX300.ttf", 128, image)
