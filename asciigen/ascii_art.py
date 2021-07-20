from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageStat
from collections import defaultdict
from bisect import bisect
import random as r

Image.MAX_IMAGE_PIXELS = 100000000

def _calc_gradient(font_object) -> defaultdict:
    gradient = defaultdict(list)
    table = defaultdict(list)
    table[0].append(chr(32))
    min = 0
    max = 0
    
    for i in range(33,127):
        # finds the characters height and width and creates an image where it pastes the 
        # character and processes it
        h, w = font_object.getsize(chr(i))
        image = Image.new('L', (h, w))
        draw = ImageDraw.Draw(image)
        draw.text((0,0), chr(i), font=font_object, fill=255)

        # finds the brightness value of the character and adds it to the table
        brightness_sum = ImageStat.Stat(image).sum[0]
        brightness_value = brightness_sum//(h*w)
        table[brightness_value].append(chr(i))

        if (brightness_value > max):
            max = brightness_value

    for key in table:
        tmp = (255 * (key - min)) // (max - min)
        gradient[tmp] = table[key]

    return gradient


def _select_symbol(gradient, val) -> str:
    keys = sorted(gradient.keys())
    idx = bisect(keys, val) - 1
    key = keys[idx]
    symbols = gradient[key]
    if (len(symbols) > 1):
        idx = r.randint(0, len(symbols) - 1)
        return symbols[idx]
    else:
        return symbols[0]


def print_dict(dictionary):
    for key in sorted(dictionary.keys()):
        print(key, dictionary[key])


def _block_brightness(image, box) -> int:
    image = image.crop(box)
    area = (box[2]-box[0])*(box[3]-box[1])
    return ImageStat.Stat(image).sum[0] // area


def _gradient_selector(font, size = None) -> [defaultdict, int]:
    try:
        ImageFont.truetype(font, 12)
    except OSError:
        try:
            ImageFont.load(font)
        except OSError:
            print('Cannot open font file')
    
    gradient = defaultdict(list)
    length = -1

    if size == None:
        for i in range(8, 131):
            tmp = _calc_gradient(ImageFont.truetype(font, i))
            tmp_length = len(tmp)
            if (tmp_length > length):
                gradient = tmp
                length = tmp_length
                size = i
    else:
        gradient = _calc_gradient(font, size)

    return gradient, size

def generate(image, font):
    gradient, size = _gradient_selector(font)
    font = ImageFont.truetype(font, size)
    ascii_art = ''
    with Image.open(image) as image:
        image_w, image_h = image.size
        font_w, font_h = font.getsize(_select_symbol(gradient, 255))

        for y in range(0, image_h, font_h):
            for x in range(0, image_w, font_w):
                brightness = _block_brightness(image, (x, y, x+font_w, y+font_h))
                char = _select_symbol(gradient, brightness)
                ascii_art += char
            ascii_art += '\n'
    return ascii_art

# def generate(image, font, fontsize, gradient):
#     font = ImageFont.truetype(font, fontsize)
#     sorted_table_keys = sorted(gradient.keys())

#     image_string = []
#     scale_ratio = 0
#     with Image.open(image) as image:
#         image_w = image.size[0]
#         image_h = image.size[1]
#         font_w, font_h = font.getsize(_select_symbol(gradient, 255))
#         font_aspect_ratio = font_w/font_h
#         font_scaler = image_h/100
#         font_w = int(font_aspect_ratio * font_scaler * 1.1)
#         font_h = int(font_scaler)

#         brightness = 0
#         scale_ratio = image_w

#         for y in range(0, image_h, font_h):
#             for x in range(0, image_w, font_w):
#                 brightness = _block_brightness(image, (x, y, x+font_w, y+font_h))
#                 char = _select_symbol(gradient, brightness)
#                 image_string.append(char)
#             image_string.append('\n')
#         image_string = ''.join(image_string) 

#     im = Image.new("RGB", (10000,10000))
#     img = ImageDraw.Draw(im)

#     img.text((0,0), image_string, font=font)
    
#     im = im.crop(im.getbbox())
#     im = im.convert('L')
#     scale_ratio /= im.size[0]
#     im = im.resize((int(im.size[0]*scale_ratio), 
#                     int(im.size[1]*scale_ratio)), 
#                     resample=Image.BICUBIC)
#     im.show()
#     return im

_gradient_selector("UbuntuMono-R.ttf")