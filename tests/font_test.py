from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageStat

ascii_list = []
for i in range(33,127):
    ascii_list.append(str(chr(i)))
ascii_list.append('\n')
for i in range(33,127):
    for j in range(33,127):
        ascii_list.append(str(chr(i)))
    ascii_list.append('\n')
ascii_string = ''.join(ascii_list)

font_ttf = ImageFont.truetype('../fonts/FSEX300.ttf', size = 22)
img_ttf = Image.new('RGB', (10000,10000))
draw = ImageDraw.Draw(img_ttf)
draw.text((0,0), ascii_string, font=None)
img_ttf = img_ttf.crop(img_ttf.getbbox())
img_ttf = img_ttf.convert('L')
img_ttf = img_ttf.resize((img_ttf.size[0], img_ttf.size[1]))
img_ttf.show()

# font_bmp = ImageFont.load('../fonts/FSEX300.ttf')
# img_bmp = Image.new('1', (300,300))
# draw = ImageDraw.Draw(img_bmp)
# draw.text((0,0), ascii_string)
# img_bmp.crop(img_bmp.getbbox())
# img_bmp.show()
