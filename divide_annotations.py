def divide_annotations(annotations_path, orig_file_path, type):

    a = open(annotations_path, 'r')  # Annotations file
    o = open(orig_file_path, 'r')  # Original train/test file list
    d = open('annotation' + '_' + type + '.txt', 'w')  # Output file

    for line_o in o:
        a = open(annotations_path, 'r')

        for line_a in a:
            if line_a.split(',')[0].replace('.png', '') == line_o.replace('.inkml', '').strip('\n'):
                d.write(line_a)
            else:
                pass

        a.close()

    o.close()
    d.close()
