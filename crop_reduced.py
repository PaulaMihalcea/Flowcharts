import os
import cv2
import random
import numpy as np
import pandas as pd


def crop_reduced(png_folder):

    pd.options.mode.chained_assignment = None  # Disable copy warnings

    annotation_file = 'annotation.csv'
    cropped_folder = png_folder + '_cropped_reduced'

    if not os.path.exists(cropped_folder):  # Creates output folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(cropped_folder)

    print('Dataset cropping started...')

    cols = ['filename', 'x_min', 'y_min', 'x_max', 'y_max', 'class']  # csv file columns
    data = pd.read_csv(annotation_file, names=cols)

    for filename in os.listdir(png_folder):

        print('Cropping ' + filename + '... ', end='')

        current_bboxs = data.copy()
        current_bboxs = current_bboxs.drop(current_bboxs[current_bboxs['filename'] != filename].index)  # Get all bounding boxes for the current file
        boxes = []  # Bounding boxes for each processed file (used to store all pboxs)

        img = cv2.imread(png_folder + '/' + filename)  # Read the specified file

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale
        gray = 255 * (gray < 128).astype(np.uint8)  # Invert black and white

        coords = cv2.findNonZero(gray)  # Find all non-zero pixels
        x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box

        i = random.randint(0, 12)

        if i == 0:
            img_cropped = img[y:2*y+h, 0:2*x+w]  # Crop top whitespace
            boxes.append(new_coords(current_bboxs.copy(), 0, y, filename, i))
        elif i == 1:
            img_cropped = img[0:2*y+h, x:2*x+w]  # Crop left whitespace
            boxes.append(new_coords(current_bboxs.copy(), x, 0, filename, i))
        elif i == 2:
            img_cropped = img[0:y+h, 0:2*x+w]  # Crop bottom whitespace
            boxes.append(new_coords(current_bboxs.copy(), 0, 0, filename, i))
        elif i == 3:
            img_cropped = img[0:2*y+h, 0:x+w]  # Crop right whitespace
            boxes.append(new_coords(current_bboxs.copy(), 0, 0, filename, i))
        elif i == 4:
            img_cropped = img[y:2*y+h, x:2*x+w]  # Crop top + left whitespace
            boxes.append(new_coords(current_bboxs.copy(), x, y, filename, i))
        elif i == 5:
            img_cropped = img[y:2*y+h, 0:x+w]  # Crop top + right whitespace
            boxes.append(new_coords(current_bboxs.copy(), 0, y, filename, i))
        elif i == 6:
            img_cropped = img[y:y+h, 0:2*x+w]  # Crop top + bottom whitespace
            boxes.append(new_coords(current_bboxs.copy(), 0, y, filename, i))
        elif i == 7:
            img_cropped = img[0:2*y+h, x:x+w]  # Crop left + right whitespace
            boxes.append(new_coords(current_bboxs.copy(), x, 0, filename, i))
        elif i == 8:
            img_cropped = img[0:y+h, x:2*x+w]  # Crop left + bottom whitespace
            boxes.append(new_coords(current_bboxs.copy(), x, 0, filename, i))
        elif i == 9:
            img_cropped = img[0:y+h, 0:x+w]  # Crop right + bottom whitespace
            boxes.append(new_coords(current_bboxs.copy(), 0, 0, filename, i))
        elif i == 10:
            img_cropped = img[0:y+h, x:x+w]  # Crop left + bottom + right whitespace
            boxes.append(new_coords(current_bboxs.copy(), x, 0, filename, i))
        elif i == 11:
            img_cropped = img[y:y+h, 0:x+w]  # Crop top + bottom + right whitespace
            boxes.append(new_coords(current_bboxs.copy(), 0, y, filename, i))
        elif i == 12:
            img_cropped = img[y:y+h, x:2*x+w]  # Crop top + left + bottom whitespace
            boxes.append(new_coords(current_bboxs.copy(), x, y, filename, i))

        cv2.imwrite(cropped_folder + '/' + filename.replace('.png', '') + '_cropped_' + str(i) + '.png', img_cropped)  # Save the image

        pboxs = pd.concat(boxes)
        pboxs.to_csv(annotation_file.replace('.csv', '') + '_cropped_reduced.csv', columns=cols, header=False, index=False, mode='a')  # Add data to the specified annotation file

        print('done!')

    print('Dataset cropping completed.')


def new_coords(current_bboxs, x, y, filename, i):

    e_min = 1  # Tolerance for minimum coordinates (in pixels)
    e_x_max = -2  # Tolerance for x maximum coordinate (in pixels)
    e_y_max = -1  # Tolerance for y maximum coordinate (in pixels)

    current_bboxs = current_bboxs.reset_index(drop=True)

    for j in range(0, len(current_bboxs['filename'])):
        current_bboxs['filename'][j] = filename.replace('.png', '') + '_cropped_' + str(i) + '.png'

        if int(current_bboxs['x_min'][j]) - x+e_min < 0:
            current_bboxs['x_min'][j] = str(0)
        else:
            current_bboxs['x_min'][j] = str(int(current_bboxs['x_min'][j]) - x+e_min)
        if int(current_bboxs['y_min'][j]) - y+e_min < 0:
            current_bboxs['y_min'][j] = str(0)
        else:
            current_bboxs['y_min'][j] = str(int(current_bboxs['y_min'][j]) - y+e_min)
        if int(current_bboxs['x_max'][j]) - x+e_x_max <0:
            current_bboxs['x_max'][j] = str(0)
        else:
            current_bboxs['x_max'][j] = str(int(current_bboxs['x_max'][j]) - x+e_x_max)
        if int(current_bboxs['y_max'][j]) - y+e_y_max < 0:
            current_bboxs['y_max'][j] = str(0)
        else:
            current_bboxs['y_max'][j] = str(int(current_bboxs['y_max'][j]) - y+e_y_max)

    return current_bboxs
