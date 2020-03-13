import os
from draw_bb import draw_bb


def png2bb(inkml_folder):  # inkml_folder must be in the same directory as this script

    bb_folder = inkml_folder + '_png_bb'  # New bb folder name

    if not os.path.exists(bb_folder):  # Creates folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(bb_folder)

    print('Bounding box drawing started...')

    for filename in os.listdir(inkml_folder):
            if '.inkml' in filename:  # Only considers inkml files in folder
                print('    - drawing bounding boxes over ' + filename.replace('.inkml', '.png') + '... ', end='')
                draw_bb('./' + inkml_folder + '/' + filename, save=True)  # Draws bounding boxes on a png file and saves a copy
                print('done!')

    print('Bounding box drawing completed.')
