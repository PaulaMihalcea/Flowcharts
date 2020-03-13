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
from bounding_boxes import bounding_boxes

inkml_file = './FCinkML/writer6_7b.inkml'
bboxs = bounding_boxes(inkml_file, plot=False)


img_path = './dataset_png/writer6_7b.png'
img = cv2.imread(img_path)

height, width, _ = img.shape

#print(img.shape)

plt.figure(figsize=(15, 10))
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(img)

img_bbox = img.copy()

xmin = 0.3403937542430414
xmax = 0.5031398506449423
ymin = 0.8236181818181818
ymax = 0.9090909090909091
xmin = int(xmin*width)
xmax = int(xmax*width)
ymin = int(ymin*height)
ymax = int(ymax*height)

xmin = 328
xmax = 343
ymin = 262
ymax = 269


#print('xmin:', xmin, 'xmax:', xmax, 'ymin:', ymin, 'ymax:', ymax)

label_name = 'Decision'
class_series = 'Decision'
class_name = 'Decision'

for i in range(0, len(bboxs)):
    cv2.rectangle(img_bbox, (int(bboxs['x_min'][i])-1, int(bboxs['y_min'][i])-1), (int(bboxs['x_max'][i])+1, int(bboxs['y_max'][i])+1), (0, 255, 0), 1)

# font = cv2.FONT_HERSHEY_SIMPLEX

# cv2.putText(img_bbox, class_name, (xmin, ymin - 10), font, 1, (0, 255, 0), 2)

#cv2.imshow('ciao', img)
#cv2.waitKey()

plt.subplot(1, 2, 2)
plt.title('Image with Bounding Box')
plt.imshow(img_bbox)
plt.show()
