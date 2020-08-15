from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageStat
from collections import defaultdict
from tqdm import tqdm
from bisect import bisect
import random as r

Image.MAX_IMAGE_PIXELS = 100000000

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
    area = (box[2]-box[0])*(box[3]-box[1])
    return ImageStat.Stat(image).sum[0] // area

def select_dictionary(font, method = 'naive', size = None):
    try:
        ImageFont.truetype(font, 12)
    except OSError:
        try:
            ImageFont.load(font)
        except OSError:
            print('Cannot open font file')
    dictionary = defaultdict(list)
    if (method == 'naive'):
        length = 0
        for i in range(8, 131):
            tmp = _find_dictionary(font, i)
            tmp_len = len(tmp)
            if (tmp_len > length):
                dictionary = tmp
                length = tmp_len
                size = i
    elif (method == 'custom'):
        dictionary = _find_dictionary(font, size)
    return dictionary, size



def generate(font, fontsize, image, gradient, save=True):
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
    font = ImageFont.truetype(font, fontsize)
    sorted_table_keys = sorted(ascii_table.keys())

    image_string = []
    scale_ratio = 0
    with Image.open(image) as image:
        image_w = image.size[0]
        image_h = image.size[1]
        font_w, font_h = font.getsize(_select_symbol(ascii_table, sorted_table_keys, 255))
        font_aspect_ratio = font_w/font_h
        font_scaler = image_h/110
        font_w = int(font_aspect_ratio * font_scaler)
        font_h = int(font_scaler)

        brightness = 0
        scale_ratio = image_w

        for y in tqdm(range(0, image_h, font_h)):
            for x in range(0, image_w, font_w):
                brightness = _block_brightness(image, (x, y, x+font_h, y+font_h))
                char = _select_symbol(ascii_table, sorted_table_keys, brightness)
                image_string.append(char)
            image_string.append('\n')
        image_string = ''.join(image_string) 

    im = Image.new("RGB", (10000,10000))
    img = ImageDraw.Draw(im)

    img.text((0,0), image_string, font=font)
    
    im = im.crop(im.getbbox())
    im = im.convert('L')
    scale_ratio /= im.size[0]
    im = im.resize((int(im.size[0]*scale_ratio), 
                    int(im.size[1]*scale_ratio)), 
                    resample=Image.BICUBIC)
    im.show()
    if (save==True):
        im.save('ascii.png')
    return im
