import matplotlib.pyplot as plt
from parse_inkml import parse_inkml


def plot_inkml(data, plot=True):

    if isinstance(data, str):
        data = parse_inkml(data)  # Parses the inkml file if the input data is a filename (string) instead of some already processed inkml data (list)

    for i in range(0, len(data)):  # data is a list of traces; each element contains a trace, and each trace has a list of [x ,y] coordinates
        x = []
        y = []
        for j in range(0, len(data[i])):  # Returns j-th point of each trace
            x.append(data[i][j][0])  # Returns x coordinate of the j-th point of each trace
            y.append(-data[i][j][1])  # Returns y coordinate of the j-th point of each trace
        plt.plot(x, y, color='black', linewidth=0.6)  # Plots current trace

    plt.axis('equal')  # Constrains proportions

    if plot:  # Only shows plot if flag is True
        plt.show()
