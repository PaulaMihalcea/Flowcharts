import os
import pandas as pd
from parse_inkml import parse_inkml
from plot_inkml import plot_inkml

def get_text_traces(inkml_file):

    traces = []  # Array of dataframes containing only traces with text

    group_id = -1

    data = parse_inkml(inkml_file)  # Get all text traces from the file

    data = data.iloc[data[data['class'] == 'Text'].index, :]

    data.index = range(len(data))

    traces.append(data.iloc[data[data['class'] == 'Text'].index, :])  # Get a dataframe with all traces containing text, and append it to the array of dataframes

    data2 = parse_inkml('./FCinkML/writer1_2.inkml')
    data2 = data2.iloc[data2[data2['class'] == 'Text'].index, :]
    data2.index = range(len(data2))
    traces.append(data2.iloc[data2[data2['class'] == 'Text'].index, :])

    pd.set_option('display.max_rows', 1000)

    group_id = 0

    for i in range(0, len(traces)):

        group_old = traces[0]['group_id'][0]
        last_row_group = group_old

        for index, row in traces[i].iterrows():
            if index == 0:
                if row['group_id'] > 0:
                    group_first = row['group_id']
                    traces[i]['group_id'][index] = 0
            if index > 0 and row['group_id'] == group_first:
                traces[i]['group_id'][index] = 0
            if row['group_id'] > group_old:
                group_id += 1
                group_old = row['group_id']
                traces[i]['group_id'][index] = group_id
            elif last_row_group != group_old:
                traces[i]['group_id'][index] = group_id
        last_row_group = row['group_id']


    text_traces = pd.concat(traces)  # Get a new dataframe of traces containing only text, from all files in the inkml folder
    text_traces.index = range(len(text_traces))

    text_traces.to_csv('text_traces.csv', header=False, index=False)  # Save file

    plot_inkml(text_traces, plot=True)  # TODO

get_text_traces('./FCinkML/writer1_1.inkml')
