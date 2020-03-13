import cv2
from bounding_boxes import bounding_boxes


def draw_bb(inkml_file, show=False, scale=0, save=False):

    filename = inkml_file.split('/')[len(inkml_file.split('/'))-1].replace('.inkml', '.png')  # Gets the current file name from the inkml file path

    img_path = './' + inkml_file.split('/')[len(inkml_file.split('/'))-2]+'_png/' + filename

    img = cv2.imread(img_path)

    with open('colors', 'r') as c:  # List of colors for each class, read from the 'colors' file
        colors = eval(c.read())

    # While matplotlib uses (0, 1) RGB values for colors, OpenCV has (0, 255) BGR colors; therefore the values in the 'colors' file must be converted
    classes = list(colors.keys())  # Get the classes name as a list
    colors = list(colors.values())  # Get the color tuples as a list (of tuples)

    for c in range(0, len(colors)):
        colors[c] = tuple([255*c for c in colors[c]])
        colors[c] = list(colors[c])
        r = colors[c][2]
        colors[c][2] = colors[c][0]
        colors[c][0] = r
        colors[c] = tuple(colors[c])

    colors = dict(zip(classes, colors))

    pboxs, _ = bounding_boxes(inkml_file, plot=False)

    print(colors[pboxs['class'][2]])

    for i in range(0, len(pboxs)):
        cv2.rectangle(img, (int(pboxs['x_min'][i]), int(pboxs['y_min'][i])), (int(pboxs['x_max'][i]), int(pboxs['y_max'][i])),  colors[pboxs['class'][i]], 1)
        cv2.putText(img, pboxs['class'][i], (int(pboxs['x_min'][i]), int(pboxs['y_min'][i]) - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, colors[pboxs['class'][i]], 1)

    if show:
        height, width, _ = img.shape
        print('Press ESC to close the image windows...')

        resized_img = cv2.resize(img, (int(width*scale), int(height*scale)))
        cv2.imshow(filename, resized_img)

        cv2.waitKey(0) & 0xff

    if save:
        cv2.imwrite('/path/to/destination/image.png', img)
