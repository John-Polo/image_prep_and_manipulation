import pandas as pd
import numpy as np
import os
import glob
from pathlib import Path
import matplotlib as plt
import PIL
from PIL import Image, ImageEnhance
import statistics
from math import ceil
import re

def list_files_with_glob(directory, extension):
    return glob.glob(os.path.join(directory, '**', '*' + extension), recursive=True)

#files_directory = 'Z:/Late_blight/ms3/lamp/bright'
files_directory = 'C:\\Users\\japolo\\Documents\\data\\LAMP'
ftype_pat = '*.jpg'

# Make a list of all the files in the directory
chiplist1 = list_files_with_glob(files_directory, ftype_pat)

imgls = list()
# Read in all the files
for g in chiplist1:
    imgls.append(Image.open(g))

# Get an image that is dark and jpg
indx1 = [i for i, s in enumerate(chiplist1) if '141107.jpg' in s]
#28
imag1 = Image.open(chiplist1[28])

# Get an image that is bright and jpg
indx2 = [i for i, s in enumerate(chiplist1) if '115410.jpg' in s]
imag2 = Image.open(chiplist1[4])

imag1.show()

# Test of measure and adjust brightness
# Get values of image
enhan1 = ImageEnhance.Brightness(imag1)
# Change the brightness
fac1 = 4
imag1_2 = enhan1.enhance(fac1)
imag1_2.save('C:/Users/japolo/Pictures/temp/chipimgtest/bright1.jpg')

# Return a brightness value
def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)
    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)
    return 1 if brightness == 255 else brightness / scale

lofbri = list()
for i in range(0, len(chiplist1)):
    lofbri.append(calculate_brightness(imgls[i]))

# Get some idea of the values from the list of images
mxbr = max(lofbri)
# 0.342
mnbr = min(lofbri)
# 0.016
# average
# 0.13
# stddev
# 0.07

# Brighten images that are below a certain value. It was 0.14 for one batch, then 0.1 for another.
def brighten(image, brt1):
    # Get the ceiling of division by using floor operator, //. Adjust the constant as needed.
    factr1 = ceil(0.14 / brt1) 
    print(factr1)
    imag_br = ImageEnhance.Brightness(image).enhance(factr1)
    return imag_br

# Loop to compare and brighten
for i in range(0, len(lofbri)):
    nm1 = 'Z:\\Late_blight\\ms3\\lamp\\bright\\more\\' + re.findall(r'[0-9]{8}_[0-9]{6}', chiplist1[i])[0] + '.jpg'
    print(nm1)
    img = imgls[i]
    brht = calculate_brightness(img)
    print(brht)
    if brht < 0.13:
        tem_im = brighten(img, brht)
        nm1 = nm1.replace('.jpg', '_br.jpg')
        print(nm1)
        tem_im.save(nm1)
    else:
        img.save(nm1)

