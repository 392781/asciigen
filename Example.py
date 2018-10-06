
from PIL import Image
import random
from bisect import bisect

greyscale = [" ",
            " ",
            ".,-",
            "_icv=!/|\\~",
            "gjez2[/(YL)t[+T7VF",
            "mdK4ZGbNDXY5P*Q",
            "W8KMA",
            "#%$"]
            
zonebounds = [36,72,108,144,180,216,252]

h = int(160/1.5)
w = int(75/1.5)

im = Image.open(r"C:\Users\Ronald\Desktop\Python\ASCII_GEN\src\Python-Logo.png")
im = im.resize((h, w),Image.BILINEAR)
im = im.convert("L")

str=""

for y in range(0, im.size[1]):
    for x in range(0, im.size[0]):
        lum = 255 - im.getpixel((x,y))
        row = bisect(zonebounds, lum)
        possibles = greyscale[row]
        str = str + possibles[random.randint(0, len(possibles) - 1)]
    str = str + "\n"
print(str) 
