def parse_inkml(inkml_file):

    f = open(inkml_file, 'r', encoding='Latin-1')

    data = []  # data is a list of traces; each element contains a trace, and each trace has a list of [x, y] coordinates
    raw_data = []  # raw_data is also a list of traces, but as the name suggests it is not ready to be further processed, as each point (made of x, y coordinates) consists of a single string item

    for line in f:
        if line.startswith('<trace id'):  # Identifies trace lines
            raw_data.append(next(f).strip('\n').split(', '))  # Extracts traces to a list

    for i in range(0, len(raw_data)):
        trace = []  # Temporarily saves trace
        for j in range(0, len(raw_data[i])):
            x, y = raw_data[i][j].split(' ')  # Splits each trace point in two coordinates
            trace.append([float(x), float(y)])  # Re-adds them to a temporary trace as a [x, y] array
        data.append(trace)  # Adds trace to final data (another list of traces, but in a processed, functional format)

    return data  # Returns a list of inkml traces, each containing a list of [x, y] coordinates
