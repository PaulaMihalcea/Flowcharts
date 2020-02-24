from svgpathtools import svg2paths


def svg2inkml(svg_file, inkml_file):

    paths, attributes = svg2paths(svg_file)  # attributes contains all information about every path, directly extracted from the svg file

    with open(inkml_file, 'w') as f:

        # Initial data
        f.write('<ink xmlns=\"http://www.w3.org/2003/InkML\">\n'
                '\n'
                '<traceFormat>\n'
                '   <channel name=\"X\" type=\"decimal\"/>\n'
                '   <channel name=\"Y\" type=\"decimal\"/>\n'
                '</traceFormat>\n'
                '\n')

        # Trace data
        for i, v in enumerate(attributes):
            trace_id = i
            f.write('<trace id=\"' + str(trace_id) + '\">\n' + v['d'].replace(' L', ', ')[1:] + '\n</trace>\n\n')

        # Final data
        f.write('<annotation type="none"></annotation>\n'
                '\n'
                '</ink>')
