'''
from PIL import Image
import numpy as np



im=Image.open("Lena.png")
width, height=im.size
print width
print height
'''

'''

im=Image.open(filename)

width, height=im.size

data=im.getdata()

rgb=im.getpixel((x,y))
'''
'''
from PIL import Image
img = Image.open("Lena.png")
width, height = img.size
 
for y in range(height):
    for x in range(width):
        rgba = img.getpixel((x,y))
        #rgba = (255 - rgba[0],255 - rgba[1],255 - rgba[2],rgba[3]);
        rgba=(255,255,255,rgba[3])
        img.putpixel((x,y), rgba)
 
img.show()
img.save("new.png")
'''
from PIL import Image
import sys
img = Image.open(sys.argv[1])
nim3 = img.rotate( 180 )
nim3.save( "ans2.png" )