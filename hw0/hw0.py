from PIL import Image
import sys
img = Image.open(sys.argv[1])
nim3 = img.rotate( 180 )
nim3.save( "ans2.png" )