"""
Version 0.1.7
Author: Ronald Lencevicius
"""

from PIL import Image, ImageEnhance, ImageFont, ImageDraw
from bisect import bisect
from math import gcd
from gradient import FontProcessor as fp

class Generator:
    def __init__(self, address, scale = None, fp = fp()):
        self.ascii_table = fp
        self.img = Image.open(address)
        self.img = self.img.convert('L')
        enh = ImageEnhance.Contrast(self.img)
        self.imgimg = enh.enhance(1)
        if (scale != None):
            self.img = self.img.resize((
                self.img.size[0]//scale, 
                self.img.size[1]//scale)
            )
    
    def generate(self):
        self.ascii_table.printdict()
        #w,h = fp.get_h_w(font, fontsize)
        w,h = image.size[0], image.size[1]
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
        while (h + yp < image.size[1]):
            while (w + xp < image.size[0]):    
                for y in range(yp, h + yp):
                    for x in range(xp, w + xp):
                        brightness += image.getpixel((x, y))
                xp += w 
                brightness  = brightness // (h*w)
                char        = ascii_table.select_symbol(brightness)
                string      = string + char      
            xp = 0
            yp += h
            string = string + "\n"
                    
        size = 10000
        canvas = Image.new("RGB", (size,size))
        layer = ImageDraw.Draw(canvas)
        layer.text((0,0), string, font = self.self.ascii_table.font)
        
        canvas = canvas.crop(canvas.getbbox())
        canvas = canvas.convert('1')
        canvas = canvas.resize((canvas.size[0]//8, canvas.size[1]//8))
        return canvas

    
def generate(font, fontsize, image):
    """
    Creates an ASCII image using a predefined lookup table
    
    Uses predefined 'ascii' string and 'breakpoints' list to then test
    the brightness of each pixel in the image and uses the breakpoints 
    to determine which value to choose from the ascii string.  The 
    chosen character is then appended to the string with linebreaks 
    between each subsequent line of pixels
    
    Parameters:
        image (image):    Image to be processed and generated
    
    Returns:
        image (image):    Image representing the original input as ascii
    """
    ascii_table = fp()
    ascii_table.printdict()
    #w,h = fp.get_h_w(font, fontsize)
    w,h = image.size[0], image.size[1]
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
    while (h + yp < image.size[1]):
        while (w + xp < image.size[0]):    
            for y in range(yp, h + yp):
                for x in range(xp, w + xp):
                    brightness += image.getpixel((x, y))
            xp += w 
            brightness  = brightness // (h*w)
            char        = ascii_table.select_symbol(brightness)
            string      = string + char      
        xp = 0
        yp += h
        string = string + "\n"
                
    size = 10000
    im = Image.new("RGB", (size,size))
    img = ImageDraw.Draw(im)
    font = ImageFont.truetype(font, fontsize)
    img.text((0,0), string, font = font)
    
    im=im.crop(im.getbbox())
    im = im.convert('1')
    im = im.resize((im.size[0]//8, im.size[1]//8))
    im.show()
    return im

#~~~~~~~~~~~~RUNNER~~~~~~~~~~~~~#
address = "../imgs/mona1.png"

image     = preprocess(address, 1)
ASCII     = generate("FSEX300.ttf", 128, image)
