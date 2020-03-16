import os
import pandas as pd
from parse_inkml import parse_inkml

def get_text_traces(inkml_folder):

    traces = []  # Array of dataframes containing only traces with text

    for inkml_file in os.listdir(inkml_folder):
        if '.inkml' in inkml_file:  # Only considers inkml files in folder
            data = parse_inkml(inkml_folder + '/' + inkml_file)  # Get all traces from the file
            traces.append(data.iloc[data[data['class'] == 'Text'].index, :])  # Get a dataframe with all traces containing text, and append it to the array of dataframes

    text_traces = pd.concat(traces)  # Get a new dataframe of traces containing only text, from all files in the inkml folder

    text_traces.to_csv('text_traces.csv', header=False, index=False)  # Save file
