from PIL import Image, ImageFont, ImageDraw

im = Image.new("RGB", (2000, 2000))

draw = ImageDraw.Draw(im)

# use a truetype font
font = ImageFont.truetype("system8x12.ttf", 32)

draw.text((0, 0), "@ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=font)

# remove unneccessory whitespaces if needed
im=im.crop(im.getbbox())
im = im.convert('1')
im.show()

# write into file
im = im.tobitmap()
file = open("bitmap.xbm", "wb")
file.write(im)
file.close()