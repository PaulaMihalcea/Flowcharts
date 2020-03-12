import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
           'connection': 1,
          'data': 2,
          'decision': 3,
          'process': 4,
          'terminator': 5,
          'text': 6}


cols = ['x', 'y', 'class', 'group_id']  # class = label
df = pd.DataFrame(columns=cols)

for i in range(0, len(data)):
    for j in range(0, len(data[i])):
        #print('x:',data[i][j][0],'y:',data[i][j][1])
        df = df.append({'x': data[i][j][0], 'y': data[i][j][1], 'class': -1, 'group_id': -1}, ignore_index=True)

row = df.loc[115, 'x']
#print(type(row))



etichette = np.empty(len(data))
trace_group_id = -1
trace_group = np.empty(len(data))
line_number = 0



for line in f:
    line_number += 1
    if line.startswith('		<annotation type'):  # Identifies trace lines
        label = int(classes[line.replace('<annotation type="truth">', '').replace('\t', '').replace('\n', '').replace('</annotation>', '')])
        trace_group_id += 1
        #print(trace_group_id, line_number)
        #print(line_number)  # Questo è il numero della linea contenente 'annotation type'
    if line.startswith('		<traceView traceDataRef'):
        x = int(line.replace('<traceView traceDataRef="', '').replace('\t', '').replace('\n', '').replace('"/>', ''))
        df.loc[x, 'class'] = label
        df.loc[x, 'group_id'] = trace_group_id  # contiene il gruppo di appartenenza di ogni traccia
        #print('label:', label)
        #print('trace:', x)

#print()
#print('etichette:',etichette)  # Ogni elemento di questo array corrisponde alla categoria cui appartiene la traccia corrispondente






for i in range(0, len(data)):  # data is a list of traces; each element contains a trace, and each trace has a list of [x, y] coordinates
    x = []
    y = []
    for j in range(0, len(data[i])):  # Returns j-th point of each trace
        x.append(data[i][j][0])  # Returns x coordinate of the j-th point of each trace
        y.append(-data[i][j][1])  # Returns y coordinate of the j-th point of each trace
    if int(df.loc[i, 'group_id']) == 0:
        plt.plot(x, y, color='blue', linewidth=0.6)  # Plots current trace
    else:
        plt.plot(x, y, color='black', linewidth=0.6)  # Plots current trace


#print()
#print()

k = 0
group_x = []
group_y = []

#print('trace_group_id:', trace_group_id)

for k in range(0, trace_group_id):
    #print(k)
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            if df.loc[i, 'group_id'] == k:
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




##############################################################################################

group_x = []
group_y = []
coord_x = []
coord_y = []

for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            if df.loc[i, 'group_id'] == 24:
                #print('i:', i,'j:',j,'data[i][j]:',data[i][j][0])
                group_x.append(data[i][j][0])  # contiene tutte le coordinate x della traccia i
                group_y.append(-data[i][j][1])  # contiene tutte le y della traccia i


group_x.sort()
group_y.sort()

min_x = group_x[0]
min_y = group_y[0]
max_x = group_x[len(group_x)-1]
max_y = group_y[len(group_y)-1]
print('min_x:',min_x,'max_x:',max_x,'min_y:',min_y,'max_y:',max_y)
print()

coord_x = [min_x, max_x, max_x, min_x, min_x]  # coord_x = [min_x, max_x, max_x, min_x]
coord_y = [max_y, max_y, min_y, min_y, max_y]  # coord_y = [max_y, max_y, min_y, min_y]

xlim = plt.gca().get_xlim()  # xlim = [0, 1531.84995+468.15104999999994]
ylim = plt.gca().get_ylim()  # ylim = [0, 2200]
print('xlim:', xlim, 'ylim:', ylim)
plt.plot(coord_x, coord_y, color='lightgreen', linewidth=1)



fig, ax = plt.subplots()
points, = ax.plot(coord_x, coord_y, 'ro')  # 'ro' è il colore (pallini rossi); l'array sono le y dei punti
ax.axis('scaled')
# ax.axis([xlim[0], xlim[1], ylim[0], ylim[1]])
ax.set_xlim(xlim[0], xlim[1])
ax.set_ylim(ylim[0], ylim[1])

# Get the x and y data and transform it into pixel coordinates
x, y = points.get_data()
fig.canvas.draw()

'''
print()
print([x, y])
print(np.vstack([x, y]))
print(np.vstack([x, y]).T)
print()
'''

print('x:',x)
print('coord_x:', coord_x)
print('coord_y:', coord_y)
xy_pixels = ax.transData.transform(np.vstack([x, y]).T)
xpix, ypix = xy_pixels.T
print('xpix:',xpix)

# In matplotlib, 0,0 is the lower left corner, whereas it's usually the upper
# left for most image software, so we'll flip the y-coords...
width, height = fig.canvas.get_width_height()
ypix = height - ypix
print('ypix:',ypix)

print()

print('Coordinates of the points in pixel coordinates...')
for xp, yp in zip(xpix, ypix):
    print('{x:0.0f}\t{y:0.0f}'.format(x=xp, y=yp))
print('(0,0):', ax.transData.transform((0, 0)))


# We have to be sure to save the figure with it's current DPI
# (savfig overrides the DPI of the figure, by default)
fig.savefig('test.png', dpi=fig.dpi)

'''
xrange = xlim[1] - xlim[0]
yrange = ylim[1] - ylim[0]
print('xrange:', xrange, 'yrange:', yrange)
xmin = min_x/xrange
xmax = max_x/xrange
ymin = min_y/yrange
ymax = max_y/yrange
print('xmin:', xmin, 'xmax:', xmax, 'ymin:', ymin, 'ymax:', ymax)
'''

##############################################################################################


plt.axis('scaled')  # Constrains proportions
#plt.axis('off')  # Removes axes from figure

plt.show()
