import os
import cv2
import numpy as np


def crop(png_folder):

    cropped_folder = png_folder + '_cropped'

    if not os.path.exists(png_folder):  # Creates folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(png_folder)

    if not os.path.exists(cropped_folder):  # Creates output folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(cropped_folder)

    print('Dataset cropping started...')

    for filename in os.listdir(png_folder):

        print('Cropping ' + filename + '... ', end='')

        img = cv2.imread(png_folder + '/' + filename)  # Read the specified file

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale
        gray = 255 * (gray < 128).astype(np.uint8)  # Invert black and white

        coords = cv2.findNonZero(gray) # Find all non-zero pixels
        x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box

        for i in range(0, 13):

            if i == 0:
                img_cropped = img[y:2*y+h, 0:2*x+w]  # Crop top whitespace
            elif i == 1:
                img_cropped = img[0:2*y+h, x:2*x+w]  # Crop left whitespace
            elif i == 2:
                img_cropped = img[0:y+h, 0:2*x+w]  # Crop bottom whitespace
            elif i == 3:
                img_cropped = img[0:2*y+h, 0:x+w]  # Crop right whitespace
            elif i == 4:
                img_cropped = img[y:2*y+h, x:2*x+w]  # Crop top + left whitespace
            elif i == 5:
                img_cropped = img[y:2*y+h, 0:x+w]  # Crop top + right whitespace
            elif i == 6:
                img_cropped = img[y:y+h, 0:2*x+w]  # Crop top + bottom whitespace
            elif i == 7:
                img_cropped = img[0:2*y+h, x:x+w]  # Crop left + right whitespace
            elif i == 8:
                img_cropped = img[0:y+h, x:2*x+w]  # Crop left + bottom whitespace
            elif i == 9:
                img_cropped = img[0:y+h, 0:x+w]  # Crop right + bottom whitespace
            elif i == 10:
                img_cropped = img[0:y+h, x:x+w]  # Crop left + bottom + right whitespace
            elif i == 11:
                img_cropped = img[y:y+h, 0:x+w]  # Crop top + bottom + right whitespace
            elif i == 12:
                img_cropped = img[y:y+h, x:2*x+w]  # Crop top + left + bottom whitespace

            '''
            if i == 12:
                cv2.imshow(filename + '_cropped', img_cropped)  # Show it
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            '''

            cv2.imwrite(cropped_folder + '/' + filename.replace('.png', '') + '_cropped_' + str(i) + '.png', img_cropped)  # Save the image

        print('done!')

    print('Dataset cropping completed.')


crop('FCinkML_png')
