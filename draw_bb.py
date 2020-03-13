import os
import cv2
from bounding_boxes import bounding_boxes


def draw_bb(inkml_file, show=False, scale=1, save=False, save_bb=False):

    filename = inkml_file.split('/')[len(inkml_file.split('/'))-1].replace('.inkml', '.png')  # Gets the current file name from the inkml file path

    img_path = './' + inkml_file.split('/')[len(inkml_file.split('/'))-2]+'_png/' + filename  # png image must have been already created with inkml2png

    img = cv2.imread(img_path)

    with open('colors', 'r') as c:  # List of colors for each class, read from the 'colors' file
        colors = eval(c.read())

    # While matplotlib uses (0, 1) RGB values for colors, OpenCV has (0, 255) BGR colors; therefore the values in the 'colors' file must be converted
    classes = list(colors.keys())  # Get the classes name as a list
    colors = list(colors.values())  # Get the color tuples as a list (of tuples)

    for c in range(0, len(colors)):
        colors[c] = tuple([255*c for c in colors[c]])  # Multiply all color values by 255 (reverse (0, 1) normalization)

        colors[c] = list(colors[c])  # Convert colors tuple to list for easy inversion of R and G values

        r = colors[c][2]
        colors[c][2] = colors[c][0]
        colors[c][0] = r
        colors[c] = tuple(colors[c])

    colors = dict(zip(classes, colors))  # Compile the colors dictionary with the new values

    pboxs, _ = bounding_boxes(inkml_file, plot=False)  # Get pixel coordinates of bounding boxes

    for i in range(0, len(pboxs)):  # Draw bounding boxes over image one by one
        cv2.rectangle(img, (int(pboxs['x_min'][i]), int(pboxs['y_min'][i])), (int(pboxs['x_max'][i]), int(pboxs['y_max'][i])),  colors[pboxs['class'][i]], 1)
        cv2.putText(img, pboxs['class'][i], (int(pboxs['x_min'][i]), int(pboxs['y_min'][i]) - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, colors[pboxs['class'][i]], 1)

    if show:  # If show = True, display the original image with bounding boxes, resized by a 'scale' factor
        height, width, _ = img.shape
        print('Press ESC to close the image window...')

        resized_img = cv2.resize(img, (int(width*scale), int(height*scale)))
        cv2.imshow(filename, resized_img)

        cv2.waitKey(0) & 0xff  # Closing the window by clicking on the X button does not kill the process; use the ESC key instead to properly close it

    if save:  # If save = True, saves the image to a new folder named after the file folder, but with '_bb' added to the end
        bb_folder = inkml_file.split('/')[len(inkml_file.split('/'))-2] + '_png_bb'

        if not os.path.exists(bb_folder):  # Creates folder if it doesn't already exist (to avoid 'directory not found' errors)
            os.makedirs(bb_folder)

        cv2.imwrite('./' + bb_folder + '/' + filename + '.png', img)

    if save_bb:
        return pboxs
