import pandas as pd
import matplotlib.pyplot as plt
from parse_inkml import parse_inkml
from transform_coord import transform_coord


def bounding_boxes(inkml_file, plot=False):

    data = parse_inkml(inkml_file)  # Parses inkml file

    cols = ['x_min', 'x_max', 'y_min', 'y_max', 'class']  # Columns of bboxs dataframe
    bboxs = pd.DataFrame(columns=cols)  # Dataframe containing all coordinates of all bounding boxes, plus the class for each bounding box

    if plot:  # If plot = True, plot the original figure first

        with open('colors','r') as c:  # List of colors for each class, read from the 'colors' file
            colors = eval(c.read())

        for i in range(0, len(data['trace'])):  # data['trace'] is a list of traces; each element contains a trace, and each trace has a list of [x, y] coordinates
            x = []  # Contains current trace x coordinates
            y = []  # Contains current trace y coordinates
            for j in range(0, len(data['trace'][i])):  # Return j-th point of each trace
                x.append(data['trace'][i][j][0])  # Returns x coordinate of the j-th point of each trace
                y.append(data['trace'][i][j][1])  # Returns y coordinate of the j-th point of each trace
            plt.plot(x, y, color='black', linewidth=0.6)  # Plot current trace in plain black
        plt.axis('equal')  # Constrain proportions
        plt.axis('off')  # Remove axes from figure

    for k in range(0, len(data['group_id'].drop_duplicates())):  # For each unique trace group of the inkml file...

        group_x = []  # Contains all x coordinates of all traces in a specific trace group
        group_y = []  # Contains all y coordinates of all traces in a specific trace group

        for i in range(0, len(data['trace'])):  # ...for each trace in the dataset...
            for j in range(0, len(data['trace'][i])):  # ...for each pair of [x, y] coordinates in trace i...
                if data['group_id'][i] == k:  # ...get the [x, y] coordinates in two separate arrays
                    label = data['class'][i]  # Identify the class of the current bounding box
                    group_x.append(data['trace'][i][j][0])  # Add all x coordinates of trace i to the group x coordinates
                    group_y.append(data['trace'][i][j][1])  # Add all y coordinates of trace i to the group y coordinates

        group_x.sort()  # Sort the x coordinates array
        group_y.sort()  # Sort the y coordinates array

        bboxs = bboxs.append({'x_min': group_x[0], 'x_max': group_x[len(group_x) - 1], 'y_min': group_y[0], 'y_max': group_y[len(group_y) - 1], 'class': label}, ignore_index=True)  # Save minimum and maximum [x, y] coordinates to the bboxs dataframe
        # Add +1 to the maximum coordinates and -1 to the minimum to get

        x_coord = [group_x[0], group_x[len(group_x)-1], group_x[len(group_x)-1], group_x[0], group_x[0]]  # Contain all x coordinates of a bounding box, plus the first one repeated to be able to draw a rectangle over the figure
        y_coord = [group_y[len(group_y)-1], group_y[len(group_y)-1], group_y[0], group_y[0], group_y[len(group_y)-1]]  # Contain all x coordinates of a bounding box, plus the first one repeated to be able to draw a rectangle over the figure

        if plot:  # If plot = True, plot one by one the resulting bounding boxes over the original figure from data coordinates (not pixels!), that has also been plotted if plot = True
            plt.plot(x_coord, y_coord, color=colors[label], linewidth=1)

    pboxs = pd.DataFrame(columns=cols)  # Create a new dataframe containing the pixel coordinates of the bounding boxes

    filename = inkml_file.split('/')[len(inkml_file.split('/'))-1]  # Gets the current file name from the inkml file path
    # print('Calculating pixel coordinates for ' + filename, end='')

    for i in range(0, len(bboxs)):  # Transform data coordinates in bboxs to pixel coordinates
        pboxs = transform_coord(data, bboxs, i, pboxs)

    # print(' done.')

    if plot:  # If plot = True, show the generated plot; the whole plot thing is for debug purposes only (and nice, coloured images)
        plt.show()

    pboxs['class'] = bboxs[['class']].copy()  # Copy the labels from the original bboxs dataframe, as they will not change later

    return pboxs, bboxs

bounding_boxes('./FCinkML/writer1_1.inkml')
