from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageStat
from timeit import default_timer as timer

with Image.open('../imgs/mona1.png') as img:
    img = img.convert('L')
    start = timer()
    test1 = img.crop((0,0,300,300))
    stats = ImageStat.Stat(test1)
    end = timer()
    print(end - start)

    brightness = 0
    start = timer()
    test2 = img.crop((0,0,300,300))
    for y in range(0, test2.size[1]):
        for x in range(0, test2.size[0]):
            brightness += test2.getpixel((x,y))
    end = timer()
    print(end - start)

    print(stats.sum[0])
    print(brightness)