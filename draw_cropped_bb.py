import cv2
import pandas as pd


for n in range(0, 13):

    pboxs = pd.read_csv('annotation_cropped.csv', names=['filename', 'x_min', 'y_min', 'x_max', 'y_max', 'class'])
    pboxs = pboxs.drop(pboxs[pboxs['filename'] != 'writer12_4_cropped_' + str(n) + '.png'].index)
    pboxs = pboxs.reset_index(drop=True)
    print(pboxs)
    img = cv2.imread('FCinkML_png_cropped/writer12_4_cropped_' + str(n) + '.png')

    with open('colors', 'r') as c:  # List of colors for each class, read from the 'colors' file
        colors = eval(c.read())


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

    for i in range(0, len(pboxs)):  # Draw bounding boxes over image one by one
        cv2.rectangle(img, (int(pboxs['x_min'][i]), int(pboxs['y_min'][i])), (int(pboxs['x_max'][i]), int(pboxs['y_max'][i])),  colors[pboxs['class'][i]], 1)
        cv2.putText(img, pboxs['class'][i], (int(pboxs['x_min'][i]), int(pboxs['y_min'][i]) - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, colors[pboxs['class'][i]], 1)

    cv2.imshow(str(n), img)

    cv2.waitKey(0) & 0xff
