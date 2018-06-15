"""
Version 0.1.2
Author: Ronald Lencevicius
"""

from PIL     import Image, ImageEnhance, ImageFont, ImageDraw
from bisect  import bisect
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
    img = img.resize((int(120/scale),int(70/scale)), Image.HAMMING)
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
    
    ascii            = " .:-=+*#%@"
    breakpoints      = [25, 51, 76, 102, 127, 153, 178, 204, 229]
    
    string = ""
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            brightness     = 255 - image.getpixel((x,y))
            char           = ascii[bisect(breakpoints, brightness)]
            string         = string + char
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
address = "allmight.jpg"

image     = preprocess(address, 1)
ASCII     = generate(image)
#file      = open("ASCII.txt", "w")

#file.write(ASCII)
#file.close()

#print(ASCII)