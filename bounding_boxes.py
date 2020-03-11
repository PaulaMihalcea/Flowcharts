import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

inkml_file = './FCinkML/writer1_1.inkml'

f = open(inkml_file, 'r', encoding='Latin-1')

data = []  # data is a list of traces; each element contains a trace, and each trace has a list of [x, y] coordinates
raw_data = []  # raw_data is also a list of traces, but as the name suggests it is not ready to be further processed, as each point (made of x, y coordinates) consists of a single string item

for line in f:
    if line.startswith('<trace id'):  # Identifies trace lines
        raw_data.append(next(f).strip('\n').split(', '))  # Extracts traces to a list
f.close()

for i in range(0, len(raw_data)):
    trace = []  # Temporarily saves trace
    for j in range(0, len(raw_data[i])):
        x, y = raw_data[i][j].split(' ')  # Splits each trace point in two coordinates
        trace.append([float(x), float(y)])  # Re-adds them to a temporary trace as a [x, y] array
    data.append(trace)  # Adds trace to final data (another list of traces, but in a processed, functional format)


# Ogni elemento di data corrisponde ad una traccia
# print(data[100])

f = open(inkml_file, 'r', encoding='Latin-1')

classes = {'arrow': 0,
          'data': 1,
          'decision': 2,
          'process': 4,
          'terminator': 5,
          'text': 6}



etichette = np.empty(len(data))
trace_group_id = -1
trace_group = np.empty(len(data))
line_number = 0
for line in f:
    line_number += 1
    if line.startswith('		<annotation type'):  # Identifies trace lines
        label = int(classes[line.replace('<annotation type="truth">', '').replace('\t', '').replace('\n', '').replace('</annotation>', '')])
        trace_group_id += 1
        print(trace_group_id, line_number)
        #print(line_number)  # Questo è il numero della linea contenente 'annotation type'
    if line.startswith('		<traceView traceDataRef'):
        x = int(line.replace('<traceView traceDataRef="', '').replace('\t', '').replace('\n', '').replace('"/>', ''))
        etichette[x] = label
        trace_group[x] = trace_group_id  # contiene il gruppo di appartenenza di ogni traccia
        #print('label:', label)
        #print('trace:', x)

print()
print('etichette:',etichette)  # Ogni elemento di questo array corrisponde alla categoria cui appartiene la traccia corrispondente






for i in range(0, len(data)):  # data is a list of traces; each element contains a trace, and each trace has a list of [x, y] coordinates
    x = []
    y = []
    for j in range(0, len(data[i])):  # Returns j-th point of each trace
        x.append(data[i][j][0])  # Returns x coordinate of the j-th point of each trace
        y.append(-data[i][j][1])  # Returns y coordinate of the j-th point of each trace
    if trace_group[i] == 0:
        plt.plot(x, y, color='blue', linewidth=0.6)  # Plots current trace
    else:
        plt.plot(x, y, color='black', linewidth=0.6)  # Plots current trace


print()
print()

k = 0
group_x = []
group_y = []

print('trace_group_id:', trace_group_id)

for k in range(0, trace_group_id):
    print(k)
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            if trace_group[i] == k:
                #print('i:', i,'j:',j,'data[i][j]:',data[i][j][0])
                group_x.append(data[i][j][0])  # contiene tutte le coordinate x della traccia i
                group_y.append(-data[i][j][1])  # contiene tutte le y della traccia i

    #print(group_x)
    #print(group_y)
    #print(k)
    group_x.sort()
    group_y.sort()
    min_x = group_x[0]
    min_y = group_y[0]
    max_x = group_x[len(group_x)-1]
    max_y = group_y[len(group_y)-1]

    coord_x = [min_x, max_x, max_x, min_x, min_x]
    coord_y = [max_y, max_y, min_y, min_y, max_y]

    plt.plot(coord_x, coord_y, color='red', linewidth=0.3)

    group_x = []
    group_y = []
    coord_x = []
    coord_y = []




plt.axis('equal')  # Constrains proportions
plt.axis('off')  # Removes axes from figure

plt.show()
