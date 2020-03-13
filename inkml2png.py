import os
from plot_inkml import plot_inkml


def inkml2png(inkml_folder):  # inkml_folder must be in the same directory as this script

    png_folder = inkml_folder + '_png'  # New png folder name

    if not os.path.exists(png_folder):  # Creates folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(png_folder)

    print('Dataset conversion started...')

    for filename in os.listdir(inkml_folder):
        if '.inkml' in filename:  # Only considers inkml files in folder
            print('Converting ' + filename + '... ', end='')
            plot_inkml(inkml_folder + '/' + filename, plot=False, save=True)  # Parses, plots and saves an inkml file
            print('done!')

    print('Dataset conversion completed.')
