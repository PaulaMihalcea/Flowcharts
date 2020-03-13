from svg2inkml import svg2inkml
from parse_inkml import parse_inkml
from plot_inkml import plot_inkml

# Example svg to inkml conversion and inkml plotting
n = 14

for i in range(0, n+1):
    svg_file = './NeoSmartpenM1_demo/neo_smtpen_m1_demo_' + str(i) + '.svg'  # svg file to be converted to inkml
    inkml_file = './NeoSmartpenM1_demo/neo_smtpen_m1_demo_' + str(i) + '.inkml'  # Converted file name
    svg2inkml(svg_file, inkml_file)  # Converts svg file to inkml
    plot_inkml(inkml_file)  # Plots the returned data

# Other test plots
show = True
plot_inkml(parse_inkml('./FCinkML/writer3_5.inkml'), plot=show)  # Plots a random inkml file from the dataset (by parsed data)
plot_inkml('./FCinkML/writer3_5.inkml', plot=show)  # Plots a random inkml file from the dataset (by filename)

plot_inkml(parse_inkml('./FCinkML/writer3_5.inkml'), plot=show, classes=True)  # Plots a random inkml file from the dataset (by parsed data) and highlights classes
plot_inkml('./FCinkML/writer3_5.inkml', plot=show, classes=True)  # Plots a random inkml file from the dataset (by filename) and highlights classes
