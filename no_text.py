import os
import pandas as pd

def no_text(png_folder, annotation_file=''):

    files = []
    save_to = open(annotation_file.replace('.txt', '').replace('.csv', '') + '_no_text.csv', 'a', encoding='Latin-1')

    for file in os.listdir(png_folder):
        files.append(file)

    for file in files:
        f = open(annotation_file, 'r', encoding='Latin-1')
        for line in f:
            if file in line:
                save_to.write(line)
        f.close()

    save_to.close()

# no_text('FCinkML_png_test_no_text', 'annotation_test.txt')
