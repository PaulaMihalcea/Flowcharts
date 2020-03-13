import matplotlib.pyplot as plt
from parse_inkml import parse_inkml


def plot_inkml(data, plot=True, save=False, classes=False):

    filename = None

    with open('colors','r') as c:  # List of colors for each class, read from the 'colors' file
        colors = eval(c.read())

    if isinstance(data, str):
        filename = data
        data = parse_inkml(data)  # Parses the inkml file if the input data is a filename (string) instead of some already processed inkml data (list)

    for i in range(0, len(data['trace'])):  # data['trace'] is a list of traces; each element contains a trace, and each trace has a list of [x, y] coordinates
        x = []
        y = []
        for j in range(0, len(data['trace'][i])):  # Returns j-th point of each trace
            x.append(data['trace'][i][j][0])  # Returns x coordinate of the j-th point of each trace
            y.append(data['trace'][i][j][1])  # Returns y coordinate of the j-th point of each trace
        if classes:
            plt.plot(x, y, color=colors[data['class'][i]], linewidth=0.6)  # Plots current trace highlighting the trace's class with a specific color
        else:
            plt.plot(x, y, color='black', linewidth=0.6)  # Plots current trace in plain black

    plt.axis('equal')  # Constrain proportions
    plt.axis('off')  # Remove axes from figure

    if plot:  # Only shows plot if plot = True
        plt.show()

    if save and filename is not None:  # If save = True and the input data is a filename (not some already processed data), it saves the plot as a 640x480 px png image in a folder with the same name as the original file folder, with '_png' added at the end
        plt.savefig(filename.partition('/')[0] + '_png/' + filename.partition('/')[2].replace('inkml', 'png'))
        plt.cla()  # Clears plot (otherwise subsequent plots would be drawn over the older ones)
