"""
Version 0.1.5
Author: Ronald Lencevicius
"""

from PIL     import Image, ImageEnhance, ImageFont, ImageDraw
from bisect  import bisect
import FontProcessor as fp
import time

def preprocess(address, scale):
    """ 
    Processes image by:
    1. Converting to greyscale 
    2. Pumping up the contrast
    3. Resizing to fit the character size 
        * Will change this up due to loss of detail
        
    Parameters:
        address (str):     Location of image
        scale (double):    Value to decrease the size of the output by
    
    Returns:
        image:             Processed image
    """
   
       
    img = Image.open(address)
    img = img.convert('L')
    enh = ImageEnhance.Contrast(img)
    img = enh.enhance(1)
    
    return img
    
def generate(image):
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
    ascii_table = fp.process("system8x12.ttf", 32)
    w = 7
    h = 12
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
            char        = fp.select_symbol(brightness, ascii_table)
            string      = string + char      
        xp = 0
        yp += h
        string = string + "\n"
                
    
    im = Image.new("RGB", (10000,10000))
    img = ImageDraw.Draw(im)
    font = ImageFont.truetype("system8x12.ttf", 32)
    img.text((0,0), string, font = font)
    
    im=im.crop(im.getbbox())
    im = im.convert('1')
    im.show()
    return im

#~~~~~~~~~~~~RUNNER~~~~~~~~~~~~~#
address = "mona1.png"

image     = preprocess(address, 1)
ASCII     = generate(image)
