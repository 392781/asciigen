from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageStat
from collections import defaultdict
from tqdm import tqdm
from bisect import bisect
from math import gcd
import random as r

Image.MAX_IMAGE_PIXELS = 100000000

'''
asciigen class tree

asciigen - param : font
    gradient - param : type, gradient, size
    generate - param : image, original_size, generate_size, color
'''

_gradient_dictionary = defaultdict(list)

def _find_dictionary(font, size):
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
        stats = ImageStat.Stat(image)
        
        # finds the brightness value of the character and adds 
        # it to the table

        sum = stats.sum[0]
                
        brightness_value = int(sum/(h*w))
        
        table[brightness_value].append(str(chr(i)))

        if (brightness_value > max):
            max = brightness_value

    for key in table:
        tmp = int((255 * (key - min)) / (max - min))
        ascii_gradient[tmp] = table[key]
    
    return ascii_gradient


def _select_symbol(dictionary, sorted_keys, val):
    gradient_idx = bisect(sorted_keys, val) - 1
    key = sorted_keys[gradient_idx]
    symbols = dictionary[key]
    if (len(symbols) > 1):
        idx = r.randint(0, len(symbols) - 1)
        return symbols[idx]
    else:
        return symbols[0]


def print_dict(dictionary):
    for key in sorted(dictionary.keys()):
        print(key, dictionary[key])


def length(dictionary):
    return len(dictionary)


def _block_brightness(image, box):
    image = image.crop(box)
    return ImageStat.Stat(image).sum[0]

def select_dictionary(method = 'naive', size = None):
    dictionary = defaultdict(list)
    if (method == 'naive'):
        length = 0
        for i in range(8, 131):
            tmp = _find_dictionary('./fonts/FSEX300.ttf', i)
            tmp_len = len(tmp)
            if (tmp_len > length):
                dictionary = tmp
                length = tmp_len
                size = i
    elif (method == 'custom'):
        dictionary = _find_dictionary('./fonts/FSEX300.ttf', size)
    return dictionary, size



def generate(font, fontsize, image, gradient = ' .:+/$@'):
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

    ascii_table = gradient

    sorted_table_keys = sorted(ascii_table.keys())

    image_string = []
    scale_ratio = 0
    with Image.open(image) as image:
        # w,h = image.size[0], image.size[1]
        # x = gcd(h, w)
        # h //= x
        # w //= x
        h, w = 12, 7
        xp = 0
        yp = 0
        brightness = 0
        scale_ratio = image.size[0]


        '''
        notes:
            img width is 1347 you want to divide it into sections 300 width
            apart... 
        '''
        image_width = image.size[0]
        image_height = image.size[1]
        for y in tqdm(range(0, image_height, h)):
            if (y + h < image_height):
                for x in range(0, image_width, w):
                    if (x + w < image_width):
                        brightness = _block_brightness(image, (x, y, x+h, y+h))
                        brightness //= h*w
                        char = _select_symbol(ascii_table, sorted_table_keys, brightness)
                        image_string.append(char)
            image_string.append('\n')
        image_string = ''.join(image_string)        


        # while (h + yp < image.size[1]):
        #     while (w + xp < image.size[0]):    
        #         for y in range(yp, h + yp):
        #             for x in range(xp, w + xp):
        #                 brightness += image.getpixel((x, y))
        #         xp += w 
        #         brightness = brightness // (h*w)
        #         char = ascii_table.select_symbol(brightness)
        #         string = string + char      
        #     xp = 0
        #     yp += h
        #     string = string + "\n"
                
    im = Image.new("RGB", (10000,10000))
    img = ImageDraw.Draw(im)
    font = ImageFont.truetype(font, fontsize)
    img.text((0,0), image_string)
    
    im = im.crop(im.getbbox())
    im = im.convert('1')
    #scale_ratio /= im.size[0]
    scale_ratio = 1
    im = im.resize((int(im.size[0]*scale_ratio), 
                    int(im.size[1]*scale_ratio)))
    im.show()
    im.save('monatest.jpg')
    return im







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
