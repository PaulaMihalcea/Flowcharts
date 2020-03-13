import pandas as pd


def parse_inkml(inkml_file):

    f = open(inkml_file, 'r', encoding='Latin-1')

    cols = ['trace', 'class', 'group_id']  # Dataframe columns
    data = pd.DataFrame(columns=cols)  # data is a dataframe where the column 'trace' is a list of traces; each row contains a trace, and each trace has a list of [x, y] coordinates. Column 'class' represents the class to which the trace belongs to (see 'classes' below), while 'group_id' is the specific figure the trace belongs to (e.g. the START ellipse)
    raw_data = []  # raw_data is also a list of traces, but as the name suggests it is not ready to be further processed, as each point (made of x, y coordinates) consists of a single string item

    classes = {'arrow': 'Arrow',       # This is the list of possible classes a trace can belong to
               'connection': 'Connection',
               'data': 'Data',
               'decision': 'Decision',
               'process': 'Process',
               'terminator': 'Terminator',
               'text': 'Text'}

    for line in f:
        if line.startswith('<trace id'):  # Identifies trace lines
            raw_data.append(next(f).strip('\n').split(', '))  # Extracts traces to a list

    f.close()  # Closes file as further processing of f would return nothing

    for i in range(0, len(raw_data)):
        trace = []  # Temporarily saves trace
        for j in range(0, len(raw_data[i])):
            x, y = raw_data[i][j].split(' ')  # Splits each trace point in two coordinates
            trace.append([float(x), -float(y)])  # Re-adds them to a temporary trace as a [x, y] array
        data = data.append({'trace': trace, 'class': None, 'group_id': None}, ignore_index=True)  # Adds trace to final data (another list of traces, but in a processed, functional format); class and group_id have not been parsed yet

    f = open(inkml_file, 'r', encoding='Latin-1')  # Opens again the file, this time to parse annotations

    label = None  # Equivalent to 'class' (couldn't name it 'class' as it is a reserved Python name)
    group_id = -1  # Unique id of the figure a trace belongs to (e.g. the START ellipse)

    for line in f:
        if line.startswith('		<annotation type'):  # Identifies trace group annotation lines
            label = classes[line.replace('<annotation type="truth">', '').replace('\t', '').replace('\n', '').replace('</annotation>', '')]  # Extracts trace group class
            group_id += 1  # A new group of traces is going to be added to the dataset, so the group id must be increased

        if line.startswith('		<traceView traceDataRef'):  # Identifies single traces within a trace group annotation
            trace_id = int(line.replace('<traceView traceDataRef="', '').replace('\t', '').replace('\n', '').replace('"/>', ''))  # Returns the current trace id
            data.loc[trace_id, 'class'] = label  # Sets the trace's class in the dataset
            data.loc[trace_id, 'group_id'] = group_id  # Sets the trace's group id in the dataset

    return data  # Returns the traces dataset complete with the 'class' and 'group_id' columns
