import os
import cv2
import pandas as pd


def bb_test(img_folder, csv_file, bb_folder):
    cols = ['filename', 'x_min', 'y_min', 'x_max', 'y_max', 'class']  # csv file columns

    pboxs = pd.read_csv(csv_file, header=None)  # Loads csv file as a Pandas dataframe
    pboxs.columns = cols  # Define dataframe column names

    # Load colors
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

    if not os.path.exists(bb_folder):  # Create folder if it doesn't already exist (to avoid 'directory not found' errors)
        os.makedirs(bb_folder)

    filename = None  # Current processed file name
    old_filename = None  # Previous processed file name

    for i in range(0, len(pboxs)):  # Draw bounding boxes over image one by one
        if i >= 1:  # Avoids referencing a negative index
            old_filename = pboxs['filename'][i-1]

        filename = pboxs['filename'][i]
        img_path = img_folder + pboxs['filename'][i]  # Path of the original image (no bounding boxes drawn)

        if filename != old_filename or filename is None:  # Load a new image if this is the first iteration or the file name has changed in the current dataframe line
            img = cv2.imread(img_path)
        else:  # Else, if the current line from the dataframe contains a bounding box of the same file, don't load the original image again
            pass

        cv2.rectangle(img, (int(pboxs['x_min'][i]), int(pboxs['y_min'][i])), (int(pboxs['x_max'][i]), int(pboxs['y_max'][i])),  colors[pboxs['class'][i]], 1)  # Draw bounding boxes
        cv2.putText(img, pboxs['class'][i], (int(pboxs['x_min'][i]), int(pboxs['y_min'][i]) - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, colors[pboxs['class'][i]], 1)  # Add class name

        cv2.imwrite('./' + bb_folder + '/' + pboxs['filename'][i], img)  # Save image to the bb_test folder
