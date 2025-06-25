# https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html
# A lot of this code is from a Google Collab notebook

import os
import sys
import numpy as np
#import torch
#import torch.utils.data
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#from google.colab import drive
#drive.mount('/content/drive', force_remount=True)

os.chdir("Z:\\Late_blight\\ms3\\lamp\\bright")

chiplist1 = []
for root, dirs, files in os.walk(os.path.abspath(os.getcwd())):
    for file in files:
        chiplist1.append(os.path.join(root, file))


## Where are the new RAW images that will need to be changed before modeling?
#img_dir = input("Please provide a directory path that has the images awaiting\
# analysis.")
#
#try:
#    os.path.exists(os.getcwd,img_dir) == False
#except:
#    exit("The path provided does not exist. Do you need to provide a\
#    leading '/' (on Windows, you need to provide 'C:\' instead).")
#
#os.chdir(img_dir)
#print("The directory provided was {}.".format(os.getcwd()))

## Searching for a file type ending. Right now, this is .jpg. Should change to __?
#inlist = list()
#
#for i in os.listdir("/content/drive/MyDrive/LAMP2023/bright"):
#    if i.endswith(".jpg"):
#        inlist.append(i)
#
#inlist

# A loop to recreate the full directory name with the file so that the file
# can be read and processed with centercrop()
mdls = []
for n in range(len(chiplist1)):
    mdls.append(os.path.join("Z:\\Late_blight\\ms3\\lamp\\bright", chiplist1[n]))

# Images that were green channel only
mdlsrem = list(filter(lambda w: 'green' in w, mdls))

# Get the difference of the two lists to remove the green channel images
#mdls.difference(mdlsrem) # This doesn't work
mdls = set(mdls) - set(mdlsrem)

# The crop rectangle: (left, upper, right, lower)-tuple.
def centercrop(img, newsize):
    width, height = img.size   # Get dimensions
    print(img.size)
    left = int((width - int(newsize))/2)
    print(left)
    top = int((height - int(newsize))/2)
    print(top)
    bottom = int(height - top)
    right = int(width - left)
    # Crop the center of the image
    ccrp = img.crop((left, top, right, bottom))
    return ccrp

# Create file names for new files to use with crop
mdls2 = []
for p in range(len(mdls)):
#    mdls2.append(os.path.join(os.getcwd(),'cropped',inlist[p].replace('tif', 'png')))
     mdls2.append(os.path.join(os.getcwd().replace('bright',''),'cropped',mdls[p]))

# Read, rotate if necessary, and crop to the size indicated
for p in range(len(mdls)):
    im_t = Image.open(mdls[p])
    print(im_t.size)
    if im_t.size[0] > im_t.size[1]:
        im_t = np.array(im_t)
        im_t = np.rot90(im_t, 3)
        im_t = Image.fromarray(im_t)
        print("Note: horizontal images detected. Inspect orientation.")
        im_t = centercrop(im_t, 1500)
        im_t.save(mdls2[p])
    else:
        im_t = centercrop(im_t, 1500)
        im_t.save(mdls2[p])
