from PIL import Image, ImageFont, ImageDraw
from collections import defaultdict
import multiprocessing as mp
from functools import partial
from timeit import default_timer as timer

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

def main():
    # Let's try to find the longest possible dictionary of values to use as a gradient (longer dictionary = more detail)

    # This function will go through each font size individually as a single process on a single CPU core
    def singleproc():
        for i in range(8, 131):
            find_dictionary('../fonts/FSEX300.ttf', i)

    # Pool will let us use multiple cores on a CPU (4 on mine) to split up our search for a gradient.  
    # in my case about 1/4th of the font sizes will go to each core and run the find_dictionary func simultaneously
    pool = mp.Pool(mp.cpu_count())
    # This bit below gives a constant parameter for the font name in our find_dictionary function.
    func_partial = partial(find_dictionary, '../fonts/FSEX300.ttf')
    # With the font parameter set, we just need to give an iterable range of sizes for our function and run it in parallel!
    pool.map(func_partial, iter(range(8,131)))
