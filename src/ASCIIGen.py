"""
Version 0.1.1
"""

from PIL 	import Image, ImageEnhance
from bisect import bisect
import time

def preprocess(address, scale):
	""" 
	Processes image by:
	1. Converting to greyscale 
	2. Pumping up the contrast
	3. Resizing to fit the character size 
		* Will change this up due to loss of detail
		
	Parameters:
	address (str): 	Location of image
	scale (double):	Value to decrease the size of the output by
	
	Returns:
	image: 			Processed image
	"""
	
	img = Image.open(address)
	img = img.convert('L')
	enh = ImageEnhance.Contrast(img)
	img = enh.enhance(1.5)
	img = img.resize((int(160/scale),int(75/scale)), Image.HAMMING)
	return img
	
def generate(image):
	"""
	Creates an ASCII image using a predefined lookup table
	
	Parameters:
	image (image):	Image to be processed and generated
	
	Returns:
	string (str):	String containing the ASCII image
	"""
	
	ascii			= " .:-=+*#%@"
	breakpoints 	= [25, 51, 76, 102, 127, 153, 178, 204, 229]
	
	string = ""
	for y in range(0, image.size[1]):
		for x in range(0, image.size[0]):
			brightness 	= image.getpixel((x,y))
			char 		= ascii[bisect(breakpoints, brightness)]
			string 		= string + char
		string = string + "\n"
	
	return string

#~~~~~~~~~~~~RUNNER~~~~~~~~~~~~~#
address = "Python-Logo.png"

image 	= preprocess(address, 1.5)
ASCII 	= generate(image)
file	= open("ASCII.txt", "w")

file.write(ASCII)
file.close()

print(ASCII)