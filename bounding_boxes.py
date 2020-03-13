import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread  # Multi-threading
from parse_inkml import parse_inkml

from potato import potato




def bounding_boxes(inkml_file, plot=False):

    data = parse_inkml(inkml_file)  # Parses inkml file

    cols = ['x_min', 'x_max', 'y_min', 'y_max']  # Columns of bboxs dataframe
    bboxs = pd.DataFrame(columns=cols)  # Dataframe containing all coordinates of all bounding boxes

    colors = {0: 'lightseagreen',  # This is the list of colors for each class
              1: 'gold',
              2: 'darkgreen',
              3: 'darkorange',
              4: 'darkblue',
              5: 'darkred',
              6: 'darkgrey'}

    if plot:  # If plot = True, plots the original figure first

        for i in range(0, len(data['trace'])):  # data['trace'] is a list of traces; each element contains a trace, and each trace has a list of [x, y] coordinates
            x = []
            y = []
            for j in range(0, len(data['trace'][i])):  # Returns j-th point of each trace
                x.append(data['trace'][i][j][0])  # Returns x coordinate of the j-th point of each trace
                y.append(data['trace'][i][j][1])  # Returns y coordinate of the j-th point of each trace
            plt.plot(x, y, color='black', linewidth=0.6)  # Plots current trace in plain black
        plt.axis('equal')  # Constrains proportions
        plt.axis('off')  # Removes axes from figure

    for k in range(0, len(data['group_id'].drop_duplicates())):  # For each unique trace group of the inkml file...

        x_pix = []
        y_pix = []
        group_x = []  # Contains all x coordinates of all traces in a specific trace group
        group_y = []  # Contains all y coordinates of all traces in a specific trace group

        for i in range(0, len(data['trace'])):  # ...for each trace in the dataset...
            for j in range(0, len(data['trace'][i])):  # ...for each pair of [x, y] coordinates in trace i...
                if data['group_id'][i] == k:  # ...gets the [x, y] coordinates in two separate arrays
                    col = data['class'][i]  # Class color for the current bounding box, used in the plot
                    group_x.append(data['trace'][i][j][0])  # Adds all x coordinates of trace i to the group x coordinates
                    group_y.append(data['trace'][i][j][1])  # Adds all y coordinates of trace i to the group y coordinates

        group_x.sort()  # Sorts the x coordinates array
        group_y.sort()  # Sorts the y coordinates array

        bboxs = bboxs.append({'x_min': group_x[0], 'x_max': group_x[len(group_x) - 1], 'y_min': group_y[0], 'y_max': group_y[len(group_y) - 1]}, ignore_index=True)  # Saves minimum and maximum [x, y] coordinates to the bboxs dataframe

        x_coord = [group_x[0], group_x[len(group_x) - 1], group_x[len(group_x) - 1], group_x[0], group_x[0]]  # Contains all x coordinates of a bounding box, plus the first one repeated to be able to draw a rectangle over the figure
        y_coord = [group_y[len(group_y) - 1], group_y[len(group_y) - 1], group_y[0], group_y[0], group_y[len(group_y) - 1]] # Contains all x coordinates of a bounding box, plus the first one repeated to be able to draw a rectangle over the figure

        plt.plot(x_coord, y_coord, color=colors[col], linewidth=1)  # Plots one by one the resulting bounding boxes over the original figure, that has been already plotted if plot = True; if not, it only plots the bounding boxes, and it is needed to correctly calculate the pixel coordinates

    pboxs = pd.DataFrame(columns=cols)

    threads = []
    x_lim_min = plt.gca().get_xlim()[0]
    x_lim_max = plt.gca().get_xlim()[1]
    y_lim_min = plt.gca().get_ylim()[0]
    y_lim_max = plt.gca().get_ylim()[1]

    print('Calculating pixel coordinates', end='')
    for i in range(0, len(bboxs)):
        pboxs = potato(data, bboxs, i, pboxs, x_lim_min, x_lim_max, y_lim_min, y_lim_max)

    # print(pboxs)

    return pboxs

'''
    for i in range(0, len(bboxs)):
        process = Thread(target=transform, args=[bboxs, i, pboxs, x_lim_min, x_lim_max, y_lim_min, y_lim_max])
        process.start()
        threads.append(process)
    for process in threads:
        process.join()

    if plot:  # If plot = True, shows the resulting plot with bounding boxes
        plt.show()

    #print(pboxs)
'''

##############################################################################################

inkml_file = './FCinkML/writer1_1.inkml'

bounding_boxes(inkml_file)
