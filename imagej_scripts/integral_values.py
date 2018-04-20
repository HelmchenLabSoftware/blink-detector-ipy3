# TODO:
# 4) Save metrics to file
# 5) Use copy of stack to save time on visualisation

from ij import IJ
from ij.plugin import Duplicator
from jarray import array
from java.awt import Color
from ij.gui import Plot

# Faster dot product
from itertools import imap
import operator

img2 = IJ.getImage()
#img2 = Duplicator().run(img1);

def expectedImgRad(pix, rad):
  return sum(imap(operator.mul, pix, rad))
  #return sum([pix[i] * rad[i] for i in range(len(pix))])

print("Processing image", img2.title)
print("width:", img2.width)
print("height:", img2.height)
print("number of slices:", img2.getNSlices())
print("number of channels:", img2.getNChannels())
print("number of time frames:", img2.getNFrames())

# Constants
nPix = img2.width * img2.height
normPix = nPix * 255;
normRad = (img2.width ** 2 + img2.height**2)**(0.5) / 2
xmid = float(img2.width / 2)
ymid = float(img2.height / 2)

# Pixel coordinates and related quantities
pixIdxList = list(range(nPix))
xpos = array([float(i % img2.width) for i in pixIdxList], 'd')
ypos = array([float(i / img2.width) for i in pixIdxList], 'd')
radNorm = array([((xpos[i] - xmid)**2 + (ypos[i]-ymid)**2)**(0.5) / normRad for i in pixIdxList], 'd')

# X-axis for plot
slicesIdx = array(list(range(img2.getNSlices())), 'd')

# Y-axis for plot
sliceAvgInt          = array([0] * img2.getNSlices(), 'd');
sliceAboveZeroNorm   = array([0] * img2.getNSlices(), 'd');
sliceExpectedRadNorm = array([0] * img2.getNSlices(), 'd');


for currentFrame in range(1, img2.getNFrames() + 1):
  for currentSlice in range(1, img2.getNSlices() + 1):
    img2.setSlice(currentSlice)
    imgProc = img2.getProcessor().convertToFloat()      # Convert to float to avoid integer problems
    pixels = imgProc.getPixels()

    intensityTotal = float(sum(pixels))
    pixelsAboveZero = float(sum(p > 0 for p in pixels))
#    print(pixelsAboveZero)

    if pixelsAboveZero > 0:
      sliceAvgInt[currentSlice-1]          = intensityTotal / pixelsAboveZero / 255
      sliceAboveZeroNorm[currentSlice-1]   = pixelsAboveZero / nPix
      sliceExpectedRadNorm[currentSlice-1] = expectedImgRad(pixels, radNorm) / intensityTotal
      
    else:
      sliceAvgInt[currentSlice-1]          = 0
      sliceAboveZeroNorm[currentSlice-1]   = 0
      sliceExpectedRadNorm[currentSlice-1] = 0

print("writing to file...")

myfile = open('/home/aleksejs/rez.txt', 'w')
for i in range(len(slicesIdx)):
  myfile.write(str(slicesIdx[i]) + " " + str(sliceAvgInt[i]) + " " + str(sliceAboveZeroNorm[i]) + " " + str(sliceExpectedRadNorm[i]) + "\n")
myfile.close()

print("plotting...")

plot = Plot("Title", "X", "Y")
plot.setLimits(1.0, img2.getNSlices(), 0.0, 1.0)
plot.setColor(Color.RED)
plot.addPoints(slicesIdx, sliceAvgInt, Plot.CROSS)
plot.setColor(Color.BLUE)
plot.addPoints(slicesIdx, sliceAboveZeroNorm, Plot.CROSS)
plot.setColor(Color.GREEN)
plot.addPoints(slicesIdx, sliceExpectedRadNorm, Plot.CROSS)
plot.show()
