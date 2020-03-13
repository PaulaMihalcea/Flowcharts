import os
import numpy as np
import pandas as pd
from draw_bb import draw_bb


def png2bb_single(inkml_folder, inkml_file, save_bb=False):  # inkml_folder must be in the same directory as this script

    bb_folder = inkml_folder + '_png_bb'  # New bb folder name

    if save_bb:  # If save_bb = True, bounding boxes pixel coordinates will be saved in a special csv file, annotation_pathless.txt
        cols = ['filename', 'x_min', 'y_min', 'x_max', 'y_max', 'class']  # csv file columns
        boxes = []  # Bounding boxes for each processed file (used to store all pboxs)
        filename = []  # 'filename' column of the annotation dataframe

    if not os.path.exists(bb_folder):  # Creates folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(bb_folder)

    print('Bounding box drawing started... ', end='')

    if save_bb:  # If save_bb = True, append the pboxs and filename of the current file to the boxes and filename list
        pboxs = draw_bb('./' + inkml_folder + '/' + inkml_file, save=True, save_bb=True)  # Draws bounding boxes on a png file and saves a copy
        boxes.append(pboxs)
        filename.extend(np.full((1, len(pboxs)), inkml_file.replace('.inkml', '.png')).tolist().pop(0))
    else:
        draw_bb('./' + inkml_folder + '/' + inkml_file, save=True)  # Draw bounding boxes on a png file and saves a copy

    print('done!')

    print('Bounding box drawing completed.')

    if save_bb:  # If save_bb = True, create the annotation dataframe with the collected data
        annotation = pd.concat(boxes)
        annotation.insert(0, 'filename', filename)

        # Cast all pixel coordinates to int
        annotation['x_min'] = annotation['x_min'].astype(int)
        annotation['y_min'] = annotation['y_min'].astype(int)
        annotation['x_max'] = annotation['x_max'].astype(int)
        annotation['y_max'] = annotation['y_max'].astype(int)

        annotation.to_csv(inkml_folder + '/annotation_pathless_' + inkml_file + '.txt', columns=cols, header=False, index=False)  # Save file

        print('Annotation data saved to annotation_pathless_' + inkml_file + '.txt.')


file = '4_11'
inkml_folder = 'FCinkML'
inkml_file = 'writer' + file + '.inkml'

png2bb_single(inkml_folder, inkml_file, save_bb=True)
