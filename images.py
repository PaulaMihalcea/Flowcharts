import numpy as np
import time
import sys
import os
import random
from skimage import io
import pandas as pd
from matplotlib import pyplot as plt
from shutil import copyfile
import cv2
import tensorflow as tf

img_path = './dataset_png/writer1_1.png'
img = cv2.imread(img_path)

height, width, _ = img.shape

print(img.shape)

plt.figure(figsize=(15, 10))
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(img)

img_bbox = img.copy()

xrange = 1063
yrange = 2200

xmin = 0.3403937542430414
xmax = 0.5031398506449423
ymin = 0.8236181818181818
ymax = 0.9090909090909091
xmin = int(xmin*width)
xmax = int(xmax*width)
ymin = int(ymin*height)
ymax = int(ymax*height)

xmin = 328
xmax = 409
ymin = 379
ymax = 410


print('xmin:', xmin, 'xmax:', xmax, 'ymin:', ymin, 'ymax:', ymax)

label_name = 'Decision'
class_series = 'Decision'
class_name = 'Decision'

cv2.rectangle(img_bbox, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

# font = cv2.FONT_HERSHEY_SIMPLEX

# cv2.putText(img_bbox, class_name, (xmin, ymin - 10), font, 1, (0, 255, 0), 2)

#cv2.imshow('ciao', img)
#cv2.waitKey()

plt.subplot(1, 2, 2)
plt.title('Image with Bounding Box')
plt.imshow(img_bbox)
plt.show()
