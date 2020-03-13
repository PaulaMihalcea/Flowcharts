import os
import numpy as np
import pandas as pd
from draw_bb import draw_bb


def png2bb(inkml_folder, save_bb=False):  # inkml_folder must be in the same directory as this script

    bb_folder = inkml_folder + '_png_bb'  # New bb folder name

    if save_bb:
        cols = ['filename', 'x_min', 'y_min', 'x_max', 'y_max', 'class']  # TODO
        boxes = []
        filename = []

    if not os.path.exists(bb_folder):  # Creates folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(bb_folder)

    print('Bounding box drawing started...')

    for file in os.listdir(inkml_folder):
            if '.inkml' in file:  # Only considers inkml files in folder
                print('    - drawing bounding boxes over ' + file.replace('.inkml', '.png') + '... ', end='')
                if save_bb:
                    pboxs = draw_bb('./' + inkml_folder + '/' + file, save=True, save_bb=True)  # Draws bounding boxes on a png file and saves a copy
                    boxes.append(pboxs)
                    filename.extend(np.full((1, len(pboxs)), file).tolist().pop(0))
                else:
                    draw_bb('./' + inkml_folder + '/' + file, save=True)  # Draws bounding boxes on a png file and saves a copy
                print('done!')

    print('Bounding box drawing completed.')

    if save_bb:
        annotation = pd.concat(boxes)
        annotation.insert(0, 'filename', filename)

        annotation.to_csv(inkml_folder + '/annotation.txt', columns=cols, header=False, index=False)

        print('Annotation data saved to annotation.txt.')
