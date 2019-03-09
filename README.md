# ASCIIGen - ASCII Art Generator
Will generate ASCII art based on an input image.

## Progress
* Generates random ASCII characters from a predefined table of brightness to create image
* Reading font bitmaps to determine brightness values
* Optimized font analyzer (work in progress)
* Improved brightness range of ASCII table (work in progress)

## Working on
* Implementation of SSIM
* Adjusting analyzer and brightness ranges
* Color

## Progress
### Original vs Fixsys
<img src="https://raw.githubusercontent.com/392781/ASCIIGen/master/src/mona1.png" width="417"/> <img src="https://raw.githubusercontent.com/392781/ASCIIGen/master/src/ASCIImona_FSEX.jpg" width="412"/>

### ASCII - System8x12 vs Fixsys
<img src="https://raw.githubusercontent.com/392781/ASCIIGen/master/src/ASCIImona1.jpg" width="429"/> <img src="https://raw.githubusercontent.com/392781/ASCIIGen/master/src/ASCIImona_FSEX.jpg" width="400"/>

### Implemented Sources
* Mikolay, Matthew. “A Basic ASCII Art Algorithm.” Mattmik, Rovi , 24 July 2012, https://web.archive.org/web/20180331191700/http://mattmik.com/articles/ascii/ascii.html.

### In-progress Sources
* Wang, Zhou, et al. "Image quality assessment: from error visibility to structural similarity." IEEE transactions on image processing 13.4 (2004): 600-612.

