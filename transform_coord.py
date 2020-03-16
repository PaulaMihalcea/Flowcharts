import numpy as np
from matplotlib import pyplot as plt

# Note from the author:

# This function is the result of many simpler solutions failed because of matplotlib's incompetence.

# Its original purpose was to transform the data coordinates of a plot to pixel coordinates, but to do this it had to be enclosed in a separate function that duplicates much code found in its calling function, bounding_boxes().

# Initially, it was supposed to consist of a few lines of code in bounding_boxes() but, as it turned out, including the matplotlib function Axes.transData.transform() in a loop will cause it to return the same results even when applied to different inputs.

# Since enclosing it in an external function would have required duplicating much code (because matplotlib doesn't return plot objects, so each time you need one you have to generate it again), the next experiment was implementing multi-threading to call Axes.transData.transform() in parallel, instead of sequentially in a loop. Turns out neither matplotlib nor Pandas are thread-safe, unless you only use 'ax' in matplotlib and never call 'plt', but guess what, they are not completely equivalent and you cannot avoid calling plt. Another failed experiment.

# Finally, after adopting the current solution, the matplotlib transform function appears to be working correctly. However, calling the bounding_boxes() function in loop over more than 10 files at once causes it to become really slow, so for the conversion of an entire dataset it is better to call it manually on 5 files at a time. Multi-threading might be an option for this, but it has not been tried.

# In conclusion, matplotlib is evil. Avoid it if you can.


def transform_coord(data, bboxs, i, pboxs):

    # Plot original figure to get the correct minimum and maximum [x, y] coordinates
    for h in range(0, len(data['trace'])):  # data['trace'] is a list of traces; each element contains a trace, and each trace has a list of [x, y] coordinates
        x = []  # Contains current trace x coordinates
        y = []  # Contains current trace y coordinates
        for j in range(0, len(data['trace'][h])):  # Return j-th point of each trace
            x.append(data['trace'][h][j][0])  # Returns x coordinate of the j-th point of each trace
            y.append(data['trace'][h][j][1])  # Returns y coordinate of the j-th point of each trace
        plt.plot(x, y, color='black', linewidth=0.6)  # Plot current trace in plain black
    plt.axis('equal')  # Constrain proportions
    plt.axis('off')  # Remove axes from figure

    # Return minimum and maximum [x, y] coordinates of the plot
    x_lim = plt.gca().get_xlim()
    y_lim = plt.gca().get_ylim()

    # Arrays containing the [x, y] coordinates of the bounding box corners (plus the first one iterated in the end, needed to correctly plot a rectangle)
    corners_x = [bboxs['x_min'][i], bboxs['x_max'][i], bboxs['x_max'][i], bboxs['x_min'][i], bboxs['x_min'][i]]
    corners_y = [bboxs['y_max'][i], bboxs['y_max'][i], bboxs['y_min'][i], bboxs['y_min'][i], bboxs['y_max'][i]]

    fig, ax = plt.subplots()  # Creates a new figure and ax
    ax.plot(corners_x, corners_y)  # Plots the bounding box
    ax.axis('scaled')  # Set the axis proportions to 'scaled' (needed because the original plot is distorted on the x axis)

    # Set the [x, y] minimum and maximum limits; needed to match the bounding box plot (ax) to the original figure plot (plt)
    ax.set_xlim(x_lim[0], x_lim[1])
    ax.set_ylim(y_lim[0], y_lim[1])

    fig.canvas.draw()  # Draws the plot

    x, y = ax.transData.transform(np.vstack([corners_x[:len(corners_x)-1], corners_y[:len(corners_x)-1]]).T).T  # Transforms data coordinates to pixel coordinates

    width, height = fig.canvas.get_width_height()  # matplotlib fixes the (0, 0) point in the lower left corner, while most image software have it in the upper left corner
    y = height - y  # For this reason, y coordinates must be flipped

    # print('.', end='')  # Progress indicator

    plt.close()  # Closes the plot generated by ax (it is only needed to calculate pixel coordinates)

    # Sort x, y coordinate arrays toeasily get the minimum and maximum
    x.sort()
    y.sort()

    e = 1  # Pixels for defining bounding box margin error (the larger e, the larger the bounding box around the object)

    # Minimum and maximum pixel coordinates with margin
    x_min = int(x[0]) - e
    x_max = int(x[len(x) - 1]) + e
    y_min = int(y[0]) - e
    y_max = int(y[len(y) - 1]) + e

    # Bounding box pixel coordinates must not exceed image width and height
    if x_min < 0:
        x_min = 0
    if x_max > width:
        x_max = width
    if y_min < 0:
        y_min = 0
    if y_max > height:
        y_max = height

    pboxs = pboxs.append({'x_min': x_min, 'x_max': x_max, 'y_min': y_min, 'y_max': y_max}, ignore_index=True)  # Add pixel coordinates to pboxs, adding a ±e margin
    
    # Cast all pixel coordinates to int
    pboxs['x_min'] = pboxs['x_min'].astype(int)
    pboxs['y_min'] = pboxs['y_min'].astype(int)
    pboxs['x_max'] = pboxs['x_max'].astype(int)
    pboxs['y_max'] = pboxs['y_max'].astype(int)

    return pboxs
