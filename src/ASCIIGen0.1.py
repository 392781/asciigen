from PIL import Image, ImageEnhance
import time

def preprocess(address):
	img = Image.open(address)
	img = img.convert('L')
	img.show()
	enh = ImageEnhance.Contrast(img)
	img = enh.enhance(1.3)
	img.show()
	img = img.resize((160,75), Image.HAMMING)
	img.show()
	return img
	
def asciier(image):
	return image 
	
address = "Python-Logo.png"

preprocess(address)